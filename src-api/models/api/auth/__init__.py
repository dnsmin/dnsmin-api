from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from lib.permissions.definitions import Permissions, Permission
from models.api import BaseApiModel
from models.enums import PrincipalTypeEnum


class Principal(BaseApiModel):
    """Represents an authentication principal."""

    id: UUID = Field(
        title='Principal ID',
        description='The unique identifier of the principal.',
        examples=[uuid4()],
    )
    """The unique identifier of the principal."""

    tenant_id: Optional[UUID] = Field(
        title='Tenant ID',
        description='The unique identifier of the tenant associated with the principal.',
        default=None,
        examples=[uuid4()],
    )
    """The unique identifier of the tenant associated with the principal."""
    
    type: PrincipalTypeEnum = Field(
        title='Type',
        description='The type of the principal.',
        examples=[
            PrincipalTypeEnum.client,
            PrincipalTypeEnum.user,
        ],
    )
    """The type of the principal."""

    permissions: Optional[set[Permission]] = Field(
        title='Principal Permissions',
        description='A list of permissions that the principal has.',
        default=None,
        examples=[
            Permissions.auth_users,
            Permissions.tenants_read,
            Permissions.zones_azone,
            Permissions.zones_rzone_read,
        ],
    )
    """The permissions that the principal has."""
