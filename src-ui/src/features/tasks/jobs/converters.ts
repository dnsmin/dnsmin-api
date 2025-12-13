import {ITaskJobInDTO, ITaskJobsPagedResponseDTO} from "@app/features/tasks/jobs/dto";
import {ITaskJob, ITaskJobsPaged} from "@app/features/tasks/jobs/models";

export function taskJobFromDTO(dto: ITaskJobInDTO): ITaskJob {
    return {
        id: dto.id,
        rootId: dto.root_id,
        parentId: dto.parent_id,
        taskId: dto.task_id,
        name: dto.name,
        args: dto.args,
        kwargs: dto.kwargs,
        options: dto.options,
        retries: dto.retries,
        runtime: dto.runtime,
        output: dto.output,
        errors: dto.errors,
        status: dto.status,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
        startedAt: dto.started_at,
        endedAt: dto.ended_at,
    }
}

export function taskJobsPagedFromDTO(dto: ITaskJobsPagedResponseDTO): ITaskJobsPaged {
    return {
        records: dto.records.map(taskJobFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}