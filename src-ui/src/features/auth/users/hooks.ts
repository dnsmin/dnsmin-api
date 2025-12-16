import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {AuthUsersService} from "@app/features/auth/users/service";
import {IUser} from "@app/features/auth/users/models";

export function useAuthUser(id: string) {
    return useQuery({
        queryKey: ["auth-user", id],
        queryFn: () => AuthUsersService.get(id),
        enabled: !!id,
    });
}

export function useAuthUsers(params?: ListResourceParams) {
    return useQuery({
        queryKey: ["auth-users", params],
        queryFn: () => AuthUsersService.search(params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateAuthUser() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<IUser, "id">) => AuthUsersService.create(payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["auth-users"]});
        }
    });
}

export function useUpdateAuthUser(id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<IUser>) => AuthUsersService.update(id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["auth-users"]});
            qc.invalidateQueries({queryKey: ["auth-user", id]});
        }
    });
}

export function useDeleteAuthUser() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => AuthUsersService.remove(id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["auth-users"]});
        }
    });
}
