import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {RZonesService} from "@app/features/zones/rzones/service";
import {IRZone} from "@app/features/zones/rzones/models";

export function useRZone(id: string) {
    return useQuery({
        queryKey: ["zones-rzone", id],
        queryFn: () => RZonesService.get(id),
        enabled: !!id,
    });
}

export function useRZones(params?: ListResourceParams) {
    return useQuery({
        queryKey: ["zones-rzones", params],
        queryFn: () => RZonesService.list(params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateRZone() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<IRZone, "id">) => RZonesService.create(payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-rzones"]});
        }
    });
}

export function useUpdateRZone(id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<IRZone>) => RZonesService.update(id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-rzones"]});
            qc.invalidateQueries({queryKey: ["zones-rzone", id]});
        }
    });
}

export function useDeleteRZone() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => RZonesService.remove(id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-rzones"]});
        }
    });
}
