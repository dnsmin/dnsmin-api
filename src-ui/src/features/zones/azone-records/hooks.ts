import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {AZoneRecordsService} from "@app/features/zones/azone-records/service";
import {IAZoneRecord} from "@app/features/zones/azone-records/models";

export function useAZoneRecord(zoneId: string, id: string) {
    return useQuery({
        queryKey: ["zones-azone-record", id],
        queryFn: () => AZoneRecordsService.get(zoneId, id),
        enabled: !!id,
    });
}

export function useAZoneRecords(zoneId: string, params?: ListResourceParams) {
    return useQuery({
        queryKey: ["zones-azone-records", params],
        queryFn: () => AZoneRecordsService.list(zoneId, params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateAZoneRecord(zoneId: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<IAZoneRecord, "id">) => AZoneRecordsService.create(zoneId, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-azone-records"]});
        }
    });
}

export function useUpdateAZoneRecord(zoneId: string, id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<IAZoneRecord>) => AZoneRecordsService.update(zoneId, id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-azone-records"]});
            qc.invalidateQueries({queryKey: ["zones-azone-record", id]});
        }
    });
}

export function useDeleteAZoneRecord(zoneId: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => AZoneRecordsService.remove(zoneId, id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-azone-records"]});
        }
    });
}
