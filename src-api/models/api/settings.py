from datetime import datetime, date, time
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models.api import BaseApiModel


class SettingInSchema(BaseApiModel):
    """Provides an API input model for a system setting."""

    key: str = Field(
        title='Setting Key',
        description='The key of this setting.',
    )
    """The key of this setting."""

    value: Optional[str] = Field(
        title='Setting Value',
        description="The value of this setting.",
        default=None,
    )
    """The value of this setting."""

    overridable: bool = Field(
        title='Setting Overridable',
        description='Whether the setting can be overridden in lower contexts.',
        default=False,
    )
    """Whether the setting can be overridden in lower contexts."""

    hidden: bool = Field(
        title='Setting Hidden',
        description='Whether the setting is hidden in lower contexts.',
        default=False,
    )
    """Whether the setting is hidden in lower contexts."""

    readonly: bool = Field(
        title='Setting Read-Only',
        description='Whether the setting can be modified in non-system contexts.',
        default=False,
    )
    """Whether the setting can be modified in non-system contexts."""


class SettingOutSchema(BaseApiModel):
    """Provides an API response model for a system setting."""

    id: UUID = Field(
        title='ID',
        description='The unique identifier of this setting.',
        examples=[uuid4()],
    )
    """The unique identifier of this setting."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The tenant ID that this setting is associated with if any.',
        default=None,
        examples=[uuid4()],
    )
    """The tenant ID that this setting is associated with."""

    user_id: Optional[UUID] = Field(
        title='User ID',
        description='The user ID that this setting is associated with if any.',
        default=None,
        examples=[uuid4()],
    )
    """The user ID that this setting is associated with."""

    key: str = Field(
        title='Setting Key',
        description='The key of this setting.',
    )
    """The key of this setting."""

    value: Optional[str | int | float | bool | datetime | date | time | tuple | list | dict] = Field(
        title='Setting Value',
        description="The value of this setting.",
        default=None,
    )
    """The value of this setting."""

    overridable: bool = Field(
        title='Setting Overridable',
        description='Whether the setting can be overridden in lower contexts.',
        default=False,
    )
    """Whether the setting can be overridden in lower contexts."""

    hidden: bool = Field(
        title='Setting Hidden',
        description='Whether the setting is hidden in lower contexts.',
        default=False,
    )
    """Whether the setting is hidden in lower contexts."""

    readonly: bool = Field(
        title='Setting Read-Only',
        description='Whether the setting can be modified in non-system contexts.',
        default=False,
    )
    """Whether the setting can be modified in non-system contexts."""

    created_at: Optional[datetime] = Field(
        title='Setting Created Timestamp',
        description='The date and time the setting was created.',
        default=None,
    )
    """The date and time the setting was created."""

    updated_at: Optional[datetime] = Field(
        title='Setting Updated Timestamp',
        description='The date and time the setting was updated.',
        default=None,
    )
    """The date and time the setting was updated."""


class SettingsOutSchema(BaseApiModel):
    """Provides an API response model for retrieving settings."""

    records: list[SettingOutSchema] = Field(
        title='Settings',
        description='A list of settings found based on the current request criteria.',
        default_factory=list,
    )
    """A list of settings found based on the current request criteria."""

    total: int = Field(
        title='Total Settings',
        description='The total number of settings.',
        default=0,
        examples=[1234],
    )
    """The total number of settings."""

    total_filtered: int = Field(
        title='Total Settings Found',
        description='The total number of settings found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of settings found based on the current request criteria."""
