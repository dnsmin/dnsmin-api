import {BaseDTO} from "@app/types/dto";

export interface AclRoleInDTO extends BaseDTO {
    id: string;
    tenant_id: string | null;
    slug: string;
    name: string;
    description: string;
    created_at: string;
    updated_at: string | null;
}

export interface AclRoleOutDTO extends BaseDTO {
    id?: string;
    tenant_id?: string | null;
    slug: string;
    name: string;
    description: string;
}

export interface AclRolesPagedResponseDTO extends BaseDTO {
    records: AclRoleInDTO[];
    total: number;
    total_filtered: number;
}

export type IAclRoleInDTO = AclRoleInDTO;
export type IAclRoleOutDTO = AclRoleOutDTO;
export type IAclRolesPagedResponseDTO = AclRolesPagedResponseDTO;