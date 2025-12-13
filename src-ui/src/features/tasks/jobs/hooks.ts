import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {TaskJobsService} from "@app/features/tasks/jobs/service";

export function useTaskJob(id: string) {
    return useQuery({
        queryKey: ["tasks-job", id],
        queryFn: () => TaskJobsService.get(id),
        enabled: !!id,
    });
}

export function useTaskJobs(params?: ListResourceParams) {
    return useQuery({
        queryKey: ["tasks-jobs", params],
        queryFn: () => TaskJobsService.list(params),
        placeholderData: (previousData) => previousData,
    });
}

export function useDeleteTaskJob() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => TaskJobsService.remove(id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["tasks-jobs"]});
        }
    });
}
