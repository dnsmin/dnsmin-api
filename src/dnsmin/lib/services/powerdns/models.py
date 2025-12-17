from typing import Optional

from pydantic import BaseModel, Field

from dnsmin.models.enums import ZoneRecordTypeEnum, SOAEditTypeEnum, RRSetChangeTypeEnum, AZoneKindEnum


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


class AZoneComment(BaseModel):
    """Provides an API input model for creating and updating authoritative zone rrset comments."""

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

    change_type: Optional[RRSetChangeTypeEnum] = Field(
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

    comments: list[AZoneComment] = Field(
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
