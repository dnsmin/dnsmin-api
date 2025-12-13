import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {SystemTimezonesService} from "@app/features/system/timezones/service";
import {ITimezone} from "@app/features/system/timezones/models";

export function useSystemTimezone(id: number) {
    return useQuery({
        queryKey: ["system-timezone", id],
        queryFn: () => SystemTimezonesService.get(id),
        enabled: !!id,
    });
}

export function useSystemTimezones(params?: ListResourceParams) {
    return useQuery({
        queryKey: ["system-timezones", params],
        queryFn: () => SystemTimezonesService.list(params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateSystemTimezone() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<ITimezone, "id">) => SystemTimezonesService.create(payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["system-timezones"]});
        }
    });
}

export function useUpdateSystemTimezone(id: number) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<ITimezone>) => SystemTimezonesService.update(id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["system-timezones"]});
            qc.invalidateQueries({queryKey: ["system-timezone", id]});
        }
    });
}

export function useDeleteSystemTimezone() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: number) => SystemTimezonesService.remove(id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["system-timezones"]});
        }
    });
}
