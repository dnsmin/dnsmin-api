from typing import Optional

from pydantic import BaseModel, Field

from dnsmin.models.enums import (
    ZoneRecordTypeEnum, SOAEditTypeEnum,
    AZoneRRSetChangeTypeEnum, RZoneRRSetChangeTypeEnum,
    AZoneKindEnum, RZoneKindEnum, CryptoKeyTypeEnum
)


class ConfigSetting(BaseModel):
    """Provides an API model representing a config setting."""

    name: str = Field(
        title='Setting Name',
        description='The name of the setting.',
    )
    """The name of the setting."""

    type: str = Field(
        title='Setting Type',
        description='The type of the setting.',
        default='ConfigSetting',
        examples=['ConfigSetting'],
    )
    """The type of the setting."""

    value: str | list[str] = Field(
        title='Setting Value',
        description='The value of the setting.',
    )
    """The value of the setting."""


class StatisticItem(BaseModel):
    """Provides an API model representing a statistic item."""

    name: str = Field(
        title='Statistic Name',
        description='The name of the statistic.',
    )
    """The name of the statistic."""

    type: str = Field(
        title='Statistic Type',
        description='The type of the statistic.',
        default='StatisticItem',
        examples=['StatisticItem'],
    )
    """The type of the statistic."""

    value: str = Field(
        title='Statistic Value',
        description='The value of the statistic.',
    )
    """The value of the statistic."""


class SimpleStatisticItem(BaseModel):
    """Provides an API model representing a simple statistic."""

    name: str = Field(
        title='Statistic Name',
        description='The name of the statistic.',
    )
    """The name of the statistic."""

    value: str = Field(
        title='Statistic Value',
        description='The value of the statistic.',
    )
    """The value of the statistic."""


class MapStatisticItem(BaseModel):
    """Provides an API model representing a map statistic item."""

    name: str = Field(
        title='Item Name',
        description='The name of the item.',
    )
    """The name of the item."""

    type: str = Field(
        title='Item Type',
        description='The type of the item.',
        default='MapStatisticItem',
        examples=['MapStatisticItem'],
    )
    """The type of the item."""

    value: list[SimpleStatisticItem] = Field(
        title='Item Values',
        description='A list of simple statistic items associated with the map statistic item.',
    )
    """A list of simple statistic items associated with the map statistic item."""


class RingStatisticItem(BaseModel):
    """Provides an API model representing a ring statistic item."""

    name: str = Field(
        title='Item Name',
        description='The name of the item.',
    )
    """The name of the item."""

    type: str = Field(
        title='Item Type',
        description='The type of the item.',
        default='RingStatisticItem',
        examples=['RingStatisticItem'],
    )
    """The type of the item."""

    size: int = Field(
        title='Ring Size',
        description='The size of the ring.',
    )
    """The size of the ring."""

    value: list[SimpleStatisticItem] = Field(
        title='Item Values',
        description='A list of simple statistic items associated with the ring statistic item.',
    )
    """A list of simple statistic items associated with the ring statistic item."""


class CacheFlushResult(BaseModel):
    """Provides an API model representing a cache flush result."""

    count: float = Field(
        title='Entry Flush Count',
        description='The count of cache entries flushed.',
    )
    """The count of cache entries flushed."""

    result: str = Field(
        title='Flush Message',
        description='The message from the cache flush.',
    )
    """The message from the cache flush."""


class ServerAutoPrimary(BaseModel):
    """Provides an API input model for creating and updating auto-primaries."""

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
        default=None,
    )
    """The account name for the auto-primary server."""


class ServerTSIGKey(BaseModel):
    """Provides an API model for managing server TSIG keys."""

    id: Optional[str] = Field(
        title='TSIG Key ID',
        description='The ID of the TSIG key.',
        default=None,
    )
    """The ID of the TSIG key."""

    type: str = Field(
        title='TSIG Key Type',
        description='The type of the TSIG key.',
        default='TSIGKey',
    )
    """The type of the TSIG key."""

    name: str = Field(
        title='TSIG Key Name',
        description='The name of the TSIG key.',
    )
    """The name of the TSIG key."""

    algorithm: str = Field(
        title='TSIG Key Algorithm',
        description='The algorithm of the TSIG key.',
    )
    """The algorithm of the TSIG key."""

    key: str = Field(
        title='TSIG Key Secret Key',
        description='The base64 encoded secret key.',
    )
    """The base64 encoded secret key."""


