import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {AZoneCryptoKeysService} from "@app/features/zones/azone-crypto-keys/service";
import {IAZoneCryptoKey} from "@app/features/zones/azone-crypto-keys/models";

export function useAZoneCryptoKey(zoneId: string, id: string) {
    return useQuery({
        queryKey: ["zones-azone-crypto-key", id],
        queryFn: () => AZoneCryptoKeysService.get(zoneId, id),
        enabled: !!id,
    });
}

export function useAZoneCryptoKeys(zoneId: string, params?: ListResourceParams) {
    return useQuery({
        queryKey: ["zones-azone-crypto-keys", params],
        queryFn: () => AZoneCryptoKeysService.search(zoneId, params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateAZoneCryptoKey(zoneId: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<IAZoneCryptoKey, "id">) => AZoneCryptoKeysService.create(zoneId, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-azone-crypto-keys"]});
        }
    });
}

export function useUpdateAZoneCryptoKey(zoneId: string, id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<IAZoneCryptoKey>) => AZoneCryptoKeysService.update(zoneId, id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-azone-crypto-keys"]});
            qc.invalidateQueries({queryKey: ["zones-azone-crypto-key", id]});
        }
    });
}

export function useDeleteAZoneCryptoKey(zoneId: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => AZoneCryptoKeysService.remove(zoneId, id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["zones-azone-crypto-keys"]});
        }
    });
}
