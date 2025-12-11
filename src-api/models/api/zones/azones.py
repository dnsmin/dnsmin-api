from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models.api import BaseApiModel
from models.enums import AZoneKindEnum, ZoneRecordTypeEnum


class AZoneInSchema(BaseApiModel):
    """Provides an API input model for creating and updating authoritative zones."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the authoritative zone if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the authoritative zone if any."""

    view_id: Optional[UUID] = Field(
        title='View ID',
        description='The unique identifier of the server view associated with the authoritative zone if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the server view associated with the authoritative zone if any."""

    fqdn: str = Field(
        title='Zone FQDN',
        description='The FQDN of the zone.',
        examples=['your-domain.com', 'third.level-domain.com', 'intranet-zone'],
    )
    """The FQDN of the zone."""

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

    dnssec: bool = Field(
        title='DNSSEC Signed',
        description='Whether or not this zone is DNSSEC signed (inferred from presigned being true XOR presence of at least one cryptokey with active being true).',
        default=False,
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

    soa_edit: Optional[str] = Field(
        title='SOA-EDIT Metadata',
        description='The SOA-EDIT metadata item.',
        default=None,
    )
    """The SOA-EDIT metadata item."""

    soa_edit_api: Optional[str] = Field(
        title='SOA-EDIT-API Metadata',
        description='The SOA-EDIT-API metadata item.',
        default=None,
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

    shared: bool = Field(
        title='Shared',
        description='Indicates whether the zone is shared between tenants.',
        default=False,
    )
    """Indicates whether the zone is shared between tenants."""


class AZoneRecordInSchema(BaseApiModel):
    """Provides an API input model for creating and updating authoritative zone records."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the authoritative zone record if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the authoritative zone record if any."""

    zone_id: UUID = Field(
        title='Zone ID',
        description='The unique identifier of the zone associated with the authoritative zone record if any.',
        examples=[uuid4()],
    )
    """The unique identifier of the zone associated with the authoritative zone record if any."""

    view_id: Optional[UUID] = Field(
        title='View ID',
        description='The unique identifier of the server view associated with the authoritative zone record if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the server view associated with the authoritative zone record if any."""

    name: Optional[str] = Field(
        title='Record Name',
        description='The name of the record.',
        default=None,
        examples=['www', 'sub-domain'],
    )
    """The name of the record."""

    type: ZoneRecordTypeEnum = Field(
        title='Record Type',
        description='The type of the record.',
        examples=[
            ZoneRecordTypeEnum.A,
            ZoneRecordTypeEnum.AAAA,
            ZoneRecordTypeEnum.MX,
            ZoneRecordTypeEnum.SOA,
            ZoneRecordTypeEnum.TXT,
        ],
    )
    """The type of the record."""

    ttl: int = Field(
        title='Record TTL',
        description='DNS TTL of the record, in seconds.',
    )
    """DNS TTL of the record, in seconds."""

    content: Optional[str] = Field(
        title='Record Content',
        description='The content of the record.',
        default=None,
    )
    """The content of the record."""

    comment: Optional[str] = Field(
        title='Record Comment',
        description='The comment associated with the record.',
        default=None,
    )
    """The comment associated with the record."""

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


class AZoneMetadataInSchema(BaseApiModel):
    """Provides an API input model for creating and updating authoritative zone metadata."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the authoritative zone metadata if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the authoritative zone metadata if any."""

    zone_id: UUID = Field(
        title='Zone ID',
        description='The unique identifier of the zone associated with the authoritative zone metadata if any.',
        examples=[uuid4()],
    )
    """The unique identifier of the zone associated with the authoritative zone metadata if any."""

    view_id: Optional[UUID] = Field(
        title='View ID',
        description='The unique identifier of the server view associated with the authoritative zone metadata if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the server view associated with the authoritative zone metadata if any."""

    name: str = Field(
        title='Metadata Type',
        description='The kind of the metadata.',
    )
    """The kind of the metadata."""

    values: Optional[list[str]] = Field(
        title='Metadata Values',
        description='The list of metadata values associated with this kind.',
        default=None,
    )
    """The list of metadata values associated with this kind."""


class AZoneOutSchema(BaseApiModel):
    """Provides an API response model for representing authoritative zones."""

    id: UUID = Field(
        title='AZone ID',
        description='The unique identifier of the authoritative zone.',
        examples=[uuid4()],
    )
    """The unique identifier of the authoritative zone."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the authoritative zone if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the authoritative zone if any."""

    view_id: Optional[UUID] = Field(
        title='View ID',
        description='The unique identifier of the server view associated with the authoritative zone if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the server view associated with the authoritative zone if any."""

    fqdn: str = Field(
        title='Zone FQDN',
        description='The FQDN of the zone.',
        examples=['your-domain.com', 'third.level-domain.com', 'intranet-zone'],
    )
    """The FQDN of the zone."""

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

    dnssec: bool = Field(
        title='DNSSEC Signed',
        description='Whether or not this zone is DNSSEC signed (inferred from presigned being true XOR presence of at least one cryptokey with active being true).',
        default=False,
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

    soa_edit: Optional[str] = Field(
        title='SOA-EDIT Metadata',
        description='The SOA-EDIT metadata item.',
        default=None,
    )
    """The SOA-EDIT metadata item."""

    soa_edit_api: Optional[str] = Field(
        title='SOA-EDIT-API Metadata',
        description='The SOA-EDIT-API metadata item.',
        default=None,
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

    shared: bool = Field(
        title='Shared',
        description='Indicates whether the zone is shared between tenants.',
        default=False,
    )
    """Indicates whether the zone is shared between tenants."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the authoritative zone was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the authoritative zone was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the authoritative zone was last updated.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the authoritative zone was last updated."""


class AZoneRecordOutSchema(BaseApiModel):
    """Provides an API response model for representing authoritative zone records."""

    id: UUID = Field(
        title='AZone ID',
        description='The unique identifier of the authoritative zone.',
        examples=[uuid4()],
    )
    """The unique identifier of the authoritative zone."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the authoritative zone record if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the authoritative zone record if any."""

    zone_id: UUID = Field(
        title='Zone ID',
        description='The unique identifier of the zone associated with the authoritative zone record if any.',
        examples=[uuid4()],
    )
    """The unique identifier of the zone associated with the authoritative zone record if any."""

    view_id: Optional[UUID] = Field(
        title='View ID',
        description='The unique identifier of the server view associated with the authoritative zone record if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the server view associated with the authoritative zone record if any."""

    name: Optional[str] = Field(
        title='Record Name',
        description='The name of the record.',
        default=None,
        examples=['www', 'sub-domain'],
    )
    """The name of the record."""

    type: ZoneRecordTypeEnum = Field(
        title='Record Type',
        description='The type of the record.',
        examples=[
            ZoneRecordTypeEnum.A,
            ZoneRecordTypeEnum.AAAA,
            ZoneRecordTypeEnum.MX,
            ZoneRecordTypeEnum.SOA,
            ZoneRecordTypeEnum.TXT,
        ],
    )
    """The type of the record."""

    ttl: int = Field(
        title='Record TTL',
        description='DNS TTL of the record, in seconds.',
    )
    """DNS TTL of the record, in seconds."""

    content: Optional[str] = Field(
        title='Record Content',
        description='The content of the record.',
        default=None,
    )
    """The content of the record."""

    comment: Optional[str] = Field(
        title='Record Comment',
        description='The comment associated with the record.',
        default=None,
    )
    """The comment associated with the record."""

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

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the authoritative zone record was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the authoritative zone record was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the authoritative zone record was last updated.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the authoritative zone record was last updated."""


class AZoneMetadataOutSchema(BaseApiModel):
    """Provides an API response model for representing authoritative zone metadata."""

    id: UUID = Field(
        title='AZone ID',
        description='The unique identifier of the authoritative zone.',
        examples=[uuid4()],
    )
    """The unique identifier of the authoritative zone."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the authoritative zone metadata if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the authoritative zone metadata if any."""

    zone_id: UUID = Field(
        title='Zone ID',
        description='The unique identifier of the zone associated with the authoritative zone metadata if any.',
        examples=[uuid4()],
    )
    """The unique identifier of the zone associated with the authoritative zone metadata if any."""

    view_id: Optional[UUID] = Field(
        title='View ID',
        description='The unique identifier of the server view associated with the authoritative zone metadata if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the server view associated with the authoritative zone metadata if any."""

    name: str = Field(
        title='Metadata Type',
        description='The kind of the metadata.',
    )
    """The kind of the metadata."""

    values: Optional[list[str]] = Field(
        title='Metadata Values',
        description='The list of metadata values associated with this kind.',
        default=None,
    )
    """The list of metadata values associated with this kind."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the authoritative zone metadata was created.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the authoritative zone metadata was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the authoritative zone metadata was last updated.',
        default=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the authoritative zone metadata was last updated."""


class AZonesSchema(BaseApiModel):
    """Provides an API response model for retrieving authoritative zones."""

    records: list[AZoneOutSchema] = Field(
        title='Authoritative Zones',
        description='A list of authoritative zones found based on the current request criteria.',
        default_factory=list,
    )
    """A list of authoritative zones found based on the current request criteria."""

    total: int = Field(
        title='Total Authoritative Zones',
        description='The total number of authoritative zones.',
        default=0,
        examples=[1234],
    )
    """The total number of authoritative zones."""

    total_filtered: int = Field(
        title='Total Authoritative Zones Found',
        description='The total number of authoritative zones found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of authoritative zones found based on the current request criteria."""


class AZoneRecordsSchema(BaseApiModel):
    """Provides an API response model for retrieving authoritative zone records."""

    records: list[AZoneRecordOutSchema] = Field(
        title='Authoritative Zone Records',
        description='A list of authoritative zone records found based on the current request criteria.',
        default_factory=list,
    )
    """A list of authoritative zone records found based on the current request criteria."""

    total: int = Field(
        title='Total Authoritative Zone Records',
        description='The total number of authoritative zone records.',
        default=0,
        examples=[1234],
    )
    """The total number of authoritative zone records."""

    total_filtered: int = Field(
        title='Total Authoritative Zone Records Found',
        description='The total number of authoritative zone records found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of authoritative zone records found based on the current request criteria."""


class AZoneMetadataSchema(BaseApiModel):
    """Provides an API response model for retrieving authoritative zone metadata."""

    records: list[AZoneMetadataOutSchema] = Field(
        title='Authoritative Zone Metadata',
        description='A list of authoritative zone metadata found based on the current request criteria.',
        default_factory=list,
    )
    """A list of authoritative zone metadata found based on the current request criteria."""

    total: int = Field(
        title='Total Authoritative Zone Metadata',
        description='The total number of authoritative zone metadata.',
        default=0,
        examples=[1234],
    )
    """The total number of authoritative zone metadata."""

    total_filtered: int = Field(
        title='Total Authoritative Zone Metadata Found',
        description='The total number of authoritative zone metadata found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of authoritative zone metadata found based on the current request criteria."""
