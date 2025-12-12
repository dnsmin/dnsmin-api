from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from models.api.zones.azones import AZoneMetadataSchema, AZoneMetadataOutSchema, AZoneMetadataInSchema
from routers.v1.zones import router


@router.post(
    '/authoritative/{zone_id}/metadata',
    response_model=AZoneMetadataSchema,
    summary='List authoritative zone metadata',
    description='List authoritative zone metadata.',
    operation_id='zones:authoritative:metadata:list',
)
async def record_list(
        zone_id:UUID,
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneMetadataSchema:
    """List authoritative zone metadata"""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.zones import AZoneMetadata

    # Build a statement to retrieve the relevant records
    stmt = select(AZoneMetadata).where(AZoneMetadata.zone_id == zone_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(AZoneMetadata.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, AZoneMetadata)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return AZoneMetadataSchema(
        records=[AZoneMetadataOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/authoritative/{zone_id}/metadata/create',
    response_model=AZoneMetadataOutSchema,
    summary='Create authoritative zone metadata',
    description='Create authoritative zone metadata.',
    operation_id='zones:authoritative:metadata:create',
)
async def record_create(
        zone_id:UUID,
        metadata: AZoneMetadataInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneMetadataOutSchema:
    """Create authoritative zone metadata"""
    from models.db.zones import AZoneMetadata

    # Create the record
    record = AZoneMetadata(
        zone_id=zone_id,
        view_id=metadata.view_id,
        name=metadata.name,
        values=metadata.values,
    )

    # Enforce tenancy
    if principal.tenant_id:
        record.tenant_id = principal.tenant_id
    else:
        record.tenant_id = record.tenant_id

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return AZoneMetadataOutSchema.model_validate(record)


@router.get(
    '/authoritative/{zone_id}/metadata/{metadata_id}',
    response_model=AZoneMetadataOutSchema,
    summary='Read authoritative zone metadata',
    description='Read authoritative zone metadata.',
    operation_id='zones:authoritative:metadata:read',
)
async def record_read(
        zone_id:UUID,
        metadata_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneMetadataOutSchema:
    """Read authoritative zone metadata"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.zones import AZoneMetadata

    # Build a statement to retrieve the record
    stmt = select(AZoneMetadata).where(AZoneMetadata.id == metadata_id, AZoneMetadata.zone_id == zone_id)

    # Retrieve the record
    record: AZoneMetadata | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Authoritative zone metadata {metadata_id} not found')

    # Build the response
    return AZoneMetadataOutSchema.model_validate(record)


@router.put(
    '/authoritative/{zone_id}/metadata/{metadata_id}',
    response_model=AZoneMetadataOutSchema,
    summary='Update authoritative zone metadata',
    description='Update authoritative zone metadata.',
    operation_id='zones:authoritative:metadata:update',
)
async def record_update(
        zone_id:UUID,
        metadata_id:UUID,
        metadata: AZoneMetadataInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneMetadataOutSchema:
    """Update authoritative zone metadata"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.zones import AZoneRecord

    # Build a statement to retrieve the record
    stmt = select(AZoneRecord).where(AZoneRecord.id == metadata_id, AZoneRecord.zone_id == zone_id)

    # Retrieve the record
    record: AZoneRecord | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Authoritative zone metadata {metadata_id} not found')

    # Update the record
    record.view_id = metadata.view_id
    record.name = metadata.name
    record.values = metadata.values

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return AZoneMetadataOutSchema.model_validate(record)


@router.delete(
    '/authoritative/{zone_id}/metadata/{metadata_id}',
    summary='Delete authoritative zone metadata',
    description='Delete authoritative zone metadata.',
    operation_id='zones:authoritative:metadata:delete',
)
async def record_delete(
        zone_id:UUID,
        metadata_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete authoritative zone metadata"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models.db.zones import AZoneMetadata

    # Build a statement to delete the record
    stmt = delete(AZoneMetadata).where(AZoneMetadata.id == metadata_id, AZoneMetadata.zone_id == zone_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Authoritative zone metadata {metadata_id} not found')