class ServerView(BaseModel):
    """Provides an API model for managing server views."""

    name: str = Field(
        title='View Name',
        description='The name of the view.',
        examples=['trusted', 'internal', 'global'],
    )
    """The name of the view."""

    zones: Optional[list[str]] = Field(
        title='View Zones',
        description='A list of the zones associated with the view.',
        default=None,
        examples=['example.com..trusted', 'intranet.lan..internal', 'company-site.com..global'],
    )
    """A list of the zones associated with the view."""


class ServerNetwork(BaseModel):
    """Provides an API model for managing server networks."""

    network: str = Field(
        title='Network CIDR',
        description='The CIDR specification of the network.',
        examples=['1.1.1.1/8', '192.168.1.0/24', '10.0.1.2/16'],
    )
    """The CIDR specification of the network."""

    view: str = Field(
        title='View Name',
        description='The name of the view.',
        examples=['trusted', 'internal', 'global'],
    )
    """The name of the view."""


class RRSetComment(BaseModel):
    """Provides an API model for managing zone rrset comments."""

    content: str = Field(
        title='Comment Content',
        description='The content of the comment.',
    )
    """The content of the comment."""

    account: Optional[str] = Field(
        title='Comment Account',
        description='The account of the comment.',
        default=None,
    )
    """The account of the comment."""

    modified_at: Optional[int] = Field(
        title='Modified Server Timestamp',
        description='Timestamp of the last change to the comment on the DNS server.',
        default=None,
    )
    """Timestamp of the last change to the comment on the DNS server."""


class RZoneRREntry(BaseModel):
    """Provides an API model for managing recursive zone rrset entries."""

    content: Optional[str] = Field(
        title='Record Content',
        description='The content of the record.',
        default=None,
    )
    """The content of the record."""

    disabled: bool = Field(
        title='Record Disabled',
        description='Whether or not this record is disabled.',
        default=False,
    )
    """Whether or not this record is disabled."""


class RZoneRRSet(BaseModel):
    """Provides an API model for managing recursive zone rrsets."""

    name: Optional[str] = Field(
        title='Record Name',
        description='The name of the record.',
        default=None,
        examples=['www', 'sub-domain'],
    )
    """The name of the record."""

    type: ZoneRecordTypeEnum = Field(
        title='RRSet Type',
        description='The type of the rrset.',
        examples=[
            ZoneRecordTypeEnum.A,
            ZoneRecordTypeEnum.AAAA,
            ZoneRecordTypeEnum.MX,
            ZoneRecordTypeEnum.SOA,
            ZoneRecordTypeEnum.TXT,
        ],
    )
    """The type of the rrset."""

    ttl: int = Field(
        title='Record TTL',
        description='DNS TTL of the record, in seconds.',
    )
    """DNS TTL of the record, in seconds."""

    change_type: Optional[RZoneRRSetChangeTypeEnum] = Field(
        title='RRSet Change Type',
        description='The change type when updating the rrset.',
        alias='changetype',
        default=None,
    )
    """The change type when updating the rrset."""

    records: list[RZoneRREntry] = Field(
        title='RRSet Entries',
        description='The entries associated with the rrset.',
        default_factory=list,
    )
    """The entries associated with the rrset."""

    comments: list[RRSetComment] = Field(
        title='RRSet Comments',
        description='The comments associated with the rrset.',
        default_factory=list,
    )
    """The comments associated with the rrset."""

    modified_at: Optional[int] = Field(
        title='Modified Server Timestamp',
        description='Timestamp of the last change to the rrset on the DNS server.',
        default=None,
    )
    """Timestamp of the last change to the rrset on the DNS server."""


