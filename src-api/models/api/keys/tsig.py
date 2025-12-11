from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models.api import BaseApiModel


class TSIGKeyInSchema(BaseApiModel):
    """Provides an API input model for creating and updating TSIG keys."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the TSIG key if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the TSIG key if any."""

    algorithm: Optional[str] = Field(
        title='TSIG Key Algorithm',
        description='The algorithm of the TSIG key.',
        default=None,
    )
    """The algorithm of the TSIG key."""

    key: Optional[str] = Field(
        title='TSIG Key Secret Key',
        description='The base64 encoded secret key.',
        default=None,
    )
    """The base64 encoded secret key."""


class TSIGKeyOutSchema(BaseApiModel):
    """Provides an API response model for representing TSIG keys."""

    id: UUID = Field(
        title='TSIG Key ID',
        description='The unique identifier of the TSIG key.',
        examples=[uuid4()],
    )
    """The unique identifier of the TSIG key."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the TSIG key if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the TSIG key if any."""

    internal_id: Optional[str] = Field(
        title='TSIG Key Internal ID',
        description='The internal identifier, read only.',
        default=False,
    )
    """The internal identifier, read only."""

    algorithm: Optional[str] = Field(
        title='TSIG Key Algorithm',
        description='The algorithm of the TSIG key.',
        default=None,
    )
    """The algorithm of the TSIG key."""

    key: Optional[str] = Field(
        title='TSIG Key Secret Key',
        description='The base64 encoded secret key.',
        default=None,
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
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the TSIG key was last updated."""


class TSIGKeysSchema(BaseApiModel):
    """Provides an API response model for retrieving TSIG keys."""

    records: list[TSIGKeyOutSchema] = Field(
        title='TSIG Keys',
        description='A list of TSIG keys found based on the current request criteria.',
        default_factory=list,
    )
    """A list of TSIG keys found based on the current request criteria."""

    total: int = Field(
        title='Total TSIG Keys',
        description='The total number of TSIG keys.',
        default=0,
        examples=[1234],
    )
    """The total number of TSIG keys."""

    total_filtered: int = Field(
        title='Total TSIG Keys Found',
        description='The total number of TSIG keys found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of TSIG keys found based on the current request criteria."""
