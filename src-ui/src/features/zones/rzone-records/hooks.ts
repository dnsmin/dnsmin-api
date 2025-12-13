import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {RZoneRecordsService} from "@app/features/zones/rzone-records/service";
import {IRZoneRecord} from "@app/features/zones/rzone-records/models";

export function useRZoneRecord(zoneId: string, id: string) {
    return useQuery({
        queryKey: ["zones-rzone-record", id],
        queryFn: () => RZoneRecordsService.get(zoneId, id),
        enabled: !!id,
    });
}

export function useRZoneRecords(zoneId: string, params?: ListResourceParams) {
    return useQuery({
        queryKey: ["zones-rzone-records", params],
        queryFn: () => RZoneRecordsService.list(zoneId, params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateRZoneRecord(zoneId: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<IRZoneRecord, "id">) => RZoneRecordsService.create(zoneId, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-rzone-records"]});
        }
    });
}

export function useUpdateRZoneRecord(zoneId: string, id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<IRZoneRecord>) => RZoneRecordsService.update(zoneId, id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-rzone-records"]});
            qc.invalidateQueries({queryKey: ["zones-rzone-record", id]});
        }
    });
}

export function useDeleteRZoneRecord(zoneId: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => RZoneRecordsService.remove(zoneId, id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-rzone-records"]});
        }
    });
}
