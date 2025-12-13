import {http} from "@app/utils/http";
import {ListResourceParams} from "@app/types/api";
import {sessionFromDTO, sessionsPagedFromDTO} from "@app/features/auth/sessions/converters";
import {ISessionInDTO, ISessionsPagedResponseDTO} from "@app/features/auth/sessions/dto";
import {ISession, ISessionsPaged} from "@app/features/auth/sessions/models";

export const AuthSessionsService = {
    async list(req?: ListResourceParams): Promise<ISessionsPaged> {
        const params = req !== undefined ? {
            filterModel: req.filterModel,
            sortModel: req.sortModel,
            paginationModel: req.paginationModel,
        } : {};

        const response = await http.post<ISessionsPagedResponseDTO>(
            "/auth/sessions", params
        );

        return sessionsPagedFromDTO(response.data);
    },

    async get(id: string): Promise<ISession> {
        const response = await http.get<ISessionInDTO>(`/auth/sessions/${id}`);
        return sessionFromDTO(response.data);
    },

    async remove(id: string): Promise<void> {
        await http.delete(`/auth/sessions/${id}`);
    },
};