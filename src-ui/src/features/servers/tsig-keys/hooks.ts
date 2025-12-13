import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {ServerTsigKeysService} from "@app/features/servers/tsig-keys/service";
import {IServerTsigKey} from "@app/features/servers/tsig-keys/models";

export function useServerTsigKey(serverId: string, id: string) {
    return useQuery({
        queryKey: ["servers-tsig-key", id],
        queryFn: () => ServerTsigKeysService.get(serverId, id),
        enabled: !!id,
    });
}

export function useServerTsigKeys(serverId: string, params?: ListResourceParams) {
    return useQuery({
        queryKey: ["servers-tsig-keys", params],
        queryFn: () => ServerTsigKeysService.list(serverId, params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateServerTsigKey(serverId: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<IServerTsigKey, "id">) => ServerTsigKeysService.create(serverId, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["servers-tsig-keys"]});
        }
    });
}

export function useUpdateServerTsigKey(serverId: string, id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<IServerTsigKey>) => ServerTsigKeysService.update(serverId, id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["servers-tsig-keys"]});
            qc.invalidateQueries({queryKey: ["servers-tsig-key", id]});
        }
    });
}

export function useDeleteServerTsigKey(serverId: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => ServerTsigKeysService.remove(serverId, id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["servers-tsig-keys"]});
        }
    });
}
