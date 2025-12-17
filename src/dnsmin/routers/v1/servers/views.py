from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnsmin.lib.api.dependencies import get_db_session, get_principal
from dnsmin.models.api import ListParamsModel
from dnsmin.models.api.auth import Principal
from dnsmin.models.api.servers.views import ServerViewsSchema, ServerViewOutSchema, ServerViewInSchema
from dnsmin.routers.v1.servers import router


@router.get(
    '/{server_id}/views',
    response_model=list[ServerViewOutSchema],
    summary='List server views',
    description='List server views.',
    operation_id='servers:views:list',
)
async def record_list(
        server_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> list[ServerViewOutSchema]:
    """List server views"""
    from sqlalchemy import select
    from dnsmin.models.db.servers import ServerView

    # Build a statement to retrieve the relevant records
    stmt = select(ServerView).where(ServerView.server_id == server_id)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return [ServerViewOutSchema.model_validate(r) for r in records]


@router.post(
    '/{server_id}/views/search',
    response_model=ServerViewsSchema,
    summary='Search server views',
    description='Search server views.',
    operation_id='servers:views:search',
)
async def record_search(
        server_id: UUID,
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerViewsSchema:
    """Search server views"""
    from sqlalchemy import select, func
    from dnsmin.lib.sql import SqlQueryBuilder
    from dnsmin.models.db.servers import ServerView

    # Build a statement to retrieve the relevant records
    stmt = select(ServerView).where(ServerView.server_id == server_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, ServerView)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return ServerViewsSchema(
        records=[ServerViewOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/{server_id}/views',
    response_model=ServerViewOutSchema,
    summary='Create server view',
    description='Create server view.',
    operation_id='servers:views:create',
)
async def record_create(
        server_id: UUID,
        view: ServerViewInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerViewOutSchema:
    """Create server view"""
    from dnsmin.models.db.servers import ServerView

    # Create the record
    record = ServerView(
        server_id=server_id,
        name=view.name,
    )

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return ServerViewOutSchema.model_validate(record)


@router.get(
    '/{server_id}/views/{view_id}',
    response_model=ServerViewOutSchema,
    summary='Read server view',
    description='Read server view.',
    operation_id='servers:views:read',
)
async def record_read(
        server_id: UUID,
        view_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerViewOutSchema:
    """Read server view"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from dnsmin.models.db.servers import ServerView

    # Build a statement to retrieve the record
    stmt = (select(ServerView)
            .where(ServerView.id == view_id, ServerView.server_id == server_id))

    # Retrieve the record
    record: ServerView | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Server view {view_id} not found')

    # Build the response
    return ServerViewOutSchema.model_validate(record)


@router.put(
    '/{server_id}/views/{view_id}',
    response_model=ServerViewOutSchema,
    summary='Update server view',
    description='Update server view.',
    operation_id='servers:views:update',
)
async def record_update(
        server_id: UUID,
        view_id: UUID,
        view: ServerViewInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ServerViewOutSchema:
    """Update server view"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from dnsmin.models.db.servers import ServerView

    # Build a statement to retrieve the record
    stmt = (select(ServerView)
            .where(ServerView.id == view_id, ServerView.server_id == server_id))

    # Retrieve the record
    record: ServerView | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Server view {view_id} not found')

    # Update the record
    record.name = view.name

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return ServerViewOutSchema.model_validate(record)


@router.delete(
    '/{server_id}/views/{view_id}',
    summary='Delete server view',
    description='Delete server view.',
    operation_id='servers:views:delete',
)
async def record_delete(
        server_id: UUID,
        view_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete server view"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from dnsmin.models.db.servers import ServerView

    # Build a statement to delete the record
    stmt = (delete(ServerView)
            .where(ServerView.id == view_id, ServerView.server_id == server_id))

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Server view {view_id} not found')
