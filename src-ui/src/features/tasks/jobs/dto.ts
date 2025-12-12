import {BaseDTO} from "@app/types/dto";

export interface TaskJobInDTO extends BaseDTO {
    id: string;
    root_id: string;
    parent_id: string | null;
    task_id: string;
    name: string;
    args: any[] | null;
    kwargs: object | null;
    options: object | null;
    retries: number;
    runtime: number | null;
    output: string | null;
    errors: string | null;
    status: string;
    created_at: string;
    updated_at: string | null;
    started_at: string | null;
    ended_at: string | null;
}

export interface TaskJobsPagedResponseDTO extends BaseDTO {
    records: TaskJobInDTO[];
    total: number;
    total_filtered: number;
}

export type ITaskJobInDTO = TaskJobInDTO;
export type ITaskJobsPagedResponseDTO = TaskJobsPagedResponseDTO;