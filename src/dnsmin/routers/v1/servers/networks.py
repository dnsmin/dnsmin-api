from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnsmin.lib.api.dependencies import get_db_session, get_principal
from dnsmin.models.api import ListParamsModel
from dnsmin.models.api.auth import Principal
from dnsmin.models.api.servers.networks import ServerNetworksSchema, ServerNetworkOutSchema, ServerNetworkInSchema
from dnsmin.routers.v1.servers import router


@router.get(
    '/{server_id}/networks',
    response_model=list[ServerNetworkOutSchema],
    summary='List server networks',
    description='List server networks.',
    operation_id='servers:networks:list',
)
async def record_list(
        server_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> list[ServerNetworkOutSchema]:
    """List server networks"""
    from sqlalchemy import select
    from dnsmin.models.db.servers import ServerNetwork

    # Build a statement to retrieve the relevant records
    stmt = select(ServerNetwork).where(ServerNetwork.server_id == server_id)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return [ServerNetworkOutSchema.model_validate(r) for r in records]


@router.post(
    '/{server_id}/networks/search',
    response_model=ServerNetworksSchema,
    summary='Search server networks',
    description='Search server networks.',
    operation_id='servers:networks:search',
)
async def record_search(
        server_id: UUID,
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerNetworksSchema:
    """Search server networks"""
    from sqlalchemy import select, func
    from dnsmin.lib.sql import SqlQueryBuilder
    from dnsmin.models.db.servers import ServerNetwork

    # Build a statement to retrieve the relevant records
    stmt = select(ServerNetwork).where(ServerNetwork.server_id == server_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, ServerNetwork)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return ServerNetworksSchema(
        records=[ServerNetworkOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/{server_id}/networks',
    response_model=ServerNetworkOutSchema,
    summary='Create server network',
    description='Create server network.',
    operation_id='servers:networks:create',
)
async def record_create(
        server_id: UUID,
        network: ServerNetworkInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerNetworkOutSchema:
    """Create server network"""
    from dnsmin.models.db.servers import ServerNetwork

    # Create the record
    record = ServerNetwork(
        server_id=server_id,
        view_id=network.view_id,
        network=network.network,
    )

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return ServerNetworkOutSchema.model_validate(record)


@router.get(
    '/{server_id}/networks/{network_id}',
    response_model=ServerNetworkOutSchema,
    summary='Read server network',
    description='Read server network.',
    operation_id='servers:networks:read',
)
async def record_read(
        server_id: UUID,
        network_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerNetworkOutSchema:
    """Read server network"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from dnsmin.models.db.servers import ServerNetwork

    # Build a statement to retrieve the record
    stmt = (select(ServerNetwork)
            .where(ServerNetwork.id == network_id, ServerNetwork.server_id == server_id))

    # Retrieve the record
    record: ServerNetwork | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Server network {network_id} not found')

    # Build the response
    return ServerNetworkOutSchema.model_validate(record)


@router.put(
    '/{server_id}/networks/{network_id}',
    response_model=ServerNetworkOutSchema,
    summary='Update server network',
    description='Update server network.',
    operation_id='servers:networks:update',
)
async def record_update(
        server_id: UUID,
        network_id: UUID,
        network: ServerNetworkInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerNetworkOutSchema:
    """Update server network"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from dnsmin.models.db.servers import ServerNetwork

    # Build a statement to retrieve the record
    stmt = (select(ServerNetwork)
            .where(ServerNetwork.id == network_id, ServerNetwork.server_id == server_id))

    # Retrieve the record
    record: ServerNetwork | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Server network {network_id} not found')

    # Update the record
    record.view_id = network.view_id
    record.network = network.network

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return ServerNetworkOutSchema.model_validate(record)


@router.delete(
    '/{server_id}/networks/{network_id}',
    summary='Delete server network',
    description='Delete server network.',
    operation_id='servers:networks:delete',
)
async def record_delete(
        server_id: UUID,
        network_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete server network"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from dnsmin.models.db.servers import ServerNetwork

    # Build a statement to delete the record
    stmt = (delete(ServerNetwork)
            .where(ServerNetwork.id == network_id, ServerNetwork.server_id == server_id))

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Server network {network_id} not found')
