import {BaseDTO} from "@app/types/dto";

export interface ClientInDTO extends BaseDTO {
    id: string;
    tenant_id: string | null;
    user_id: string | null;
    name: string;
    redirect_uri: string | null;
    scopes: string[] | null;
    enabled: boolean;
    created_at: string;
    updated_at: string | null;
    expires_at: string | null;
}

export interface ClientOutDTO extends BaseDTO {
    id?: string;
    tenant_id?: string | null;
    user_id?: string | null;
    secret?: string | null;
    name: string;
    redirect_uri?: string | null;
    scopes?: string[] | null;
    enabled: boolean;
}

export interface ClientsPagedResponseDTO extends BaseDTO {
    records: ClientInDTO[];
    total: number;
    total_filtered: number;
}

export type IClientInDTO = ClientInDTO;
export type IClientOutDTO = ClientOutDTO;
export type IClientsPagedResponseDTO = ClientsPagedResponseDTO;