import {BaseDTO} from "@app/types/dto";

export interface AclPolicyInDTO extends BaseDTO {
    id: string;
    tenant_id: string | null;
    resource_type: string;
    resource_id: string | null;
    principal_type: string;
    principal_id: string | null;
    permission: string;
    deny: boolean;
    created_at: string;
    updated_at: string | null;
}

export interface AclPolicyOutDTO extends BaseDTO {
    id?: string;
    tenant_id?: string | null;
    resource_type: string;
    resource_id?: string | null;
    principal_type: string;
    principal_id?: string | null;
    permission: string;
    deny: boolean;
}

export interface AclPoliciesPagedResponseDTO extends BaseDTO {
    records: AclPolicyInDTO[];
    total: number;
    total_filtered: number;
}

export type IAclPolicyInDTO = AclPolicyInDTO;
export type IAclPolicyOutDTO = AclPolicyOutDTO;
export type IAclPoliciesPagedResponseDTO = AclPoliciesPagedResponseDTO;