from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from routers.v1.servers import router


@router.post(
    '/{server_id}/networks',
    summary='List server networks',
    description='List server networks.',
    operation_id='servers:networks:list',
)
async def record_list(
        server_id: UUID,
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """List server networks"""


@router.post(
    '/{server_id}/networks/create',
    summary='Create server network',
    description='Create server network.',
    operation_id='servers:networks:create',
)
async def record_create(
        server_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Create server network"""


@router.get(
    '/{server_id}/networks/{network_id}',
    summary='Read server network',
    description='Read server network.',
    operation_id='servers:networks:read',
)
async def record_read(
        server_id: UUID,
        network_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Read server network"""


@router.put(
    '/{server_id}/networks/{network_id}',
    summary='Update server network',
    description='Update server network.',
    operation_id='servers:networks:update',
)
async def record_update(
        server_id: UUID,
        network_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Update server network"""


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
