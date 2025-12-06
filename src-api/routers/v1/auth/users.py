from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel, Principal
from models.api.auth.users import UsersSchema, UserOutSchema, UserInSchema
from routers.v1.auth import router


@router.post(
    '/users',
    response_model=UsersSchema,
    summary='List Users',
    description='Lists authentication policies for the current authentication context.',
    operation_id='auth:users:list',
)
async def record_list(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> UsersSchema:
    """List authentication users."""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.auth import User

    # Build a statement to retrieve the relevant records
    stmt = select(User)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(User.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, User)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return UsersSchema(
        records=[UserOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
    )


@router.post(
    '/users/create',
    response_model=UserOutSchema,
    summary='Create authentication user',
    description='Create authentication user for the current authentication context.',
    operation_id='auth:users:create',
)
async def record_create(
        user: UserInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> UserOutSchema:
    """Create authentication user"""
    from fastapi import HTTPException, status
    from models.db.auth import User

    # Create the record
    record = User(
        username=user.username,
        status=user.status,
    )
    record.password = user.password

    # Enforce tenancy
    if principal.tenant_id:
        record.tenant_id = principal.tenant_id
    else:
        record.tenant_id = user.tenant_id

    # Check that the username is available
    if not await User.check_username_available(session, record.username, record.tenant_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username is already taken.')

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return UserOutSchema.model_validate(record)


@router.get(
    '/users/{user_id}',
    response_model=UserOutSchema,
    summary='Read authentication user',
    description='Read authentication user from the current authentication context.',
    operation_id='auth:users:read',
)
async def record_read(
        user_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> UserOutSchema:
    """Read authentication user"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.auth import User

    # Build a statement to retrieve the record
    stmt = select(User).where(User.id == user_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(User.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: User | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User {user_id} not found')

    # Build the response
    return UserOutSchema.model_validate(record)


@router.patch(
    '/users/{user_id}',
    response_model=UserOutSchema,
    summary='Update authentication user',
    description='Update authentication user in the current authentication context.',
    operation_id='auth:users:update',
)
async def record_update(
        user_id: UUID,
        user: UserInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> UserOutSchema:
    """Update authentication user"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.auth import User

    # Build a statement to retrieve the record
    stmt = select(User).where(User.id == user_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(User.tenant_id == principal.tenant_id)

    # Retrieve the record
    record: User | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User {user_id} not found')

    # Update the record
    record.username = user.username
    record.status = user.status

    if isinstance(user.password, str):
        record.password = user.password

    # Check that the username is available
    if not await User.check_username_available(session, record.username, record.tenant_id, record.id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Username is already taken.')

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return UserOutSchema.model_validate(record)


@router.delete(
    '/users/{user_id}',
    summary='Delete authentication user',
    description='Delete authentication user from the current authentication context.',
    operation_id='auth:users:delete',
)
async def record_delete(
        user_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete authentication user"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models.db.auth import User

    # Build a statement to delete the record
    stmt = delete(User).where(User.id == user_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(User.tenant_id == principal.tenant_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User {user_id} not found')
