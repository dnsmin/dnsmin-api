import {IAclPrincipalInDTO, IAclPrincipalOutDTO, IAclPrincipalsPagedResponseDTO} from "@app/features/acl/principals/dto";
import {IAclPrincipal, IAclPrincipalsPaged} from "@app/features/acl/principals/models";

export function principalFromDTO(dto: IAclPrincipalInDTO): IAclPrincipal {
    return {
        id: dto.id,
        tenantId: dto.tenant_id,
        type: dto.type,
        createdAt: dto.created_at,
    }
}

export function principalToDTO(principal: IAclPrincipal): IAclPrincipalOutDTO {
    return {
        id: principal.id,
        tenant_id: principal.tenantId,
        type: principal.type,
    }
}

export function principalsPagedFromDTO(dto: IAclPrincipalsPagedResponseDTO): IAclPrincipalsPaged {
    return {
        records: dto.records.map(principalFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}