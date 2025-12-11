from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from models.api.servers.autoprimaries import (ServerAutoPrimariesSchema, ServerAutoPrimaryOutSchema,
                                              ServerAutoPrimaryInSchema)
from routers.v1.servers import router


@router.post(
    '/{server_id}/auto-primaries',
    response_model=ServerAutoPrimariesSchema,
    summary='List server auto-primaries',
    description='List server auto-primaries.',
    operation_id='servers:auto_primaries:list',
)
async def record_list(
        server_id: UUID,
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """List server auto-primaries"""


@router.post(
    '/{server_id}/auto-primaries/create',
    summary='Create server auto-primary',
    description='Create server auto-primary.',
    operation_id='servers:auto_primaries:create',
)
async def record_create(
        server_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Create server auto-primary"""


@router.get(
    '/{server_id}/auto-primaries/{auto_primary_id}',
    summary='Read server auto-primary',
    description='Read server auto-primary.',
    operation_id='servers:auto_primaries:read',
)
async def record_read(
        server_id: UUID,
        auto_primary_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Read server auto-primary"""


@router.put(
    '/{server_id}/auto-primaries/{auto_primary_id}',
    summary='Update server auto-primary',
    description='Update server auto-primary.',
    operation_id='servers:auto_primaries:update',
)
async def record_update(
        server_id: UUID,
        auto_primary_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Update server auto-primary"""


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
