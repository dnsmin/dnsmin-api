import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/services/base";
import {UserService} from "@app/services/auth.service";
import {User} from "@app/types/models/auth";

export function useUser(id: string) {
    return useQuery({
        queryKey: ["user", id],
        queryFn: () => UserService.get(id),
        enabled: !!id,
    });
}

export function useUsers(params?: ListResourceParams) {
    return useQuery({
        queryKey: ["users", params],
        queryFn: () => UserService.list(params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateUser() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<User, "id">) => UserService.create(payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["users"]});
        }
    });
}

export function useUpdateUser(id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<User>) => UserService.update(id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["users"]});
            qc.invalidateQueries({queryKey: ["user", id]});
        }
    });
}

export function useDeleteUser() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => UserService.remove(id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["users"]});
        }
    });
}
