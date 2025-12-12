"""
DNS Zone Database Models

This file defines the database models associated with DNS zone functionality.
"""
import uuid
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, Integer, String, TEXT, Uuid, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import DB_PREFIX
from models.db import BaseSqlModel, JSONType
from models.enums import AZoneKindEnum, RZoneKindEnum, ZoneRecordTypeEnum, CryptoKeyTypeEnum


class AZone(BaseSqlModel):
    """Represents an authoritative DNS zone."""

    __tablename__ = f'{DB_PREFIX}_azones'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the zone."""

    tenant_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_tenants.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True
    )
    """The unique identifier of the tenant that owns this zone if any."""

    view_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_server_views.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True
    )
    """The unique identifier of the view associated with this zone if any."""

    fqdn: Mapped[str] = mapped_column(String(253), nullable=False)
    """The FQDN of the zone."""

    kind: Mapped[AZoneKindEnum] = mapped_column(String(20), nullable=False)
    """The kind of the zone."""

    serial: Mapped[int] = mapped_column(Integer, nullable=False)
    """The SOA serial number."""

    notified_serial: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    """The SOA serial notifications have been sent out for."""

    edited_serial: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    """The SOA serial as seen in query responses."""

    masters: Mapped[Optional[list[str]]] = mapped_column(JSONType, nullable=True)
    """List of IP addresses configured as a master for this zone (“Slave” type zones only)."""

    dnssec: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Whether or not this zone is DNSSEC signed (inferred from presigned being true XOR presence of at least one cryptokey with active being true)."""

    nsec3param: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    """The NSEC3PARAM record."""

    nsec3narrow: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    """Whether or not the zone uses NSEC3 narrow."""

    presigned: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    """Whether or not the zone is pre-signed."""

    soa_edit: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    """The SOA-EDIT metadata item."""

    soa_edit_api: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    """The SOA-EDIT-API metadata item."""

    api_rectify: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    """Whether or not the zone will be rectified on data changes via the API."""

    zone: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    """MAY contain a BIND-style zone file when creating a zone."""

    catalog: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    """The catalog this zone is a member of."""

    account: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    """The account this zone is a member of."""

    master_tsig_key_ids: Mapped[Optional[list[str]]] = mapped_column(JSONType, nullable=True)
    """The id of the TSIG keys used for master operation in this zone."""

    slave_tsig_key_ids: Mapped[Optional[list[str]]] = mapped_column(JSONType, nullable=True)
    """The id of the TSIG keys used for slave operation in this zone."""

    shared: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Indicates whether the zone is shared between tenants."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the zone was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, default=None, onupdate=datetime.now, server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the zone was last updated."""

    tenant = relationship('Tenant', back_populates='azones', cascade='expunge')
    """The tenant associated with the zone."""

    view = relationship('ServerView', back_populates='azones', cascade='expunge')
    """The view associated with the zone."""

    records = relationship('AZoneRecord', back_populates='zone', cascade='all, delete, delete-orphan')
    """A list of resource records associated with the zone."""

    metadata_ = relationship('AZoneMetadata', back_populates='zone', cascade='all, delete, delete-orphan')
    """A list of metadata records associated with the zone."""

    crypto_keys = relationship('AZoneCryptoKey', back_populates='zone', cascade='all, delete, delete-orphan')
    """A list of crypto keys associated with the zone."""


class AZoneRecord(BaseSqlModel):
    """Represents an authoritative DNS zone record."""

    __tablename__ = f'{DB_PREFIX}_azone_records'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the record."""

    tenant_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_tenants.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True
    )
    """The unique identifier of the tenant that owns this record if any."""

    zone_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_azones.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )
    """The unique identifier of the zone this record belongs to."""

    view_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_server_views.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True
    )
    """The unique identifier of the view associated with this record if any."""

    name: Mapped[str] = mapped_column(String(255), nullable=True)
    """The name of the record."""

    type: Mapped[ZoneRecordTypeEnum] = mapped_column(String(20), nullable=False)
    """The type of the record."""

    ttl: Mapped[int] = mapped_column(Integer, nullable=False)
    """DNS TTL of the record, in seconds."""

    content: Mapped[str] = mapped_column(TEXT, nullable=True)
    """The content of the record."""

    comment: Mapped[str] = mapped_column(TEXT, nullable=True)
    """The comment associated with the record."""

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Whether or not this record is disabled."""

    modified_at: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    """Timestamp of the last change to the record on the DNS server."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, default=None, onupdate=datetime.now, server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the record was last updated."""

    zone = relationship('AZone', back_populates='records', cascade='expunge')
    """The zone associated with the resource record."""

    view = relationship('ServerView', back_populates='azone_records', cascade='expunge')
    """The view associated with the record."""


