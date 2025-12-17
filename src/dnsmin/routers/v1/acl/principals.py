from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnsmin.lib.api.dependencies import get_db_session, get_principal
from dnsmin.models.api import Principal, ListParamsModel
from dnsmin.models.api.acl.principals import PrincipalsSchema, PrincipalOutSchema, PrincipalInSchema
from dnsmin.routers.v1.acl import router


@router.get(
    '/principals',
    response_model=list[PrincipalOutSchema],
    summary='List ACL principals',
    description='Lists ACL principals.',
    operation_id='acl:principals:list',
)
async def record_list(
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> list[PrincipalOutSchema]:
    """List ACL principals"""
    from sqlalchemy import select
    from dnsmin.models.db.acl import Principal

    # Build a statement to retrieve the relevant records
    stmt = select(Principal)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Principal.tenant_id == principal.tenant_id)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return [PrincipalOutSchema.model_validate(r) for r in records]


@router.post(
    '/principals/search',
    response_model=PrincipalsSchema,
    summary='Search ACL principals',
    description='Search ACL principals.',
    operation_id='acl:principals:search',
)
async def record_search(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> PrincipalsSchema:
    """Search ACL principals"""
    from sqlalchemy import select, func
    from dnsmin.lib.sql import SqlQueryBuilder
    from dnsmin.models.db.acl import Principal

    # Build a statement to retrieve the relevant records
    stmt = select(Principal)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Principal.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, Principal)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return PrincipalsSchema(
        records=[PrincipalOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/principals',
    response_model=PrincipalOutSchema,
    summary='Create ACL principal',
    description='Creates ACL principal.',
    operation_id='acl:principals:create',
)
async def record_create(
        principal_: PrincipalInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> PrincipalOutSchema:
    """Create ACL principal"""
    from dnsmin.models.db.acl import Principal

    # Create the record
    record = Principal(
        id=principal_.id,
        type=principal_.type,
    )

    # Enforce tenancy
    if principal.tenant_id:
        record.tenant_id = principal.tenant_id
    else:
        record.tenant_id = principal_.tenant_id

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return PrincipalOutSchema.model_validate(record)


@router.get(
    '/principals/{principal_id}',
    response_model=PrincipalOutSchema,
    summary='Read ACL principal',
    description='Read ACL principal.',
    operation_id='acl:principals:read',
)
async def record_read(
        principal_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> PrincipalOutSchema:
    """Read ACL principal"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from dnsmin.models.db.acl import Principal

    # Build a statement to retrieve the record
    stmt = select(Principal).where(Principal.id == principal_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Principal.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: Principal | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Principal {principal_id} not found')

    # Build the response
    return PrincipalOutSchema.model_validate(record)


@router.delete(
    '/principals/{principal_id}',
    summary='Delete ACL principal',
    description='Delete ACL principal.',
    operation_id='acl:principals:delete',
)
async def record_delete(
        principal_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> None:
    """Delete ACL principal"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from dnsmin.models.db.acl import Principal

    # Build a statement to delete the record
    stmt = delete(Principal).where(Principal.id == principal_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Principal.tenant_id == principal.tenant_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Principal {principal_id} not found')
