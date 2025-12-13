import {http} from "@app/utils/http";
import {ListResourceParams} from "@app/types/api";
import {tenantFromDTO, tenantsPagedFromDTO, tenantToDTO} from "@app/features/tenants/tenants/converters";
import {ITenantInDTO, ITenantsPagedResponseDTO} from "@app/features/tenants/tenants/dto";
import {ITenant, ITenantsPaged} from "@app/features/tenants/tenants/models";

export const TenantsService = {
    async list(req?: ListResourceParams): Promise<ITenantsPaged> {
        const params = req !== undefined ? {
            filterModel: req.filterModel,
            sortModel: req.sortModel,
            paginationModel: req.paginationModel,
        } : {};

        const response = await http.post<ITenantsPagedResponseDTO>(
            "/tenants/tenants", params
        );

        return tenantsPagedFromDTO(response.data);
    },

    async get(id: string): Promise<ITenant> {
        const response = await http.get<ITenantInDTO>(`/tenants/tenants/${id}`);
        return tenantFromDTO(response.data);
    },

    async create(payload: Omit<ITenant, "id">): Promise<ITenant> {
        const dtoPayload = tenantToDTO(payload as ITenant);
        const response = await http.post<ITenantInDTO>("/tenants/tenants/create", dtoPayload);
        return tenantFromDTO(response.data);
    },

    async update(id: string, payload: Partial<ITenant>): Promise<ITenant> {
        const dtoPayload = tenantToDTO(payload as ITenant);
        const response = await http.put<ITenantInDTO>(`/tenants/tenants/${id}`, dtoPayload);
        return tenantFromDTO(response.data);
    },

    async remove(id: string): Promise<void> {
        await http.delete(`/tenants/tenants/${id}`);
    },
};