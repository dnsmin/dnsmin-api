import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {AuthSessionsService} from "@app/features/auth/sessions/service";

export function useAuthSession(id: string) {
    return useQuery({
        queryKey: ["auth-session", id],
        queryFn: () => AuthSessionsService.get(id),
        enabled: !!id,
    });
}

export function useAuthSessions(params?: ListResourceParams) {
    return useQuery({
        queryKey: ["auth-sessions", params],
        queryFn: () => AuthSessionsService.list(params),
        placeholderData: (previousData) => previousData,
    });
}

export function useDeleteAuthSession() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => AuthSessionsService.remove(id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["auth-sessions"]});
        }
    });
}
