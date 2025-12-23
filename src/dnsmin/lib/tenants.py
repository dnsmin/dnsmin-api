from typing import Optional
from uuid import UUID

from fastapi import WebSocket
from fastapi.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession

from dnsmin.models.db.tenants import Tenant


class TenantManager:
    """Provides an interface for managing and interacting with tenant data."""

    @staticmethod
    async def get_tenant_id_by_fqdn(session: AsyncSession, fqdn: Optional[str]) -> Optional[UUID]:
        """Retrieves a tenant ID by associated FQDN."""
        from sqlalchemy import select
        from dnsmin.models.db.system import StopgapDomain

        if not isinstance(fqdn, str):
            return None

        # Attempt to identify tenant by associated FQDN
        stmt = select(Tenant.id).where(Tenant.fqdn == fqdn)

        tenant_id = (await session.execute(stmt)).scalar_one_or_none()

        if isinstance(tenant_id, UUID):
            return tenant_id

        # Attempt to identify tenant by associated stopgap domain if not found by FQDN
        fqdn_parts = fqdn.split('.', 1)
        hostname = fqdn_parts[0]
        stopgap_domain = fqdn_parts[1] if len(fqdn_parts) > 1 else None

        if stopgap_domain is None:
            return None

        stmt = select(StopgapDomain.id).where(StopgapDomain.fqdn == stopgap_domain)
        stopgap_domain_id = (await session.execute(stmt)).scalar_one_or_none()

        if not isinstance(stopgap_domain_id, UUID):
            return None

        stmt = select(Tenant.id).where(
            Tenant.stopgap_domain_id == stopgap_domain_id, Tenant.stopgap_hostname == hostname
        )

        return (await session.execute(stmt)).scalar_one_or_none()

    @staticmethod
    async def validate_tenant_request(
            session: AsyncSession, request: Request | WebSocket, tenant_id: UUID | str
    ) -> bool:
        """Validates a tenant request to ensure the request host matches the tenant configuration."""

        if tenant_id is None:
            return False

        if isinstance(tenant_id, str):
            tenant_id = UUID(tenant_id)

        found_id: UUID | None = await TenantManager.get_tenant_id_by_fqdn(session, request.headers.get('host'))

        return found_id == tenant_id

    @staticmethod
    async def get_request_tenant_id(session: AsyncSession, request: Request | WebSocket) -> Optional[UUID]:
        """Retrieves a tenant ID based on information available in a FastAPI request."""
        from fastapi import HTTPException, status
        from dnsmin.lib.security import TENANT_HEADER_NAME

        tenant_id: Optional[UUID] = None

        # Attempt to identity the tenant by header
        if TENANT_HEADER_NAME in request.headers:
            try:
                tenant_id = UUID(request.headers[TENANT_HEADER_NAME])
            except ValueError:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Tenant ID')

        if isinstance(tenant_id, UUID):
            if not TenantManager.validate_tenant_request(session, request, tenant_id):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid Tenant Host')
            return tenant_id

        # Attempt to identify the tenant by hostname if not provided by request header
        return  await TenantManager.get_tenant_id_by_fqdn(session, request.headers.get('host'))
