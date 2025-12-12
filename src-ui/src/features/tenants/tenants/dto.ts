import {BaseDTO} from "@app/types/dto";

export interface TenantInDTO extends BaseDTO {
    id: string;
    name: string;
    fqdn: string | null;
    stopgap_domain_id: string | null;
    stopgap_hostname: string | null;
    created_at: string;
    updated_at: string | null;
}

export interface TenantOutDTO extends BaseDTO {
    id?: string;
    name: string;
    fqdn?: string | null;
    stopgap_domain_id?: string | null;
    stopgap_hostname?: string | null;
}

export interface TenantsPagedResponseDTO extends BaseDTO {
    records: TenantInDTO[];
    total: number;
    total_filtered: number;
}

export type ITenantInDTO = TenantInDTO;
export type ITenantOutDTO = TenantOutDTO;
export type ITenantsPagedResponseDTO = TenantsPagedResponseDTO;