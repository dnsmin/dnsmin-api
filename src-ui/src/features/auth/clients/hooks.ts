import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {AuthClientsService} from "@app/features/auth/clients/service";
import {IClient} from "@app/features/auth/clients/models";

export function useAuthClient(id: string) {
    return useQuery({
        queryKey: ["auth-client", id],
        queryFn: () => AuthClientsService.get(id),
        enabled: !!id,
    });
}

export function useAuthClients(params?: ListResourceParams) {
    return useQuery({
        queryKey: ["auth-clients", params],
        queryFn: () => AuthClientsService.list(params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateAuthClient() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<IClient, "id">) => AuthClientsService.create(payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["auth-clients"]});
        }
    });
}

export function useUpdateAuthClient(id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<IClient>) => AuthClientsService.update(id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["auth-clients"]});
            qc.invalidateQueries({queryKey: ["auth-client", id]});
        }
    });
}

export function useDeleteAuthClient() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => AuthClientsService.remove(id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["auth-clients"]});
        }
    });
}
