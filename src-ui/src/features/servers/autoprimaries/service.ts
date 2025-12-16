import {http} from "@app/utils/http";
import {ListResourceParams} from "@app/types/api";
import {autoPrimaryFromDTO, autoPrimariesPagedFromDTO, autoPrimaryToDTO} from "@app/features/servers/autoprimaries/converters";
import {IServerAutoPrimaryInDTO, IServerAutoPrimariesPagedResponseDTO} from "@app/features/servers/autoprimaries/dto";
import {IServerAutoPrimary, IServerAutoPrimariesPaged} from "@app/features/servers/autoprimaries/models";

export const ServerAutoPrimariesService = {
    async search(serverId: string, req?: ListResourceParams): Promise<IServerAutoPrimariesPaged> {
        const params = req !== undefined ? {
            filterModel: req.filterModel,
            sortModel: req.sortModel,
            paginationModel: req.paginationModel,
        } : {};

        const response = await http.post<IServerAutoPrimariesPagedResponseDTO>(
            `/servers/${serverId}/auto-primaries/search`, params
        );

        return autoPrimariesPagedFromDTO(response.data);
    },

    async get(serverId: string, id: string): Promise<IServerAutoPrimary> {
        const response = await http.get<IServerAutoPrimaryInDTO>(`/servers/${serverId}/auto-primaries/${id}`);
        return autoPrimaryFromDTO(response.data);
    },

    async create(serverId: string, payload: Omit<IServerAutoPrimary, "id">): Promise<IServerAutoPrimary> {
        const dtoPayload = autoPrimaryToDTO(payload as IServerAutoPrimary);
        const response = await http.post<IServerAutoPrimaryInDTO>(`/servers/${serverId}/auto-primaries`, dtoPayload);
        return autoPrimaryFromDTO(response.data);
    },

    async update(serverId: string, id: string, payload: Partial<IServerAutoPrimary>): Promise<IServerAutoPrimary> {
        const dtoPayload = autoPrimaryToDTO(payload as IServerAutoPrimary);
        const response = await http.put<IServerAutoPrimaryInDTO>(`/servers/${serverId}/auto-primaries/${id}`, dtoPayload);
        return autoPrimaryFromDTO(response.data);
    },

    async remove(serverId: string, id: string): Promise<void> {
        await http.delete(`/servers/${serverId}/auto-primaries/${id}`);
    },
};