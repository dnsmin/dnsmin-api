import {BaseDTO} from "@app/types/dto";

export interface CryptoKeyInDTO extends BaseDTO {
    id: string;
    tenant_id: string | null;
    zone_id: string;
    internal_id: number | null;
    type: string;
    active: boolean;
    published: boolean;
    dns_key: string;
    ds: string[];
    cds: string[];
    private_key: string;
    algorithm: string;
    bits: number;
    created_at: string;
    updated_at: string | null;
}

export interface CryptoKeyOutDTO extends BaseDTO {
    id?: string;
    tenant_id?: string | null;
    zone_id: string;
    type: string;
    active: boolean;
    published: boolean;
    dns_key: string;
    ds: string[];
    cds: string[];
    private_key: string;
    algorithm: string;
    bits: number;
}

export interface CryptoKeysPagedResponseDTO extends BaseDTO {
    records: CryptoKeyInDTO[];
    total: number;
    total_filtered: number;
}

export type ICryptoKeyInDTO = CryptoKeyInDTO;
export type ICryptoKeyOutDTO = CryptoKeyOutDTO;
export type ICryptoKeysPagedResponseDTO = CryptoKeysPagedResponseDTO;