class RZone(BaseModel):
    """Provides an API model for managing recursive zones."""

    id: Optional[str] = Field(
        title='Zone ID',
        description='The ID of the zone.',
        default=None,
    )
    """The ID of the zone."""

    name: str = Field(
        title='Zone Name',
        description='The name of the zone.',
        examples=['your-domain.com', 'third.level-domain.com', 'intranet-zone'],
    )
    """The name of the zone."""

    type: str = Field(
        title='Zone Type',
        description='The type of the zone.',
        default='Zone',
        examples=['Zone'],
    )
    """The type of the zone."""

    url: Optional[str] = Field(
        title='Zone URL',
        description='The API endpoint of the zone.',
        default=None,
    )
    """The API endpoint of the zone."""

    kind: RZoneKindEnum = Field(
        title='Zone Kind',
        description='The kind of the zone.',
        examples=[
            RZoneKindEnum.NATIVE,
            RZoneKindEnum.FORWARDED,
        ],
    )
    """The kind of the zone."""

    rrsets: Optional[list[RZoneRRSet]] = Field(
        title='Zone RRSets',
        description='The RRSets associated with the zone.',
        default=None,
    )
    """The RRSets associated with the zone."""

    servers: Optional[list[str]] = Field(
        title='Forwarding Server IP Addresses',
        description='List of IP addresses to forward the zone to when used as a forwarded zone.',
        default=None,
        examples=['1.1.1.1', '1.1.4.4', '1.1.8.8'],
    )
    """List of IP addresses to forward the zone to when used as a forwarded zone."""

    recursion_desired: Optional[bool] = Field(
        title='Recursion Desired',
        description='Whether or not the RD bit should be set in the query.',
        default=None,
    )
    """Whether or not the RD bit should be set in the query."""

    notify_allowed: Optional[bool] = Field(
        title='Notify Allowed',
        description='Whether or not to permit incoming NOTIFY to wipe cache for the domain.',
        default=None,
    )
    """Whether or not to permit incoming NOTIFY to wipe cache for the domain."""


class AZoneRecord(BaseModel):
    """Provides an API input model for creating and updating authoritative zone rrset records."""

    content: Optional[str] = Field(
        title='Record Content',
        description='The content of the record.',
        default=None,
    )
    """The content of the record."""

    disabled: bool = Field(
        title='Record Disabled',
        description='Whether or not this record is disabled.',
        default=False,
    )
    """Whether or not this record is disabled."""

    modified_at: Optional[int] = Field(
        title='Modified Server Timestamp',
        description='Timestamp of the last change to the record on the DNS server.',
        default=None,
    )
    """Timestamp of the last change to the record on the DNS server."""


class AZoneRRSet(BaseModel):
    """Provides an API input model for creating and updating authoritative zone rrsets."""

    name: Optional[str] = Field(
        title='Record Name',
        description='The name of the record.',
        default=None,
        examples=['www', 'sub-domain'],
    )
    """The name of the record."""

    type: ZoneRecordTypeEnum = Field(
        title='RRSet Type',
        description='The type of the rrset.',
        examples=[
            ZoneRecordTypeEnum.A,
            ZoneRecordTypeEnum.AAAA,
            ZoneRecordTypeEnum.MX,
            ZoneRecordTypeEnum.SOA,
            ZoneRecordTypeEnum.TXT,
        ],
    )
    """The type of the rrset."""

    ttl: int = Field(
        title='Record TTL',
        description='DNS TTL of the record, in seconds.',
    )
    """DNS TTL of the record, in seconds."""

    change_type: Optional[AZoneRRSetChangeTypeEnum] = Field(
        title='RRSet Change Type',
        description='The change type when updating the rrset.',
        alias='changetype',
        default=None,
    )
    """The change type when updating the rrset."""

    records: list[AZoneRecord] = Field(
        title='RRSet Records',
        description='The records associated with the rrset.',
        default_factory=list,
    )
    """The records associated with the rrset."""

    comments: list[RRSetComment] = Field(
        title='RRSet Comments',
        description='The comments associated with the rrset.',
        default_factory=list,
    )
    """The comments associated with the rrset."""


