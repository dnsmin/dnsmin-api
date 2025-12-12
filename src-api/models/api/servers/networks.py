from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models.api import BaseApiModel


class ServerNetworkInSchema(BaseApiModel):
    """Provides an API input model for creating and updating server networks."""

    server_id: UUID = Field(
        title='Server ID',
        description='The unique identifier of the server associated with the network.',
        examples=[uuid4()],
    )
    """The unique identifier of the server associated with the network."""

    view_id: UUID = Field(
        title='View ID',
        description='The unique identifier of the view associated with the network.',
        examples=[uuid4()],
    )
    """The unique identifier of the view associated with the network."""

    network: str = Field(
        title='Network CIDR',
        description='The CIDR specification of the network.',
        examples=['1.1.1.1/8', '192.168.1.0/24', '10.0.1.2/16'],
    )
    """The CIDR specification of the network."""


class ServerNetworkOutSchema(BaseApiModel):
    """Provides an API response model for representing server networks."""

    id: UUID = Field(
        title='ServerNetwork ID',
        description='The unique identifier of the server.',
        examples=[uuid4()],
    )
    """The unique identifier of the server."""

    server_id: UUID = Field(
        title='Server ID',
        description='The unique identifier of the server associated with the network.',
        examples=[uuid4()],
    )
    """The unique identifier of the server associated with the network."""

    view_id: UUID = Field(
        title='View ID',
        description='The unique identifier of the view associated with the network.',
        examples=[uuid4()],
    )
    """The unique identifier of the view associated with the network."""

    network: str = Field(
        title='Network CIDR',
        description='The CIDR specification of the network.',
        examples=['1.1.1.1/8', '192.168.1.0/24', '10.0.1.2/16'],
    )
    """The CIDR specification of the network."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the network was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the network was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the network was last updated.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the network was last updated."""


class ServerNetworksSchema(BaseApiModel):
    """Provides an API response model for retrieving server networks."""

    records: list[ServerNetworkOutSchema] = Field(
        title='Server Networks',
        description='A list of server networks found based on the current request criteria.',
        default_factory=list,
    )
    """A list of server networks found based on the current request criteria."""

    total: int = Field(
        title='Total Server Networks',
        description='The total number of server networks.',
        default=0,
        examples=[1234],
    )
    """The total number of server networks."""

    total_filtered: int = Field(
        title='Total Server Networks Found',
        description='The total number of server networks found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of server networks found based on the current request criteria."""
