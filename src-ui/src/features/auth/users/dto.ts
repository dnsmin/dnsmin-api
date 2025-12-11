import {BaseDTO} from "@app/types/dto";

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
    total_filtered: number;
}

export type IUserInDTO = UserInDTO;
export type IUserOutDTO = UserOutDTO;