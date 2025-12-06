from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from routers.v1.servers import router


@router.post(
    '',
    summary='List servers',
    description='List servers.',
    operation_id='servers:list',
)
async def record_list(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """List servers"""


@router.post(
    '/create',
    summary='Create server',
    description='Create server.',
    operation_id='servers:create',
)
async def record_create(
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Create server"""


@router.get(
    '/{server_id}',
    summary='Read server',
    description='Read server.',
    operation_id='servers:read',
)
async def record_read(
        server_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Read server"""


@router.patch(
    '/{server_id}',
    summary='Update server',
    description='Update server.',
    operation_id='servers:update',
)
async def record_update(
        server_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Update server"""


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
