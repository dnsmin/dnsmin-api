import {BaseDTO} from "@app/types/dto";

export interface ServerInDTO extends BaseDTO {
    id: string;
    type: string;
    version: string;
    hostname: string;
    api_url: string;
    api_key: string;
    shared: boolean;
    created_at: string;
    updated_at: string | null;
}

export interface ServerOutDTO extends BaseDTO {
    id?: string;
    type: string;
    version: string;
    hostname: string;
    api_url: string;
    api_key: string;
    shared: boolean;
}

export interface ServersPagedResponseDTO extends BaseDTO {
    records: ServerInDTO[];
    total: number;
    total_filtered: number;
}

export type IServerInDTO = ServerInDTO;
export type IServerOutDTO = ServerOutDTO;
export type IServersPagedResponseDTO = ServersPagedResponseDTO;