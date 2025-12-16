from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from models.api.auth.sessions import SessionsSchema, SessionOutSchema
from routers.v1.auth import router


@router.get(
    '/sessions',
    response_model=list[SessionOutSchema],
    summary='List Sessions',
    description='Lists sessions.',
    operation_id='auth:sessions:list',
)
async def record_list(
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> list[SessionOutSchema]:
    """List sessions."""
    from sqlalchemy import select
    from models.db.auth import Session

    # Build a statement to retrieve the relevant records
    stmt = select(Session)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Session.tenant_id == principal.tenant_id)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return [SessionOutSchema.model_validate(r) for r in records]


@router.post(
    '/sessions/search',
    response_model=SessionsSchema,
    summary='Search Sessions',
    description='Search sessions.',
    operation_id='auth:sessions:search',
)
async def record_search(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> SessionsSchema:
    """Search sessions."""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.auth import Session

    # Build a statement to retrieve the relevant records
    stmt = select(Session)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Session.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, Session)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return SessionsSchema(
        records=[SessionOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.get(
    '/sessions/{session_id}',
    response_model=SessionOutSchema,
    summary='Read session',
    description='Read session from the current context.',
    operation_id='auth:sessions:read',
)
async def record_read(
        session_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> SessionOutSchema:
    """Read session"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.auth import Session

    # Build a statement to retrieve the record
    stmt = select(Session).where(Session.id == session_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Session.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: Session | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Session {session_id} not found')

    # Build the response
    return SessionOutSchema.model_validate(record)


@router.delete(
    '/sessions/{session_id}',
    summary='Delete session',
    description='Delete session from the current context.',
    operation_id='auth:sessions:delete',
)
async def record_delete(
        session_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete session"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models.db.auth import Session

    # Build a statement to delete the record
    stmt = delete(Session).where(Session.id == session_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(Session.tenant_id == principal.tenant_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Session {session_id} not found')
