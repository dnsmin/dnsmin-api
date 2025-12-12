from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from models.api.servers.tsig_keys import ServerTSIGKeysSchema, ServerTSIGKeyOutSchema, ServerTSIGKeyInSchema
from routers.v1.servers import router


@router.post(
    '/{server_id}/tsig-keys',
    response_model=ServerTSIGKeysSchema,
    summary='List server TSIG keys',
    description='List server TSIG keys.',
    operation_id='servers:tsig_keys:list',
)
async def record_list(
        server_id: UUID,
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerTSIGKeysSchema:
    """List server TSIG keys."""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.servers import ServerTsigKey

    # Build a statement to retrieve the relevant records
    stmt = select(ServerTsigKey).where(ServerTsigKey.server_id == server_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(ServerTsigKey.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, ServerTsigKey)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return ServerTSIGKeysSchema(
        records=[ServerTSIGKeyOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/{server_id}/tsig-keys/create',
    response_model=ServerTSIGKeyOutSchema,
    summary='Create server TSIG key',
    description='Create server TSIG key.',
    operation_id='servers:tsig_keys:create',
)
async def record_create(
        server_id: UUID,
        tsig_key: ServerTSIGKeyInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerTSIGKeyOutSchema:
    """Create server TSIG key"""
    from models.db.servers import ServerTsigKey

    # Create the record
    record = ServerTsigKey(
        server_id=server_id,
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
    return ServerTSIGKeyOutSchema.model_validate(record)


@router.get(
    '/{server_id}/tsig-keys/{tsig_key_id}',
    response_model=ServerTSIGKeyOutSchema,
    summary='Read server TSIG key',
    description='Read server TSIG key.',
    operation_id='servers:tsig_keys:read',
)
async def record_read(
        server_id: UUID,
        tsig_key_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerTSIGKeyOutSchema:
    """Read server TSIG key"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.servers import ServerTsigKey

    # Build a statement to retrieve the record
    stmt = select(ServerTsigKey).where(ServerTsigKey.id == tsig_key_id, ServerTsigKey.server_id == server_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(ServerTsigKey.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: ServerTsigKey | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Server server TSIG key {tsig_key_id} not found')

    # Build the response
    return ServerTSIGKeyOutSchema.model_validate(record)


@router.put(
    '/{server_id}/tsig-keys/{tsig_key_id}',
    response_model=ServerTSIGKeyOutSchema,
    summary='Update server TSIG key',
    description='Update server TSIG key.',
    operation_id='servers:tsig_keys:update',
)
async def record_update(
        server_id: UUID,
        tsig_key_id: UUID,
        tsig_key: ServerTSIGKeyInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerTSIGKeyOutSchema:
    """Update server TSIG key"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.servers import ServerTsigKey

    # Build a statement to retrieve the record
    stmt = (select(ServerTsigKey)
            .where(ServerTsigKey.id == tsig_key_id, ServerTsigKey.server_id == server_id))

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(ServerTsigKey.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: ServerTsigKey | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Server server TSIG key {tsig_key_id} not found')

    # Update the record
    record.algorithm = tsig_key.algorithm
    record.key = tsig_key.key

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return ServerTSIGKeyOutSchema.model_validate(record)


@router.delete(
    '/{server_id}/tsig-keys/{tsig_key_id}',
    summary='Delete server TSIG key',
    description='Delete server TSIG key.',
    operation_id='servers:tsig_keys:delete',
)
async def record_delete(
        server_id: UUID,
        tsig_key_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete server TSIG key"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models.db.servers import ServerTsigKey

    # Build a statement to delete the record
    stmt = (delete(ServerTsigKey)
            .where(ServerTsigKey.id == tsig_key_id, ServerTsigKey.server_id == server_id))

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(ServerTsigKey.tenant_id == principal.tenant_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Server server TSIG key {tsig_key_id} not found')
