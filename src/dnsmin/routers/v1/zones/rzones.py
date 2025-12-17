from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnsmin.lib.api.dependencies import get_db_session, get_principal
from dnsmin.models.api import ListParamsModel
from dnsmin.models.api.auth import Principal
from dnsmin.models.api.zones.rzones import RZonesSchema, RZoneOutSchema, RZoneInSchema
from dnsmin.routers.v1.zones import router


@router.get(
    '/recursive',
    response_model=list[RZoneOutSchema],
    summary='List recursive zones',
    description='List recursive zones.',
    operation_id='zones:recursive:list',
)
async def record_list(
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> list[RZoneOutSchema]:
    """List recursive zones"""
    from sqlalchemy import select
    from dnsmin.models.db.zones import RZone

    # Build a statement to retrieve the relevant records
    stmt = select(RZone)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(RZone.tenant_id == principal.tenant_id)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return [RZoneOutSchema.model_validate(r) for r in records]


@router.post(
    '/recursive/search',
    response_model=RZonesSchema,
    summary='Search recursive zones',
    description='Search recursive zones.',
    operation_id='zones:recursive:search',
)
async def record_search(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RZonesSchema:
    """Search recursive zones"""
    from sqlalchemy import select, func
    from dnsmin.lib.sql import SqlQueryBuilder
    from dnsmin.models.db.zones import RZone

    # Build a statement to retrieve the relevant records
    stmt = select(RZone)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(RZone.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, RZone)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return RZonesSchema(
        records=[RZoneOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/recursive',
    response_model=RZoneOutSchema,
    summary='Create recursive zone',
    description='Create recursive zone.',
    operation_id='zones:recursive:create',
)
async def record_create(
        zone: RZoneInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RZoneOutSchema:
    """Create recursive zone"""
    from dnsmin.models.db.zones import RZone

    # Create the record
    record = RZone(
        fqdn=zone.fqdn,
        kind=zone.kind,
        servers=zone.servers,
        recursion_desired=zone.recursion_desired,
        notify_allowed=zone.notify_allowed,
    )

    # Enforce tenancy
    if principal.tenant_id:
        record.tenant_id = principal.tenant_id
    else:
        record.tenant_id = zone.tenant_id

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return RZoneOutSchema.model_validate(record)


@router.get(
    '/recursive/{zone_id}',
    response_model=RZoneOutSchema,
    summary='Retrieve recursive zone',
    description='Retrieve recursive zone.',
    operation_id='zones:recursive:read',
)
async def record_read(
        zone_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RZoneOutSchema:
    """Read recursive zone"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from dnsmin.models.db.zones import RZone

    # Build a statement to retrieve the record
    stmt = select(RZone).where(RZone.id == zone_id)

    # Retrieve the record
    record: RZone | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Recursive zone {zone_id} not found')

    # Build the response
    return RZoneOutSchema.model_validate(record)


@router.put(
    '/recursive/{zone_id}',
    response_model=RZoneOutSchema,
    summary='Update recursive zone',
    description='Update recursive zone.',
    operation_id='zones:recursive:update',
)
async def record_update(
        zone_id:UUID,
        zone: RZoneInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RZoneOutSchema:
    """Update recursive zone"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from dnsmin.models.db.zones import RZone

    # Build a statement to retrieve the record
    stmt = select(RZone).where(RZone.id == zone_id)

    # Retrieve the record
    record: RZone | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Recursive zone {zone_id} not found')

    # Update the record
    record.fqdn = zone.fqdn
    record.kind = zone.kind
    record.servers = zone.servers
    record.recursion_desired = zone.recursion_desired
    record.notify_allowed = zone.notify_allowed

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return RZoneOutSchema.model_validate(record)


@router.delete(
    '/recursive/{zone_id}',
    summary='Delete recursive zone',
    description='Delete recursive zone.',
    operation_id='zones:recursive:delete',
)
async def record_delete(
        zone_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete recursive zone"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from dnsmin.models.db.zones import RZone

    # Build a statement to delete the record
    stmt = delete(RZone).where(RZone.id == zone_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Recursive zone {zone_id} not found')
