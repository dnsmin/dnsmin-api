import {BaseDTO} from "@app/types/dto";

export interface ServerTsigKeyInDTO extends BaseDTO {
    id: string;
    server_id: string;
    internal_id: string | null;
    algorithm: string;
    key: string;
    created_at: string;
    updated_at: string | null;
}

export interface ServerTsigKeyOutDTO extends BaseDTO {
    id?: string;
    server_id: string;
    algorithm: string;
    key: string;
}

export interface ServerTsigKeysPagedResponseDTO extends BaseDTO {
    records: ServerTsigKeyInDTO[];
    total: number;
    total_filtered: number;
}

export type IServerTsigKeyInDTO = ServerTsigKeyInDTO;
export type IServerTsigKeyOutDTO = ServerTsigKeyOutDTO;
export type IServerTsigKeysPagedResponseDTO = ServerTsigKeysPagedResponseDTO;