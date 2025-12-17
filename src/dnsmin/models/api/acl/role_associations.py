from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field

from dnsmin.models.api import BaseApiModel


class RoleAssociationInSchema(BaseApiModel):
    """Provides an API input model for creating ACL role associations."""

    child_role_id: UUID = Field(
        title='Child Role ID',
        description='The unique identifier of the child role.',
        examples=[uuid4()],
    )
    """The unique identifier of the child role."""

    parent_role_id: UUID = Field(
        title='Parent Role ID',
        description='The unique identifier of the parent role.',
        examples=[uuid4()],
    )
    """The unique identifier of the parent role."""


class RoleAssociationOutSchema(BaseApiModel):
    """Provides an API response model for representing ACL role associations."""

    child_role_id: UUID = Field(
        title='Child Role ID',
        description='The unique identifier of the child role.',
        examples=[uuid4()],
    )
    """The unique identifier of the child role."""

    parent_role_id: UUID = Field(
        title='Parent Role ID',
        description='The unique identifier of the parent role.',
        examples=[uuid4()],
    )
    """The unique identifier of the parent role."""

    created_at: datetime = Field(
        title='Created At',
        description='The timestamp representing when the association was created.',
        default_factory=datetime.now,
        examples=[datetime.now()],
    )
    """The timestamp representing when the association was created."""


class RoleAssociationsSchema(BaseApiModel):
    """Provides an API response model for retrieving ACL principals."""

    records: list[RoleAssociationOutSchema] = Field(
        title='Role Associations',
        description='A list of role associations found based on the current request criteria.',
        default_factory=list[RoleAssociationOutSchema],
    )
    """A list of role associations found based on the current request criteria."""

    total: int = Field(
        title='Total Role Associations',
        description='The total number of role associations.',
        default=0,
        examples=[4],
    )
    """The total number of role associations."""

    total_filtered: int = Field(
        title='Total Role Associations Found',
        description='The total number of role associations found based on the current request criteria.',
        default=0,
        examples=[1234],
    )
    """The total number of role associations found based on the current request criteria."""
