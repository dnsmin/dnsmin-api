import {ModelBase} from "@app/types/models";

export interface ServerTsigKey extends ModelBase {
    id?: string;
    serverId: string;
    internalId?: string | null;
    algorithm: string;
    key: string;
    createdAt?: string | null;
    updatedAt?: string | null;
}

export interface ServerTsigKeysPaged extends ModelBase {
    records: ServerTsigKey[];
    total: number;
    totalFiltered: number;
}

export type IServerTsigKey = ServerTsigKey;
export type IServerTsigKeysPaged = ServerTsigKeysPaged;