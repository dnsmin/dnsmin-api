from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from lib.api.dependencies import get_db_session, get_principal
from models.api import ListParamsModel
from models.api.auth import Principal
from models.api.system.stopgap_domains import StopgapDomainsSchema, StopgapDomainOutSchema, StopgapDomainInSchema
from routers.v1.system import router


@router.get(
    '/stopgap-domains',
    response_model=list[StopgapDomainOutSchema],
    summary='List stopgap domains',
    description='List stopgap domains.',
    operation_id='system:stopgap_domains:list',
)
async def record_list(
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> list[StopgapDomainOutSchema]:
    """List stopgap domains"""
    from sqlalchemy import select
    from models.db.system import StopgapDomain

    # Build a statement to retrieve the relevant records
    stmt = select(StopgapDomain)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return [StopgapDomainOutSchema.model_validate(r) for r in records]


@router.post(
    '/stopgap-domains/search',
    response_model=StopgapDomainsSchema,
    summary='Search stopgap domains',
    description='Search stopgap domains.',
    operation_id='system:stopgap_domains:search',
)
async def record_search(
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> StopgapDomainsSchema:
    """Search stopgap domains"""
    from sqlalchemy import select, func
    from lib.sql import SqlQueryBuilder
    from models.db.system import StopgapDomain

    # Build a statement to retrieve the relevant records
    stmt = select(StopgapDomain)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, StopgapDomain)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return StopgapDomainsSchema(
        records=[StopgapDomainOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/stopgap-domains',
    response_model=StopgapDomainOutSchema,
    summary='Create stopgap domain',
    description='Create stopgap domain.',
    operation_id='system:stopgap_domains:create',
)
async def record_create(
        stopgap_domain: StopgapDomainInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> StopgapDomainOutSchema:
    """Create stopgap domain"""
    from models.db.system import StopgapDomain

    # Create the record
    record = StopgapDomain(
        name=stopgap_domain.name,
        fqdn=stopgap_domain.fqdn,
        restricted_hosts=stopgap_domain.restricted_hosts,
    )

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return StopgapDomainOutSchema.model_validate(record)


@router.get(
    '/stopgap-domains/{stopgap_domain_id}',
    response_model=StopgapDomainOutSchema,
    summary='Read stopgap domain',
    description='Read stopgap domain.',
    operation_id='system:stopgap_domains:read',
)
async def record_read(
        stopgap_domain_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> StopgapDomainOutSchema:
    """Read stopgap domain"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.system import StopgapDomain

    # Build a statement to retrieve the record
    stmt = select(StopgapDomain).where(StopgapDomain.id == stopgap_domain_id)

    # Retrieve the record
    record: StopgapDomain | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Stopgap domain {stopgap_domain_id} not found')

    # Build the response
    return StopgapDomainOutSchema.model_validate(record)


@router.put(
    '/stopgap-domains/{stopgap_domain_id}',
    response_model=StopgapDomainOutSchema,
    summary='Update stopgap domain',
    description='Update stopgap domain.',
    operation_id='system:stopgap_domains:update',
)
async def record_update(
        stopgap_domain_id: UUID,
        stopgap_domain: StopgapDomainInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> StopgapDomainOutSchema:
    """Update stopgap domain"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from models.db.system import StopgapDomain

    # Build a statement to retrieve the record
    stmt = select(StopgapDomain).where(StopgapDomain.id == stopgap_domain_id)

    # Retrieve the record
    record: StopgapDomain | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Stopgap domain {stopgap_domain_id} not found')

    # Update the record
    record.name = stopgap_domain.name
    record.fqdn = stopgap_domain.fqdn
    record.restricted_hosts = stopgap_domain.restricted_hosts

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return StopgapDomainOutSchema.model_validate(record)


@router.delete(
    '/stopgap-domains/{stopgap_domain_id}',
    summary='Delete stopgap domain',
    description='Delete stopgap domain.',
    operation_id='system:stopgap_domains:delete',
)
async def record_delete(
        stopgap_domain_id: UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete stopgap domain"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from models.db.system import StopgapDomain

    # Build a statement to delete the record
    stmt = delete(StopgapDomain).where(StopgapDomain.id == stopgap_domain_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Stopgap domain {stopgap_domain_id} not found')
