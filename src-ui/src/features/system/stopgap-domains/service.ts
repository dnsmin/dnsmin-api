import {http} from "@app/utils/http";
import {ListResourceParams} from "@app/types/api";
import {stopgapDomainFromDTO, stopgapDomainsPagedFromDTO, stopgapDomainToDTO} from "@app/features/system/stopgap-domains/converters";
import {IStopgapDomainInDTO, IStopgapDomainsPagedResponseDTO} from "@app/features/system/stopgap-domains/dto";
import {IStopgapDomain, IStopgapDomainsPaged} from "@app/features/system/stopgap-domains/models";

export const SystemStopgapDomainsService = {
    async list(req?: ListResourceParams): Promise<IStopgapDomainsPaged> {
        const params = req !== undefined ? {
            filterModel: req.filterModel,
            sortModel: req.sortModel,
            paginationModel: req.paginationModel,
        } : {};

        const response = await http.post<IStopgapDomainsPagedResponseDTO>(
            "/system/stopgap-domains", params
        );

        return stopgapDomainsPagedFromDTO(response.data);
    },

    async get(id: string): Promise<IStopgapDomain> {
        const response = await http.get<IStopgapDomainInDTO>(`/system/stopgap-domains/${id}`);
        return stopgapDomainFromDTO(response.data);
    },

    async create(payload: Omit<IStopgapDomain, "id">): Promise<IStopgapDomain> {
        const dtoPayload = stopgapDomainToDTO(payload as IStopgapDomain);
        const response = await http.post<IStopgapDomainInDTO>("/system/stopgap-domains/create", dtoPayload);
        return stopgapDomainFromDTO(response.data);
    },

    async update(id: string, payload: Partial<IStopgapDomain>): Promise<IStopgapDomain> {
        const dtoPayload = stopgapDomainToDTO(payload as IStopgapDomain);
        const response = await http.put<IStopgapDomainInDTO>(`/system/stopgap-domains/${id}`, dtoPayload);
        return stopgapDomainFromDTO(response.data);
    },

    async remove(id: string): Promise<void> {
        await http.delete(`/system/stopgap-domains/${id}`);
    },
};