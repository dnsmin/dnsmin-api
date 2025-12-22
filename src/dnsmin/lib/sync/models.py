from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ZoneSyncJobActionEnum(str, Enum):
    """Defines the sync job action types available for sync jobs."""
    create_db = "create_db"
    create_server = "create_server"
    update_db = "update_db"
    update_server = "update_server"
    purge_db = "purge_db"
    purge_server = "purge_server"


class SyncJobMetadata(BaseModel):
    """Defines sync metadata used by sync workers for sync jobs."""

    resource_id: str
    """The resource ID relevant to the sync job."""

    ts: Optional[int] = None
    """The timestamp when a sync job was queued."""

    reason: Optional[str] = None
    """The reason why an execution workflow changed expected course."""


class ZoneSyncJobMetadata(SyncJobMetadata):
    """Defines sync metadata used by sync workers for zone sync jobs."""

    action: ZoneSyncJobActionEnum
    """The action to be taken during the sync job."""

    server_id: UUID
    """The server ID relevant to the sync job."""


class ZoneSyncPolicy(BaseModel):
    """Defines a synchronization policy for zones that are synchronized with DNS servers."""

    create_missing_zones_in_server: bool = Field(
        title='Create Missing Zones In Server',
        description='Whether to create zones in a DNS server that are present in the database.',
        default=False,
    )
    """Whether to create zones in a DNS server that are present in the database."""

    update_zones_in_db: bool = Field(
        title='Update Zones In Database',
        description='Whether to update zones in the database from updates in a DNS server.',
        default=False,
    )
    """Whether to update zones in the database from updates in a DNS server."""

    update_zones_in_server: bool = Field(
        title='Update Zones In Server',
        description='Whether to update zones in a DNS server from updates in the database.',
        default=False,
    )
    """Whether to update zones in a DNS server from updates in the database."""

    purge_missing_zones_in_db: bool = Field(
        title='Purge Missing Zones In Database',
        description='Whether to purge zones in the database that are not present in a DNS server.',
        default=False,
    )
    """Whether to purge zones in the database that are not present in a DNS server."""

    purge_missing_zones_in_server: bool = Field(
        title='Purge Missing Zones In Server',
        description='Whether to purge zones in a DNS server that are not present in the database.',
        default=False,
    )
    """Whether to purge zones in a DNS server that are not present in the database."""

    create_missing_records_in_db: bool = Field(
        title='Create Missing Records In Database',
        description='Whether to create records in the database that are present in a DNS server.',
        default=False,
    )
    """Whether to create records in the database that are present in a DNS server."""

    create_missing_records_in_server: bool = Field(
        title='Create Missing Records In Server',
        description='Whether to create records in a DNS server that are present in the database.',
        default=False,
    )
    """Whether to create records in a DNS server that are present in the database."""

    update_records_in_db: bool = Field(
        title='Update Records In Database',
        description='Whether to update records in the database from updates in a DNS server.',
        default=False,
    )
    """Whether to update records in the database from updates in a DNS server."""

    update_records_in_server: bool = Field(
        title='Update Records In Server',
        description='Whether to update records in a DNS server from updates in the database.',
        default=False,
    )
    """Whether to update records in a DNS server from updates in the database."""

    purge_missing_records_in_db: bool = Field(
        title='Purge Missing Records In Database',
        description='Whether to purge records in the database that are not present in a DNS server.',
        default=False,
    )
    """Whether to purge records in the database that are not present in a DNS server."""

    purge_missing_records_in_server: bool = Field(
        title='Purge Missing Records In Server',
        description='Whether to purge records in a DNS server that are not present in the database.',
        default=False,
    )
    """Whether to purge records in a DNS server that are not present in the database."""


class ServerSyncPolicy(ZoneSyncPolicy):
    """Defines a zone synchronization policy for servers."""

    create_missing_zones_in_db: bool = Field(
        title='Create Missing Zones In Database',
        description='Whether to create zones in the database that are present in a DNS server.',
        default=False,
    )
    """Whether to create zones in the database that are present in a DNS server."""
