from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field

from models import BaseApiModel, PrincipalTypeEnum
from models.api.acl.roles import RoleOutSchema


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
