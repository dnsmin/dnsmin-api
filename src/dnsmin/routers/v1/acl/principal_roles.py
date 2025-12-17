from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnsmin.lib.api.dependencies import get_db_session, get_principal
from dnsmin.models.api import Principal, ListParamsModel
from dnsmin.models.api.acl.principal_roles import PrincipalRolesSchema, PrincipalRoleOutSchema, PrincipalRoleInSchema
from dnsmin.routers.v1.acl import router


@router.get(
    '/principal-roles',
    response_model=list[PrincipalRoleOutSchema],
    summary='List ACL principal role associations',
    description='Lists ACL principal role associations.',
    operation_id='acl:principal_roles:list',
)
async def record_list(
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> list[PrincipalRoleOutSchema]:
    """List ACL principal role associations"""
    from sqlalchemy import select
    from dnsmin.models.db.acl import PrincipalRoleAssoc

    # Build a statement to retrieve the relevant records
    stmt = select(PrincipalRoleAssoc)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return [PrincipalRoleOutSchema.model_validate(r) for r in records]


@router.post(
    '/principal-roles/search',
    response_model=PrincipalRolesSchema,
    summary='Search ACL principal roles',
    description='Search ACL principal roles.',
    operation_id='acl:principal_roles:search',
)
async def record_search(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> PrincipalRolesSchema:
    """Search ACL principal role associations"""
    from sqlalchemy import select, func
    from dnsmin.lib.sql import SqlQueryBuilder
    from dnsmin.models.db.acl import PrincipalRoleAssoc

    # Build a statement to retrieve the relevant records
    stmt = select(PrincipalRoleAssoc)
    
    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, PrincipalRoleAssoc)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return PrincipalRolesSchema(
        records=[PrincipalRoleOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/principal-roles',
    response_model=PrincipalRoleOutSchema,
    summary='Create ACL principal role association',
    description='Creates ACL principal role association.',
    operation_id='acl:principal_roles:create',
)
async def record_create(
        principal_role: PrincipalRoleInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> PrincipalRoleOutSchema:
    """Create ACL principal role association"""
    from dnsmin.models.db.acl import PrincipalRoleAssoc

    # Create the record
    record = PrincipalRoleAssoc(
        principal_id=principal_role.principal_id,
        role_id=principal_role.role_id,
    )

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return PrincipalRoleOutSchema.model_validate(record)


@router.delete(
    '/principal-roles/{principal_id}/{role_id}',
    summary='Delete ACL principal role association',
    description='Delete ACL principal role association.',
    operation_id='acl:principal_roles:delete',
)
async def record_delete(
        principal_id: UUID,
        role_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> None:
    """Delete ACL principal role association"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from dnsmin.models.db.acl import PrincipalRoleAssoc

    # Build a statement to delete the record
    stmt = (delete(PrincipalRoleAssoc)
            .where(PrincipalRoleAssoc.principal_id == principal_id, PrincipalRoleAssoc.role_id == role_id))

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Principal Role Association {principal_id}/{role_id} not found')
