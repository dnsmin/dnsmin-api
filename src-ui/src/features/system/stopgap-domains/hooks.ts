import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {SystemStopgapDomainsService} from "@app/features/system/stopgap-domains/service";
import {IStopgapDomain} from "@app/features/system/stopgap-domains/models";

export function useSystemStopgapDomain(id: string) {
    return useQuery({
        queryKey: ["system-stopgap-domain", id],
        queryFn: () => SystemStopgapDomainsService.get(id),
        enabled: !!id,
    });
}

export function useSystemStopgapDomains(params?: ListResourceParams) {
    return useQuery({
        queryKey: ["system-stopgap-domains", params],
        queryFn: () => SystemStopgapDomainsService.search(params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateSystemStopgapDomain() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<IStopgapDomain, "id">) => SystemStopgapDomainsService.create(payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["system-stopgap-domains"]});
        }
    });
}

export function useUpdateSystemStopgapDomain(id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<IStopgapDomain>) => SystemStopgapDomainsService.update(id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["system-stopgap-domains"]});
            qc.invalidateQueries({queryKey: ["system-stopgap-domain", id]});
        }
    });
}

export function useDeleteSystemStopgapDomain() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => SystemStopgapDomainsService.remove(id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["system-stopgap-domains"]});
        }
    });
}
