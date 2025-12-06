from uuid import UUID

from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from lib.api.dependencies import get_db_session, authorize_oauth_client
from routers.root import router_responses
from routers.v1 import router as v1_router

router = APIRouter(
    prefix='',
    responses=router_responses,
)

# Setup descendent routers
router.include_router(v1_router)


@router.post('/token')
async def token(
        session: AsyncSession = Depends(get_db_session),
        client_id: UUID = Depends(authorize_oauth_client),
        scope: str = Form(None),
) -> dict:
    """Handle OAuth token grants."""
    from lib.settings import SettingsManager
    from lib.settings.definitions import sd
    from lib.api.oauth import create_access_token
    from models.db.auth import RefreshToken

    jwt_payload = {'sub': str(client_id)}

    if isinstance(scope, str):
        jwt_payload['scope'] = scope

    access_token_age = (await SettingsManager.get(session=session, key=sd.auth_access_token_age.key)).value
    refresh_token_age = (await SettingsManager.get(session=session, key=sd.auth_refresh_token_age.key)).value

    # Create the JWT access token
    access_token = create_access_token(payload=jwt_payload, age=access_token_age)

    # Create a refresh token
    refresh = await RefreshToken.create_token(session, refresh_token_age, client_id)

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'expires_in': access_token_age,
        'refresh_token': str(refresh.id),
    }


@router.post('/token/refresh')
async def token_refresh(
        grant_type: str = Form(...),
        client_id: UUID = Form(...),
        client_secret: str = Form(...),
        refresh_token: str = Form(...),
        scope: str = Form(None),
        session: AsyncSession = Depends(get_db_session),
):
    """Handle OAuth token grants."""
    from loguru import logger
    from lib.security import TokenGrantTypeEnum, TokenErrorTypeEnum
    from lib.settings import SettingsManager
    from lib.settings.definitions import sd
    from lib.api.oauth import create_access_token
    from models.db.auth import Client, RefreshToken

    # Retrieve the referenced client
    client = await Client.get_by_id(session, client_id)

    # Validate the client
    if not client or not client.verify_secret(client_secret):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, TokenErrorTypeEnum.invalid_client.value)

    if grant_type != TokenGrantTypeEnum.refresh_token.value:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, TokenErrorTypeEnum.unsupported_grant_type)

    # Retrieve the referenced token
    stored = await RefreshToken.get_by_id(session, refresh_token)

    # Validate the token
    if not stored or not stored.validate(client_id):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, TokenErrorTypeEnum.invalid_token.value)

    # Revoke the previous token
    await RefreshToken.revoke_token(session, stored)

    jwt_payload = {'sub': str(stored.user_id) if stored.user_id else client_id}

    if isinstance(scope, str):
        jwt_payload['scope'] = scope

    # TODO: Handle scope changes
    logger.critical('Token refresh endpoint needs permissions finished!')

    access_token_age = (await SettingsManager.get(session=session, key=sd.auth_access_token_age.key)).value
    refresh_token_age = (await SettingsManager.get(session=session, key=sd.auth_refresh_token_age.key)).value

    # Create the JWT access token
    access_token = create_access_token(payload=jwt_payload, age=access_token_age)

    # Create a refresh token
    refresh = await RefreshToken.create_token(session, refresh_token_age, client_id, stored.user_id)

    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'expires_in': access_token_age,
        'refresh_token': str(refresh.id),
    }
