from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models import BaseApiModel, ZoneRecordTypeEnum


class AZoneRecordInSchema(BaseApiModel):
    """Provides an API input model for creating and updating authoritative zone records."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the authoritative zone record if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the authoritative zone record if any."""

    zone_id: UUID = Field(
        title='Zone ID',
        description='The unique identifier of the zone associated with the authoritative zone record.',
        examples=[uuid4()],
    )
    """The unique identifier of the zone associated with the authoritative zone record."""

    view_id: Optional[UUID] = Field(
        title='View ID',
        description='The unique identifier of the server view associated with the authoritative zone record if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the server view associated with the authoritative zone record if any."""

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


class AZoneRecordOutSchema(BaseApiModel):
    """Provides an API response model for representing authoritative zone records."""

    id: UUID = Field(
        title='Record ID',
        description='The unique identifier of the authoritative zone.',
        examples=[uuid4()],
    )
    """The unique identifier of the authoritative zone."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the authoritative zone record if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the authoritative zone record if any."""

    zone_id: UUID = Field(
        title='Zone ID',
        description='The unique identifier of the zone associated with the authoritative zone record.',
        examples=[uuid4()],
    )
    """The unique identifier of the zone associated with the authoritative zone record."""

    view_id: Optional[UUID] = Field(
        title='View ID',
        description='The unique identifier of the server view associated with the authoritative zone record if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the server view associated with the authoritative zone record if any."""

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
        description='The timestamp representing when the authoritative zone record was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the authoritative zone record was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the authoritative zone record was last updated.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the authoritative zone record was last updated."""


class AZoneRecordsSchema(BaseApiModel):
    """Provides an API response model for retrieving authoritative zone records."""

    records: list[AZoneRecordOutSchema] = Field(
        title='Authoritative Zone Records',
        description='A list of authoritative zone records found based on the current request criteria.',
        default_factory=list,
    )
    """A list of authoritative zone records found based on the current request criteria."""

    total: int = Field(
        title='Total Authoritative Zone Records',
        description='The total number of authoritative zone records.',
        default=0,
        examples=[1234],
    )
    """The total number of authoritative zone records."""

    total_filtered: int = Field(
        title='Total Authoritative Zone Records Found',
        description='The total number of authoritative zone records found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of authoritative zone records found based on the current request criteria."""
