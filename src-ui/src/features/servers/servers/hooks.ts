import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {ServersService} from "@app/features/servers/servers/service";
import {IServer} from "@app/features/servers/servers/models";

export function useServer(id: string) {
    return useQuery({
        queryKey: ["servers-server", id],
        queryFn: () => ServersService.get(id),
        enabled: !!id,
    });
}

export function useServers(params?: ListResourceParams) {
    return useQuery({
        queryKey: ["servers-servers", params],
        queryFn: () => ServersService.search(params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateServer() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<IServer, "id">) => ServersService.create(payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["servers-servers"]});
        }
    });
}

export function useUpdateServer(id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<IServer>) => ServersService.update(id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["servers-servers"]});
            qc.invalidateQueries({queryKey: ["servers-server", id]});
        }
    });
}

export function useDeleteServer() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => ServersService.remove(id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["servers-servers"]});
        }
    });
}
