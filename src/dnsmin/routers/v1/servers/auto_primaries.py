from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnsmin.lib.api.dependencies import get_db_session, get_principal
from dnsmin.models.api import ListParamsModel
from dnsmin.models.api.auth import Principal
from dnsmin.models.api.servers.autoprimaries import (ServerAutoPrimariesSchema, ServerAutoPrimaryOutSchema,
                                              ServerAutoPrimaryInSchema)
from dnsmin.routers.v1.servers import router


@router.get(
    '/{server_id}/auto-primaries',
    response_model=list[ServerAutoPrimaryOutSchema],
    summary='List server auto-primaries',
    description='List server auto-primaries.',
    operation_id='servers:auto_primaries:list',
)
async def record_list(
        server_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> list[ServerAutoPrimaryOutSchema]:
    """List server auto-primaries"""
    from sqlalchemy import select
    from dnsmin.models.db.servers import ServerAutoPrimary

    # Build a statement to retrieve the relevant records
    stmt = select(ServerAutoPrimary).where(ServerAutoPrimary.server_id == server_id)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return [ServerAutoPrimaryOutSchema.model_validate(r) for r in records]


@router.post(
    '/{server_id}/auto-primaries/search',
    response_model=ServerAutoPrimariesSchema,
    summary='Search server auto-primaries',
    description='Search server auto-primaries.',
    operation_id='servers:auto_primaries:search',
)
async def record_search(
        server_id: UUID,
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerAutoPrimariesSchema:
    """Search server auto-primaries"""
    from sqlalchemy import select, func
    from dnsmin.lib.sql import SqlQueryBuilder
    from dnsmin.models.db.servers import ServerAutoPrimary

    # Build a statement to retrieve the relevant records
    stmt = select(ServerAutoPrimary).where(ServerAutoPrimary.server_id == server_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, ServerAutoPrimary)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return ServerAutoPrimariesSchema(
        records=[ServerAutoPrimaryOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/{server_id}/auto-primaries',
    response_model=ServerAutoPrimaryOutSchema,
    summary='Create server auto-primary',
    description='Create server auto-primary.',
    operation_id='servers:auto_primaries:create',
)
async def record_create(
        server_id: UUID,
        autoprimary: ServerAutoPrimaryInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerAutoPrimaryOutSchema:
    """Create server auto-primary"""
    from dnsmin.models.db.servers import ServerAutoPrimary

    # Create the record
    record = ServerAutoPrimary(
        server_id=server_id,
        ip=autoprimary.ip,
        nameserver=autoprimary.nameserver,
        account=autoprimary.account,
    )

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return ServerAutoPrimaryOutSchema.model_validate(record)


@router.get(
    '/{server_id}/auto-primaries/{auto_primary_id}',
    response_model=ServerAutoPrimaryOutSchema,
    summary='Read server auto-primary',
    description='Read server auto-primary.',
    operation_id='servers:auto_primaries:read',
)
async def record_read(
        server_id: UUID,
        auto_primary_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerAutoPrimaryOutSchema:
    """Read server auto-primary"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from dnsmin.models.db.servers import ServerAutoPrimary

    # Build a statement to retrieve the record
    stmt = (select(ServerAutoPrimary)
            .where(ServerAutoPrimary.id == auto_primary_id, ServerAutoPrimary.server_id == server_id))

    # Retrieve the record
    record: ServerAutoPrimary | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Server auto-primary {auto_primary_id} not found')

    # Build the response
    return ServerAutoPrimaryOutSchema.model_validate(record)


@router.put(
    '/{server_id}/auto-primaries/{auto_primary_id}',
    response_model=ServerAutoPrimaryOutSchema,
    summary='Update server auto-primary',
    description='Update server auto-primary.',
    operation_id='servers:auto_primaries:update',
)
async def record_update(
        server_id: UUID,
        auto_primary_id: UUID,
        autoprimary: ServerAutoPrimaryInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerAutoPrimaryOutSchema:
    """Update server auto-primary"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from dnsmin.models.db.servers import ServerAutoPrimary

    # Build a statement to retrieve the record
    stmt = (select(ServerAutoPrimary)
            .where(ServerAutoPrimary.id == auto_primary_id, ServerAutoPrimary.server_id == server_id))

    # Retrieve the record
    record: ServerAutoPrimary | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Server auto-primary {server_id} not found')

    # Update the record
    record.ip = autoprimary.ip
    record.nameserver = autoprimary.nameserver
    record.account = autoprimary.account

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return ServerAutoPrimaryOutSchema.model_validate(record)


@router.delete(
    '/{server_id}/auto-primaries/{auto_primary_id}',
    summary='Delete server auto-primary',
    description='Delete server auto-primary.',
    operation_id='servers:auto_primaries:delete',
)
async def record_delete(
        server_id: UUID,
        auto_primary_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete server auto-primary"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from dnsmin.models.db.servers import ServerAutoPrimary

    # Build a statement to delete the record
    stmt = (delete(ServerAutoPrimary)
            .where(ServerAutoPrimary.id == auto_primary_id, ServerAutoPrimary.server_id == server_id))

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Server auto-primary {server_id} not found')
