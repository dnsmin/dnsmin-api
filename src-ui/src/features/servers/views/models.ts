import {ModelBase} from "@app/types/models";

export interface ServerView extends ModelBase {
    id?: string;
    serverId: string;
    name: string;
    createdAt?: string | null;
    updatedAt?: string | null;
}

export interface ServerViewsPaged extends ModelBase {
    records: ServerView[];
    total: number;
    totalFiltered: number;
}

export type IServerView = ServerView;
export type IServerViewsPaged = ServerViewsPaged;