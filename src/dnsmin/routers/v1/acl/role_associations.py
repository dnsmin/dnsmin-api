from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnsmin.lib.api.dependencies import get_db_session, get_principal
from dnsmin.models.api import Principal, ListParamsModel
from dnsmin.models.api.acl.role_associations import RoleAssociationsSchema, RoleAssociationOutSchema, RoleAssociationInSchema
from dnsmin.routers.v1.acl import router


@router.get(
    '/role-associations',
    response_model=list[RoleAssociationOutSchema],
    summary='List ACL role associations',
    description='Lists ACL role associations.',
    operation_id='acl:role_associations:list',
)
async def record_list(
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> list[RoleAssociationOutSchema]:
    """List ACL role associations"""
    from sqlalchemy import select
    from dnsmin.models.db.acl import RoleInheritance

    # Build a statement to retrieve the relevant records
    stmt = select(RoleInheritance)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return [RoleAssociationOutSchema.model_validate(r) for r in records]


@router.post(
    '/role-associations/search',
    response_model=RoleAssociationsSchema,
    summary='Search ACL principal roles',
    description='Search ACL principal roles.',
    operation_id='acl:role_associations:search',
)
async def record_search(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RoleAssociationsSchema:
    """Search ACL role associations"""
    from sqlalchemy import select, func
    from dnsmin.lib.sql import SqlQueryBuilder
    from dnsmin.models.db.acl import RoleInheritance

    # Build a statement to retrieve the relevant records
    stmt = select(RoleInheritance)
    
    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, RoleInheritance)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return RoleAssociationsSchema(
        records=[RoleAssociationOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/role-associations',
    response_model=RoleAssociationOutSchema,
    summary='Create ACL role association',
    description='Creates ACL role association.',
    operation_id='acl:role_associations:create',
)
async def record_create(
        role_association: RoleAssociationInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RoleAssociationOutSchema:
    """Create ACL role association"""
    from dnsmin.models.db.acl import RoleInheritance

    # Create the record
    record = RoleInheritance(
        child_role_id=role_association.child_role_id,
        parent_role_id=role_association.parent_role_id,
    )

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return RoleAssociationOutSchema.model_validate(record)


@router.delete(
    '/role-associations/{child_role_id}/{parent_role_id}',
    summary='Delete ACL role association',
    description='Delete ACL role association.',
    operation_id='acl:role_associations:delete',
)
async def record_delete(
        child_role_id: UUID,
        parent_role_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> None:
    """Delete ACL role association"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from dnsmin.models.db.acl import RoleInheritance

    # Build a statement to delete the record
    stmt = (delete(RoleInheritance)
            .where(RoleInheritance.child_role_id == child_role_id, RoleInheritance.parent_role_id == parent_role_id))

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Role Association {child_role_id}/{parent_role_id} not found')
