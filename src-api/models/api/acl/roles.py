from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models.api import BaseApiModel
from models.enums import PrincipalTypeEnum


class PrincipalInSchema(BaseApiModel):
    """Provides an API input model for creating ACL role principals."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the principal if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the principal if any."""

    type: PrincipalTypeEnum = Field(
        title='Principal Type',
        description='The type of the associated principal.',
        examples=[
            PrincipalTypeEnum.user,
            PrincipalTypeEnum.client,
        ],
    )
    """The type of the associated principal."""


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


class PrincipalOutSchema(BaseApiModel):
    """Provides an API response model for representing ACL role principals."""

    id: UUID = Field(
        title='Principal ID',
        description='The unique identifier of the principal.',
        default_factory=uuid4,
        examples=[uuid4()],
    )
    """The unique identifier of the principal."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the principal if any.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the principal if any."""

    type: PrincipalTypeEnum = Field(
        title='Principal Type',
        description='The type of the associated principal.',
        examples=[
            PrincipalTypeEnum.user,
            PrincipalTypeEnum.client,
        ],
    )
    """The type of the associated principal."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the association was created.',
        default_factory=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the association was created."""


class RoleOutSchema(BaseApiModel):
    """Provides an API response model for representing ACL roles."""

    id: UUID = Field(
        title='Role ID',
        description='The unique identifier of the role.',
        default_factory=uuid4,
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


class PrincipalsSchema(BaseApiModel):
    """Provides an API response model for retrieving ACL principals."""

    records: list[PrincipalOutSchema] = Field(
        title='Principals',
        description='A list of principals found based on the current request criteria.',
        default_factory=list[RoleOutSchema],
    )
    """A list of principals found based on the current request criteria."""

    total: int = Field(
        title='Total Principals',
        description='The total number of principals.',
        default=0,
        examples=[4],
    )
    """The total number of principals."""

    total_filtered: int = Field(
        title='Total Principals Found',
        description='The total number of principals found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of principals found based on the current request criteria."""
