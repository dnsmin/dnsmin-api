import {http} from "@app/utils/http";
import {ListResourceParams} from "@app/types/api";
import {viewFromDTO, viewsPagedFromDTO, viewToDTO} from "@app/features/servers/views/converters";
import {IServerViewInDTO, IServerViewsPagedResponseDTO} from "@app/features/servers/views/dto";
import {IServerView, IServerViewsPaged} from "@app/features/servers/views/models";

export const ServerViewsService = {
    async list(serverId: string, req?: ListResourceParams): Promise<IServerViewsPaged> {
        const params = req !== undefined ? {
            filterModel: req.filterModel,
            sortModel: req.sortModel,
            paginationModel: req.paginationModel,
        } : {};

        const response = await http.post<IServerViewsPagedResponseDTO>(
            `/servers/${serverId}/views`, params
        );

        return viewsPagedFromDTO(response.data);
    },

    async get(serverId: string, id: string): Promise<IServerView> {
        const response = await http.get<IServerViewInDTO>(`/servers/${serverId}/views/${id}`);
        return viewFromDTO(response.data);
    },

    async create(serverId: string, payload: Omit<IServerView, "id">): Promise<IServerView> {
        const dtoPayload = viewToDTO(payload as IServerView);
        const response = await http.post<IServerViewInDTO>(`/servers/${serverId}/views/create`, dtoPayload);
        return viewFromDTO(response.data);
    },

    async update(serverId: string, id: string, payload: Partial<IServerView>): Promise<IServerView> {
        const dtoPayload = viewToDTO(payload as IServerView);
        const response = await http.put<IServerViewInDTO>(`/servers/${serverId}/views/${id}`, dtoPayload);
        return viewFromDTO(response.data);
    },

    async remove(serverId: string, id: string): Promise<void> {
        await http.delete(`/servers/${serverId}/views/${id}`);
    },
};