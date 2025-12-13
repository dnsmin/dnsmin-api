import {http} from "@app/utils/http";
import {ListResourceParams} from "@app/types/api";
import {principalFromDTO, principalsPagedFromDTO, principalToDTO} from "@app/features/acl/principals/converters";
import {IAclPrincipalInDTO, IAclPrincipalsPagedResponseDTO} from "@app/features/acl/principals/dto";
import {IAclPrincipal, IAclPrincipalsPaged} from "@app/features/acl/principals/models";

export const AclPrincipalsService = {
    async list(req?: ListResourceParams): Promise<IAclPrincipalsPaged> {
        const params = req !== undefined ? {
            filterModel: req.filterModel,
            sortModel: req.sortModel,
            paginationModel: req.paginationModel,
        } : {};

        const response = await http.post<IAclPrincipalsPagedResponseDTO>(
            "/acl/principals", params
        );

        return principalsPagedFromDTO(response.data);
    },

    async get(id: string): Promise<IAclPrincipal> {
        const response = await http.get<IAclPrincipalInDTO>(`/acl/principals/${id}`);
        return principalFromDTO(response.data);
    },

    async create(payload: Omit<IAclPrincipal, "id">): Promise<IAclPrincipal> {
        const dtoPayload = principalToDTO(payload as IAclPrincipal);
        const response = await http.post<IAclPrincipalInDTO>("/acl/principals/create", dtoPayload);
        return principalFromDTO(response.data);
    },

    async remove(id: string): Promise<void> {
        await http.delete(`/acl/principals/${id}`);
    },
};