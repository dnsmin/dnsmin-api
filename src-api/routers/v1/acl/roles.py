from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import Principal, ListParamsModel
from models.api.acl.roles import RolesSchema, RoleOutSchema, RoleInSchema
from routers.v1.acl import router


@router.post(
    '/roles',
    response_model=RolesSchema,
    summary='List ACL roles',
    description='Lists ACL roles for the current authentication context.',
    operation_id='acl:roles:list',
)
async def record_list(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RolesSchema:
    """List ACL roles"""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.acl import Role

    # Build a statement to retrieve the relevant records
    stmt = select(Role)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Role.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, Role)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return RolesSchema(
        records=[RoleOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
    )


@router.post(
    '/roles/create',
    response_model=RoleOutSchema,
    summary='Create ACL role',
    description='Creates ACL role for the current authentication context.',
    operation_id='acl:roles:create',
)
async def record_create(
        role: RoleInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RoleOutSchema:
    """Create ACL role"""
    from models.db.acl import Role

    # Create the record
    record = Role(
        slug=role.slug,
        description=role.description,
    )

    # Enforce tenancy
    if principal.tenant_id:
        record.tenant_id = principal.tenant_id
    else:
        record.tenant_id = role.tenant_id

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return RoleOutSchema.model_validate(record)


@router.get(
    '/roles/{role_id}',
    response_model=RoleOutSchema,
    summary='Read ACL role',
    description='Read ACL role from the current authentication context.',
    operation_id='acl:roles:read',
)
async def record_read(
        role_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RoleOutSchema:
    """Read ACL role"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.acl import Role

    # Build a statement to retrieve the record
    stmt = select(Role).where(Role.id == role_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Role.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: Role | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Role {role_id} not found')

    # Build the response
    return RoleOutSchema.model_validate(record)


@router.patch(
    '/roles/{role_id}',
    response_model=RoleOutSchema,
    summary='Update ACL role',
    description='Update ACL role in the current authentication context.',
    operation_id='acl:roles:update',
)
async def record_update(
        role_id: UUID,
        role: RoleInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RoleOutSchema:
    """Update ACL role"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.acl import Role

    # Build a statement to retrieve the record
    stmt = select(Role).where(Role.id == role_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Role.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: Role | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Role {role_id} not found')

    # Update the record
    record.slug = role.slug
    record.description = role.description

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return RoleOutSchema.model_validate(record)


@router.delete(
    '/roles/{role_id}',
    summary='Delete ACL role',
    description='Delete ACL role in the current authentication context.',
    operation_id='acl:roles:delete',
)
async def record_delete(
        role_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> None:
    """Delete ACL role"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models.db.acl import Role

    # Build a statement to delete the record
    stmt = delete(Role).where(Role.id == role_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Role.tenant_id == principal.tenant_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Role {role_id} not found')
