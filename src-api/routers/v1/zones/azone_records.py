from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from models.api.zones.azone_records import AZoneRecordInSchema, AZoneRecordOutSchema, AZoneRecordsSchema
from routers.v1.zones import router


@router.get(
    '/authoritative/{zone_id}/records',
    response_model=list[AZoneRecordOutSchema],
    summary='List authoritative zone records',
    description='List authoritative zone records.',
    operation_id='zones:authoritative:records:list',
)
async def record_list(
        zone_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> list[AZoneRecordOutSchema]:
    """List authoritative zone records"""
    from sqlalchemy import select
    from models.db.zones import AZoneRecord

    # Build a statement to retrieve the relevant records
    stmt = select(AZoneRecord).where(AZoneRecord.zone_id == zone_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(AZoneRecord.tenant_id == principal.tenant_id)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return [AZoneRecordOutSchema.model_validate(r) for r in records]


@router.post(
    '/authoritative/{zone_id}/records/search',
    response_model=AZoneRecordsSchema,
    summary='Search authoritative zone records',
    description='Search authoritative zone records.',
    operation_id='zones:authoritative:records:search',
)
async def record_search(
        zone_id:UUID,
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneRecordsSchema:
    """Search authoritative zone records"""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.zones import AZoneRecord

    # Build a statement to retrieve the relevant records
    stmt = select(AZoneRecord).where(AZoneRecord.zone_id == zone_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(AZoneRecord.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, AZoneRecord)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return AZoneRecordsSchema(
        records=[AZoneRecordOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/authoritative/{zone_id}/records',
    response_model=AZoneRecordOutSchema,
    summary='Create authoritative zone record',
    description='Create authoritative zone record.',
    operation_id='zones:authoritative:records:create',
)
async def record_create(
        zone_id:UUID,
        record: AZoneRecordInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneRecordOutSchema:
    """Create authoritative zone record"""
    from models.db.zones import AZoneRecord

    # Create the record
    db_record = AZoneRecord(
        zone_id=zone_id,
        view_id=record.view_id,
        name=record.name,
        type=record.type,
        ttl=record.ttl,
        content=record.content,
        comment=record.comment,
        disabled=record.disabled,
    )

    # Enforce tenancy
    if principal.tenant_id:
        db_record.tenant_id = principal.tenant_id
    else:
        db_record.tenant_id = record.tenant_id

    # Commit the changes to the database
    session.add(db_record)
    await session.commit()
    await session.refresh(db_record)

    # Build the response
    return AZoneRecordOutSchema.model_validate(db_record)


@router.get(
    '/authoritative/{zone_id}/records/{record_id}',
    response_model=AZoneRecordOutSchema,
    summary='Read authoritative zone record',
    description='Read authoritative zone record.',
    operation_id='zones:authoritative:records:read',
)
async def record_read(
        zone_id:UUID,
        record_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneRecordOutSchema:
    """Read authoritative zone record"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.zones import AZoneRecord

    # Build a statement to retrieve the record
    stmt = select(AZoneRecord).where(AZoneRecord.id == record_id, AZoneRecord.zone_id == zone_id)

    # Retrieve the record
    record: AZoneRecord | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Authoritative zone record {record_id} not found')

    # Build the response
    return AZoneRecordOutSchema.model_validate(record)


@router.put(
    '/authoritative/{zone_id}/records/{record_id}',
    response_model=AZoneRecordOutSchema,
    summary='Update authoritative zone record',
    description='Update authoritative zone record.',
    operation_id='zones:authoritative:records:update',
)
async def record_update(
        zone_id:UUID,
        record_id:UUID,
        record: AZoneRecordInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneRecordOutSchema:
    """Update authoritative zone record"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.zones import AZoneRecord

    # Build a statement to retrieve the record
    stmt = select(AZoneRecord).where(AZoneRecord.id == record_id, AZoneRecord.zone_id == zone_id)

    # Retrieve the record
    db_record: AZoneRecord | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Authoritative zone record {record_id} not found')

    # Update the record
    db_record.name = record.name
    db_record.type = record.type
    db_record.ttl = record.ttl
    db_record.content = record.content
    db_record.comment = record.comment
    db_record.disabled = record.disabled

    # Commit the changes to the database
    session.add(db_record)
    await session.commit()
    await session.refresh(db_record)

    # Build the response
    return AZoneRecordOutSchema.model_validate(db_record)


@router.delete(
    '/authoritative/{zone_id}/records/{record_id}',
    summary='Delete authoritative zone record',
    description='Delete authoritative zone record.',
    operation_id='zones:authoritative:records:delete',
)
async def record_delete(
        zone_id:UUID,
        record_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete authoritative zone record"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models.db.zones import AZoneRecord

    # Build a statement to delete the record
    stmt = delete(AZoneRecord).where(AZoneRecord.id == record_id, AZoneRecord.zone_id == zone_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Authoritative zone record {record_id} not found')
