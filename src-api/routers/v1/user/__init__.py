from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.requests import Request
from fastapi.responses import Response, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_session_user
from models.api.auth.users import UserOutSchema
from routers.root import router_responses

router = APIRouter(
    prefix='/user',
    tags=['user'],
    responses=router_responses,
)


@router.get(
    '/session',
    response_model=Optional[UserOutSchema],
    summary='Current Session Data',
    description='Provides the session data for the currently authenticated user (if any).',
)
async def session(
        user: UserOutSchema = Depends(get_session_user),
) -> Optional[UserOutSchema]:
    return user


@router.post('/login', response_model=UserOutSchema)
async def login(
        request: Request,
        response: Response,
        session: AsyncSession = Depends(get_db_session),
        username: str = Form(...),
        password: str = Form(...),
) -> UserOutSchema:
    from lib.tenants import TenantManager
    from lib.settings import SettingsManager
    from lib.settings.definitions import sd
    from models.db.auth import User, Session
    from models.enums import UserStatusEnum

    cookie_name = (await SettingsManager.get(session=session, key=sd.auth_session_cookie_name.key)).value
    cookie_age = (await SettingsManager.get(session=session, key=sd.auth_session_expiration_age.key)).value

    # Delete any existing session cookie
    response.delete_cookie(
        key=cookie_name,
        path='/',
        httponly=True,
        samesite='strict',
        secure=True,
    )

    if not username or isinstance(username, str) and not len(username.strip()):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'No username provided.')

    if not password or isinstance(password, str) and not len(password.strip()):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'No password provided.')

    # Identify the tenant ID (if any) based on request host
    tenant_id = await TenantManager.get_tenant_id_by_fqdn(session, request.headers.get('host'))

    # Attempt to retrieve a user from the database based on the given username
    db_user = await User.get_by_username(session, username, tenant_id)

    if not db_user or not db_user.verify_password(password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, 'Invalid credentials provided.')

    # Ensure that the user has an appropriate status
    if db_user.status != UserStatusEnum.active:
        reason = 'This user is not active.'

        if db_user.status == UserStatusEnum.pending:
            reason = 'This user has not yet been invited.'

        if db_user.status == UserStatusEnum.invited:
            reason = 'This user has not yet been confirmed.'

        if db_user.status == UserStatusEnum.suspended:
            reason = 'This user has been suspended.'

        if db_user.status == UserStatusEnum.disabled:
            reason = 'This user has been disabled.'

        raise HTTPException(status.HTTP_401_UNAUTHORIZED, reason)

    # Update the user's last authentication timestamp
    await User.mark_authentication(session, db_user)

    # Create the user schema from the database user
    user = UserOutSchema.model_validate(db_user)

    # Create a new auth session for the user
    auth_session = await Session.create_session(session, user, request.client.host)

    response.set_cookie(
        key=cookie_name,
        value=auth_session.token,
        max_age=cookie_age,
        path='/',
        httponly=True,
        samesite='strict',
        secure=True,
    )

    return user


@router.get('/logout')
async def logout(
        request: Request,
        response: Response,
        session: AsyncSession = Depends(get_db_session),
) -> JSONResponse:
    from lib.settings import SettingsManager
    from lib.settings.definitions import sd
    from models.db.auth import Session

    cookie_name = (await SettingsManager.get(session=session, key=sd.auth_session_cookie_name.key)).value

    session_token = request.cookies.get(cookie_name)

    if session_token:
        db_session = await Session.get_by_token(session, session_token, request.client.host)
        if db_session:
            await Session.destroy_session(session, db_session.id)

    # Delete any existing session cookie
    response.delete_cookie(
        key=cookie_name,
        path='/',
        httponly=True,
        samesite='strict',
        secure=True,
    )

    return JSONResponse({'message': 'Successfully logged out.'})
