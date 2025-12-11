from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models.api import BaseApiModel
from models.enums import CryptoKeyTypeEnum


class CryptoKeyInSchema(BaseApiModel):
    """Provides an API input model for creating and updating crypto keys."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the crypto key if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the crypto key if any."""

    type: CryptoKeyTypeEnum = Field(
        title='Crypto Key Type',
        description='The type of the key.',
    )
    """The type of the key."""

    active: bool = Field(
        title='Crypto Key Active',
        description='Whether the key is in active use.',
        default=False,
    )
    """Whether the key is in active use."""

    published: bool = Field(
        title='Crypto Key Published',
        description='Whether the DNSKEY crypto key is published in the zone.',
        default=False,
    )
    """Whether the DNSKEY crypto key is published in the zone."""

    dns_key: Optional[str] = Field(
        title='Crypto Key DNSKEY',
        description='The DNSKEY crypto key for this key.',
        default=None,
    )
    """The DNSKEY crypto key for this key."""

    ds: Optional[list[str]] = Field(
        title='DS Crypto Keys',
        description='A list of DS crypto keys for this key.',
        default=None,
    )
    """A list of DS crypto keys for this key."""

    cds: Optional[list[str]] = Field(
        title='Filtered DS Crypto Keys',
        description='A list of DS crypto keys for this key, filtered by CDS publication settings.',
        default=None,
    )
    """A list of DS crypto keys for this key, filtered by CDS publication settings."""

    private_key: Optional[str] = Field(
        title='Private Key',
        description='The private key in ISC format.',
        default=None,
    )
    """The private key in ISC format."""

    algorithm: Optional[str] = Field(
        title='Crypto Key Algorithm',
        description='The name of the algorithm of the key, should be a mnemonic.',
        default=None,
    )
    """The name of the algorithm of the key, should be a mnemonic."""

    bits: int = Field(
        title='Crypto Key Bits',
        description='The size of the key.',
        examples=[128, 256, 512, 1024, 2048, 4096],
    )
    """The size of the key."""


class CryptoKeyOutSchema(BaseApiModel):
    """Provides an API response model for representing crypto keys."""

    id: UUID = Field(
        title='Crypto Key ID',
        description='The unique identifier of the crypto key.',
        examples=[uuid4()],
    )
    """The unique identifier of the crypto key."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the crypto key if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the crypto key if any."""

    internal_id: Optional[int] = Field(
        title='Crypto Key Internal ID',
        description='The internal identifier, read only.',
        default=False,
    )
    """The internal identifier, read only."""

    type: CryptoKeyTypeEnum = Field(
        title='Crypto Key Type',
        description='The type of the key.',
    )
    """The type of the key."""

    active: bool = Field(
        title='Crypto Key Active',
        description='Whether the key is in active use.',
        default=False,
    )
    """Whether the key is in active use."""

    published: bool = Field(
        title='Crypto Key Published',
        description='Whether the DNSKEY crypto key is published in the zone.',
        default=False,
    )
    """Whether the DNSKEY crypto key is published in the zone."""

    dns_key: Optional[str] = Field(
        title='Crypto Key DNSKEY',
        description='The DNSKEY crypto key for this key.',
        default=None,
    )
    """The DNSKEY crypto key for this key."""

    ds: Optional[list[str]] = Field(
        title='DS Crypto Keys',
        description='A list of DS crypto keys for this key.',
        default=None,
    )
    """A list of DS crypto keys for this key."""

    cds: Optional[list[str]] = Field(
        title='Filtered DS Crypto Keys',
        description='A list of DS crypto keys for this key, filtered by CDS publication settings.',
        default=None,
    )
    """A list of DS crypto keys for this key, filtered by CDS publication settings."""

    private_key: Optional[str] = Field(
        title='Private Key',
        description='The private key in ISC format.',
        default=None,
    )
    """The private key in ISC format."""

    algorithm: Optional[str] = Field(
        title='Crypto Key Algorithm',
        description='The name of the algorithm of the key, should be a mnemonic.',
        default=None,
    )
    """The name of the algorithm of the key, should be a mnemonic."""

    bits: int = Field(
        title='Crypto Key Bits',
        description='The size of the key.',
        examples=[128, 256, 512, 1024, 2048, 4096],
    )
    """The size of the key."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the crypto key was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the crypto key was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the crypto key was last updated.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the crypto key was last updated."""


class CryptoKeysSchema(BaseApiModel):
    """Provides an API response model for retrieving crypto keys."""

    records: list[CryptoKeyOutSchema] = Field(
        title='Crypto Keys',
        description='A list of crypto keys found based on the current request criteria.',
        default_factory=list,
    )
    """A list of crypto keys found based on the current request criteria."""

    total: int = Field(
        title='Total Crypto Keys',
        description='The total number of crypto keys.',
        default=0,
        examples=[1234],
    )
    """The total number of crypto keys."""

    total_filtered: int = Field(
        title='Total Crypto Keys Found',
        description='The total number of crypto keys found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of crypto keys found based on the current request criteria."""
