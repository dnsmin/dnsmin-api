import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {AZoneMetadataService} from "@app/features/zones/azone-metadata/service";
import {IAZoneMetadata} from "@app/features/zones/azone-metadata/models";

export function useAZoneMetadata(zoneId: string, id: string) {
    return useQuery({
        queryKey: ["zones-azone-metadata", id],
        queryFn: () => AZoneMetadataService.get(zoneId, id),
        enabled: !!id,
    });
}

export function useAZoneMetadatas(zoneId: string, params?: ListResourceParams) {
    return useQuery({
        queryKey: ["zones-azone-metadatas", params],
        queryFn: () => AZoneMetadataService.search(zoneId, params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateAZoneMetadata(zoneId: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<IAZoneMetadata, "id">) => AZoneMetadataService.create(zoneId, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-azone-metadatas"]});
        }
    });
}

export function useUpdateAZoneMetadata(zoneId: string, id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<IAZoneMetadata>) => AZoneMetadataService.update(zoneId, id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-azone-metadatas"]});
            qc.invalidateQueries({queryKey: ["zones-azone-metadata", id]});
        }
    });
}

export function useDeleteAZoneMetadata(zoneId: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => AZoneMetadataService.remove(zoneId, id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-azone-metadatas"]});
        }
    });
}
