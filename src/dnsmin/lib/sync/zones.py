from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import Mapped, selectinload

from dnsmin.lib.services.powerdns.auth import PowerDNSApiConfig, PowerDNSAuthApi
from dnsmin.models.db.zones import AZone, AZoneServer
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


class AuthZoneSyncManager:
    """Provides an interface for performing zone synchronization between the app and a DNS server."""

    _db: async_sessionmaker[AsyncSession]

    @property
    def db(self) -> async_sessionmaker[AsyncSession]:
        return self._db

    def __init__(self, db: async_sessionmaker[AsyncSession]):
        self._db = db

    async def check_zones(self) -> None:
        """
        Compares the list of zones in the database to the zones available on DNS servers and queues zone
        synchronization as needed.
        """
        # TODO: Execute zone comparison process

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

    def load_resource(self, zone_id: str):
        """Loads zone data from database"""

    def sync_resource(self, zone_id: str, zone):
        """Performs zone synchronization"""
        # TODO: perform zone sync

    def mark_clean(self, zone_id: str):
        """Updates zone status in database"""
