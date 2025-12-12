import {ModelBase} from "@app/types/models";

export interface Server extends ModelBase {
    id?: string;
    type: string;
    version: string;
    hostname: string;
    apiUrl: string;
    apiKey: string;
    shared: boolean;
    createdAt?: string | null;
    updatedAt?: string | null;
}

export interface ServersPaged extends ModelBase {
    records: Server[];
    total: number;
    totalFiltered: number;
}

export type IServer = Server;
export type IServersPaged = ServersPaged;