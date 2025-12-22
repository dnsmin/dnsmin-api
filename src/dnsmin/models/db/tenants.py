"""
Tenant Database Models

This file defines the database models associated with tenant functionality.
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime, String, Uuid, text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dnsmin.app import DB_PREFIX
from dnsmin.models.db import BaseSqlModel


class Tenant(BaseSqlModel):
    """Represents a tenant."""

    __tablename__ = f'{DB_PREFIX}_tenants'
    """Defines the database table name."""

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    """The unique identifier of the tenant."""

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    """The name of the tenant."""

    fqdn: Mapped[Optional[str]] = mapped_column(String(253), nullable=True)
    """The FQDN for the tenant UI."""

    stopgap_domain_id: Mapped[UUID] = mapped_column(
        Uuid, ForeignKey(f'{DB_PREFIX}_stopgap_domains.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=True
    )
    """The unique identifier of the associated stopgap domain."""

    stopgap_hostname: Mapped[str] = mapped_column(String(253), nullable=True)
    """The hostname used within the associated stopgap domain."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now, server_default=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the tenant was created."""

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True, default=None, onupdate=datetime.now, server_onupdate=text('CURRENT_TIMESTAMP')
    )
    """The timestamp representing when the tenant was last updated."""

    stopgap_domain = relationship('StopgapDomain', back_populates='tenants', cascade='expunge')
    """The stopgap domain associated with the tenant."""

    settings = relationship('Setting', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of settings associated with the tenant."""

    auth_users = relationship('User', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of auth users associated with the tenant."""

    auth_user_authenticators = relationship('UserAuthenticator', back_populates='tenant',
                                            cascade='all, delete, delete-orphan')
    """A list of auth user authenticators associated with the tenant."""

    auth_sessions = relationship('Session', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of auth sessions associated with the tenant."""

    auth_clients = relationship('Client', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of auth clients associated with the tenant."""

    auth_refresh_tokens = relationship('RefreshToken', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of auth refresh tokens associated with the tenant."""

    acl_roles = relationship('Role', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of ACL roles associated with the tenant."""

    acl_principals = relationship('Principal', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of ACL principals associated with the tenant."""

    acl_policies = relationship('Policy', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of ACL policies associated with the tenant."""

    azones = relationship('AZone', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of authoritative zones associated with the tenant."""

    rzones = relationship('RZone', back_populates='tenant', cascade='all, delete, delete-orphan')
    """A list of recursive zones associated with the tenant."""
