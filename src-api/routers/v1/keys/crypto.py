from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from models.api.keys.crypto import CryptoKeysSchema, CryptoKeyOutSchema, CryptoKeyInSchema
from routers.v1.keys import router


@router.post(
    '/crypto',
    response_model=CryptoKeysSchema,
    summary='List Crypto Keys',
    description='Lists crypto keys for the current authentication context.',
    operation_id='keys:crypto:list',
)
async def record_list(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> CryptoKeysSchema:
    """List crypto keys."""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.keys import CryptoKey

    # Build a statement to retrieve the relevant records
    stmt = select(CryptoKey)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(CryptoKey.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, CryptoKey)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return CryptoKeysSchema(
        records=[CryptoKeyOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/crypto/create',
    response_model=CryptoKeyOutSchema,
    summary='Create crypto key',
    description='Create crypto key for the current authentication context.',
    operation_id='keys:crypto:create',
)
async def record_create(
        crypto_key: CryptoKeyInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> CryptoKeyOutSchema:
    """Create crypto key"""
    from models.db.keys import CryptoKey

    # Create the record
    record = CryptoKey(
        type=crypto_key.type,
        active=crypto_key.active,
        published=crypto_key.published,
        dns_key=crypto_key.dns_key,
        ds=crypto_key.ds,
        cds=crypto_key.cds,
        private_key=crypto_key.private_key,
        algorithm=crypto_key.algorithm,
        bits=crypto_key.bits,
    )

    # Enforce tenancy
    if principal.tenant_id:
        record.tenant_id = principal.tenant_id
    else:
        record.tenant_id = crypto_key.tenant_id

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return CryptoKeyOutSchema.model_validate(record)


@router.get(
    '/crypto/{crypto_key_id}',
    response_model=CryptoKeyOutSchema,
    summary='Read crypto key',
    description='Read crypto key from the current authentication context.',
    operation_id='keys:crypto:read',
)
async def record_read(
        crypto_key_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> CryptoKeyOutSchema:
    """Read crypto key"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.keys import CryptoKey

    # Build a statement to retrieve the record
    stmt = select(CryptoKey).where(CryptoKey.id == crypto_key_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(CryptoKey.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: CryptoKey | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Crypto key {crypto_key_id} not found')

    # Build the response
    return CryptoKeyOutSchema.model_validate(record)


@router.put(
    '/crypto/{crypto_key_id}',
    response_model=CryptoKeyOutSchema,
    summary='Update crypto key',
    description='Update crypto key in the current authentication context.',
    operation_id='keys:crypto:update',
)
async def record_update(
        crypto_key_id: UUID,
        crypto_key: CryptoKeyInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> CryptoKeyOutSchema:
    """Update crypto key"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.keys import CryptoKey

    # Build a statement to retrieve the record
    stmt = select(CryptoKey).where(CryptoKey.id == crypto_key_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(CryptoKey.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: CryptoKey | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Crypto key {crypto_key_id} not found')

    # Update the record
    record.type = crypto_key.type
    record.active = crypto_key.active
    record.published = crypto_key.published
    record.dns_key = crypto_key.dns_key
    record.ds = crypto_key.ds
    record.cds = crypto_key.cds
    record.private_key = crypto_key.private_key
    record.algorithm = crypto_key.algorithm
    record.bits = crypto_key.bits

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return CryptoKeyOutSchema.model_validate(record)


@router.delete(
    '/crypto/{crypto_key_id}',
    summary='Delete crypto key',
    description='Delete crypto key from the current authentication context.',
    operation_id='keys:crypto:delete',
)
async def record_delete(
        crypto_key_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete crypto key"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models.db.keys import CryptoKey

    # Build a statement to delete the record
    stmt = delete(CryptoKey).where(CryptoKey.id == crypto_key_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(CryptoKey.tenant_id == principal.tenant_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Crypto key {crypto_key_id} not found')
