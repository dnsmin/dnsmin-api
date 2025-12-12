import {ModelBase} from "@app/types/models";

export interface ServerNetwork extends ModelBase {
    id?: string;
    serverId: string;
    viewId: string;
    network: string;
    createdAt?: string | null;
    updatedAt?: string | null;
}

export interface ServerNetworksPaged extends ModelBase {
    records: ServerNetwork[];
    total: number;
    totalFiltered: number;
}

export type IServerNetwork = ServerNetwork;
export type IServerNetworksPaged = ServerNetworksPaged;