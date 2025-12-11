from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models.api import BaseApiModel


class ServerAutoPrimaryInSchema(BaseApiModel):
    """Provides an API input model for creating and updating auto-primaries."""

    server_id: UUID = Field(
        title='Server ID',
        description='The unique identifier of the server associated with the auto-primary.',
        examples=[uuid4()],
    )
    """The unique identifier of the server associated with the auto-primary."""

    ip: str = Field(
        title='Auto-Primary IP Address',
        description='The IP address of the auto-primary server.',
        examples=['1.1.1.1', '10.0.0.1'],
    )
    """The IP address of the auto-primary server."""

    nameserver: str = Field(
        title='Auto-Primary DNS Name',
        description='The DNS name of the auto-primary server.',
    )
    """The DNS name of the auto-primary server."""

    account: Optional[str] = Field(
        title='Auto-Primary Account Name',
        description='The account name for the auto-primary server.',
    )
    """The account name for the auto-primary server."""


class ServerAutoPrimaryOutSchema(BaseApiModel):
    """Provides an API response model for representing auto-primaries."""

    id: UUID = Field(
        title='Auto-Primary ID',
        description='The unique identifier of the auto-primary.',
        examples=[uuid4()],
    )
    """The unique identifier of the auto-primary."""

    server_id: UUID = Field(
        title='Server ID',
        description='The unique identifier of the server associated with the auto-primary.',
        examples=[uuid4()],
    )
    """The unique identifier of the server associated with the auto-primary."""

    ip: str = Field(
        title='Auto-Primary IP Address',
        description='The IP address of the auto-primary server.',
        examples=['1.1.1.1', '10.0.0.1'],
    )
    """The IP address of the auto-primary server."""

    nameserver: str = Field(
        title='Auto-Primary DNS Name',
        description='The DNS name of the auto-primary server.',
    )
    """The DNS name of the auto-primary server."""

    account: Optional[str] = Field(
        title='Auto-Primary Account Name',
        description='The account name for the auto-primary server.',
    )
    """The account name for the auto-primary server."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the auto-primary was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the auto-primary was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the auto-primary was last updated.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the auto-primary was last updated."""


class ServerAutoPrimariesSchema(BaseApiModel):
    """Provides an API response model for retrieving auto-primaries."""

    records: list[ServerAutoPrimaryOutSchema] = Field(
        title='Auto-Primaries',
        description='A list of auto-primaries found based on the current request criteria.',
        default_factory=list,
    )
    """A list of auto-primaries found based on the current request criteria."""

    total: int = Field(
        title='Total Auto-Primaries',
        description='The total number of auto-primaries.',
        default=0,
        examples=[1234],
    )
    """The total number of auto-primaries."""

    total_filtered: int = Field(
        title='Total Auto-Primaries Found',
        description='The total number of auto-primaries found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of auto-primaries found based on the current request criteria."""
