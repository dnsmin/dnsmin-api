from typing import Optional
from uuid import UUID

from aiohttp.client_exceptions import ClientResponseError
from loguru import logger
from pydantic import BaseModel, ConfigDict
from redis.asyncio.client import Redis
from sqlalchemy import select, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import Mapped, selectinload

from dnsmin.lib.services.powerdns.auth import PowerDNSApiConfig, PowerDNSAuthApi
from dnsmin.lib.services.powerdns.models import AZone as SAZone
from dnsmin.lib.sync.models import ZoneSyncJobActionEnum, ZoneSyncJobMetadata, ServerSyncPolicy, ZoneSyncPolicy
from dnsmin.models.db.servers import Server
from dnsmin.models.db.zones import AZone, AZoneServer
from dnsmin.models.enums import ServerTypeEnum, ZoneServerStateEnum
from . import RedisStreamSyncWorker


class ServerIDInvalidException(Exception):
    """Raised when a server ID is invalid."""


class ZoneIDInvalidException(Exception):
    """Raised when a zone ID is invalid."""


class ZoneNameInvalidException(Exception):
    """Raised when a zone name is invalid."""


class ZoneServerRelationshipInvalidException(Exception):
    """Raised when a zone server relationship reference is invalid."""


class ZoneMissingFromDatabaseException(Exception):
    """Raised when a zone is missing in the database."""


class ZoneMissingFromServerException(Exception):
    """Raised when a zone is missing in a server."""


