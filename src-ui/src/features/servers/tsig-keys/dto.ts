import {BaseDTO} from "@app/types/dto";

export interface TsigKeyInDTO extends BaseDTO {
    id: string;
    server_id: string;
    internal_id: string | null;
    algorithm: string;
    key: string;
    created_at: string;
    updated_at: string | null;
}

export interface TsigKeyOutDTO extends BaseDTO {
    id?: string;
    server_id: string;
    algorithm: string;
    key: string;
}

export interface TsigKeysPagedResponseDTO extends BaseDTO {
    records: TsigKeyInDTO[];
    total: number;
    total_filtered: number;
}

export type ITsigKeyInDTO = TsigKeyInDTO;
export type ITsigKeyOutDTO = TsigKeyOutDTO;
export type ITsigKeysPagedResponseDTO = TsigKeysPagedResponseDTO;