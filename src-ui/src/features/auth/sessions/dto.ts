import {BaseDTO} from "@app/types/dto";

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

export type ISessionInDTO = SessionInDTO;