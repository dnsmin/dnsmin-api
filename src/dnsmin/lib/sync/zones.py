from typing import Any, Optional
from uuid import UUID

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
from dnsmin.models.enums import ServerTypeEnum
from . import RedisStreamSyncWorker


class ServerIDInvalidException(Exception):
    """Raised when a server ID is invalid."""


class ZoneIDInvalidException(Exception):
    """Raised when a zone ID is invalid."""


class ZoneNameInvalidException(Exception):
    """Raised when a zone name is invalid."""


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

    _worker: 'ZoneSyncWorker'

    @property
    def redis(self) -> Redis:
        return self._redis

    @property
    def db(self) -> async_sessionmaker[AsyncSession]:
        return self._db

    @property
    def worker(self) -> 'ZoneSyncWorker':
        return self._worker

    def __init__(self, redis: Redis, db: async_sessionmaker[AsyncSession]):
        self._redis = redis
        self._db = db
        self._worker = ZoneSyncWorker(redis=redis, db=db)

    async def check_zones(self) -> None:
        """
        Compares the list of zones in the database to the zones available on DNS servers and queues zone
        synchronization as needed.
        """
        
        servers_stmt = (select(Server).options(selectinload(Server.azones).selectinload(AZoneServer.zone))
                        .where(Server.type == ServerTypeEnum.authoritative)
                        .order_by(Server.mode))
        
        async with self.db() as session:
            db_servers: ScalarResult[Server] = (await session.execute(servers_stmt)).scalars()
        
        api_clients: dict[UUID, PowerDNSAuthApi] = {}
        servers: dict[UUID, Server] = {}
        zones: dict[str, AuthSyncZone] = {}
        
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

            server_zones = await api.zones.list()

            for relationship in server.azones:
                if not relationship.zone.fqdn in zones:
                    zones[relationship.zone.fqdn] = AuthSyncZone(fqdn=relationship.zone.fqdn, zone=relationship.zone)
                zones[relationship.zone.fqdn].assigned_servers[server.id] = server

                # Default to using a zone-level sync policy associated with each server
                zones[relationship.zone.fqdn].sync_policies[server.id] = relationship.sync_policy

                # Fallback to server sync policy if zone sync policy is not set
                if not isinstance(zones[relationship.zone.fqdn].sync_policies[server.id], ZoneSyncPolicy):
                    zones[relationship.zone.fqdn].sync_policies[server.id] = server.sync_policy

            for server_zone in server_zones:
                if not server_zone.fqdn in zones:
                    zones[server_zone.fqdn] = AuthSyncZone(fqdn=server_zone.fqdn)
                zones[server_zone.fqdn].deployed_servers[server.id] = server_zone

        new_db_zones: dict[str, tuple[UUID, SAZone]] = {}
        new_server_zones: dict[str, dict[UUID, AZone]] = {}
        update_db_zones: dict[str, tuple[UUID, SAZone]] = {}
        update_server_zones: dict[str, dict[UUID, AZone]] = {}
        purge_db_zones: list[str] = []
        purge_server_zones: dict[str, dict[UUID, AZone]] = {}

        # TODO: Implement purge detection

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
                        logger.trace(f'Skipping server zone {fqdn} ({server_id}) with lower serial {server_zone.serial}.')
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
                    logger.trace(f'Skipping DB zone {fqdn} with matching serial {sync_zone.zone.serial} for server {server_id}.')
                    continue

                # Zone serial is higher in DB than assigned server, queue update
                if sync_policy.update_zones_in_server and sync_zone.zone.serial > server_zone.serial:
                    update_server_zones[sync_zone.fqdn][server_id] = sync_zone.zone
                    logger.trace(f'Updating DB zone {fqdn} with higher serial {sync_zone.zone.serial} / {server_zone.serial} in server {server_id}.')
                    continue

                # Zone serial is higher in assigned server than DB, queue update
                if sync_policy.update_zones_in_db and sync_zone.zone.serial < server_zone.serial:
                    # Skip updates where a higher serial has already been queued

                    if sync_zone.fqdn in update_db_zones and update_db_zones[sync_zone.fqdn][1].serial >= server_zone.serial:
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

    async def sync_zone(self, zone_name: str) -> None:
        """Performs authoritative zone synchronization using a zone ID."""

        if not isinstance(zone_name, str) or not len(zone_name := zone_name.strip()):
            raise ZoneNameInvalidException

        if zone_name.endswith('.'):
            zone_name = zone_name[:-1]

        if not len(zone_name):
            raise ZoneNameInvalidException

        stmt = (select(AZone)
                .options(selectinload(AZone.servers).selectinload(AZoneServer.server))
                .where(AZone.fqdn == zone_name))

        async with self.db() as session:
            zone: AZone | None = (await session.execute(stmt)).scalar_one_or_none()

        # TODO: Verify server sync policy before raising exception

        if zone is None:
            # TODO: Create zone in database if policy allows or raise exception
            raise ZoneMissingFromDatabaseException

        if not zone.servers:
            return

        for sr in zone.servers:
            sp = sr.sync_policy
            sync_flags = (
                sp.create_missing_zones_in_server,
                sp.create_missing_records_in_db,
                sp.create_missing_records_in_server,
                sp.update_zones_in_db,
                sp.update_zones_in_server,
                sp.update_records_in_db,
                sp.update_records_in_server,
                sp.purge_missing_zones_in_db,
                sp.purge_missing_zones_in_server,
                sp.purge_missing_records_in_db,
                sp.purge_missing_records_in_server
            )

            # Skip processing if policy prohibits the following actions
            if not any(sync_flags):
                continue

            api_config: PowerDNSApiConfig = PowerDNSApiConfig(
                server_id=sr.server.server_id,
                version=sr.server.version,
                api_url=sr.server.api_url,
                api_key=sr.server.api_key,
            )

            api: PowerDNSAuthApi = PowerDNSAuthApi(api_config)

            szone = await api.zones.get(zone_id=f'{zone.fqdn}.', rrsets=False)

            if szone is None:
                if not sp.create_missing_zones_in_server:
                    raise ZoneMissingFromServerException
                # TODO: Create the zone in the DNS server
                continue

            # Compare zone serial numbers to determine which direction to sync if any
            if zone.serial > szone.serial:
                # Database zone is newer, push zone to server
                if sp.update_zones_in_server or sp.update_records_in_server:
                    await self.push_zone_to_server(zone.id, sr.server.id)
                continue

            elif zone.serial < szone.serial:
                # Database zone is older, pull zone from server
                if sp.update_zones_in_db or sp.update_records_in_db:
                    await self.pull_zone_from_server(zone.id, sr.server.id)
                continue

    async def push_zone_to_server(
            self, zone_id: UUID | Mapped[UUID] | str, server_id: UUID | Mapped[UUID] | str,
    ) -> None:
        """Pushes zone data to a DNS server."""

        if isinstance(zone_id, str):
            try:
                zone_id = UUID(zone_id)
            except ValueError:
                raise ZoneIDInvalidException

        if isinstance(server_id, str):
            try:
                server_id = UUID(server_id)
            except ValueError:
                raise ServerIDInvalidException

    async def pull_zone_from_server(
            self, zone_id: UUID | Mapped[UUID] | str, server_id: UUID | Mapped[UUID] | str,
    ) -> None:
        """Pulls zone data from a DNS server."""

        if isinstance(zone_id, str):
            try:
                zone_id = UUID(zone_id)
            except ValueError:
                raise ZoneIDInvalidException

        if isinstance(server_id, str):
            try:
                server_id = UUID(server_id)
            except ValueError:
                raise ServerIDInvalidException

    async def remove_zone_from_db(self, zone_id: UUID | Mapped[UUID] | str) -> None:
        """Removes a zone from the database."""

        if isinstance(zone_id, str):
            try:
                zone_id = UUID(zone_id)
            except ValueError:
                raise ZoneIDInvalidException

    async def remove_zone_from_server(
            self, zone_id: UUID | Mapped[UUID] | str, server_id: UUID | Mapped[UUID] | str
    ) -> None:
        """Removes a zone from a DNS server."""

        if isinstance(zone_id, str):
            try:
                zone_id = UUID(zone_id)
            except ValueError:
                raise ZoneIDInvalidException

        if isinstance(server_id, str):
            try:
                server_id = UUID(server_id)
            except ValueError:
                raise ServerIDInvalidException


class ZoneSyncWorker(RedisStreamSyncWorker):
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

    def sync_resource(self, resource_id: str, metadata: ZoneSyncJobMetadata):
        """Performs zone synchronization"""
        logger.warning(f'Synchronizing Zone {resource_id}, Metadata: {metadata}')
        # TODO: perform zone sync

    def mark_clean(self, resource_id: str, metadata: ZoneSyncJobMetadata):
        """Updates zone server relationship status in database"""
        # TODO
