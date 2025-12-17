from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from dnsmin.lib.permissions.definitions import Permissions
from dnsmin.models.api import BaseApiModel


class ClientInSchema(BaseApiModel):
    """Provides an API input model for creating and updating authentication clients."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the client.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the client if any."""

    user_id: Optional[UUID] = Field(
        title='User ID',
        description='The unique identifier of the user associated with the client.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the user associated with the client if any."""

    secret: Optional[str] = Field(
        title='Client Secret',
        description='The secret used for authenticating the client.',
        default=None,
    )
    """The secret used for authenticating the client."""

    name: str = Field(
        title='Client Name',
        description='The name of the client.',
        default=None,
    )
    """The name of the client."""

    redirect_uri: Optional[str] = Field(
        title='Redirect URI',
        description='The URL to redirect after authorization (if using auth code flow).',
        default=None,
        examples=['https://example.com'],
    )
    """The URL to redirect after authorization (if using auth code flow)."""

    scopes: Optional[list[str]] = Field(
        title='Scopes',
        description='The scopes associated with this client.',
        default=None,
        examples=[[
            Permissions.auth_users.uri,
            Permissions.auth_sessions.uri,
            Permissions.auth_clients.uri,
        ]],
    )
    """A list of scopes associated with the client."""

    enabled: bool = Field(
        title='Client Status',
        description='Whether the client is enabled.',
        default=True,
    )
    """Whether the client is enabled."""


class ClientOutSchema(BaseApiModel):
    """Provides an API response model for representing authentication clients."""

    id: UUID = Field(
        title='Client ID',
        description='The unique identifier of the client.',
        examples=[uuid4()],
    )
    """The unique identifier of the client."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the client if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the client if any."""

    user_id: Optional[UUID] = Field(
        title='User ID',
        description='The unique identifier of the user associated with the client if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the user associated with the client if any."""

    name: str = Field(
        title='Client Name',
        description='The name of the client.',
        default=None,
    )
    """The name of the client."""

    redirect_uri: Optional[str] = Field(
        title='Redirect URI',
        description='The URL to redirect after authorization (if using auth code flow).',
        default=None,
        examples=['https://example.com'],
    )
    """The URL to redirect after authorization (if using auth code flow)."""

    scopes: Optional[list[str]] = Field(
        title='Scopes',
        description='The scopes associated with this client.',
        default=None,
        examples=[[
            Permissions.auth_users.uri,
            Permissions.auth_sessions.uri,
            Permissions.auth_clients.uri,
        ]],
    )
    """A list of scopes associated with the client."""

    enabled: bool = Field(
        title='Client Status',
        description='Whether the client is enabled.',
        default=True,
    )
    """Whether the client is enabled."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the client was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the client was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the client was last updated.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the client was last updated."""

    expires_at: Optional[datetime] = Field(
        title='Expires At',
        description='The timestamp representing when the client expires.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the client expires."""


class ClientsSchema(BaseApiModel):
    """Provides an API response model for retrieving authentication clients."""

    records: list[ClientOutSchema] = Field(
        title='Clients',
        description='A list of clients found based on the current request criteria.',
        default_factory=list,
    )
    """A list of clients found based on the current request criteria."""

    total: int = Field(
        title='Total Clients',
        description='The total number of clients.',
        default=0,
        examples=[1234],
    )
    """The total number of clients."""

    total_filtered: int = Field(
        title='Total Clients Found',
        description='The total number of clients found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of clients found based on the current request criteria."""
