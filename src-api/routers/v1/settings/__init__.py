from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api.auth import Principal
from models.api.settings import SettingInSchema, SettingOutSchema, SettingsOutSchema
from routers.root import router_responses

router = APIRouter(
    prefix='/settings',
    tags=['settings'],
    responses=router_responses,
)


@router.post(
    '',
    response_model=SettingsOutSchema,
    summary='List settings',
    description='List settings.',
    operation_id='settings:list',
)
async def record_list(
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """List settings"""


@router.post(
    '/create',
    response_model=SettingOutSchema,
    summary='Create setting override',
    description='Create setting override.',
    operation_id='settings:create',
)
async def record_create(
        setting: SettingInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Create setting override"""


@router.get(
    '/{key}',
    response_model=SettingOutSchema,
    summary='Read setting override',
    description='Read setting override.',
    operation_id='settings:read',
)
async def record_read(
        key: str,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Read setting override"""


@router.put(
    '/{key}',
    response_model=SettingOutSchema,
    summary='Update setting override',
    description='Update setting override.',
    operation_id='settings:update',
)
async def record_update(
        key: str,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Update setting override"""


@router.delete(
    '/{key}',
    summary='Delete setting override',
    description='Delete setting override.',
    operation_id='settings:delete',
)
async def record_delete(
        key: str,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete setting override"""
