from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models.api import BaseApiModel
from models.enums import RZoneKindEnum


class RZoneInSchema(BaseApiModel):
    """Provides an API input model for creating and updating recursive zones."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the recursive zone if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the recursive zone if any."""

    fqdn: str = Field(
        title='Zone FQDN',
        description='The FQDN of the zone.',
        examples=['your-domain.com', 'third.level-domain.com', 'intranet-zone'],
    )
    """The FQDN of the zone."""

    kind: RZoneKindEnum = Field(
        title='Zone Kind',
        description='The kind of the zone.',
        examples=[
            RZoneKindEnum.NATIVE,
            RZoneKindEnum.FORWARDED,
        ],
    )
    """The kind of the zone."""

    servers: list[str] = Field(
        title='Zone Responders',
        description='The list of upstream servers to forward queries to.',
        examples=['1.1.1.1', '1.1.4.4', '1.1.8.8'],
    )
    """The list of upstream servers to forward queries to."""

    recursion_desired: Optional[bool] = Field(
        title='Recursion Desired',
        description='Whether or not the RD bit should be set in the upstream query for forwarded zone kinds.',
        default=None,
    )
    """Whether or not the RD bit should be set in the upstream query for forwarded zone kinds."""

    notify_allowed: Optional[bool] = Field(
        title='Allow Notifications',
        description='Whether or not to permit incoming NOTIFY to wipe cache for the forwarded zone kind.',
        default=None,
    )
    """Whether or not to permit incoming NOTIFY to wipe cache for the forwarded zone kind."""


class RZoneOutSchema(BaseApiModel):
    """Provides an API response model for representing recursive zones."""

    id: UUID = Field(
        title='RZone ID',
        description='The unique identifier of the recursive zone.',
        examples=[uuid4()],
    )
    """The unique identifier of the recursive zone."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the recursive zone if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the recursive zone if any."""

    fqdn: str = Field(
        title='Zone FQDN',
        description='The FQDN of the zone.',
        examples=['your-domain.com', 'third.level-domain.com', 'intranet-zone'],
    )
    """The FQDN of the zone."""

    kind: RZoneKindEnum = Field(
        title='Zone Kind',
        description='The kind of the zone.',
        examples=[
            RZoneKindEnum.NATIVE,
            RZoneKindEnum.FORWARDED,
        ],
    )
    """The kind of the zone."""

    servers: list[str] = Field(
        title='Zone Responders',
        description='The list of upstream servers to forward queries to.',
        examples=['1.1.1.1', '1.1.4.4', '1.1.8.8'],
    )
    """The list of upstream servers to forward queries to."""

    recursion_desired: Optional[bool] = Field(
        title='Recursion Desired',
        description='Whether or not the RD bit should be set in the upstream query for forwarded zone kinds.',
        default=None,
    )
    """Whether or not the RD bit should be set in the upstream query for forwarded zone kinds."""

    notify_allowed: Optional[bool] = Field(
        title='Allow Notifications',
        description='Whether or not to permit incoming NOTIFY to wipe cache for the forwarded zone kind.',
        default=None,
    )
    """Whether or not to permit incoming NOTIFY to wipe cache for the forwarded zone kind."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the recursive zone was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the recursive zone was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the recursive zone was last updated.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the recursive zone was last updated."""


class RZonesSchema(BaseApiModel):
    """Provides an API response model for retrieving recursive zones."""

    records: list[RZoneOutSchema] = Field(
        title='Recursive Zones',
        description='A list of recursive zones found based on the current request criteria.',
        default_factory=list,
    )
    """A list of recursive zones found based on the current request criteria."""

    total: int = Field(
        title='Total Recursive Zones',
        description='The total number of recursive zones.',
        default=0,
        examples=[1234],
    )
    """The total number of recursive zones."""

    total_filtered: int = Field(
        title='Total Recursive Zones Found',
        description='The total number of recursive zones found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of recursive zones found based on the current request criteria."""


