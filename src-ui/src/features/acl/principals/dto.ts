import {BaseDTO} from "@app/types/dto";

export interface AclPrincipalInDTO extends BaseDTO {
    id: string;
    tenant_id: string | null;
    type: string;
    created_at: string;
}

export interface AclPrincipalOutDTO extends BaseDTO {
    id?: string;
    tenant_id?: string | null;
    type: string;
}

export interface AclPrincipalsPagedResponseDTO extends BaseDTO {
    records: AclPrincipalInDTO[];
    total: number;
    total_filtered: number;
}

export type IAclPrincipalInDTO = AclPrincipalInDTO;
export type IAclPrincipalOutDTO = AclPrincipalOutDTO;
export type IAclPrincipalsPagedResponseDTO = AclPrincipalsPagedResponseDTO;