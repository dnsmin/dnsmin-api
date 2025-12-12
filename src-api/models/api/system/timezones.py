from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models.api import BaseApiModel


class TimezoneInSchema(BaseApiModel):
    """Provides an API input model for creating and updating timezones."""

    name: str = Field(
        title='Timezone IANA Name',
        description='The unique IANA name for the timezone.',
        examples=['Africa/Johannesburg', 'America/Indiana/Indianapolis', 'Asia/Tokyo'],
    )
    """The unique IANA name for the timezone."""

    offset: int = Field(
        title='Timezone Offset',
        description='The offset from UTC in seconds for the timezone.',
    )
    """The offset from UTC in seconds for the timezone."""

    offset_dst: int = Field(
        title='Timezone DST Offset',
        description='The offset from UTC in seconds during daylight savings time for the timezone.',
    )
    """The offset from UTC in seconds during daylight savings time for the timezone."""


class TimezoneOutSchema(BaseApiModel):
    """Provides an API response model for representing timezones."""

    id: UUID = Field(
        title='Timezone ID',
        description='The unique identifier of the timezone.',
        examples=[uuid4()],
    )
    """The unique identifier of the timezone."""

    name: str = Field(
        title='Timezone IANA Name',
        description='The unique IANA name for the timezone.',
        examples=['Africa/Johannesburg', 'America/Indiana/Indianapolis', 'Asia/Tokyo'],
    )
    """The unique IANA name for the timezone."""

    offset: int = Field(
        title='Timezone Offset',
        description='The offset from UTC in seconds for the timezone.',
    )
    """The offset from UTC in seconds for the timezone."""

    offset_dst: int = Field(
        title='Timezone DST Offset',
        description='The offset from UTC in seconds during daylight savings time for the timezone.',
    )
    """The offset from UTC in seconds during daylight savings time for the timezone."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the timezone was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the timezone was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the timezone was last updated.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the timezone was last updated."""


class TimezonesSchema(BaseApiModel):
    """Provides an API response model for retrieving timezones."""

    records: list[TimezoneOutSchema] = Field(
        title='Timezones',
        description='A list of timezones found based on the current request criteria.',
        default_factory=list,
    )
    """A list of timezones found based on the current request criteria."""

    total: int = Field(
        title='Total Timezones',
        description='The total number of timezones.',
        default=0,
        examples=[1234],
    )
    """The total number of timezones."""

    total_filtered: int = Field(
        title='Total Timezones Found',
        description='The total number of timezones found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of timezones found based on the current request criteria."""
