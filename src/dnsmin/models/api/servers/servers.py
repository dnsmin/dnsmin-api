from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from dnsmin.lib.sync.models import ServerSyncPolicy
from dnsmin.models.api import BaseApiModel
from dnsmin.models.enums import ServerTypeEnum, AuthServerModeEnum


class ServerInSchema(BaseApiModel):
    """Provides an API input model for creating and updating servers."""

    type: ServerTypeEnum = Field(
        title='Server Type',
        description='The type of DNS server.',
    )
    """The type of DNS server."""

    mode: AuthServerModeEnum = Field(
        title='Server Mode',
        description='The mode of DNS server.',
    )
    """The mode of DNS server."""

    server_id: str = Field(
        title='Server API ID',
        description='The API server ID of the server.',
        default='localhost',
    )
    """The API server ID of the server."""

    version: str = Field(
        title='Software Version',
        description='The version of the server software.',
        examples=['5.0.2', '4.9.11'],
    )
    """The version of the server software."""

    hostname: str = Field(
        title='Server Hostname',
        description='The hostname or IP address of the server.',
    )
    """The hostname or IP address of the server."""

    api_url: str = Field(
        title='Server API URL',
        description='The fully qualified or relative URL of the server\'s API endpoint.',
    )
    """The fully qualified or relative URL of the server's API endpoint."""

    api_key: str = Field(
        title='Server API Key',
        description='The API key used to authenticate to the server API.',
    )
    """The API key used to authenticate to the server API."""

    shared: bool = Field(
        title='Server Shared',
        description='Indicates whether the server is shared between tenants.',
        default=False,
    )
    """Indicates whether the server is shared between tenants."""

    sync_policy: Optional[ServerSyncPolicy] = Field(
        title='Synchronization Policy',
        description='The synchronization policy of the server.',
        default=None,
        examples=[ServerSyncPolicy()],
    )
    """The synchronization policy of the server."""


class ServerOutSchema(BaseApiModel):
    """Provides an API response model for representing servers."""

    id: UUID = Field(
        title='Server ID',
        description='The unique identifier of the server.',
        examples=[uuid4()],
    )
    """The unique identifier of the server."""

    type: ServerTypeEnum = Field(
        title='Server Type',
        description='The type of DNS server.',
    )
    """The type of DNS server."""

    mode: AuthServerModeEnum = Field(
        title='Server Mode',
        description='The mode of DNS server.',
    )
    """The mode of DNS server."""

    server_id: str = Field(
        title='Server API ID',
        description='The API server ID of the server.',
        default='localhost',
    )
    """The API server ID of the server."""

    version: str = Field(
        title='Software Version',
        description='The version of the server software.',
        examples=['5.0.2', '4.9.11'],
    )
    """The version of the server software."""

    hostname: str = Field(
        title='Server Hostname',
        description='The hostname or IP address of the server.',
    )
    """The hostname or IP address of the server."""

    api_url: str = Field(
        title='Server API URL',
        description='The fully qualified or relative URL of the server\'s API endpoint.',
    )
    """The fully qualified or relative URL of the server's API endpoint."""

    api_key: str = Field(
        title='Server API Key',
        description='The API key used to authenticate to the server API.',
    )
    """The API key used to authenticate to the server API."""

    shared: bool = Field(
        title='Server Shared',
        description='Indicates whether the server is shared between tenants.',
        default=False,
    )
    """Indicates whether the server is shared between tenants."""

    sync_policy: Optional[ServerSyncPolicy] = Field(
        title='Synchronization Policy',
        description='The synchronization policy of the server.',
        default=None,
        examples=[ServerSyncPolicy()],
    )
    """The synchronization policy of the server."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the server was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the server was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the server was last updated.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the server was last updated."""


class ServersSchema(BaseApiModel):
    """Provides an API response model for retrieving servers."""

    records: list[ServerOutSchema] = Field(
        title='Servers',
        description='A list of servers found based on the current request criteria.',
        default_factory=list,
    )
    """A list of servers found based on the current request criteria."""

    total: int = Field(
        title='Total Servers',
        description='The total number of servers.',
        default=0,
        examples=[1234],
    )
    """The total number of servers."""

    total_filtered: int = Field(
        title='Total Servers Found',
        description='The total number of servers found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of servers found based on the current request criteria."""
