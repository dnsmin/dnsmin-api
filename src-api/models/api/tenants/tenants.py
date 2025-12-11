from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models.api import BaseApiModel


class TenantInSchema(BaseApiModel):
    """Provides an API input model for creating and updating tenants."""

    name: str = Field(
        title='Tenant Name',
        description='The name of the tenant.',
    )
    """The name of the tenant."""

    fqdn: Optional[str] = Field(
        title='Tenant FQDN',
        description='The FQDN for the tenant UI.',
    )
    """The FQDN for the tenant UI."""

    stopgap_domain_id: Optional[UUID] = Field(
        title='Stopgap Domain ID',
        description='The unique identifier of the associated stopgap domain.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the associated stopgap domain."""

    stopgap_hostname: Optional[str] = Field(
        title='Stopgap Hostname',
        description='The hostname used within the associated stopgap domain.',
        default=None,
    )
    """The hostname used within the associated stopgap domain."""


class TenantOutSchema(BaseApiModel):
    """Provides an API response model for representing tenants."""

    id: UUID = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant.',
        examples=[uuid4()],
    )
    """The unique identifier of the tenant."""

    name: str = Field(
        title='Tenant Name',
        description='The name of the tenant.',
    )
    """The name of the tenant."""

    fqdn: Optional[str] = Field(
        title='Tenant FQDN',
        description='The FQDN for the tenant UI.',
    )
    """The FQDN for the tenant UI."""

    stopgap_domain_id: Optional[UUID] = Field(
        title='Stopgap Domain ID',
        description='The unique identifier of the associated stopgap domain.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the associated stopgap domain."""

    stopgap_hostname: Optional[str] = Field(
        title='Stopgap Hostname',
        description='The hostname used within the associated stopgap domain.',
        default=None,
    )
    """The hostname used within the associated stopgap domain."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the tenant was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the tenant was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the tenant was last updated.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the tenant was last updated."""


class TenantsSchema(BaseApiModel):
    """Provides an API response model for retrieving tenants."""

    records: list[TenantOutSchema] = Field(
        title='Tenants',
        description='A list of tenants found based on the current request criteria.',
        default_factory=list,
    )
    """A list of tenants found based on the current request criteria."""

    total: int = Field(
        title='Total Tenants',
        description='The total number of tenants.',
        default=0,
        examples=[1234],
    )
    """The total number of tenants."""

    total_filtered: int = Field(
        title='Total Tenants Found',
        description='The total number of tenants found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of tenants found based on the current request criteria."""
