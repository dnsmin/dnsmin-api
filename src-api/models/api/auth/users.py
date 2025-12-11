from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models.api import BaseApiModel
from models.enums import UserStatusEnum


class UserInSchema(BaseApiModel):
    """Provides an API input model for creating and updating authentication users."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the user (if any).',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the user (if any)."""

    username: str = Field(
        title='Username',
        description='The username of the user.',
        examples=['YourName', 'your.name@your-domain.com'],
    )
    """The username of the user."""

    password: Optional[str] = Field(
        title='Password',
        description='The password of the user.',
        default=None,
    )
    """The password of the user."""

    email: Optional[str] = Field(
        title='Email',
        description='The email address of the user.',
        default=None,
        examples=['your.name@yourdomain.com'],
    )
    """The email address of the user."""

    phone_number: Optional[str] = Field(
        title='Phone Number',
        description='The phone number of the user in E.164 format.',
        default=None,
        examples=['17685551234', '18005554321'],
    )
    """The phone number of the user in E.164 format."""

    status: UserStatusEnum = Field(
        title='Status',
        description='The status of the user.',
        default=UserStatusEnum.pending,
        examples=[
            UserStatusEnum.pending.value,
            UserStatusEnum.invited.value,
            UserStatusEnum.active.value,
            UserStatusEnum.suspended.value,
            UserStatusEnum.disabled.value,
        ],
    )
    """The status of the user."""


class UserOutSchema(BaseApiModel):
    """Provides an API response model for representing authentication users."""

    id: Optional[UUID] = Field(
        title='User ID',
        description='The unique identifier of the user.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the user."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the user (if any).',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the user (if any)."""

    username: str = Field(
        title='Username',
        description='The username of the user.',
        examples=['YourName', 'your.name@your-domain.com'],
    )
    """The username of the user."""

    email: Optional[str] = Field(
        title='Email',
        description='The email address of the user.',
        examples=['your.name@yourdomain.com'],
    )
    """The email address of the user."""

    phone_number: Optional[str] = Field(
        title='Phone Number',
        description='The phone number of the user in E.164 format.',
        examples=['17685551234', '18005554321'],
    )
    """The phone number of the user in E.164 format."""

    status: UserStatusEnum = Field(
        title='Status',
        description='The status of the user.',
        default=UserStatusEnum.pending,
        examples=[
            UserStatusEnum.pending.value,
            UserStatusEnum.invited.value,
            UserStatusEnum.active.value,
            UserStatusEnum.suspended.value,
            UserStatusEnum.disabled.value,
        ],
    )
    """The status of the user."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the user was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the user was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the user was last updated.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the user was last updated."""

    authenticated_at: Optional[datetime] = Field(
        title='Authenticated At',
        description='The timestamp representing when the user was last authenticated.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the user was last authenticated."""


class UsersSchema(BaseApiModel):
    """Provides an API response model for retrieving authentication users."""

    records: list[UserOutSchema] = Field(
        title='Users',
        description='A list of users found based on the current request criteria.',
        default_factory=list,
    )
    """A list of users found based on the current request criteria."""

    total: int = Field(
        title='Total Users Found',
        description='The total number of users found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of users found based on the current request criteria."""
