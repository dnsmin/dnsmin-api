from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from models.api.servers.servers import ServersSchema, ServerOutSchema, ServerInSchema
from routers.v1.servers import router


@router.post(
    '',
    response_model=ServersSchema,
    summary='List servers',
    description='List servers.',
    operation_id='servers:list',
)
async def record_list(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServersSchema:
    """List servers"""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.servers import Server

    # Build a statement to retrieve the relevant records
    stmt = select(Server)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Server.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, Server)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return ServersSchema(
        records=[ServerOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/create',
    response_model=ServerOutSchema,
    summary='Create server',
    description='Create server.',
    operation_id='servers:create',
)
async def record_create(
        server: ServerInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerOutSchema:
    """Create server"""
    from models.db.servers import Server

    # Create the record
    record = Server(
        type=server.type,
        version=server.version,
        hostname=server.hostname,
        api_url=server.api_url,
        api_key=server.api_key,
        shared=server.shared,
    )

    # Enforce tenancy
    if principal.tenant_id:
        record.tenant_id = principal.tenant_id
    else:
        record.tenant_id = server.tenant_id

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return ServerOutSchema.model_validate(record)


@router.get(
    '/{server_id}',
    response_model=ServerOutSchema,
    summary='Read server',
    description='Read server.',
    operation_id='servers:read',
)
async def record_read(
        server_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerOutSchema:
    """Read server"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.servers import Server

    # Build a statement to retrieve the record
    stmt = select(Server).where(Server.id == server_id)

    # Retrieve the record
    record: Server | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Server {server_id} not found')

    # Build the response
    return ServerOutSchema.model_validate(record)


@router.put(
    '/{server_id}',
    response_model=ServerOutSchema,
    summary='Update server',
    description='Update server.',
    operation_id='servers:update',
)
async def record_update(
        server_id: UUID,
        server: ServerInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerOutSchema:
    """Update server"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.servers import Server

    # Build a statement to retrieve the record
    stmt = select(Server).where(Server.id == server_id)

    # Retrieve the record
    record: Server | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Server {server_id} not found')

    # Update the record
    record.type = server.type
    record.version = server.version
    record.hostname = server.hostname
    record.api_url = server.api_url
    record.api_key = server.api_key
    record.shared = server.shared

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return ServerOutSchema.model_validate(record)


@router.delete(
    '/{server_id}',
    summary='Delete server',
    description='Delete server.',
    operation_id='servers:delete',
)
async def record_delete(
        server_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete server"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models.db.servers import Server

    # Build a statement to delete the record
    stmt = delete(Server).where(Server.id == server_id)
    
    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Server {server_id} not found')
