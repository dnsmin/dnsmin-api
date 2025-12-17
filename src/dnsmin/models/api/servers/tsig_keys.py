from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from dnsmin.models.api import BaseApiModel


class ServerTSIGKeyInSchema(BaseApiModel):
    """Provides an API input model for creating and updating server TSIG keys."""

    server_id: UUID = Field(
        title='Server ID',
        description='The unique identifier of the server associated with the TSIG key.',
        examples=[uuid4()],
    )
    """The unique identifier of the server associated with the TSIG key."""

    algorithm: str = Field(
        title='TSIG Key Algorithm',
        description='The algorithm of the TSIG key.',
    )
    """The algorithm of the TSIG key."""

    key: str = Field(
        title='TSIG Key Secret Key',
        description='The base64 encoded secret key.',
    )
    """The base64 encoded secret key."""


class ServerTSIGKeyOutSchema(BaseApiModel):
    """Provides an API response model for representing server TSIG keys."""

    id: UUID = Field(
        title='TSIG Key ID',
        description='The unique identifier of the TSIG key.',
        examples=[uuid4()],
    )
    """The unique identifier of the TSIG key."""

    server_id: UUID = Field(
        title='Server ID',
        description='The unique identifier of the server associated with the TSIG key.',
        examples=[uuid4()],
    )
    """The unique identifier of the server associated with the TSIG key."""

    internal_id: Optional[str] = Field(
        title='TSIG Key Internal ID',
        description='The internal identifier, read only.',
        default=None,
    )
    """The internal identifier, read only."""

    algorithm: str = Field(
        title='TSIG Key Algorithm',
        description='The algorithm of the TSIG key.',
    )
    """The algorithm of the TSIG key."""

    key: str = Field(
        title='TSIG Key Secret Key',
        description='The base64 encoded secret key.',
    )
    """The base64 encoded secret key."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the TSIG key was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the TSIG key was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the TSIG key was last updated.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the TSIG key was last updated."""


class ServerTSIGKeysSchema(BaseApiModel):
    """Provides an API response model for retrieving server TSIG keys."""

    records: list[ServerTSIGKeyOutSchema] = Field(
        title='Server TSIG Keys',
        description='A list of server TSIG keys found based on the current request criteria.',
        default_factory=list,
    )
    """A list of server TSIG keys found based on the current request criteria."""

    total: int = Field(
        title='Total Server TSIG Keys',
        description='The total number of server TSIG keys.',
        default=0,
        examples=[1234],
    )
    """The total number of server TSIG keys."""

    total_filtered: int = Field(
        title='Total Server TSIG Keys Found',
        description='The total number of server TSIG keys found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of server TSIG keys found based on the current request criteria."""
