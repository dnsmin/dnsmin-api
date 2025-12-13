import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {AclPoliciesService} from "@app/features/acl/policies/service";
import {IAclPolicy} from "@app/features/acl/policies/models";

export function useAclPolicy(id: string) {
    return useQuery({
        queryKey: ["acl-policy", id],
        queryFn: () => AclPoliciesService.get(id),
        enabled: !!id,
    });
}

export function useAclPolicies(params?: ListResourceParams) {
    return useQuery({
        queryKey: ["acl-policies", params],
        queryFn: () => AclPoliciesService.list(params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateAclPolicy() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<IAclPolicy, "id">) => AclPoliciesService.create(payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["acl-policies"]});
        }
    });
}

export function useUpdateAclPolicy(id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<IAclPolicy>) => AclPoliciesService.update(id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["acl-policies"]});
            qc.invalidateQueries({queryKey: ["acl-policy", id]});
        }
    });
}

export function useDeleteAclPolicy() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => AclPoliciesService.remove(id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["acl-policies"]});
        }
    });
}
