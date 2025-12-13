import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {AclPrincipalsService} from "@app/features/acl/principals/service";
import {IAclPrincipal} from "@app/features/acl/principals/models";

export function useAclPrincipal(id: string) {
    return useQuery({
        queryKey: ["acl-principal", id],
        queryFn: () => AclPrincipalsService.get(id),
        enabled: !!id,
    });
}

export function useAclPrincipals(params?: ListResourceParams) {
    return useQuery({
        queryKey: ["acl-principals", params],
        queryFn: () => AclPrincipalsService.list(params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateAclPrincipal() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<IAclPrincipal, "id">) => AclPrincipalsService.create(payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["acl-principals"]});
        }
    });
}

export function useDeleteAclPrincipal() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => AclPrincipalsService.remove(id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["acl-principals"]});
        }
    });
}
