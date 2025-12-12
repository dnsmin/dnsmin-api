import {BaseDTO} from "@app/types/dto";

export interface ServerNetworkInDTO extends BaseDTO {
    id: string;
    server_id: string;
    view_id: string;
    network: string;
    created_at: string;
    updated_at: string | null;
}

export interface ServerNetworkOutDTO extends BaseDTO {
    id?: string;
    server_id: string;
    view_id: string;
    network: string;
}

export interface ServerNetworksPagedResponseDTO extends BaseDTO {
    records: ServerNetworkInDTO[];
    total: number;
    total_filtered: number;
}

export type IServerNetworkInDTO = ServerNetworkInDTO;
export type IServerNetworkOutDTO = ServerNetworkOutDTO;
export type IServerNetworksPagedResponseDTO = ServerNetworksPagedResponseDTO;