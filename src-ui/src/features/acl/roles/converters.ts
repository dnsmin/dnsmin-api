import {IAclRoleInDTO, IAclRoleOutDTO, IAclRolesPagedResponseDTO} from "@app/features/acl/roles/dto";
import {IAclRole, IAclRolesPaged} from "@app/features/acl/roles/models";

export function roleFromDTO(dto: IAclRoleInDTO): IAclRole {
    return {
        id: dto.id,
        tenantId: dto.tenant_id,
        slug: dto.slug,
        name: dto.name,
        description: dto.description,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
    }
}

export function roleToDTO(role: IAclRole): IAclRoleOutDTO {
    return {
        id: role.id,
        tenant_id: role.tenantId,
        slug: role.slug,
        name: role.name,
        description: role.description,
    }
}

export function rolesPagedFromDTO(dto: IAclRolesPagedResponseDTO): IAclRolesPaged {
    return {
        records: dto.records.map(roleFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}