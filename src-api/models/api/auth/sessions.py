from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models.api import BaseApiModel


class SessionOutSchema(BaseApiModel):
    """Provides an API response model for representing authentication sessions."""

    id: UUID = Field(
        title='Session ID',
        description='The unique identifier of the session.',
        examples=[uuid4()],
    )
    """The unique identifier of the session."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the user (if any).',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the user (if any)."""

    user_id: UUID = Field(
        title='User ID',
        description='The unique identifier of the user associated with the session.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the user associated with the session."""

    client_ip: str = Field(
        title='Client IP',
        description='The IPv4 or IPv6 address of the session client.',
        examples=['1.1.1.1', '2001:0db8:85a3:0000:0000:8a2e:0370:7334'],
    )
    """The IPv4 or IPv6 address of the session client."""

    token: str = Field(
        title='Session Token',
        description='The opaque identifier token for session persistence on clients.',
    )
    """The opaque identifier token for session persistence on clients."""

    data: Optional[dict] = Field(
        title='Session Data',
        description='The JSON-encoded data of the session.',
    )
    """The JSON-encoded data of the session."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the session was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the session was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the session was last updated.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the session was last updated."""

    expires_at: Optional[datetime] = Field(
        title='Expires At',
        description='The timestamp representing when the session expires.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the session expires."""


class SessionsSchema(BaseApiModel):
    """Provides an API response model for retrieving authentication sessions."""

    records: list[SessionOutSchema] = Field(
        title='Sessions',
        description='A list of sessions found based on the current request criteria.',
        default_factory=list,
    )
    """A list of sessions found based on the current request criteria."""

    total: int = Field(
        title='Total Sessions',
        description='The total number of sessions.',
        default=0,
        examples=[1234],
    )
    """The total number of sessions."""

    total_filtered: int = Field(
        title='Total Sessions Found',
        description='The total number of sessions found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of sessions found based on the current request criteria."""
