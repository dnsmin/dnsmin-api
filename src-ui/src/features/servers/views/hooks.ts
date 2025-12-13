import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {ServerViewsService} from "@app/features/servers/views/service";
import {IServerView} from "@app/features/servers/views/models";

export function useServerView(serverId: string, id: string) {
    return useQuery({
        queryKey: ["servers-view", id],
        queryFn: () => ServerViewsService.get(serverId, id),
        enabled: !!id,
    });
}

export function useServerViews(serverId: string, params?: ListResourceParams) {
    return useQuery({
        queryKey: ["servers-views", params],
        queryFn: () => ServerViewsService.list(serverId, params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateServerView(serverId: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<IServerView, "id">) => ServerViewsService.create(serverId, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["servers-views"]});
        }
    });
}

export function useUpdateServerView(serverId: string, id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<IServerView>) => ServerViewsService.update(serverId, id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["servers-views"]});
            qc.invalidateQueries({queryKey: ["servers-view", id]});
        }
    });
}

export function useDeleteServerView(serverId: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => ServerViewsService.remove(serverId, id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["servers-views"]});
        }
    });
}
