from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel, Principal
from models.api.auth.clients import ClientOutSchema, ClientsSchema
from routers.v1.auth import router


@router.post(
    '/clients',
    response_model=ClientsSchema,
    summary='List Clients',
    description='Lists authentication clients for the current authentication context.',
    operation_id='auth:clients:list',
)
async def record_list(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> ClientsSchema:
    """List authentication clients."""
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

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return ClientsSchema(
        records=[ClientOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
    )
