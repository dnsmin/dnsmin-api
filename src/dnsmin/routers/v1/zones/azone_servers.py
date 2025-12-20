from typing import Optional
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from dnsmin.lib.api.dependencies import get_db_session, get_principal
from dnsmin.models.api import ListParamsModel
from dnsmin.models.api.auth import Principal
from dnsmin.models.api.zones.azone_servers import AZoneServerInSchema, AZoneServerOutSchema, AZoneServersSchema
from dnsmin.routers.v1.zones import router


@router.get(
    '/authoritative/{zone_id}/servers',
    response_model=list[AZoneServerOutSchema],
    summary='List authoritative zone server relationships',
    description='List authoritative zone server relationships.',
    operation_id='zones:authoritative:servers:list',
)
async def record_list(
        zone_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> list[AZoneServerOutSchema]:
    """List authoritative zone server relationships"""
    from sqlalchemy import select
    from dnsmin.models.db.zones import AZoneServer

    # Build a statement to retrieve the relevant records
    stmt = select(AZoneServer).where(AZoneServer.zone_id == zone_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(AZoneServer.tenant_id == principal.tenant_id)

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return [AZoneServerOutSchema.model_validate(r) for r in records]


@router.post(
    '/authoritative/{zone_id}/servers/search',
    response_model=AZoneServersSchema,
    summary='Search authoritative zone server relationships',
    description='Search authoritative zone server relationships.',
    operation_id='zones:authoritative:servers:search',
)
async def record_search(
        zone_id:UUID,
        params: Optional[ListParamsModel] = None,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneServersSchema:
    """Search authoritative zone server relationships"""
    from sqlalchemy import select, func
    from dnsmin.lib.sql import SqlQueryBuilder
    from dnsmin.models.db.zones import AZoneServer

    # Build a statement to retrieve the relevant records
    stmt = select(AZoneServer).where(AZoneServer.zone_id == zone_id)

    # Enforce tenancy
    if principal.tenant_id:
        stmt = stmt.where(AZoneServer.tenant_id == principal.tenant_id)

    # Build a statement to retrieve the total count of unfiltered records
    stmt_count = select(func.count()).select_from(stmt.subquery())

    # Apply record filtering, sorting, and pagination
    if params:
        stmt = SqlQueryBuilder.apply_params(params, stmt, AZoneServer)

    # Build a statement to retrieve the total count of filtered records
    stmt_filtered_count = select(func.count()).select_from(stmt.limit(None).offset(None).subquery())

    # Retrieve the records
    records = (await session.execute(stmt)).scalars().all()

    # Build the response
    return AZoneServersSchema(
        records=[AZoneServerOutSchema.model_validate(r) for r in records],
        total=(await session.execute(stmt_count)).scalar_one(),
        total_filtered=(await session.execute(stmt_filtered_count)).scalar_one(),
    )


@router.post(
    '/authoritative/{zone_id}/servers',
    response_model=AZoneServerOutSchema,
    summary='Create authoritative zone server relationship',
    description='Create authoritative zone server relationship.',
    operation_id='zones:authoritative:servers:create',
)
async def record_create(
        zone_id:UUID,
        relationship: AZoneServerInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneServerOutSchema:
    """Create authoritative zone server relationship"""
    from dnsmin.models.db.zones import AZoneServer

    # Create the record
    db_record = AZoneServer(
        zone_id=relationship.zone_id,
        server_id=relationship.server_id,
        state=relationship.state,
        sync_policy=relationship.sync_policy,
    )

    # Enforce tenancy
    if principal.tenant_id:
        db_record.tenant_id = principal.tenant_id
    else:
        db_record.tenant_id = relationship.tenant_id

    # Commit the changes to the database
    session.add(db_record)
    await session.commit()
    await session.refresh(db_record)

    # Build the response
    return AZoneServerOutSchema.model_validate(db_record)


@router.get(
    '/authoritative/{zone_id}/servers/{server_id}',
    response_model=AZoneServerOutSchema,
    summary='Read authoritative zone server relationship',
    description='Read authoritative zone server relationship.',
    operation_id='zones:authoritative:servers:read',
)
async def record_read(
        zone_id:UUID,
        server_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneServerOutSchema:
    """Read authoritative zone server relationship"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from dnsmin.models.db.zones import AZoneServer

    # Build a statement to retrieve the record
    stmt = select(AZoneServer).where(AZoneServer.zone_id == zone_id, AZoneServer.server_id == server_id)

    # Retrieve the record
    record: AZoneServer | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Authoritative zone server relationship {zone_id}/{server_id} not found')

    # Build the response
    return AZoneServerOutSchema.model_validate(record)


@router.put(
    '/authoritative/{zone_id}/servers/{server_id}',
    response_model=AZoneServerOutSchema,
    summary='Update authoritative zone server relationship',
    description='Update authoritative zone server relationship.',
    operation_id='zones:authoritative:servers:update',
)
async def record_update(
        zone_id:UUID,
        server_id:UUID,
        relationship: AZoneServerInSchema,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
) -> AZoneServerOutSchema:
    """Update authoritative zone server relationship"""
    from fastapi import HTTPException, status
    from sqlalchemy import select
    from dnsmin.models.db.zones import AZoneServer

    # Build a statement to retrieve the record
    stmt = select(AZoneServer).where(AZoneServer.zone_id == zone_id, AZoneServer.server_id == server_id)

    # Retrieve the record
    record: AZoneServer | None = (await session.execute(stmt)).scalar_one_or_none()

    # Raise an HTTP 404 exception if the record could not be found
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Authoritative zone server relationship {zone_id}/{server_id} not found')

    # Update the record
    record.state = relationship.state
    record.sync_policy = relationship.sync_policy

    # Commit the changes to the database
    session.add(record)
    await session.commit()
    await session.refresh(record)

    # Build the response
    return AZoneServerOutSchema.model_validate(record)


@router.delete(
    '/authoritative/{zone_id}/servers/{server_id}',
    summary='Delete authoritative zone server relationship',
    description='Delete authoritative zone server relationship.',
    operation_id='zones:authoritative:servers:delete',
)
async def record_delete(
        zone_id:UUID,
        server_id:UUID,
        session: AsyncSession = Depends(get_db_session),
        principal: Principal = Depends(get_principal),
):
    """Delete authoritative zone server relationship"""
    from fastapi import HTTPException, status
    from sqlalchemy import delete
    from dnsmin.models.db.zones import AZoneServer

    # Build a statement to delete the record
    stmt = delete(AZoneServer).where(AZoneServer.zone_id == zone_id, AZoneServer.server_id == server_id)

    # Delete the record
    result = (await session.execute(stmt))

    # Commit the changes to the database
    await session.commit()

    # Raise an HTTP 404 exception if the record could not be found
    if not result.rowcount:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Authoritative zone server relationship {zone_id}/{server_id} not found')
