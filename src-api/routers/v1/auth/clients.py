from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from models.api.auth.clients import ClientsSchema, ClientOutSchema, ClientInSchema
from routers.v1.auth import router


@router.get(
    '/clients',
    response_model=list[ClientOutSchema],
    summary='List Clients',
    description='Lists clients.',
    operation_id='auth:clients:list',
)
async def record_list(
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> list[ClientOutSchema]:
    """List clients."""
    from sqlalchemy import select, func
    from models.db.auth import Client

    # Build a statement to retrieve the relevant records
    stmt = select(Client)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Client.tenant_id == principal.tenant_id)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return [ClientOutSchema.model_validate(r) for r in records]


@router.post(
    '/clients/search',
    response_model=ClientsSchema,
    summary='Search Clients',
    description='Search clients.',
    operation_id='auth:clients:search',
)
async def record_search(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ClientsSchema:
    """Search clients."""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.auth import Client

    # Build a statement to retrieve the relevant records
    stmt = select(Client)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Client.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, Client)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return ClientsSchema(
        records=[ClientOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/clients',
    response_model=ClientOutSchema,
    summary='Create client',
    description='Create client.',
    operation_id='auth:clients:create',
)
async def record_create(
        client: ClientInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ClientOutSchema:
    """Create client"""
    from models.db.auth import Client

    # Create the record
    record = Client(
        user_id=client.user_id,
        name=client.name,
        redirect_uri=client.redirect_uri,
        scopes=client.scopes,
        enabled=client.enabled,
    )
    record.secret = client.secret

    # Enforce tenancy
    if principal.tenant_id:
        record.tenant_id = principal.tenant_id
    else:
        record.tenant_id = client.tenant_id

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return ClientOutSchema.model_validate(record)


@router.get(
    '/clients/{client_id}',
    response_model=ClientOutSchema,
    summary='Read client',
    description='Read client.',
    operation_id='auth:clients:read',
)
async def record_read(
        client_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ClientOutSchema:
    """Read client"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.auth import Client

    # Build a statement to retrieve the record
    stmt = select(Client).where(Client.id == client_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Client.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: Client | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Client {client_id} not found')

    # Build the response
    return ClientOutSchema.model_validate(record)


@router.put(
    '/clients/{client_id}',
    response_model=ClientOutSchema,
    summary='Update client',
    description='Update client.',
    operation_id='auth:clients:update',
)
async def record_update(
        client_id: UUID,
        client: ClientInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ClientOutSchema:
    """Update client"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.auth import Client

    # Build a statement to retrieve the record
    stmt = select(Client).where(Client.id == client_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Client.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: Client | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Client {client_id} not found')

    # Update the record
    record.user_id = client.user_id
    record.name = client.name
    record.redirect_uri = client.redirect_uri
    record.scopes = client.scopes
    record.enabled = client.enabled

    if isinstance(client.secret, str):
        record.secret = client.secret

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return ClientOutSchema.model_validate(record)


@router.delete(
    '/clients/{client_id}',
    summary='Delete client',
    description='Delete client.',
    operation_id='auth:clients:delete',
)
async def record_delete(
        client_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete client"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models.db.auth import Client

    # Build a statement to delete the record
    stmt = delete(Client).where(Client.id == client_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Client.tenant_id == principal.tenant_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Client {client_id} not found')