class AZone(BaseModel):
    """Provides an API input model for creating authoritative zones."""

    id: Optional[str] = Field(
        title='Zone ID',
        description='The ID of the zone.',
        default=None,
    )
    """The ID of the zone."""

    name: str = Field(
        title='Zone Name',
        description='The name of the zone.',
        examples=['your-domain.com', 'third.level-domain.com', 'intranet-zone'],
    )
    """The name of the zone."""

    type: str = Field(
        title='Zone Type',
        description='The type of the zone.',
        default='Zone',
        examples=['Zone'],
    )
    """The type of the zone."""

    url: Optional[str] = Field(
        title='Zone URL',
        description='The API endpoint of the zone.',
        default=None,
    )
    """The API endpoint of the zone."""

    kind: AZoneKindEnum = Field(
        title='Zone Kind',
        description='The kind of the zone.',
        examples=[
            AZoneKindEnum.NATIVE,
            AZoneKindEnum.MASTER,
            AZoneKindEnum.SLAVE,
            AZoneKindEnum.PRODUCER,
            AZoneKindEnum.CONSUMER,
        ],
    )
    """The kind of the zone."""

    rrsets: Optional[list[AZoneRRSet]] = Field(
        title='Zone RRSets',
        description='The RRSets associated with the zone.',
        default=None,
    )
    """The RRSets associated with the zone."""

    serial: int = Field(
        title='SOA Serial Number',
        description='The SOA serial number.',
    )
    """The SOA serial number."""

    notified_serial: Optional[int] = Field(
        title='Notification Serial Number',
        description='The SOA serial notifications have been sent out for.',
        default=None,
    )
    """The SOA serial notifications have been sent out for."""

    edited_serial: Optional[int] = Field(
        title='Query Response Serial Number',
        description='The SOA serial as seen in query responses.',
        default=None,
    )
    """The SOA serial as seen in query responses."""

    masters: Optional[list[str]] = Field(
        title='Master IP Addresses',
        description='List of IP addresses configured as a master for this zone (“Slave” type zones only).',
        default=None,
        examples=['1.1.1.1', '1.1.4.4', '1.1.8.8'],
    )
    """List of IP addresses configured as a master for this zone (“Slave” type zones only)."""

    dnssec: Optional[bool] = Field(
        title='DNSSEC Signed',
        description='Whether or not this zone is DNSSEC signed (inferred from presigned being true XOR presence of at least one cryptokey with active being true).',
        default=None,
    )
    """Whether or not this zone is DNSSEC signed (inferred from presigned being true XOR presence of at least one cryptokey with active being true)."""

    nsec3param: Optional[str] = Field(
        title='NSEC3PARAM Record',
        description='The NSEC3PARAM record.',
        default=None,
    )
    """The NSEC3PARAM record."""

    nsec3narrow: Optional[bool] = Field(
        title='NSEC3 Narrow Enabled',
        description='Whether or not the zone uses NSEC3 narrow.',
        default=None,
    )
    """Whether or not the zone uses NSEC3 narrow."""

    presigned: Optional[bool] = Field(
        title='Presigned',
        description='Whether or not the zone is pre-signed.',
        default=None,
    )
    """Whether or not the zone is pre-signed."""

    soa_edit: Optional[SOAEditTypeEnum] = Field(
        title='SOA-EDIT Metadata',
        description='The SOA-EDIT metadata item.',
        default=None,
        examples=[
            SOAEditTypeEnum.DEFAULT,
            SOAEditTypeEnum.INCREASE,
            SOAEditTypeEnum.EPOCH,
            SOAEditTypeEnum.OFF,
            SOAEditTypeEnum.EMPTY,
        ],
    )
    """The SOA-EDIT metadata item."""

    soa_edit_api: Optional[SOAEditTypeEnum] = Field(
        title='SOA-EDIT-API Metadata',
        description='The SOA-EDIT-API metadata item.',
        default=None,
        examples=[
            SOAEditTypeEnum.DEFAULT,
            SOAEditTypeEnum.INCREASE,
            SOAEditTypeEnum.EPOCH,
            SOAEditTypeEnum.OFF,
        ],
    )
    """The SOA-EDIT-API metadata item."""

    api_rectify: Optional[bool] = Field(
        title='API Rectify',
        description='Whether or not the zone will be rectified on data changes via the API.',
        default=None,
    )
    """Whether or not the zone will be rectified on data changes via the API."""

    zone: Optional[str] = Field(
        title='Zone File',
        description='MAY contain a BIND-style zone file when creating a zone.',
        default=None,
    )
    """MAY contain a BIND-style zone file when creating a zone."""

    catalog: Optional[str] = Field(
        title='Zone Catalog',
        description='The catalog this zone is a member of.',
        default=None,
    )
    """The catalog this zone is a member of."""

    account: Optional[str] = Field(
        title='Zone Account',
        description='The account this zone is a member of.',
        default=None,
    )
    """The account this zone is a member of."""

    nameservers: Optional[list[str]] = Field(
        title='Zone Nameservers',
        description='The nameservers of the zone used during creation.',
        default=None,
    )
    """The nameservers of the zone used during creation."""

    master_tsig_key_ids: Optional[list[str]] = Field(
        title='Master TSIG Key IDs',
        description='The ids of the TSIG keys used for master operation in this zone.',
        default=None,
    )
    """The ids of the TSIG keys used for master operation in this zone."""

    slave_tsig_key_ids: Optional[list[str]] = Field(
        title='Slave TSIG Key IDs',
        description='The ids of the TSIG keys used for slave operation in this zone.',
        default=None,
    )
    """The ids of the TSIG keys used for slave operation in this zone."""


