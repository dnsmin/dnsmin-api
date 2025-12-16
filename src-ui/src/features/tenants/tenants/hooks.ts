import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {TenantsService} from "@app/features/tenants/tenants/service";
import {ITenant} from "@app/features/tenants/tenants/models";

export function useTenant(id: string) {
    return useQuery({
        queryKey: ["tenants-tenant", id],
        queryFn: () => TenantsService.get(id),
        enabled: !!id,
    });
}

export function useTenants(params?: ListResourceParams) {
    return useQuery({
        queryKey: ["tenants-tenants", params],
        queryFn: () => TenantsService.search(params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateTenant() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<ITenant, "id">) => TenantsService.create(payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["tenants-tenants"]});
        }
    });
}

export function useUpdateTenant(id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<ITenant>) => TenantsService.update(id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["tenants-tenants"]});
            qc.invalidateQueries({queryKey: ["tenants-tenant", id]});
        }
    });
}

export function useDeleteTenant() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => TenantsService.remove(id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["tenants-tenants"]});
        }
    });
}
