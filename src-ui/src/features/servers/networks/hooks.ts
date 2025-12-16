import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {ServerNetworksService} from "@app/features/servers/networks/service";
import {IServerNetwork} from "@app/features/servers/networks/models";

export function useServerNetwork(serverId: string, id: string) {
    return useQuery({
        queryKey: ["servers-network", id],
        queryFn: () => ServerNetworksService.get(serverId, id),
        enabled: !!id,
    });
}

export function useServerNetworks(serverId: string, params?: ListResourceParams) {
    return useQuery({
        queryKey: ["servers-networks", params],
        queryFn: () => ServerNetworksService.search(serverId, params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateServerNetwork(serverId: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<IServerNetwork, "id">) => ServerNetworksService.create(serverId, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["servers-networks"]});
        }
    });
}

export function useUpdateServerNetwork(serverId: string, id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<IServerNetwork>) => ServerNetworksService.update(serverId, id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["servers-networks"]});
            qc.invalidateQueries({queryKey: ["servers-network", id]});
        }
    });
}

export function useDeleteServerNetwork(serverId: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => ServerNetworksService.remove(serverId, id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["servers-networks"]});
        }
    });
}
