from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from dnsmin.models.api import BaseApiModel


class RoleInSchema(BaseApiModel):
    """Provides an API input model for creating and updating ACL roles."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the role if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the role if any."""

    slug: str = Field(
        title='Role Slug',
        description='The slug of the role.',
        examples=['system_admin', 'tenant_admin', 'tenant_owner', 'zone_admin'],
    )
    """The slug of the role."""

    name: str = Field(
        title='Role Name',
        description='The name of the role.',
        examples=['System Admin', 'Tenant Admin', 'Tenant Owner', 'Zone Admin'],
    )
    """The name of the role."""

    description: str = Field(
        title='Role Description',
        description='The description of the role.',
        examples=[
            'Provides permissions for system administrators.',
            'Provides permissions for tenant administrators.',
            'Provides permissions for tenant owners.',
            'Provides permissions for zone managers.',
        ],
    )
    """The description of the role."""


class RoleOutSchema(BaseApiModel):
    """Provides an API response model for representing ACL roles."""

    id: UUID = Field(
        title='Role ID',
        description='The unique identifier of the role.',
        examples=[uuid4()],
    )
    """The unique identifier of the role."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the role if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the role if any."""

    slug: str = Field(
        title='Role Slug',
        description='The slug of the role.',
        examples=['system_admin', 'tenant_admin', 'tenant_owner', 'zone_admin'],
    )
    """The slug of the role."""

    name: str = Field(
        title='Role Name',
        description='The name of the role.',
        examples=['System Admin', 'Tenant Admin', 'Tenant Owner', 'Zone Admin'],
    )
    """The name of the role."""

    description: str = Field(
        title='Role Description',
        description='The description of the role.',
        examples=[
            'Provides permissions for system administrators.',
            'Provides permissions for tenant administrators.',
            'Provides permissions for tenant owners.',
            'Provides permissions for zone managers.',
        ],
    )
    """The description of the role."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the role was created.',
        default_factory=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the role was created."""

    updated_at: Optional[datetime] = Field(
        title='Updated At',
        description='The timestamp representing when the role was last updated.',
        default=None,
        examples=[datetime.now()],
    )
    """The timestamp representing when the role was last updated."""


class RolesSchema(BaseApiModel):
    """Provides an API response model for retrieving ACL roles."""

    records: list[RoleOutSchema] = Field(
        title='Roles',
        description='A list of roles found based on the current request criteria.',
        default_factory=list[RoleOutSchema],
        examples=[[
            RoleOutSchema(slug='system_admin', name='System Admin', description='A role for system administrators.'),
            RoleOutSchema(slug='tenant_admin', name='Tenant Admin', description='A role for tenant administrators.'),
            RoleOutSchema(slug='tenant_owner', name='Tenant Owner', description='A role for tenant owners.'),
            RoleOutSchema(slug='zone_admin', name='Zone Admin', description='A role for zone administrators.'),
        ]],
    )
    """A list of roles found based on the current request criteria."""

    total: int = Field(
        title='Total Roles',
        description='The total number of roles.',
        default=0,
        examples=[4],
    )
    """The total number of roles."""

    total_filtered: int = Field(
        title='Total Roles Found',
        description='The total number of roles found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of roles found based on the current request criteria."""


