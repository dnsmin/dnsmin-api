from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models.api import BaseApiModel


class ServerViewInSchema(BaseApiModel):
    """Provides an API input model for creating and updating server views."""

    server_id: UUID = Field(
        title='Server ID',
        description='The unique identifier of the server associated with the view.',
        examples=[uuid4()],
    )
    """The unique identifier of the server associated with the view."""

    name: str = Field(
        title='View Name',
        description='The name of the view.',
        examples=['trusted', 'internal', 'global'],
    )
    """The name of the view."""


class ServerViewOutSchema(BaseApiModel):
    """Provides an API response model for representing server views."""

    id: UUID = Field(
        title='ServerView ID',
        description='The unique identifier of the server.',
        examples=[uuid4()],
    )
    """The unique identifier of the server."""

    server_id: UUID = Field(
        title='Server ID',
        description='The unique identifier of the server associated with the view.',
        examples=[uuid4()],
    )
    """The unique identifier of the server associated with the view."""

    name: str = Field(
        title='View Name',
        description='The name of the view.',
        examples=['trusted', 'internal', 'global'],
    )
    """The name of the view."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the view was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the view was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the view was last updated.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the view was last updated."""


class ServerViewsSchema(BaseApiModel):
    """Provides an API response model for retrieving server views."""

    records: list[ServerViewOutSchema] = Field(
        title='Server Views',
        description='A list of server views found based on the current request criteria.',
        default_factory=list,
    )
    """A list of server views found based on the current request criteria."""

    total: int = Field(
        title='Total Server Views',
        description='The total number of server views.',
        default=0,
        examples=[1234],
    )
    """The total number of server views."""

    total_filtered: int = Field(
        title='Total Server Views Found',
        description='The total number of server views found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of server views found based on the current request criteria."""
