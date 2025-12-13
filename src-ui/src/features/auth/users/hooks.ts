import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {AuthUsersService} from "@app/features/auth/users/service";

import {User} from "@app/features/auth/users/models";

export function useUser(id: string) {
    return useQuery({
        queryKey: ["user", id],
        queryFn: () => AuthUsersService.get(id),
        enabled: !!id,
    });
}

export function useUsers(params?: ListResourceParams) {
    return useQuery({
        queryKey: ["users", params],
        queryFn: () => AuthUsersService.list(params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateUser() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<User, "id">) => AuthUsersService.create(payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["users"]});
        }
    });
}

export function useUpdateUser(id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<User>) => AuthUsersService.update(id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["users"]});
            qc.invalidateQueries({queryKey: ["user", id]});
        }
    });
}

export function useDeleteUser() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => AuthUsersService.remove(id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["users"]});
        }
    });
}
