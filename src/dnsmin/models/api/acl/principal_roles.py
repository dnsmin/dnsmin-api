from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field

from dnsmin.models.api import BaseApiModel


class PrincipalRoleInSchema(BaseApiModel):
    """Provides an API input model for creating ACL principal role associations."""

    principal_id: UUID = Field(
        title='Principal ID',
        description='The unique identifier of the principal.',
        examples=[uuid4()],
    )
    """The unique identifier of the principal."""

    role_id: UUID = Field(
        title='Role ID',
        description='The unique identifier of the role.',
        examples=[uuid4()],
    )
    """The unique identifier of the role."""


class PrincipalRoleOutSchema(BaseApiModel):
    """Provides an API response model for representing ACL principal role associations."""

    principal_id: UUID = Field(
        title='Principal ID',
        description='The unique identifier of the principal.',
        examples=[uuid4()],
    )
    """The unique identifier of the principal."""

    role_id: UUID = Field(
        title='Role ID',
        description='The unique identifier of the role.',
        examples=[uuid4()],
    )
    """The unique identifier of the role."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the association was created.',
        default_factory=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the association was created."""


class PrincipalRolesSchema(BaseApiModel):
    """Provides an API response model for retrieving ACL principals."""

    records: list[PrincipalRoleOutSchema] = Field(
        title='Principal Role Associations',
        description='A list of principal role associations found based on the current request criteria.',
        default_factory=list[PrincipalRoleOutSchema],
    )
    """A list of principal role associations found based on the current request criteria."""

    total: int = Field(
        title='Total Principal Role Associations',
        description='The total number of principal role associations.',
        default=0,
        examples=[4],
    )
    """The total number of principal role associations."""

    total_filtered: int = Field(
        title='Total Principal Role Associations Found',
        description='The total number of principal role associations found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of principal role associations found based on the current request criteria."""
