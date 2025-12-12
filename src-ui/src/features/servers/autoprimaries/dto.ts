import {BaseDTO} from "@app/types/dto";

export interface ServerAutoPrimaryInDTO extends BaseDTO {
    id: string;
    server_id: string;
    ip: string;
    nameserver: string;
    account: string;
    created_at: string;
    updated_at: string | null;
}

export interface ServerAutoPrimaryOutDTO extends BaseDTO {
    id?: string;
    server_id: string;
    ip: string;
    nameserver: string;
    account: string;
}

export interface ServerAutoPrimariesPagedResponseDTO extends BaseDTO {
    records: ServerAutoPrimaryInDTO[];
    total: number;
    total_filtered: number;
}

export type IServerAutoPrimaryInDTO = ServerAutoPrimaryInDTO;
export type IServerAutoPrimaryOutDTO = ServerAutoPrimaryOutDTO;
export type IServerAutoPrimariesPagedResponseDTO = ServerAutoPrimariesPagedResponseDTO;