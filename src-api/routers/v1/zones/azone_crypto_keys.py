from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from models.api.zones.azone_crypto_keys import AZoneCryptoKeyInSchema, AZoneCryptoKeyOutSchema, AZoneCryptoKeysSchema
from routers.v1.zones import router


@router.post(
    '/authoritative/{zone_id}/crypto-keys',
    response_model=AZoneCryptoKeysSchema,
    summary='List authoritative zone crypto keys',
    description='List authoritative zone crypto keys.',
    operation_id='zones:authoritative:crypto_keys:list',
)
async def record_list(
        zone_id: UUID,
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneCryptoKeysSchema:
    """List authoritative zone crypto keys."""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models import AZoneCryptoKey

    # Build a statement to retrieve the relevant records
    stmt = select(AZoneCryptoKey).where(AZoneCryptoKey.zone_id == zone_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(AZoneCryptoKey.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, AZoneCryptoKey)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return AZoneCryptoKeysSchema(
        records=[AZoneCryptoKeyOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/authoritative/{zone_id}/crypto-keys/create',
    response_model=AZoneCryptoKeyOutSchema,
    summary='Create authoritative zone crypto key',
    description='Create authoritative zone crypto key.',
    operation_id='zones:authoritative:crypto_keys:create',
)
async def record_create(
        zone_id: UUID,
        crypto_key: AZoneCryptoKeyInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneCryptoKeyOutSchema:
    """Create authoritative zone crypto key"""
    from models import AZoneCryptoKey

    # Create the record
    record = AZoneCryptoKey(
        zone_id=zone_id,
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
    return AZoneCryptoKeyOutSchema.model_validate(record)


@router.get(
    '/authoritative/{zone_id}/crypto-keys/{crypto_key_id}',
    response_model=AZoneCryptoKeyOutSchema,
    summary='Read authoritative zone crypto key',
    description='Read authoritative zone crypto key.',
    operation_id='zones:authoritative:crypto_keys:read',
)
async def record_read(
        zone_id: UUID,
        crypto_key_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneCryptoKeyOutSchema:
    """Read authoritative zone crypto key"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models import AZoneCryptoKey

    # Build a statement to retrieve the record
    stmt = select(AZoneCryptoKey).where(AZoneCryptoKey.id == crypto_key_id, AZoneCryptoKey.zone_id == zone_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(AZoneCryptoKey.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: AZoneCryptoKey | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Authoritative zone crypto key {crypto_key_id} not found')

    # Build the response
    return AZoneCryptoKeyOutSchema.model_validate(record)


@router.put(
    '/authoritative/{zone_id}/crypto-keys/{crypto_key_id}',
    response_model=AZoneCryptoKeyOutSchema,
    summary='Update authoritative zone crypto key',
    description='Update authoritative zone crypto key.',
    operation_id='zones:authoritative:crypto_keys:update',
)
async def record_update(
        zone_id: UUID,
        crypto_key_id: UUID,
        crypto_key: AZoneCryptoKeyInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneCryptoKeyOutSchema:
    """Update authoritative zone crypto key"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models import AZoneCryptoKey

    # Build a statement to retrieve the record
    stmt = (select(AZoneCryptoKey)
            .where(AZoneCryptoKey.id == crypto_key_id, AZoneCryptoKey.zone_id == zone_id))

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(AZoneCryptoKey.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: AZoneCryptoKey | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Authoritative zone crypto key {crypto_key_id} not found')

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
    return AZoneCryptoKeyOutSchema.model_validate(record)


@router.delete(
    '/authoritative/{zone_id}/crypto-keys/{crypto_key_id}',
    summary='Delete authoritative zone crypto key',
    description='Delete authoritative zone crypto key.',
    operation_id='zones:authoritative:crypto_keys:delete',
)
async def record_delete(
        zone_id: UUID,
        crypto_key_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete authoritative zone crypto key"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models import AZoneCryptoKey

    # Build a statement to delete the record
    stmt = (delete(AZoneCryptoKey)
            .where(AZoneCryptoKey.id == crypto_key_id, AZoneCryptoKey.zone_id == zone_id))

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(AZoneCryptoKey.tenant_id == principal.tenant_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Authoritative zone crypto key {crypto_key_id} not found')
