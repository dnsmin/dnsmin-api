from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from models.api.system.timezones import TimezonesSchema, TimezoneOutSchema, TimezoneInSchema
from routers.v1.system import router


@router.get(
    '/timezones',
    response_model=list[TimezoneOutSchema],
    summary='List timezones',
    description='List timezones.',
    operation_id='system:timezones:list',
)
async def record_list(
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> list[TimezoneOutSchema]:
    """List timezones"""
    from sqlalchemy import select
    from models.db.system import RefTimezone

    # Build a statement to retrieve the relevant records
    stmt = select(RefTimezone)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return [TimezoneOutSchema.model_validate(r) for r in records]


@router.post(
    '/timezones/search',
    response_model=TimezonesSchema,
    summary='Search timezones',
    description='Search timezones.',
    operation_id='system:timezones:search',
)
async def record_search(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> TimezonesSchema:
    """Search timezones"""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.system import RefTimezone

    # Build a statement to retrieve the relevant records
    stmt = select(RefTimezone)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, RefTimezone)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return TimezonesSchema(
        records=[TimezoneOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/timezones',
    response_model=TimezoneOutSchema,
    summary='Create timezone',
    description='Create timezone.',
    operation_id='system:timezones:create',
)
async def record_create(
        timezone: TimezoneInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> TimezoneOutSchema:
    """Create timezone"""
    from models.db.system import RefTimezone

    # Create the record
    record = RefTimezone(
        name=timezone.name,
        offset=timezone.offset,
        offset_dst=timezone.offset_dst,
    )

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return TimezoneOutSchema.model_validate(record)


@router.get(
    '/timezones/{timezone_id}',
    response_model=TimezoneOutSchema,
    summary='Read timezone',
    description='Read timezone.',
    operation_id='system:timezones:read',
)
async def record_read(
        timezone_id: int,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> TimezoneOutSchema:
    """Read timezone"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.system import RefTimezone

    # Build a statement to retrieve the record
    stmt = select(RefTimezone).where(RefTimezone.id == timezone_id)

    # Retrieve the record
    record: RefTimezone | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Timezone {timezone_id} not found')

    # Build the response
    return TimezoneOutSchema.model_validate(record)


@router.put(
    '/timezones/{timezone_id}',
    response_model=TimezoneOutSchema,
    summary='Update timezone',
    description='Update timezone.',
    operation_id='system:timezones:update',
)
async def record_update(
        timezone_id: int,
        timezone: TimezoneInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> TimezoneOutSchema:
    """Update timezone"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.system import RefTimezone

    # Build a statement to retrieve the record
    stmt = select(RefTimezone).where(RefTimezone.id == timezone_id)

    # Retrieve the record
    record: RefTimezone | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Timezone {timezone_id} not found')

    # Update the record
    record.name = timezone.name
    record.offset = timezone.offset
    record.offset_dst = timezone.offset_dst

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return TimezoneOutSchema.model_validate(record)


@router.delete(
    '/timezones/{timezone_id}',
    summary='Delete timezone',
    description='Delete timezone.',
    operation_id='system:timezones:delete',
)
async def record_delete(
        timezone_id: int,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete timezone"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models.db.system import RefTimezone

    # Build a statement to delete the record
    stmt = delete(RefTimezone).where(RefTimezone.id == timezone_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Timezone {timezone_id} not found')
