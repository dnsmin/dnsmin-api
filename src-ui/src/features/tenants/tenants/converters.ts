import {ITenantInDTO, ITenantOutDTO, ITenantsPagedResponseDTO} from "@app/features/tenants/tenants/dto";
import {ITenant, ITenantsPaged} from "@app/features/tenants/tenants/models";

export function tenantFromDTO(dto: ITenantInDTO): ITenant {
    return {
        id: dto.id,
        name: dto.name,
        fqdn: dto.fqdn,
        stopgapDomainId: dto.stopgap_domain_id,
        stopgapHostname: dto.stopgap_hostname,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
    }
}

export function tenantToDTO(tenant: ITenant): ITenantOutDTO {
    return {
        id: tenant.id,
        name: tenant.name,
        fqdn: tenant.fqdn,
        stopgap_domain_id: tenant.stopgapDomainId,
        stopgap_hostname: tenant.stopgapHostname,
    }
}

export function tenantsPagedFromDTO(dto: ITenantsPagedResponseDTO): ITenantsPaged {
    return {
        records: dto.records.map(tenantFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}