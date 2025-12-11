from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models.api import BaseApiModel
from models.enums import RZoneKindEnum, ZoneRecordTypeEnum


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


class RZoneRecordInSchema(BaseApiModel):
    """Provides an API input model for creating and updating recursive zone records."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the recursive zone record if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the recursive zone record if any."""

    zone_id: UUID = Field(
        title='Zone ID',
        description='The unique identifier of the zone associated with the recursive zone record if any.',
        examples=[uuid4()],
    )
    """The unique identifier of the zone associated with the recursive zone record if any."""

    name: Optional[str] = Field(
        title='Record Name',
        description='The name of the record.',
        default=None,
        examples=['www', 'sub-domain'],
    )
    """The name of the record."""

    type: ZoneRecordTypeEnum = Field(
        title='Record Type',
        description='The type of the record.',
        examples=[
            ZoneRecordTypeEnum.A,
            ZoneRecordTypeEnum.AAAA,
            ZoneRecordTypeEnum.MX,
            ZoneRecordTypeEnum.SOA,
            ZoneRecordTypeEnum.TXT,
        ],
    )
    """The type of the record."""

    ttl: int = Field(
        title='Record TTL',
        description='DNS TTL of the record, in seconds.',
    )
    """DNS TTL of the record, in seconds."""

    content: Optional[str] = Field(
        title='Record Content',
        description='The content of the record.',
        default=None,
    )
    """The content of the record."""

    comment: Optional[str] = Field(
        title='Record Comment',
        description='The comment associated with the record.',
        default=None,
    )
    """The comment associated with the record."""

    disabled: bool = Field(
        title='Record Disabled',
        description='Whether or not this record is disabled.',
        default=False,
    )
    """Whether or not this record is disabled."""

    modified_at: Optional[int] = Field(
        title='Modified Server Timestamp',
        description='Timestamp of the last change to the record on the DNS server.',
        default=None,
    )
    """Timestamp of the last change to the record on the DNS server."""


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
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the recursive zone was last updated."""


class RZoneRecordOutSchema(BaseApiModel):
    """Provides an API response model for representing recursive zone records."""

    id: UUID = Field(
        title='RZone ID',
        description='The unique identifier of the recursive zone.',
        examples=[uuid4()],
    )
    """The unique identifier of the recursive zone."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the recursive zone record if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the recursive zone record if any."""

    zone_id: UUID = Field(
        title='Zone ID',
        description='The unique identifier of the zone associated with the recursive zone record if any.',
        examples=[uuid4()],
    )
    """The unique identifier of the zone associated with the recursive zone record if any."""

    name: Optional[str] = Field(
        title='Record Name',
        description='The name of the record.',
        default=None,
        examples=['www', 'sub-domain'],
    )
    """The name of the record."""

    type: ZoneRecordTypeEnum = Field(
        title='Record Type',
        description='The type of the record.',
        examples=[
            ZoneRecordTypeEnum.A,
            ZoneRecordTypeEnum.AAAA,
            ZoneRecordTypeEnum.MX,
            ZoneRecordTypeEnum.SOA,
            ZoneRecordTypeEnum.TXT,
        ],
    )
    """The type of the record."""

    ttl: int = Field(
        title='Record TTL',
        description='DNS TTL of the record, in seconds.',
    )
    """DNS TTL of the record, in seconds."""

    content: Optional[str] = Field(
        title='Record Content',
        description='The content of the record.',
        default=None,
    )
    """The content of the record."""

    comment: Optional[str] = Field(
        title='Record Comment',
        description='The comment associated with the record.',
        default=None,
    )
    """The comment associated with the record."""

    disabled: bool = Field(
        title='Record Disabled',
        description='Whether or not this record is disabled.',
        default=False,
    )
    """Whether or not this record is disabled."""

    modified_at: Optional[int] = Field(
        title='Modified Server Timestamp',
        description='Timestamp of the last change to the record on the DNS server.',
        default=None,
    )
    """Timestamp of the last change to the record on the DNS server."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the recursive zone record was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the recursive zone record was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the recursive zone record was last updated.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the recursive zone record was last updated."""


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


class RZoneRecordsSchema(BaseApiModel):
    """Provides an API response model for retrieving recursive zone records."""

    records: list[RZoneRecordOutSchema] = Field(
        title='Recursive Zone Records',
        description='A list of recursive zone records found based on the current request criteria.',
        default_factory=list,
    )
    """A list of recursive zone records found based on the current request criteria."""

    total: int = Field(
        title='Total Recursive Zone Records',
        description='The total number of recursive zone records.',
        default=0,
        examples=[1234],
    )
    """The total number of recursive zone records."""

    total_filtered: int = Field(
        title='Total Recursive Zone Records Found',
        description='The total number of recursive zone records found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of recursive zone records found based on the current request criteria."""