class AuthSyncZone(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    fqdn: str
    zone: AZone | None = None
    sync_policies: dict[UUID, ZoneSyncPolicy] = {}
    assigned_servers: dict[UUID, Server] = {}
    deployed_servers: dict[UUID, SAZone] = {}


class AuthZoneSyncManager:
    """Provides an interface for performing zone synchronization between the app and a DNS server."""

    _redis: Redis

    _db: async_sessionmaker[AsyncSession]

    _worker: 'AuthZoneSyncWorker | None'

    @property
    def redis(self) -> Redis:
        return self._redis

    @property
    def db(self) -> async_sessionmaker[AsyncSession]:
        return self._db

    @property
    def worker(self) -> 'AuthZoneSyncWorker | None':
        return self._worker

    def __init__(self, redis: Redis, db: async_sessionmaker[AsyncSession], worker_init: bool = False):
        self._redis = redis
        self._db = db
        if worker_init:
            self._worker = AuthZoneSyncWorker(redis=redis, db=db)
        else:
            self._worker = None

    async def check_zone(self, zone_name: str):
        """Checks if the given zone needs to be synchronized and queues zone synchronization accordingly."""

        if not isinstance(zone_name, str):
            raise ZoneNameInvalidException()

        if zone_name.endswith('.'):
            zone_name = zone_name[:-1]

        zone_stmt = (select(AZone).options(selectinload(AZone.servers).selectinload(AZoneServer.server))
                     .where(AZone.fqdn == zone_name))

        servers_stmt = select(Server).where(Server.type == ServerTypeEnum.authoritative).order_by(Server.mode)

        async with self.db() as session:
            db_zone: AZone | None = (await session.execute(zone_stmt)).scalar_one_or_none()
            db_servers_result: ScalarResult[Server] = (await session.execute(servers_stmt)).scalars()

        api_clients: dict[UUID, PowerDNSAuthApi] = {}
        db_servers: dict[UUID, Server] = {}
        server_zones: dict[UUID, SAZone] = {}

        for server in db_servers_result:
            db_servers[server.id] = server
            api_clients[server.id] = PowerDNSAuthApi(PowerDNSApiConfig(
                server_id=server.server_id,
                version=server.version,
                api_url=server.api_url,
                api_key=server.api_key,
            ))

            if (zones := await api_clients[server.id].zones.list(zone=f'{zone_name}.')):
                server_zones[server.id] = zones[0]

        # Discontinue processing if the zone doesn't exist in the DB or any registered servers
        if not isinstance(db_zone, AZone) and not server_zones:
            logger.trace(f'Zone {zone_name} not found in database or registered servers.')
            return

        # Zone doesn't exist in DB, queue it for creation if server policy permits
        if not isinstance(db_zone, AZone):
            zone: SAZone | None = None
            selected_server_id: UUID | None = None

            for server_id, szone in server_zones.items():
                server = db_servers[server_id]

                if not server.sync_policy:
                    logger.trace(f'Skipping zone server {server_id} for zone {zone_name} due to missing sync policy.')
                    continue

                if not server.sync_policy.create_missing_zones_in_db:
                    logger.trace(f'Skipping zone server {server_id} for zone {zone_name} due to no creation policy.')
                    continue

                if isinstance(zone, SAZone) and zone.serial >= szone.serial:
                    logger.trace(f'Skipping zone server {server_id} for zone {zone_name} due to lower or equal serial.')
                    continue

                logger.trace(f'Selecting zone server {server_id} for zone {zone_name}.')
                zone = szone
                selected_server_id = server_id

            if selected_server_id is None:
                logger.trace(f'Skipping zone {zone_name} as no server sync policies allowed for creation.')
                return

            await self.worker.mark_dirty(zone_name, ZoneSyncJobMetadata(
                resource_id=zone_name, action=ZoneSyncJobActionEnum.create_db, server_id=selected_server_id
            ))

            return

        # Zone doesn't have any servers associated with it
        if not db_zone.servers:
            logger.trace(f'Zone {zone_name} not associated with any servers.')
            return

        # Zone exists in DB, check if it needs to be created or updated in associated servers and queue accordingly

        # Zone doesn't exist in any servers so queue it to be created if policy allows
        if not server_zones:
            for relationship in db_zone.servers:
                sync_policy = relationship.sync_policy

                # Fallback to server-level sync policy if relationship did not have one defined
                if not sync_policy:
                    sync_policy = db_servers[relationship.server.id].sync_policy

                # Skip server as no sync policy was found
                if not sync_policy:
                    logger.trace(
                        f'Skipping server {relationship.server_id} for zone {zone_name} due to missing sync policy.')
                    continue

                # Skip server as sync policy does not allow for server zone creation
                if not sync_policy.create_missing_zones_in_server:
                    logger.trace(
                        f'Skipping server {relationship.server_id} for zone {zone_name} due to no creation policy.')
                    continue

                # Queue the zone for creation on the server
                await self.worker.mark_dirty(zone_name, ZoneSyncJobMetadata(
                    resource_id=zone_name, action=ZoneSyncJobActionEnum.create_server, server_id=relationship.server_id
                ))

            return

        # Zone exists in some servers, determine where it needs to be created, updated, or removed

        assigned_servers = set(r.server.id for r in db_zone.servers)
        deployed_servers = set(server_zones.keys())
        purge_servers = deployed_servers - assigned_servers

        # Zone exists on servers it's not assigned to, queue purge if policy allows
        if purge_servers:
            for server_id in purge_servers:
                # Skip server for having no sync policy defined
                if not db_servers[server_id].sync_policy:
                    logger.trace(f'Skipping server {server_id} for zone {zone_name} purge due to missing sync policy.')
                    continue

                # Skip server for having a no purge policy
                if not db_servers[server_id].sync_policy.purge_missing_zones_in_server:
                    logger.trace(f'Skipping server {server_id} for zone {zone_name} purge due to no purge policy.')
                    continue

                # Queue zone for purge from the server
                await self.worker.mark_dirty(zone_name, ZoneSyncJobMetadata(
                    resource_id=zone_name, action=ZoneSyncJobActionEnum.purge_server, server_id=server_id
                ))

        for relationship in db_zone.servers:
            sync_policy = relationship.sync_policy

            # Fallback to server-level sync policy if relationship did not have one defined
            if not sync_policy:
                sync_policy = relationship.server.sync_policy

            # Skip server as no sync policy was found
            if not sync_policy:
                logger.trace(
                    f'Skipping server {relationship.server_id} for zone {zone_name} due to missing sync policy.')
                continue

            # Zone doesn't exist on an assigned server, queue for creation if policy allows
            if relationship.server_id not in server_zones:
                # Skip server as policy does not allow creation
                if not sync_policy.create_missing_zones_in_server:
                    logger.trace(
                        f'Skipping server {relationship.server_id} for zone {zone_name} due to no creation policy.')
                    continue

                # Queue zone creation for server
                await self.worker.mark_dirty(zone_name, ZoneSyncJobMetadata(
                    resource_id=zone_name, action=ZoneSyncJobActionEnum.create_server, server_id=relationship.server_id
                ))

                continue

            # Zone exists on assigned server, determine which side needs updated if any and queue accordingly

            # Skip server as zone serials match
            if db_zone.serial == server_zones[relationship.server_id].serial:
                logger.trace(f'Skipping server {relationship.server_id} for zone {zone_name} due to matching serial.')
                continue

            # Queue server update if zone serial is higher in DB
            if db_zone.serial > server_zones[relationship.server_id].serial:
                await self.worker.mark_dirty(zone_name, ZoneSyncJobMetadata(
                    resource_id=zone_name, action=ZoneSyncJobActionEnum.update_server, server_id=relationship.server_id
                ))
                continue

            # Queue DB update as zone serial is higher on server
            await self.worker.mark_dirty(zone_name, ZoneSyncJobMetadata(
                resource_id=zone_name, action=ZoneSyncJobActionEnum.update_db, server_id=relationship.server_id
            ))

    async def check_zones(self) -> None:
        """
        Compares the list of zones in the database to the zones available on DNS servers and queues zone
        synchronization accordingly.
        """

        stmt = (select(Server).options(selectinload(Server.azones).selectinload(AZoneServer.zone))
                .where(Server.type == ServerTypeEnum.authoritative)
                .order_by(Server.mode))

        async with self.db() as session:
            db_servers: ScalarResult[Server] = (await session.execute(stmt)).scalars()

        api_clients: dict[UUID, PowerDNSAuthApi] = {}
        servers: dict[UUID, Server] = {}
        zones: dict[str, AuthSyncZone] = {}
        server_zones: dict[str, dict[UUID, SAZone]] = {}

        for server in db_servers:
            servers[server.id] = server

            api_config: PowerDNSApiConfig = PowerDNSApiConfig(
                server_id=server.server_id,
                version=server.version,
                api_url=server.api_url,
                api_key=server.api_key,
            )

            api: PowerDNSAuthApi = PowerDNSAuthApi(api_config)

            api_clients[server.id] = api

            for relationship in server.azones:
                if not relationship.zone.fqdn in zones:
                    zones[relationship.zone.fqdn] = AuthSyncZone(fqdn=relationship.zone.fqdn, zone=relationship.zone)
                zones[relationship.zone.fqdn].assigned_servers[server.id] = server

                # Default to using a zone-level sync policy associated with each server
                zones[relationship.zone.fqdn].sync_policies[server.id] = relationship.sync_policy

                # Fallback to server sync policy if zone sync policy is not set
                if not isinstance(zones[relationship.zone.fqdn].sync_policies[server.id], ZoneSyncPolicy):
                    zones[relationship.zone.fqdn].sync_policies[server.id] = server.sync_policy

            for server_zone in await api.zones.list():
                if not server_zone.fqdn in server_zones:
                    server_zones[server_zone.fqdn] = {}

                if not server_zone.fqdn in zones:
                    zones[server_zone.fqdn] = AuthSyncZone(fqdn=server_zone.fqdn)

                server_zones[server_zone.fqdn][server.id] = server_zone
                zones[server_zone.fqdn].deployed_servers[server.id] = server_zone

        new_db_zones: dict[str, tuple[UUID, SAZone]] = {}
        new_server_zones: dict[str, dict[UUID, AZone]] = {}
        update_db_zones: dict[str, tuple[UUID, SAZone]] = {}
        update_server_zones: dict[str, dict[UUID, AZone]] = {}
        purge_db_zones: list[str] = []
        purge_server_zones: dict[str, dict[UUID, AZone]] = {}

        for fqdn, sync_zone in zones.items():
            logger.trace(f'Checking Zone {fqdn}')

            # Find zones missing from database that should be synchronized per policy
            if not isinstance(sync_zone.zone, AZone):
                # Check each server that zone was found in to determine if the zone should be pulled from server into DB
                for server_id, server_zone in sync_zone.deployed_servers.items():
                    server = servers[server_id]

                    # Skip zones that don't have a sync policy defined on the associated server
                    if not isinstance(server.sync_policy, ServerSyncPolicy):
                        logger.trace(f'Skipping server zone {fqdn} ({server_id}) with no sync policy.')
                        continue

                    # Skip zones where policy doesn't dictate the creation in the DB
                    if not server.sync_policy.create_missing_zones_in_db:
                        logger.trace(f'Skipping server zone {fqdn} ({server_id}) with no creation policy.')
                        continue

                    # If the zone is found in multiple DNS servers, use the one with the highest serial
                    if server_zone.fqdn not in new_db_zones:
                        new_db_zones[server_zone.fqdn] = server_id, server_zone
                    elif new_db_zones[server_zone.fqdn][1].serial > server_zone.serial:
                        new_db_zones[server_zone.fqdn] = server_id, server_zone
                    else:
                        logger.trace(
                            f'Skipping server zone {fqdn} ({server_id}) with lower serial {server_zone.serial}.')
                        continue

                    logger.trace(f'Creating server zone {fqdn} ({server_zone.serial}) in DB.')

                continue

            # Check for zones missing from assigned servers that should be synchronized per policy
            for server_id, server in sync_zone.assigned_servers.items():
                sync_policy = sync_zone.sync_policies[server_id]

                # Skip zones that don't have a zone or server sync policy
                if not sync_policy:
                    logger.trace(f'Skipping DB zone {fqdn} with no sync policy for server {server_id}.')
                    continue

                # Check for zones that should be deleted from servers and queue accordingly if policy allows
                if sync_zone.zone.purged is not None:
                    if sync_zone.zone.fqdn in server_zones and sync_policy.purge_missing_zones_in_server:
                        logger.trace(f'Purging server zone {fqdn} in server {server_id}.')
                        purge_server_zones[sync_zone.zone.fqdn][server_id] = sync_zone.zone
                    logger.trace(f'Purging DB zone {fqdn} in server {server_id}.')
                    purge_db_zones.append(sync_zone.zone.fqdn)
                    continue

                # Zone missing from assigned server
                if server_id not in sync_zone.deployed_servers:
                    # Skip zone if policy doesn't dictate the creation in DNS server
                    if not sync_policy.create_missing_zones_in_server:
                        logger.trace(f'Skipping DB zone {fqdn} with no creation policy for server {server_id}.')
                        continue

                    if not sync_zone.fqdn in new_server_zones:
                        new_server_zones[sync_zone.fqdn] = {}

                    new_server_zones[sync_zone.fqdn][server_id] = sync_zone.zone
                    logger.trace(f'Creating DB zone {fqdn} in server {server_id}')
                    continue

                # Zone exists in assigned server

                # Skip zones that should not be updated in either direction
                if not sync_policy.update_zones_in_db and not sync_policy.update_zones_in_server:
                    logger.trace(f'Skipping DB zone {fqdn} with no update policy for server {server_id}.')
                    continue

                server_zone = sync_zone.deployed_servers[server_id]

                # Skip zones where serials match on the deployed server
                if sync_zone.zone.serial == server_zone.serial:
                    logger.trace(
                        f'Skipping DB zone {fqdn} with matching serial {sync_zone.zone.serial} for server {server_id}.')
                    continue

                # Zone serial is higher in DB than assigned server, queue update
                if sync_policy.update_zones_in_server and sync_zone.zone.serial > server_zone.serial:
                    update_server_zones[sync_zone.fqdn][server_id] = sync_zone.zone
                    logger.trace(
                        f'Updating DB zone {fqdn} with higher serial {sync_zone.zone.serial} / {server_zone.serial} in server {server_id}.')
                    continue

                # Zone serial is higher in assigned server than DB, queue update
                if sync_policy.update_zones_in_db and sync_zone.zone.serial < server_zone.serial:
                    # Skip updates where a higher serial has already been queued

                    if sync_zone.fqdn in update_db_zones and update_db_zones[sync_zone.fqdn][
                        1].serial >= server_zone.serial:
                        match = update_db_zones[sync_zone.fqdn][1].serial == server_zone.serial
                        logger.trace(f'Skipping DB zone {fqdn} with lower serial {sync_zone.zone.serial} / '
                                     + f'{server_zone.serial} from {'matching' if match else 'stale'} server {server_id}.')
                        continue

                    update_db_zones[sync_zone.fqdn] = server_id, server_zone
                    logger.trace(f'Updating DB zone {fqdn} with lower serial {sync_zone.zone.serial} / '
                                 + f'{server_zone.serial} from server {server_id}.')
                    continue

        # Queue DB zone updates
        for fqdn, meta in update_db_zones.items():
            await self.worker.mark_dirty(
                fqdn, ZoneSyncJobMetadata(resource_id=fqdn, action=ZoneSyncJobActionEnum.update_db, server_id=meta[0])
            )

        # Queue server zone updates
        for fqdn, servers in update_server_zones.items():
            for server_id, server in servers.items():
                await self.worker.mark_dirty(
                    fqdn, ZoneSyncJobMetadata(
                        resource_id=fqdn, action=ZoneSyncJobActionEnum.update_server, server_id=server_id
                    )
                )

        # Queue DB zone creation
        for fqdn, meta in new_db_zones.items():
            await self.worker.mark_dirty(
                fqdn, ZoneSyncJobMetadata(resource_id=fqdn, action=ZoneSyncJobActionEnum.create_db, server_id=meta[0])
            )

        # Queue server zone creation
        for fqdn, servers in new_server_zones.items():
            for server_id, server in servers.items():
                await self.worker.mark_dirty(
                    fqdn, ZoneSyncJobMetadata(
                        resource_id=fqdn, action=ZoneSyncJobActionEnum.create_server, server_id=server_id
                    )
                )

        # Queue server zone purges
        for fqdn, servers in purge_server_zones.items():
            for server_id, server in servers.items():
                await self.worker.mark_dirty(
                    fqdn, ZoneSyncJobMetadata(
                        resource_id=fqdn, action=ZoneSyncJobActionEnum.purge_server, server_id=server_id
                    )
                )

        # Queue DB zone purges
        for fqdn in purge_db_zones:
            await self.worker.mark_dirty(
                fqdn, ZoneSyncJobMetadata(resource_id=fqdn, action=ZoneSyncJobActionEnum.purge_db)
            )

    async def update_zone_server_state(
            self, zone_name: str, server_id: UUID | Mapped[UUID] | str, state: ZoneServerStateEnum
    ) -> None:
        """Updates the state of a zone's server relationship."""

        if not isinstance(zone_name, str) or not len(zone_name := zone_name.strip()):
            raise ZoneNameInvalidException

        if zone_name.endswith('.'):
            zone_name = zone_name[:-1]

        if not len(zone_name):
            raise ZoneNameInvalidException

        if isinstance(server_id, str):
            try:
                server_id = UUID(server_id)
            except ValueError:
                raise ServerIDInvalidException

        stmt = (select(AZone).join(AZone.servers).options(selectinload(AZone.servers))
                .where(AZone.fqdn == zone_name, AZoneServer.server_id == server_id))

        async with self.db() as session:
            zone: AZone | None = (await session.execute(stmt)).scalar_one_or_none()

            if not isinstance(zone, AZone):
                raise ZoneServerRelationshipInvalidException

            zone.servers[0].state = state
            session.add(zone.servers[0])
            await session.commit()

    async def push_zone_to_server(self, zone_name: str, server_id: UUID | Mapped[UUID] | str) -> None:
        """Pushes zone data to a DNS server."""

        logger.trace(f'Pushing zone {zone_name} to server {server_id}.')

        if not isinstance(zone_name, str) or not len(zone_name := zone_name.strip()):
            raise ZoneNameInvalidException

        if zone_name.endswith('.'):
            zone_name = zone_name[:-1]

        if not len(zone_name):
            raise ZoneNameInvalidException

        if isinstance(server_id, str):
            try:
                server_id = UUID(server_id)
            except ValueError:
                raise ServerIDInvalidException

        zone_stmt = (select(AZone).join(AZoneServer)
                     .options(selectinload(AZone.servers).selectinload(AZoneServer.server))
                     .where(AZone.fqdn == zone_name, AZoneServer.server_id == server_id))

        async with self.db() as session:
            db_zone: AZone | None = (await session.execute(zone_stmt)).scalar_one_or_none()

        if not isinstance(db_zone, AZone):
            raise ZoneMissingFromDatabaseException

        relationship: AZoneServer = db_zone.servers[0]
        server: Server = relationship.server

        api_client: PowerDNSAuthApi = PowerDNSAuthApi(PowerDNSApiConfig(
            server_id=server.server_id,
            version=server.version,
            api_url=server.api_url,
            api_key=server.api_key,
        ))

        sync_policy = relationship.sync_policy

        if sync_policy is None:
            sync_policy = server.sync_policy

        if sync_policy is None:
            return

        try:
            szone: SAZone | None = await api_client.zones.get(db_zone.fqdn + '.',  rrsets=True)
        except ClientResponseError as err:
            if err.status != 404:
                raise
            szone = None
            logger.trace(f'Zone {db_zone.fqdn} missing from server {server_id}.')

        if szone is None:
            if not sync_policy.create_missing_zones_in_server:
                logger.trace(f'Skipping zone {db_zone.fqdn} for server {server_id} due to no create policy.')
                return

            # TODO: Create the zone on the server

            return

        # TODO: Update zone on the server based on sync policy

    async def pull_zone_from_server(self, zone_name: str, server_id: UUID | Mapped[UUID] | str) -> None:
        """Pulls zone data from a DNS server."""

        if not isinstance(zone_name, str) or not len(zone_name := zone_name.strip()):
            raise ZoneNameInvalidException

        if zone_name.endswith('.'):
            zone_name = zone_name[:-1]

        if not len(zone_name):
            raise ZoneNameInvalidException

        if isinstance(server_id, str):
            try:
                server_id = UUID(server_id)
            except ValueError:
                raise ServerIDInvalidException

        logger.trace(f'Pulling zone {zone_name} from server {server_id}.')
        # TODO

    async def remove_zone_from_db(self, zone_name: str) -> None:
        """Removes a zone from the database."""

        if not isinstance(zone_name, str) or not len(zone_name := zone_name.strip()):
            raise ZoneNameInvalidException

        if zone_name.endswith('.'):
            zone_name = zone_name[:-1]

        if not len(zone_name):
            raise ZoneNameInvalidException

        logger.trace(f'Removing zone {zone_name} from DB.')
        # TODO

    async def remove_zone_from_server(self, zone_name: str, server_id: UUID | Mapped[UUID] | str) -> None:
        """Removes a zone from a DNS server."""

        if not isinstance(zone_name, str) or not len(zone_name := zone_name.strip()):
            raise ZoneNameInvalidException

        if zone_name.endswith('.'):
            zone_name = zone_name[:-1]

        if not len(zone_name):
            raise ZoneNameInvalidException

        if isinstance(server_id, str):
            try:
                server_id = UUID(server_id)
            except ValueError:
                raise ServerIDInvalidException

        logger.trace(f'Removing zone {zone_name} from server {server_id}.')
        # TODO


class AuthZoneSyncWorker(RedisStreamSyncWorker):
    LOCK_TTL_SECONDS = 300

    def __init__(
            self,
            *,
            redis: Redis,
            db: async_sessionmaker[AsyncSession],
            consumer_name: Optional[str] = None,
    ):
        if not isinstance(consumer_name, str):
            consumer_name = 'sync-worker'

        super().__init__(
            redis=redis,
            db=db,
            namespace='dns',
            consumer_group='dns-sync',
            consumer_name=consumer_name,
            metadata_class=ZoneSyncJobMetadata,
        )

        self.manager = AuthZoneSyncManager(redis=redis, db=db, worker_init=False)

    async def sync_resource(self, resource_id: str, metadata: ZoneSyncJobMetadata):
        """Performs zone synchronization"""
        logger.warning(
            f'Consumer {self.consumer_name} Synchronizing: Zone: {resource_id}, Action: {metadata.action.value}')

        if metadata.action in (ZoneSyncJobActionEnum.create_db, ZoneSyncJobActionEnum.update_db):
            await self.manager.pull_zone_from_server(resource_id, metadata.server_id)
        elif metadata.action in (ZoneSyncJobActionEnum.create_server, ZoneSyncJobActionEnum.update_server):
            await self.manager.push_zone_to_server(resource_id, metadata.server_id)
        elif metadata.action == ZoneSyncJobActionEnum.purge_db:
            await self.manager.remove_zone_from_db(resource_id)
        elif metadata.action == ZoneSyncJobActionEnum.purge_server:
            await self.manager.remove_zone_from_server(resource_id, metadata.server_id)
        else:
            logger.error(
                f'Consumer {self.consumer_name} Unknown Action Received: Zone: {resource_id}, Action: {metadata.action.value}, Server ID: {metadata.server_id}')

    async def mark_clean(self, resource_id: str, metadata: ZoneSyncJobMetadata):
        """Updates zone server relationship status in database"""
        if metadata.action == ZoneSyncJobActionEnum.purge_server:
            await self.manager.update_zone_server_state(
                resource_id, metadata.server_id, ZoneServerStateEnum.purged
            )
        elif not metadata.action == ZoneSyncJobActionEnum.purge_db:
            await self.manager.update_zone_server_state(
                resource_id, metadata.server_id, ZoneServerStateEnum.synchronized
            )
