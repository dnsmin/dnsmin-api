from uuid import UUID

from sqlalchemy.orm import Mapped
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from . import RedisStreamSyncWorker


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

    async def sync_zone_by_name(self, zone_name: str, create_missing: bool = False, delete_missing: bool = False)\
            -> None:
        """Performs authoritative zone synchronization using a zone name."""
        from sqlalchemy import select
        from dnsmin.models.db.zones import AZone

        if not isinstance(zone_name, str) or not len(zone_name := zone_name.strip()):
            raise ZoneNameInvalidException

        if zone_name.endswith('.'):
            zone_name = zone_name[:-1]

        if not len(zone_name):
            raise ZoneNameInvalidException

        stmt = select(AZone.id).where(AZone.fqdn == zone_name)

        async with self.db() as session:
            zone: AZone | None = (await session.execute(stmt)).scalar_one_or_none()

        if zone is None:
            raise ZoneMissingFromDatabaseException

        await self.sync_zone(zone.id)

    async def sync_zone(self, zone_id: UUID | Mapped[UUID] | str, create_missing: bool = False,
                        delete_missing: bool = False) -> None:
        """Performs authoritative zone synchronization using a zone ID."""
        from sqlalchemy import select
        from sqlalchemy.orm import selectinload
        from dnsmin.models.db.zones import AZone

        if isinstance(zone_id, str):
            try:
                zone_id = UUID(zone_id)
            except ValueError:
                raise ZoneIDInvalidException

        stmt = (select(AZone)
                .options(selectinload(AZone.records, AZone.metadata_, AZone.crypto_keys, AZone.servers))
                .where(AZone.id == zone_id))

        async with self.db() as session:
            zone: AZone | None = (await session.execute(stmt)).scalar_one_or_none()

        if zone is None:
            raise ZoneMissingFromDatabaseException

        # TODO


class ZoneSyncWorker(RedisStreamSyncWorker):
    LOCK_TTL_SECONDS = 300

    def load_resource(self, zone_id: str):
        """Loads zone data from database"""

    def sync_resource(self, zone_id: str, zone):
        """Performs zone synchronization"""
        # TODO: perform zone sync

    def mark_clean(self, zone_id: str):
        """Updates zone status in database"""
