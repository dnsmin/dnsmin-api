from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from dnsmin.models import BaseApiModel


class AZoneMetadataInSchema(BaseApiModel):
    """Provides an API input model for creating and updating authoritative zone metadata."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the authoritative zone metadata if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the authoritative zone metadata if any."""

    zone_id: UUID = Field(
        title='Zone ID',
        description='The unique identifier of the zone associated with the authoritative zone metadata if any.',
        examples=[uuid4()],
    )
    """The unique identifier of the zone associated with the authoritative zone metadata if any."""

    view_id: Optional[UUID] = Field(
        title='View ID',
        description='The unique identifier of the server view associated with the authoritative zone metadata if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the server view associated with the authoritative zone metadata if any."""

    name: str = Field(
        title='Metadata Type',
        description='The kind of the metadata.',
    )
    """The kind of the metadata."""

    values: Optional[list[str]] = Field(
        title='Metadata Values',
        description='The list of metadata values associated with this kind.',
        default=None,
    )
    """The list of metadata values associated with this kind."""


class AZoneMetadataOutSchema(BaseApiModel):
    """Provides an API response model for representing authoritative zone metadata."""

    id: UUID = Field(
        title='Metadata ID',
        description='The unique identifier of the authoritative zone.',
        examples=[uuid4()],
    )
    """The unique identifier of the authoritative zone."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the authoritative zone metadata if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the authoritative zone metadata if any."""

    zone_id: UUID = Field(
        title='Zone ID',
        description='The unique identifier of the zone associated with the authoritative zone metadata if any.',
        examples=[uuid4()],
    )
    """The unique identifier of the zone associated with the authoritative zone metadata if any."""

    view_id: Optional[UUID] = Field(
        title='View ID',
        description='The unique identifier of the server view associated with the authoritative zone metadata if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the server view associated with the authoritative zone metadata if any."""

    name: str = Field(
        title='Metadata Type',
        description='The kind of the metadata.',
    )
    """The kind of the metadata."""

    values: Optional[list[str]] = Field(
        title='Metadata Values',
        description='The list of metadata values associated with this kind.',
        default=None,
    )
    """The list of metadata values associated with this kind."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the authoritative zone metadata was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the authoritative zone metadata was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the authoritative zone metadata was last updated.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the authoritative zone metadata was last updated."""


class AZoneMetadataSchema(BaseApiModel):
    """Provides an API response model for retrieving authoritative zone metadata."""

    records: list[AZoneMetadataOutSchema] = Field(
        title='Authoritative Zone Metadata',
        description='A list of authoritative zone metadata found based on the current request criteria.',
        default_factory=list,
    )
    """A list of authoritative zone metadata found based on the current request criteria."""

    total: int = Field(
        title='Total Authoritative Zone Metadata',
        description='The total number of authoritative zone metadata.',
        default=0,
        examples=[1234],
    )
    """The total number of authoritative zone metadata."""

    total_filtered: int = Field(
        title='Total Authoritative Zone Metadata Found',
        description='The total number of authoritative zone metadata found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of authoritative zone metadata found based on the current request criteria."""
