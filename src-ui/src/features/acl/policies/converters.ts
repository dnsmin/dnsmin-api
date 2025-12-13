import {IAclPolicyInDTO, IAclPolicyOutDTO, IAclPoliciesPagedResponseDTO} from "@app/features/acl/policies/dto";
import {IAclPolicy, IAclPoliciesPaged} from "@app/features/acl/policies/models";

export function policyFromDTO(dto: IAclPolicyInDTO): IAclPolicy {
    return {
        id: dto.id,
        tenantId: dto.tenant_id,
        resourceType: dto.resource_type,
        resourceId: dto.resource_id,
        principalType: dto.principal_type,
        principalId: dto.principal_id,
        permission: dto.permission,
        deny: dto.deny,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
    }
}

export function policyToDTO(policy: IAclPolicy): IAclPolicyOutDTO {
    return {
        id: policy.id,
        tenant_id: policy.tenantId,
        resource_type: policy.resourceType,
        resource_id: policy.resourceId,
        principal_type: policy.principalType,
        principal_id: policy.principalId,
        permission:  policy.permission,
        deny: policy.deny,
    }
}

export function policiesPagedFromDTO(dto: IAclPoliciesPagedResponseDTO): IAclPoliciesPaged {
    return {
        records: dto.records.map(policyFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}