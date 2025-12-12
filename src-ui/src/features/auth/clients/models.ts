import {ModelBase} from "@app/types/models";

export interface Client extends ModelBase {
    id?: string;
    tenantId?: string | null;
    userId?: string | null;
    name: string;
    redirectUri: string | null;
    scopes: string[] | null;
    enabled: boolean;
    createdAt?: string | null;
    updatedAt?: string | null;
    expiresAt?: string | null;
}

export interface ClientsPaged extends ModelBase {
    records: Client[];
    total: number;
    totalFiltered: number;
}

export type IClient = Client;
export type IClientsPaged = ClientsPaged;