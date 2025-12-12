from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from models.api.zones.azones import AZonesSchema, AZoneOutSchema, AZoneInSchema
from routers.v1.zones import router


@router.post(
    '/authoritative',
    response_model=AZonesSchema,
    summary='List authoritative zones',
    description='List authoritative zones.',
    operation_id='zones:authoritative:list',
)
async def record_list(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZonesSchema:
    """List authoritative zones"""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.zones import AZone

    # Build a statement to retrieve the relevant records
    stmt = select(AZone)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(AZone.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, AZone)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return AZonesSchema(
        records=[AZoneOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/authoritative/create',
    response_model=AZoneOutSchema,
    summary='Create authoritative zone',
    description='Create authoritative zone.',
    operation_id='zones:authoritative:create',
)
async def record_create(
        zone: AZoneInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneOutSchema:
    """Create authoritative zone"""
    from models.db.zones import AZone

    # Create the record
    record = AZone(
        view_id=zone.view_id,
        fqdn=zone.fqdn,
        kind=zone.kind,
        serial=zone.serial,
        notified_serial=zone.notified_serial,
        edited_serial=zone.edited_serial,
        masters=zone.masters,
        dnssec=zone.dnssec,
        nsec3param=zone.nsec3param,
        nsec3narrow=zone.nsec3narrow,
        presigned=zone.presigned,
        soa_edit=zone.soa_edit,
        soa_edit_api=zone.soa_edit_api,
        api_rectify=zone.api_rectify,
        zone=zone.zone,
        catalog=zone.catalog,
        account=zone.account,
        master_tsig_key_ids=zone.master_tsig_key_ids,
        slave_tsig_key_ids=zone.slave_tsig_key_ids,
        shared=zone.shared,
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
    return AZoneOutSchema.model_validate(record)


@router.get(
    '/authoritative/{zone_id}',
    response_model=AZoneOutSchema,
    summary='Read authoritative zone',
    description='Read authoritative zone.',
    operation_id='zones:authoritative:read',
)
async def record_read(
        zone_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneOutSchema:
    """Read authoritative zone"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.zones import AZone

    # Build a statement to retrieve the record
    stmt = select(AZone).where(AZone.id == zone_id)

    # Retrieve the record
    record: AZone | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Authoritative zone {zone_id} not found')

    # Build the response
    return AZoneOutSchema.model_validate(record)


@router.put(
    '/authoritative/{zone_id}',
    response_model=AZoneOutSchema,
    summary='Update authoritative zone',
    description='Update authoritative zone.',
    operation_id='zones:authoritative:update',
)
async def record_update(
        zone_id:UUID,
        zone: AZoneInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneOutSchema:
    """Update authoritative zone"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.zones import AZone

    # Build a statement to retrieve the record
    stmt = select(AZone).where(AZone.id == zone_id)

    # Retrieve the record
    record: AZone | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Authoritative zone {zone_id} not found')

    # Update the record
    record.view_id = zone.view_id
    record.fqdn = zone.fqdn
    record.kind = zone.kind
    record.serial = zone.serial
    record.notified_serial = zone.notified_serial
    record.edited_serial = zone.edited_serial
    record.masters = zone.masters
    record.dnssec = zone.dnssec
    record.nsec3param = zone.nsec3param
    record.nsec3narrow = zone.nsec3narrow
    record.presigned = zone.presigned
    record.soa_edit = zone.soa_edit
    record.soa_edit_api = zone.soa_edit_api
    record.api_rectify = zone.api_rectify
    record.zone = zone.zone
    record.catalog = zone.catalog
    record.account = zone.account
    record.master_tsig_key_ids = zone.master_tsig_key_ids
    record.slave_tsig_key_ids = zone.slave_tsig_key_ids
    record.shared = zone.shared

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return AZoneOutSchema.model_validate(record)


@router.delete(
    '/authoritative/{zone_id}',
    summary='Delete authoritative zone',
    description='Delete authoritative zone.',
    operation_id='zones:authoritative:delete',
)
async def record_delete(
        zone_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete authoritative zone"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models.db.zones import AZone

    # Build a statement to delete the record
    stmt = delete(AZone).where(AZone.id == zone_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Authoritative zone {zone_id} not found')
