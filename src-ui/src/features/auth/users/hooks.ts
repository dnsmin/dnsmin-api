import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {UsersService} from "@app/features/auth/users/service";

import {User} from "@app/features/auth/users/models";

export function useUser(id: string) {
    return useQuery({
        queryKey: ["user", id],
        queryFn: () => UsersService.get(id),
        enabled: !!id,
    });
}

export function useUsers(params?: ListResourceParams) {
    return useQuery({
        queryKey: ["users", params],
        queryFn: () => UsersService.list(params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateUser() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<User, "id">) => UsersService.create(payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["users"]});
        }
    });
}

export function useUpdateUser(id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<User>) => UsersService.update(id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["users"]});
            qc.invalidateQueries({queryKey: ["user", id]});
        }
    });
}

export function useDeleteUser() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => UsersService.remove(id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["users"]});
        }
    });
}
