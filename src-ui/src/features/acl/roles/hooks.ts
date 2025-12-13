import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {AclRolesService} from "@app/features/acl/roles/service";
import {IAclRole} from "@app/features/acl/roles/models";

export function useAclRole(id: string) {
    return useQuery({
        queryKey: ["acl-role", id],
        queryFn: () => AclRolesService.get(id),
        enabled: !!id,
    });
}

export function useAclRoles(params?: ListResourceParams) {
    return useQuery({
        queryKey: ["acl-roles", params],
        queryFn: () => AclRolesService.list(params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateAclRole() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<IAclRole, "id">) => AclRolesService.create(payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["acl-roles"]});
        }
    });
}

export function useUpdateAclRole(id: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<IAclRole>) => AclRolesService.update(id, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["acl-roles"]});
            qc.invalidateQueries({queryKey: ["acl-role", id]});
        }
    });
}

export function useDeleteAclRole() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (id: string) => AclRolesService.remove(id),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["acl-roles"]});
        }
    });
}