class AZoneUpdate(BaseModel):
    """Provides an API input model for updating authoritative zones."""

    kind: AZoneKindEnum = Field(
        title='Zone Kind',
        description='The kind of the zone.',
        examples=[
            AZoneKindEnum.NATIVE,
            AZoneKindEnum.MASTER,
            AZoneKindEnum.SLAVE,
            AZoneKindEnum.PRODUCER,
            AZoneKindEnum.CONSUMER,
        ],
    )
    """The kind of the zone."""

    masters: Optional[list[str]] = Field(
        title='Master IP Addresses',
        description='List of IP addresses configured as a master for this zone (“Slave” type zones only).',
        default=None,
        examples=['1.1.1.1', '1.1.4.4', '1.1.8.8'],
    )
    """List of IP addresses configured as a master for this zone (“Slave” type zones only)."""

    dnssec: Optional[bool] = Field(
        title='DNSSEC Signed',
        description='Whether or not this zone is DNSSEC signed (inferred from presigned being true XOR presence of at least one cryptokey with active being true).',
        default=None,
    )
    """Whether or not this zone is DNSSEC signed (inferred from presigned being true XOR presence of at least one cryptokey with active being true)."""

    nsec3param: Optional[str] = Field(
        title='NSEC3PARAM Record',
        description='The NSEC3PARAM record.',
        default=None,
    )
    """The NSEC3PARAM record."""

    soa_edit: Optional[SOAEditTypeEnum] = Field(
        title='SOA-EDIT Metadata',
        description='The SOA-EDIT metadata item.',
        default=None,
        examples=[
            SOAEditTypeEnum.DEFAULT,
            SOAEditTypeEnum.INCREASE,
            SOAEditTypeEnum.EPOCH,
            SOAEditTypeEnum.OFF,
            SOAEditTypeEnum.EMPTY,
        ],
    )
    """The SOA-EDIT metadata item."""

    soa_edit_api: Optional[SOAEditTypeEnum] = Field(
        title='SOA-EDIT-API Metadata',
        description='The SOA-EDIT-API metadata item.',
        default=None,
        examples=[
            SOAEditTypeEnum.DEFAULT,
            SOAEditTypeEnum.INCREASE,
            SOAEditTypeEnum.EPOCH,
            SOAEditTypeEnum.OFF,
        ],
    )
    """The SOA-EDIT-API metadata item."""

    api_rectify: Optional[bool] = Field(
        title='API Rectify',
        description='Whether or not the zone will be rectified on data changes via the API.',
        default=None,
    )
    """Whether or not the zone will be rectified on data changes via the API."""

    catalog: Optional[str] = Field(
        title='Zone Catalog',
        description='The catalog this zone is a member of.',
        default=None,
    )
    """The catalog this zone is a member of."""

    account: Optional[str] = Field(
        title='Zone Account',
        description='The account this zone is a member of.',
        default=None,
    )
    """The account this zone is a member of."""


class AZoneMetadata(BaseModel):
    """Provides an API input model for creating and updating authoritative zone metadata."""

    name: str = Field(
        title='Metadata Type',
        description='The kind of the metadata.',
        alias='kind',
    )
    """The kind of the metadata."""

    values: Optional[list[str]] = Field(
        title='Metadata Values',
        description='The list of metadata values associated with this kind.',
        alias='metadata',
        default=None,
    )
    """The list of metadata values associated with this kind."""


class AZoneCryptoKey(BaseModel):
    """Provides an API model for managing authoritative zone crypto keys."""

    id: Optional[int] = Field(
        title='Crypto Key ID',
        description='The ID of the crypto key.',
        default=None,
    )
    """The ID of the crypto key."""

    type: CryptoKeyTypeEnum = Field(
        title='Crypto Key Type',
        description='The type of the key.',
    )
    """The type of the key."""

    key_type: Optional[str] = Field(
        title='Key Type',
        description='The key type of this key.',
        alias='keytype',
        default=None,
    )
    """The key type of this key."""

    active: Optional[bool] = Field(
        title='Crypto Key Active',
        description='Whether the key is in active use.',
        default=None,
    )
    """Whether the key is in active use."""

    published: Optional[bool] = Field(
        title='Crypto Key Published',
        description='Whether the DNSKEY crypto key is published in the zone.',
        default=None,
    )
    """Whether the DNSKEY crypto key is published in the zone."""

    dns_key: str = Field(
        title='Crypto Key DNSKEY',
        description='The DNSKEY crypto key for this key.',
        alias='dnskey',
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
        alias='privatekey',
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
