import {ModelBase} from "@app/types/models";

export interface TaskJob extends ModelBase {
    id?: string;
    rootId: string;
    parentId?: string | null;
    taskId: string;
    name: string;
    args?: any[] | null;
    kwargs?: object | null;
    options?: object | null;
    retries: number;
    runtime?: number | null;
    output?: string | null;
    errors?: string | null;
    status: string;
    createdAt?: string | null;
    updatedAt?: string | null;
    startedAt?: string | null;
    endedAt?: string | null;
}

export interface TaskJobsPaged extends ModelBase {
    records: TaskJob[];
    total: number;
    totalFiltered: number;
}

export type ITaskJob = TaskJob;
export type ITaskJobsPaged = TaskJobsPaged;