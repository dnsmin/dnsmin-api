import {BaseDTO} from "@app/types/dto/base";

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
    name: string;
    redirect_uri?: string | null;
    scopes?: string[] | null;
    enabled: boolean;
}

export interface UserInDTO extends BaseDTO {
    id: string;
    tenant_id: string | null;
    username: string;
    email: string | null;
    phone_number: string | null;
    status: string;
    created_at: string;
    updated_at: string | null;
    authenticated_at: string | null;
}

export interface UserOutDTO extends BaseDTO {
    id?: string;
    tenant_id?: string | null;
    username: string;
    password?: string | null;
    email?: string | null;
    phone_number?: string | null;
    status: string;
}

export interface UsersPagedResponseDTO extends BaseDTO {
    records: UserInDTO[];
    total: number;
}

export interface SessionInDTO extends BaseDTO {
    id: string;
    tenant_id: string | null;
    user_id: string | null;
    client_ip: string;
    token: string;
    data: object | null;
    created_at: string;
    updated_at: string | null;
    expires_at: string | null;
}

export type IClientInDTO = ClientInDTO;
export type IClientOutDTO = ClientOutDTO;
export type IUserInDTO = UserInDTO;
export type IUserOutDTO = UserOutDTO;
export type ISessionInDTO = SessionInDTO;