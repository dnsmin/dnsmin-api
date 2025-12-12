from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from models.api.zones.rzone_records import RZoneRecordInSchema, RZoneRecordOutSchema, RZoneRecordsSchema
from routers.v1.zones import router


@router.post(
    '/recursive/{zone_id}/records',
    response_model=RZoneRecordsSchema,
    summary='List recursive zone records',
    description='List recursive zone records.',
    operation_id='zones:recursive:records:list',
)
async def record_list(
        zone_id:UUID,
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RZoneRecordsSchema:
    """List recursive zone records"""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.zones import RZoneRecord

    # Build a statement to retrieve the relevant records
    stmt = select(RZoneRecord).where(RZoneRecord.zone_id == zone_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(RZoneRecord.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, RZoneRecord)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return RZoneRecordsSchema(
        records=[RZoneRecordOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/recursive/{zone_id}/records/create',
    response_model=RZoneRecordOutSchema,
    summary='Create recursive zone record',
    description='Create recursive zone record.',
    operation_id='zones:recursive:records:create',
)
async def record_create(
        zone_id:UUID,
        record: RZoneRecordInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RZoneRecordOutSchema:
    """Create recursive zone record"""
    from models.db.zones import RZoneRecord

    # Create the record
    db_record = RZoneRecord(
        zone_id=zone_id,
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
    return RZoneRecordOutSchema.model_validate(db_record)


@router.get(
    '/recursive/{zone_id}/records/{record_id}',
    response_model=RZoneRecordOutSchema,
    summary='Read recursive zone record',
    description='Read recursive zone record.',
    operation_id='zones:recursive:records:read',
)
async def record_read(
        zone_id:UUID,
        record_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RZoneRecordOutSchema:
    """Read recursive zone record"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.zones import RZoneRecord

    # Build a statement to retrieve the record
    stmt = select(RZoneRecord).where(RZoneRecord.id == record_id, RZoneRecord.zone_id == zone_id)

    # Retrieve the record
    record: RZoneRecord | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Recursive zone record {record_id} not found')

    # Build the response
    return RZoneRecordOutSchema.model_validate(record)


@router.put(
    '/recursive/{zone_id}/records/{record_id}',
    response_model=RZoneRecordOutSchema,
    summary='Update recursive zone record',
    description='Update recursive zone record.',
    operation_id='zones:recursive:records:update',
)
async def record_update(
        zone_id:UUID,
        record_id:UUID,
        record: RZoneRecordInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> RZoneRecordOutSchema:
    """Update recursive zone record"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.zones import RZoneRecord

    # Build a statement to retrieve the record
    stmt = select(RZoneRecord).where(RZoneRecord.id == record_id, RZoneRecord.zone_id == zone_id)

    # Retrieve the record
    db_record: RZoneRecord | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not db_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Recursive zone record {record_id} not found')

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
    return RZoneRecordOutSchema.model_validate(db_record)


@router.delete(
    '/recursive/{zone_id}/records/{record_id}',
    summary='Delete recursive zone record',
    description='Delete recursive zone record.',
    operation_id='zones:recursive:records:delete',
)
async def record_delete(
        zone_id:UUID,
        record_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete recursive zone record"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models.db.zones import RZoneRecord

    # Build a statement to delete the record
    stmt = delete(RZoneRecord).where(RZoneRecord.id == record_id, RZoneRecord.zone_id == zone_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Recursive zone record {record_id} not found')
