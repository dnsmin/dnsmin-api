from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from routers.v1.servers import router


@router.get(
    '/{server_id}/views',
    summary='List server views',
    description='List server views.',
    operation_id='servers:views:list',
)
async def record_list(
        server_id: UUID,
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """List server views"""


@router.post(
    '/{server_id}/views/create',
    summary='Create server view',
    description='Create server view.',
    operation_id='servers:views:create',
)
async def record_create(
        server_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Create server view"""


@router.get(
    '/{server_id}/views/{view_id}',
    summary='Read server view',
    description='Read server view.',
    operation_id='servers:views:read',
)
async def record_read(
        server_id: UUID,
        view_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Read server view"""


@router.patch(
    '/{server_id}/views/{view_id}',
    summary='Update server view',
    description='Update server view.',
    operation_id='servers:views:update',
)
async def record_update(
        server_id: UUID,
        view_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Update server view"""


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
