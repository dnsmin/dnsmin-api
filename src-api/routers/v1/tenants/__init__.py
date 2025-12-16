from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from models.api.tenants.tenants import TenantsSchema, TenantOutSchema, TenantInSchema
from routers.root import router_responses

router = APIRouter(
    prefix='/tenants',
    tags=['tenants'],
    responses=router_responses,
)


@router.get(
    '/tenants',
    response_model=list[TenantOutSchema],
    summary='List tenants',
    description='List tenants.',
    operation_id='tenants:list',
)
async def record_list(
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> list[TenantOutSchema]:
    """List tenants"""
    from sqlalchemy import select
    from models.db.tenants import Tenant

    # Build a statement to retrieve the relevant records
    stmt = select(Tenant)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return [TenantOutSchema.model_validate(r) for r in records]


@router.post(
    '/tenants/search',
    response_model=TenantsSchema,
    summary='Search tenants',
    description='Search tenants.',
    operation_id='tenants:search',
)
async def record_search(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> TenantsSchema:
    """Search tenants"""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.tenants import Tenant

    # Build a statement to retrieve the relevant records
    stmt = select(Tenant)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, Tenant)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return TenantsSchema(
        records=[TenantOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/tenants',
    response_model=TenantOutSchema,
    summary='Create tenant',
    description='Create tenant.',
    operation_id='tenants:create',
)
async def record_create(
        tenant: TenantInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> TenantOutSchema:
    """Create tenant"""
    from models.db.tenants import Tenant

    # Create the record
    record = Tenant(
        name=tenant.name,
        fqdn=tenant.fqdn,
        stopgap_domain_id=tenant.stopgap_domain_id,
        stopgap_hostname=tenant.stopgap_hostname,
    )

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return TenantOutSchema.model_validate(record)


@router.get(
    '/tenants/{tenant_id}',
    response_model=TenantOutSchema,
    summary='Read tenant',
    description='Read tenant.',
    operation_id='tenants:read',
)
async def record_read(
        tenant_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> TenantOutSchema:
    """Read tenant"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.tenants import Tenant

    # Build a statement to retrieve the record
    stmt = select(Tenant).where(Tenant.id == tenant_id)

    # Retrieve the record
    record: Tenant | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Tenant {tenant_id} not found')

    # Build the response
    return TenantOutSchema.model_validate(record)


@router.put(
    '/tenants/{tenant_id}',
    response_model=TenantOutSchema,
    summary='Update tenant',
    description='Update tenant.',
    operation_id='tenants:update',
)
async def record_update(
        tenant_id: UUID,
        tenant: TenantInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> TenantOutSchema:
    """Update tenant"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.tenants import Tenant

    # Build a statement to retrieve the record
    stmt = select(Tenant).where(Tenant.id == tenant_id)

    # Retrieve the record
    record: Tenant | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Tenant {tenant_id} not found')

    # Update the record
    record.name = tenant.name
    record.fqdn = tenant.fqdn
    record.stopgap_domain_id = tenant.stopgap_domain_id
    record.stopgap_hostname = tenant.stopgap_hostname

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return TenantOutSchema.model_validate(record)


@router.delete(
    '/tenants/{tenant_id}',
    summary='Delete tenant',
    description='Delete tenant.',
    operation_id='tenants:delete',
)
async def record_delete(
        tenant_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete tenant"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models.db.tenants import Tenant

    # Build a statement to delete the record
    stmt = delete(Tenant).where(Tenant.id == tenant_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Tenant {tenant_id} not found')
