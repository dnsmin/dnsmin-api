from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models.api import BaseApiModel


class StopgapDomainInSchema(BaseApiModel):
    """Provides an API input model for creating and updating stopgap domains."""

    name: str = Field(
        title='Stopgap Domain Friendly Name',
        description='The friendly name of the stopgap domain.',
        examples=['US Tenants', 'European Tenants'],
    )
    """The friendly name of the stopgap domain."""

    fqdn: str = Field(
        title='Stopgap FQDN',
        description='The FQDN for the base stopgap domain.',
    )
    """The FQDN for the base stopgap domain."""

    restricted_hosts: Optional[list[str]] = Field(
        title='Restricted Hosts',
        description='The list of hostnames that are restricted from use by tenants.',
    )
    """The list of hostnames that are restricted from use by tenants."""


class StopgapDomainOutSchema(BaseApiModel):
    """Provides an API response model for representing stopgap domains."""

    id: UUID = Field(
        title='Stopgap Domain ID',
        description='The unique identifier of the stopgap domain.',
        examples=[uuid4()],
    )
    """The unique identifier of the stopgap domain."""

    name: str = Field(
        title='Stopgap Domain Friendly Name',
        description='The friendly name of the stopgap domain.',
        examples=['US Tenants', 'European Tenants'],
    )
    """The friendly name of the stopgap domain."""

    fqdn: str = Field(
        title='Stopgap FQDN',
        description='The FQDN for the base stopgap domain.',
    )
    """The FQDN for the base stopgap domain."""

    restricted_hosts: Optional[list[str]] = Field(
        title='Restricted Hosts',
        description='The list of hostnames that are restricted from use by tenants.',
    )
    """The list of hostnames that are restricted from use by tenants."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the stopgap domain was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the stopgap domain was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the stopgap domain was last updated.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the stopgap domain was last updated."""


class StopgapDomainsSchema(BaseApiModel):
    """Provides an API response model for retrieving stopgap domains."""

    records: list[StopgapDomainOutSchema] = Field(
        title='Stopgap Domains',
        description='A list of stopgap domains found based on the current request criteria.',
        default_factory=list,
    )
    """A list of stopgap domains found based on the current request criteria."""

    total: int = Field(
        title='Total Stopgap Domains',
        description='The total number of stopgap domains.',
        default=0,
        examples=[1234],
    )
    """The total number of stopgap domains."""

    total_filtered: int = Field(
        title='Total Stopgap Domains Found',
        description='The total number of stopgap domains found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of stopgap domains found based on the current request criteria."""