class AZoneMetadata(BaseSqlModel):
    """Represents an authoritative DNS zone metadata record."""

    __tablename__ = f'{DB_PREFIX}_azone_metadata'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the metadata."""

    tenant_id: Mapped[Optional[UUID]] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_tenants.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True
    )
    """The unique identifier of the tenant that owns this metadata if any."""

    zone_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_azones.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )
    """The unique identifier of the zone this metadata belongs to."""

    view_id: Mapped[Optional[UUID]] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_server_views.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True
    )
    """The unique identifier of the view associated with this record if any."""

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    """The kind of the metadata."""

    values: Mapped[Optional[list[str]]] = mapped_column(JSONType, nullable=True)
    """The list of metadata values associated with this kind."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the metadata was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, default=None, onupdate=datetime.now, server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the metadata was last updated."""

    zone = relationship('AZone', back_populates='metadata_', cascade='expunge')
    """The zone associated with the metadata."""

    view = relationship('ServerView', back_populates='azone_metadata', cascade='expunge')
    """The view associated with the metadata."""


class AZoneCryptoKey(BaseSqlModel):
    """Represents a DNSSEC cryptographic key."""

    __tablename__ = f'{DB_PREFIX}_azone_crypto_keys'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    """The unique identifier of the crypto key."""

    tenant_id: Mapped[Optional[UUID]] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_tenants.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True
    )
    """The unique identifier of the tenant that owns the crypto key if any."""

    zone_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_azones.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )
    """The unique identifier of the zone this crypto key belongs to."""

    internal_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    """The internal identifier, read only."""

    type: Mapped[CryptoKeyTypeEnum] = mapped_column(String(20), nullable=False)
    """The type of the key."""

    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Whether the key is in active use."""

    published: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Whether the DNSKEY crypto key is published in the zone."""

    dns_key: Mapped[str] = mapped_column(TEXT, nullable=False)
    """The DNSKEY crypto key for this key."""

    ds: Mapped[list[str]] = mapped_column(JSONType, nullable=False)
    """A list of DS crypto keys for this key."""

    cds: Mapped[list[str]] = mapped_column(JSONType, nullable=False)
    """A list of DS crypto keys for this key, filtered by CDS publication settings."""

    private_key: Mapped[str] = mapped_column(TEXT, nullable=False)
    """The private key in ISC format."""

    algorithm: Mapped[str] = mapped_column(String(20), nullable=False)
    """The name of the algorithm of the key, should be a mnemonic."""

    bits: Mapped[int] = mapped_column(Integer, nullable=False)
    """The size of the key."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the crypto key was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, default=None, onupdate=datetime.now, server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the crypto key was last updated."""

    zone = relationship('AZone', back_populates='crypto_keys', cascade='expunge')
    """The zone associated with the metadata."""


class RZone(BaseSqlModel):
    """Represents a recursor DNS zone."""

    __tablename__ = f'{DB_PREFIX}_rzones'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the zone."""

    tenant_id: Mapped[Optional[UUID]] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_tenants.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True
    )
    """The unique identifier of the tenant that owns the zone if any."""

    fqdn: Mapped[str] = mapped_column(String(255), nullable=False)
    """The FQDN of the zone."""

    kind: Mapped[RZoneKindEnum] = mapped_column(String(20), nullable=False)
    """The kind of the zone."""

    servers: Mapped[list[str]] = mapped_column(Integer, nullable=False)
    """The list of upstream servers to forward queries to."""

    recursion_desired: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    """Whether or not the RD bit should be set in the upstream query for forwarded zone kinds."""

    notify_allowed: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    """Whether or not to permit incoming NOTIFY to wipe cache for the forwarded zone kind."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the zone was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, default=None, onupdate=datetime.now, server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the zone was last updated."""

    tenant = relationship('Tenant', back_populates='rzones', cascade='expunge')
    """The tenant associated with the zone."""

    records = relationship('RZoneRecord', back_populates='zone', cascade='all, delete, delete-orphan')
    """A list of resource records associated with the zone."""


class RZoneRecord(BaseSqlModel):
    """Represents a recursor DNS zone record."""

    __tablename__ = f'{DB_PREFIX}_rzone_records'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the resource record."""

    tenant_id: Mapped[Optional[UUID]] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_tenants.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True
    )
    """The unique identifier of the tenant that owns the resource record if any."""

    zone_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_rzones.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )
    """The unique identifier of the zone this resource record belongs to."""

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    """The name of the record."""

    type: Mapped[ZoneRecordTypeEnum] = mapped_column(String(20), nullable=False)
    """The type of the record."""

    ttl: Mapped[int] = mapped_column(Integer, nullable=False)
    """DNS TTL of the records, in seconds."""

    content: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    """The content of the record."""

    comment: Mapped[Optional[str]] = mapped_column(TEXT, nullable=True)
    """The comment associated with the record."""

    disabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Whether or not this record is disabled."""

    modified_at: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    """Timestamp of the last change to the resource record on the DNS server."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the resource record was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=True, default=None, onupdate=datetime.now, server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the resource record was last updated."""

    zone = relationship('RZone', back_populates='records', cascade='expunge')
    """The zone associated with the resource record."""
