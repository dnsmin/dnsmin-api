import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {AZonesService} from "@app/features/zones/azones/service";
import {IAZone} from "@app/features/zones/azones/models";

export function useAZone(id: string) {
    return useQuery({
        queryKey: ["zones-azone", id],
        queryFn: () => AZonesService.get(id),
        enabled: !!id,
    });
}

export function useAZones(params?: ListResourceParams) {
    return useQuery({
        queryKey: ["zones-azones", params],
        queryFn: () => AZonesService.search(params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateAZone() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<IAZone, "id">) => AZonesService.create(payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-azones"]});
        }
    });
}

export function useUpdateAZone(id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<IAZone>) => AZonesService.update(id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-azones"]});
            qc.invalidateQueries({queryKey: ["zones-azone", id]});
        }
    });
}

export function useDeleteAZone() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => AZonesService.remove(id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-azones"]});
        }
    });
}
