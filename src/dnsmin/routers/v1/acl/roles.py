from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnsmin.lib.api.dependencies import get_db_session, get_principal
from dnsmin.models.api import Principal, ListParamsModel
from dnsmin.models.api.acl.roles import RolesSchema, RoleOutSchema, RoleInSchema
from dnsmin.routers.v1.acl import router


@router.get(
    '/roles',
    response_model=list[RoleOutSchema],
    summary='List ACL roles',
    description='Lists ACL roles.',
    operation_id='acl:roles:list',
)
async def record_list(
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> list[RoleOutSchema]:
    """List ACL roles"""
    from sqlalchemy import select
    from dnsmin.models.db.acl import Role

    # Build a statement to retrieve the relevant records
    stmt = select(Role)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Role.tenant_id == principal.tenant_id)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return [RoleOutSchema.model_validate(r) for r in records]


@router.post(
    '/roles/search',
    response_model=RolesSchema,
    summary='Search ACL roles',
    description='Search ACL roles.',
    operation_id='acl:roles:search',
)
async def record_search(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RolesSchema:
    """Search ACL roles"""
    from sqlalchemy import select, func
    from dnsmin.lib.sql import SqlQueryBuilder
    from dnsmin.models.db.acl import Role

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

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return RolesSchema(
        records=[RoleOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/roles',
    response_model=RoleOutSchema,
    summary='Create ACL role',
    description='Creates ACL role.',
    operation_id='acl:roles:create',
)
async def record_create(
        role: RoleInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RoleOutSchema:
    """Create ACL role"""
    from dnsmin.models.db.acl import Role

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
    description='Read ACL role.',
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
    from dnsmin.models.db.acl import Role

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
    description='Update ACL role.',
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
    from dnsmin.models.db.acl import Role

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
    description='Delete ACL role.',
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
    from dnsmin.models.db.acl import Role

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
