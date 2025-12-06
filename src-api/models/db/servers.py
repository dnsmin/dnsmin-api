"""
DNS Server Database Models

This file defines the database models associated with DNS server functionality.
"""
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import Boolean, DateTime, String, TEXT, Uuid, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import DB_PREFIX
from models.db import BaseSqlModel
from models.enums import ServerTypeEnum


class Server(BaseSqlModel):
    """Represents a DNS server."""

    __tablename__ = f'{DB_PREFIX}_servers'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the server."""

    type: Mapped[ServerTypeEnum] = mapped_column(String(20), nullable=False)
    """The type of DNS server."""

    version: Mapped[str] = mapped_column(String(20), nullable=False)
    """The version of the server software."""

    hostname: Mapped[str] = mapped_column(String(253), nullable=False)
    """The hostname or IP address of the server."""

    api_url: Mapped[str] = mapped_column(TEXT, nullable=False)
    """The fully qualified or relative URL of the server's API endpoint."""

    api_key: Mapped[str] = mapped_column(TEXT, nullable=False)
    """The API key used to authenticate to the server API."""

    shared: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    """Indicates whether the server is shared between tenants."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the server was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the server was last updated."""

    auto_primaries = relationship('ServerAutoPrimary', back_populates='server', cascade='all, delete, delete-orphan')
    """A list of auto primary registrations associated with the server."""

    views = relationship('ServerView', back_populates='server', cascade='all, delete, delete-orphan')
    """A list of views associated with the server."""

    networks = relationship('ServerNetwork', back_populates='server', cascade='all, delete, delete-orphan')
    """A list of networks associated with the server."""


class ServerAutoPrimary(BaseSqlModel):
    """Represents an auto-primary registration for a server."""

    __tablename__ = f'{DB_PREFIX}_server_auto_primaries'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the auto-primary."""

    server_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_servers.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )
    """The unique identifier of the server this auto-primary belongs to."""

    ip: Mapped[str] = mapped_column(String(45), nullable=False)
    """The IP address of the autoprimary server."""

    nameserver: Mapped[str] = mapped_column(String(253), nullable=False)
    """The DNS name of the autoprimary server."""

    account: Mapped[str] = mapped_column(String(255), nullable=False)
    """The account name for the autoprimary server."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the auto-primary was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the auto-primary was last updated."""

    server = relationship('Server', back_populates='auto_primaries', cascade='expunge, delete')
    """The server associated with the auto primary registration."""


class ServerView(BaseSqlModel):
    """Represents a server view."""

    __tablename__ = f'{DB_PREFIX}_server_views'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the view."""

    server_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_servers.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )
    """The unique identifier of the server this view is associated with."""

    name: Mapped[str] = mapped_column(String(253), nullable=False)
    """The name of the view."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the view was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the view was last updated."""

    server = relationship('Server', back_populates='views', cascade='expunge, delete')
    """The server associated with the view."""

    networks = relationship('ServerNetwork', back_populates='view', cascade='all, delete, delete-orphan')
    """A list of networks associated with the view."""

    azones = relationship('AZone', back_populates='view', cascade='all, delete, delete-orphan')
    """A list of authoritative zones associated with the view."""

    azone_records = relationship('AZoneRecord', back_populates='view', cascade='all, delete, delete-orphan')
    """A list of authoritative zone records associated with the view."""

    azone_metadata = relationship('AZoneMetadata', back_populates='view', cascade='all, delete, delete-orphan')
    """A list of authoritative zone metadata associated with the view."""


class ServerNetwork(BaseSqlModel):
    """Represents a server network."""

    __tablename__ = f'{DB_PREFIX}_server_networks'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the network."""

    server_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_servers.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )
    """The unique identifier of the server this network is associated with."""

    view_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_server_views.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False
    )
    """The unique identifier of the view this network is associated with."""

    network: Mapped[str] = mapped_column(String(45), nullable=False)
    """The CIDR specification of the network."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the network was created."""

    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, onupdate=datetime.now,
        server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the network was last updated."""

    server = relationship('Server', back_populates='networks', cascade='expunge, delete')
    """The server associated with the network."""

    view = relationship('ServerView', back_populates='networks', cascade='expunge, delete')
    """The view associated with the network."""
