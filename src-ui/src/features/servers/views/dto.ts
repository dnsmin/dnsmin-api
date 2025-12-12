import {BaseDTO} from "@app/types/dto";

export interface ServerViewInDTO extends BaseDTO {
    id: string;
    server_id: string;
    name: string;
    created_at: string;
    updated_at: string | null;
}

export interface ServerViewOutDTO extends BaseDTO {
    id?: string;
    server_id: string;
    name: string;
}

export interface ServerViewsPagedResponseDTO extends BaseDTO {
    records: ServerViewInDTO[];
    total: number;
    total_filtered: number;
}

export type IServerViewInDTO = ServerViewInDTO;
export type IServerViewOutDTO = ServerViewOutDTO;
export type IServerViewsPagedResponseDTO = ServerViewsPagedResponseDTO;