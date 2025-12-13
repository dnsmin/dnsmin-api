import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {ServerAutoPrimariesService} from "@app/features/servers/autoprimaries/service";
import {IServerAutoPrimary} from "@app/features/servers/autoprimaries/models";

export function useServerAutoPrimary(serverId: string, id: string) {
    return useQuery({
        queryKey: ["servers-auto-primary", id],
        queryFn: () => ServerAutoPrimariesService.get(serverId, id),
        enabled: !!id,
    });
}

export function useServerAutoPrimaries(serverId: string, params?: ListResourceParams) {
    return useQuery({
        queryKey: ["servers-auto-primaries", params],
        queryFn: () => ServerAutoPrimariesService.list(serverId, params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateServerAutoPrimary(serverId: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<IServerAutoPrimary, "id">) => ServerAutoPrimariesService.create(serverId, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["servers-auto-primaries"]});
        }
    });
}

export function useUpdateServerAutoPrimary(serverId: string, id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<IServerAutoPrimary>) => ServerAutoPrimariesService.update(serverId, id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["servers-auto-primaries"]});
            qc.invalidateQueries({queryKey: ["servers-auto-primary", id]});
        }
    });
}

export function useDeleteServerAutoPrimary(serverId: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => ServerAutoPrimariesService.remove(serverId, id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["servers-auto-primaries"]});
        }
    });
}
