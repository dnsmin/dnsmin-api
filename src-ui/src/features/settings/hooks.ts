import {useQuery, useQueryClient, useMutation} from "@tanstack/react-query";
import {ListResourceParams} from "@app/types/api";
import {SettingsService} from "@app/features/settings/service";
import {ISetting} from "@app/features/settings/models";

export function useSetting(key: string) {
    return useQuery({
        queryKey: ["setting", key],
        queryFn: () => SettingsService.get(key),
        enabled: !!key,
    });
}

export function useSettings(params?: ListResourceParams) {
    return useQuery({
        queryKey: ["settings", params],
        queryFn: () => SettingsService.list(params),
        placeholderData: (previousData) => previousData,
    });
}

export function useCreateSetting() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Omit<ISetting, "id">) => SettingsService.create(payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["settings"]});
        }
    });
}

export function useUpdateSetting(key: string) {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (payload: Partial<ISetting>) => SettingsService.update(key, payload),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["settings"]});
            qc.invalidateQueries({queryKey: ["setting", key]});
        }
    });
}

export function useDeleteSetting() {
    const qc = useQueryClient();

    return useMutation({
        mutationFn: (key: string) => SettingsService.remove(key),
        onSuccess: () => {
            qc.invalidateQueries({queryKey: ["settings"]});
        }
    });
}
