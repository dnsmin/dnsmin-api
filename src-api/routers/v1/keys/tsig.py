from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from models.api.keys.tsig import TSIGKeysSchema, TSIGKeyOutSchema, TSIGKeyInSchema
from routers.v1.auth import router


@router.post(
    '/tsig',
    response_model=TSIGKeysSchema,
    summary='List TSIG Keys',
    description='Lists TSIG keys for the current authentication context.',
    operation_id='keys:tsig:list',
)
async def record_list(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> TSIGKeysSchema:
    """List TSIG keys."""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.keys import TsigKey

    # Build a statement to retrieve the relevant records
    stmt = select(TsigKey)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(TsigKey.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, TsigKey)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return TSIGKeysSchema(
        records=[TSIGKeyOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/tsig/create',
    response_model=TSIGKeyOutSchema,
    summary='Create TSIG key',
    description='Create TSIG key for the current authentication context.',
    operation_id='keys:tsig:create',
)
async def record_create(
        tsig_key: TSIGKeyInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> TSIGKeyOutSchema:
    """Create TSIG key"""
    from models.db.keys import TsigKey

    # Create the record
    record = TsigKey(
        algorithm=tsig_key.algorithm,
        key=tsig_key.key,
    )

    # Enforce tenancy
    if principal.tenant_id:
        record.tenant_id = principal.tenant_id
    else:
        record.tenant_id = tsig_key.tenant_id

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return TSIGKeyOutSchema.model_validate(record)


@router.get(
    '/tsig/{tsig_key_id}',
    response_model=TSIGKeyOutSchema,
    summary='Read TSIG key',
    description='Read TSIG key from the current authentication context.',
    operation_id='keys:tsig:read',
)
async def record_read(
        tsig_key_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> TSIGKeyOutSchema:
    """Read TSIG key"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.keys import TsigKey

    # Build a statement to retrieve the record
    stmt = select(TsigKey).where(TsigKey.id == tsig_key_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(TsigKey.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: TsigKey | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'TSIG key {tsig_key_id} not found')

    # Build the response
    return TSIGKeyOutSchema.model_validate(record)


@router.put(
    '/tsig/{tsig_key_id}',
    response_model=TSIGKeyOutSchema,
    summary='Update TSIG key',
    description='Update TSIG key in the current authentication context.',
    operation_id='keys:tsig:update',
)
async def record_update(
        tsig_key_id: UUID,
        tsig_key: TSIGKeyInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> TSIGKeyOutSchema:
    """Update TSIG key"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.keys import TsigKey

    # Build a statement to retrieve the record
    stmt = select(TsigKey).where(TsigKey.id == tsig_key_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(TsigKey.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: TsigKey | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'TSIG key {tsig_key_id} not found')

    # Update the record
    record.algorithm = tsig_key.algorithm
    record.key = tsig_key.key

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return TSIGKeyOutSchema.model_validate(record)


@router.delete(
    '/tsig/{tsig_key_id}',
    summary='Delete TSIG key',
    description='Delete TSIG key from the current authentication context.',
    operation_id='keys:tsig:delete',
)
async def record_delete(
        tsig_key_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete TSIG key"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models.db.keys import TsigKey

    # Build a statement to delete the record
    stmt = delete(TsigKey).where(TsigKey.id == tsig_key_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(TsigKey.tenant_id == principal.tenant_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'TSIG key {tsig_key_id} not found')
