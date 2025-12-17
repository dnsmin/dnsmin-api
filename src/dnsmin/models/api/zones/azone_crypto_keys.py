from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from dnsmin.models import BaseApiModel, CryptoKeyTypeEnum


class AZoneCryptoKeyInSchema(BaseApiModel):
    """Provides an API input model for creating and updating authoritative zone crypto keys."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the crypto key if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the crypto key if any."""

    zone_id: UUID = Field(
        title='Zone ID',
        description='The unique identifier of the zone associated with the crypto key.',
        examples=[uuid4()],
    )
    """The unique identifier of the zone associated with the crypto key."""

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

    dns_key: str = Field(
        title='Crypto Key DNSKEY',
        description='The DNSKEY crypto key for this key.',
    )
    """The DNSKEY crypto key for this key."""

    ds: list[str] = Field(
        title='DS Crypto Keys',
        description='A list of DS crypto keys for this key.',
    )
    """A list of DS crypto keys for this key."""

    cds: list[str] = Field(
        title='Filtered DS Crypto Keys',
        description='A list of DS crypto keys for this key, filtered by CDS publication settings.',
    )
    """A list of DS crypto keys for this key, filtered by CDS publication settings."""

    private_key: str = Field(
        title='Private Key',
        description='The private key in ISC format.',
    )
    """The private key in ISC format."""

    algorithm: str = Field(
        title='Crypto Key Algorithm',
        description='The name of the algorithm of the key, should be a mnemonic.',
    )
    """The name of the algorithm of the key, should be a mnemonic."""

    bits: int = Field(
        title='Crypto Key Bits',
        description='The size of the key.',
        examples=[128, 256, 512, 1024, 2048, 4096],
    )
    """The size of the key."""


class AZoneCryptoKeyOutSchema(BaseApiModel):
    """Provides an API response model for representing authoritative zone crypto keys."""

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

    zone_id: UUID = Field(
        title='Zone ID',
        description='The unique identifier of the zone associated with the crypto key.',
        examples=[uuid4()],
    )
    """The unique identifier of the zone associated with the crypto key."""

    internal_id: Optional[int] = Field(
        title='Crypto Key Internal ID',
        description='The internal identifier, read only.',
        default=None,
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

    dns_key: str = Field(
        title='Crypto Key DNSKEY',
        description='The DNSKEY crypto key for this key.',
    )
    """The DNSKEY crypto key for this key."""

    ds: list[str] = Field(
        title='DS Crypto Keys',
        description='A list of DS crypto keys for this key.',
    )
    """A list of DS crypto keys for this key."""

    cds: list[str] = Field(
        title='Filtered DS Crypto Keys',
        description='A list of DS crypto keys for this key, filtered by CDS publication settings.',
    )
    """A list of DS crypto keys for this key, filtered by CDS publication settings."""

    private_key: str = Field(
        title='Private Key',
        description='The private key in ISC format.',
    )
    """The private key in ISC format."""

    algorithm: str = Field(
        title='Crypto Key Algorithm',
        description='The name of the algorithm of the key, should be a mnemonic.',
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
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the crypto key was last updated."""


class AZoneCryptoKeysSchema(BaseApiModel):
    """Provides an API response model for retrieving authoritative zone crypto keys."""

    records: list[AZoneCryptoKeyOutSchema] = Field(
        title='Authoritative Zone Crypto Keys',
        description='A list of authoritative zone crypto keys found based on the current request criteria.',
        default_factory=list,
    )
    """A list of authoritative zone crypto keys found based on the current request criteria."""

    total: int = Field(
        title='Total Authoritative Zone Crypto Keys',
        description='The total number of authoritative zone crypto keys.',
        default=0,
        examples=[1234],
    )
    """The total number of authoritative zone crypto keys."""

    total_filtered: int = Field(
        title='Total Authoritative Zone Crypto Keys Found',
        description='The total number of authoritative zone crypto keys found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of authoritative zone crypto keys found based on the current request criteria."""
