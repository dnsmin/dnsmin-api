from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from dnsmin.lib.sync.models import ZoneSyncPolicy
from dnsmin.models import BaseApiModel
from dnsmin.models.enums import ZoneServerStateEnum


class AZoneServerInSchema(BaseApiModel):
    """Provides an API input model for creating and updating authoritative zone server relationships."""

    zone_id: UUID = Field(
        title='Zone ID',
        description='The unique identifier of the zone associated with the relationship.',
        examples=[uuid4()],
    )
    """The unique identifier of the zone associated with the relationship."""

    server_id: UUID = Field(
        title='Server ID',
        description='The unique identifier of the server associated with the relationship.',
        examples=[uuid4()],
    )
    """The unique identifier of the zone associated with the relationship."""

    state: ZoneServerStateEnum = Field(
        title='Synchronization State',
        description='The synchronization state of the relationship.',
        examples=[
            ZoneServerStateEnum.dirty,
            ZoneServerStateEnum.stale,
            ZoneServerStateEnum.synchronized,
            ZoneServerStateEnum.syncing,
        ],
    )
    """The synchronization state of the relationship."""

    sync_policy: Optional[ZoneSyncPolicy] = Field(
        title='Synchronization Policy',
        description='The synchronization policy of the relationship.',
        default=None,
        examples=[ZoneSyncPolicy()],
    )
    """The synchronization policy of the relationship."""


class AZoneServerOutSchema(BaseApiModel):
    """Provides an API response model for representing authoritative zone server relationships."""

    zone_id: UUID = Field(
        title='Zone ID',
        description='The unique identifier of the zone associated with the relationship.',
        examples=[uuid4()],
    )
    """The unique identifier of the zone associated with the relationship."""

    server_id: UUID = Field(
        title='Server ID',
        description='The unique identifier of the server associated with the relationship.',
        examples=[uuid4()],
    )
    """The unique identifier of the zone associated with the relationship."""

    state: ZoneServerStateEnum = Field(
        title='Synchronization State',
        description='The synchronization state of the relationship.',
        examples=[
            ZoneServerStateEnum.dirty,
            ZoneServerStateEnum.stale,
            ZoneServerStateEnum.synchronized,
            ZoneServerStateEnum.syncing,
        ],
    )
    """The synchronization state of the relationship."""

    sync_policy: Optional[ZoneSyncPolicy] = Field(
        title='Synchronization Policy',
        description='The synchronization policy of the relationship.',
        default=None,
        examples=[ZoneSyncPolicy()],
    )
    """The synchronization policy of the relationship."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the relationship was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the relationship was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the relationship was last updated.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the relationship was last updated."""


class AZoneServersSchema(BaseApiModel):
    """Provides an API response model for retrieving authoritative zone server relationships."""

    records: list[AZoneServerOutSchema] = Field(
        title='Authoritative Zone Server Relationships',
        description='A list of authoritative zone server relationships found based on the current request criteria.',
        default_factory=list,
    )
    """A list of authoritative zone server relationships found based on the current request criteria."""

    total: int = Field(
        title='Total Authoritative Zone Server Relationships',
        description='The total number of authoritative zone server relationships.',
        default=0,
        examples=[1234],
    )
    """The total number of authoritative zone server relationships."""

    total_filtered: int = Field(
        title='Total Authoritative Zone Server Relationships Found',
        description='The total number of authoritative zone server relationships found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of authoritative zone server relationships found based on the current request criteria."""
