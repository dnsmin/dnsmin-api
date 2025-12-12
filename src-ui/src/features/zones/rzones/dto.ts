import {BaseDTO} from "@app/types/dto";

export interface RZoneInDTO extends BaseDTO {
    id: string;
    tenant_id: string | null;
    fqdn: string;
    kind: string;
    servers: string[];
    recursion_desired: boolean | null;
    notify_allowed: boolean | null;
    created_at: string;
    updated_at: string | null;
}

export interface RZoneOutDTO extends BaseDTO {
    id?: string;
    tenant_id?: string | null;
    fqdn: string;
    kind: string;
    servers: string[];
    recursion_desired?: boolean | null;
    notify_allowed?: boolean | null;
}

export interface RZonesPagedResponseDTO extends BaseDTO {
    records: RZoneInDTO[];
    total: number;
    total_filtered: number;
}

export type IRZoneInDTO = RZoneInDTO;
export type IRZoneOutDTO = RZoneOutDTO;
export type IRZonesPagedResponseDTO = RZonesPagedResponseDTO;