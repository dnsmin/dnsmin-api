from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnsmin.lib.api.dependencies import get_db_session, get_principal
from dnsmin.models.api import ListParamsModel
from dnsmin.models.api.auth import Principal
from dnsmin.models.api.auth.users import UsersSchema, UserOutSchema, UserInSchema
from dnsmin.routers.v1.auth import router


@router.get(
    '/users',
    response_model=list[UserOutSchema],
    summary='List Users',
    description='Lists users.',
    operation_id='auth:users:list',
)
async def record_list(
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> list[UserOutSchema]:
    """List users."""
    from sqlalchemy import select
    from dnsmin.models.db.auth import User

    # Build a statement to retrieve the relevant records
    stmt = select(User)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(User.tenant_id == principal.tenant_id)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return [UserOutSchema.model_validate(r) for r in records]


@router.post(
    '/users/search',
    response_model=UsersSchema,
    summary='Search Users',
    description='Searches users.',
    operation_id='auth:users:search',
)
async def record_search(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> UsersSchema:
    """Search users."""
    from sqlalchemy import select, func
    from dnsmin.lib.sql import SqlQueryBuilder
    from dnsmin.models.db.auth import User

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

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return UsersSchema(
        records=[UserOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/users',
    response_model=UserOutSchema,
    summary='Create user',
    description='Create user.',
    operation_id='auth:users:create',
)
async def record_create(
        user: UserInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> UserOutSchema:
    """Create user"""
    from fastapi import HTTPException, status
    from dnsmin.models.db.auth import User

    # Create the record
    record = User(
        username=user.username,
        email=user.email,
        phone_number=user.phone_number,
        status=user.status,
    )
    record.password = user.password

    # Enforce tenancy
    if principal.tenant_id:
        record.tenant_id = principal.tenant_id
    else:
        record.tenant_id = user.tenant_id

    # Provide additional data validation
    validation_errors = []

    # Check that the username is available
    if not await User.check_username_available(session, record.username, record.tenant_id):
        validation_errors.append({
            'loc': ['body', 'username'],
            'msg': f'Username "{record.username}" is already taken.',
            'type': 'value_error.forbidden_value',
        })

    # Check that the email is available
    if not await User.check_email_available(session, record.email, record.tenant_id):
        validation_errors.append({
            'loc': ['body', 'email'],
            'msg': f'Email address "{record.email}" is already in use.',
            'type': 'value_error.forbidden_value',
        })

    # Raise HTTP exception if any validation errors were created
    if validation_errors:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=validation_errors)

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return UserOutSchema.model_validate(record)


@router.get(
    '/users/{user_id}',
    response_model=UserOutSchema,
    summary='Read user',
    description='Read user.',
    operation_id='auth:users:read',
)
async def record_read(
        user_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> UserOutSchema:
    """Read user"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from dnsmin.models.db.auth import User

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


@router.put(
    '/users/{user_id}',
    response_model=UserOutSchema,
    summary='Update user',
    description='Update user.',
    operation_id='auth:users:update',
)
async def record_update(
        user_id: UUID,
        user: UserInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> UserOutSchema:
    """Update user"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from dnsmin.models.db.auth import User

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
    record.email = user.email
    record.phone_number = user.phone_number
    record.status = user.status

    if isinstance(user.password, str) and len(user.password.strip()):
        record.password = user.password

    # Provide additional data validation
    validation_errors = []

    # Check that the username is available
    if not await User.check_username_available(session, record.username, record.tenant_id, record.id):
        validation_errors.append({
            'loc': ['body', 'username'],
            'msg': f'Username "{record.username}" is already taken.',
            'type': 'value_error.forbidden_value',
        })

    # Check that the email is available
    if not await User.check_email_available(session, record.email, record.tenant_id, record.id):
        validation_errors.append({
            'loc': ['body', 'email'],
            'msg': f'Email address "{record.email}" is already in use.',
            'type': 'value_error.forbidden_value',
        })

    # Raise HTTP exception if any validation errors were created
    if validation_errors:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=validation_errors)

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return UserOutSchema.model_validate(record)


@router.delete(
    '/users/{user_id}',
    summary='Delete user',
    description='Delete user.',
    operation_id='auth:users:delete',
)
async def record_delete(
        user_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete user"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from dnsmin.models.db.auth import User

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
