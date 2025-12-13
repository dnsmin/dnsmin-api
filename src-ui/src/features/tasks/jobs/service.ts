import {http} from "@app/utils/http";
import {ListResourceParams} from "@app/types/api";
import {taskJobFromDTO, taskJobsPagedFromDTO} from "@app/features/tasks/jobs/converters";
import {ITaskJobInDTO, ITaskJobsPagedResponseDTO} from "@app/features/tasks/jobs/dto";
import {ITaskJob, ITaskJobsPaged} from "@app/features/tasks/jobs/models";

export const TaskJobsService = {
    async list(req?: ListResourceParams): Promise<ITaskJobsPaged> {
        const params = req !== undefined ? {
            filterModel: req.filterModel,
            sortModel: req.sortModel,
            paginationModel: req.paginationModel,
        } : {};

        const response = await http.post<ITaskJobsPagedResponseDTO>(
            "/tasks/jobs", params
        );

        return taskJobsPagedFromDTO(response.data);
    },

    async get(id: string): Promise<ITaskJob> {
        const response = await http.get<ITaskJobInDTO>(`/tasks/jobs/${id}`);
        return taskJobFromDTO(response.data);
    },

    async remove(id: string): Promise<void> {
        await http.delete(`/tasks/jobs/${id}`);
    },
};