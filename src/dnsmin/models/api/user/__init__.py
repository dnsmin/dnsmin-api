from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from dnsmin.models.api import BaseApiModel
from dnsmin.models.enums import AuthenticatorTypeEnum


class UserAuthenticatorSchema(BaseApiModel):
    """Represents an authentication user authenticator for API interactions."""

    id: Optional[UUID] = Field(
        title='Session ID',
        description='The unique identifier of the authenticator.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the session."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the authenticator (if any).',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the authenticator (if any)."""

    user_id: UUID = Field(
        title='User ID',
        description='The unique identifier of the user associated with the authenticator.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the user associated with the authenticator."""

    type: AuthenticatorTypeEnum = Field(
        title='Authenticator Type',
        description='The type of the authenticator.',
        examples=[
            AuthenticatorTypeEnum.WEBAUTHN,
            AuthenticatorTypeEnum.TOTP,
            AuthenticatorTypeEnum.SMS,
            AuthenticatorTypeEnum.EMAIL,
        ],
    )
    """The type of the authenticator."""

    name: str = Field(
        title='Authenticator Name',
        description='The name of the authenticator.',
        examples=[
            AuthenticatorTypeEnum.WEBAUTHN,
            AuthenticatorTypeEnum.TOTP,
            AuthenticatorTypeEnum.SMS,
            AuthenticatorTypeEnum.EMAIL,
        ],
    )
    """The name of the authenticator."""

    data: str = Field(
        title='Secret Data',
        description='The secret data of the authenticator.',
    )
    """The secret data of the authenticator."""

    enabled: bool = Field(
        title='Authenticator Enabled',
        description='Whether the authenticator is enabled.',
        default=True,
    )
    """Whether the authenticator is enabled."""

    created_at: Optional[datetime] = Field(
        title='Created At',
        description='The timestamp representing when the authenticator was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the authenticator was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the authenticator was last updated.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the authenticator was last updated."""

    used_at: Optional[datetime] = Field(
        title='Last Used At',
        description='The timestamp representing when the authenticator was last used.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the authenticator was last used."""


class UserAuthenticatorsSchema(BaseApiModel):
    """Represents a list of authentication user authenticators for API interactions."""

    records: list[UserAuthenticatorSchema] = Field(
        title='Authenticators',
        description='A list of user authenticators found based on the current request criteria.',
        default_factory=list,
    )
    """A list of user authenticators found based on the current request criteria."""

    total: int = Field(
        title='Total User Authenticators Found',
        description='The total number of user authenticators found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of user authenticators found based on the current request criteria."""
