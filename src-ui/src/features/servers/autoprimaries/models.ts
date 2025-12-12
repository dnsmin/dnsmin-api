import {ModelBase} from "@app/types/models";

export interface ServerAutoPrimary extends ModelBase {
    id?: string;
    serverId: string;
    ip: string;
    nameserver: string;
    account: string;
    createdAt?: string | null;
    updatedAt?: string | null;
}

export interface ServerAutoPrimariesPaged extends ModelBase {
    records: ServerAutoPrimary[];
    total: number;
    totalFiltered: number;
}

export type IServerAutoPrimary = ServerAutoPrimary;
export type IServerAutoPrimariesPaged = ServerAutoPrimariesPaged;