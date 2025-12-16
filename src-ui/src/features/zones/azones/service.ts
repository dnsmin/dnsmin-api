import {http} from "@app/utils/http";
import {ListResourceParams} from "@app/types/api";
import {zoneFromDTO, zonesPagedFromDTO, zoneToDTO} from "@app/features/zones/azones/converters";
import {IAZoneInDTO, IAZonesPagedResponseDTO} from "@app/features/zones/azones/dto";
import {IAZone, IAZonesPaged} from "@app/features/zones/azones/models";

export const AZonesService = {
    async search(req?: ListResourceParams): Promise<IAZonesPaged> {
        const params = req !== undefined ? {
            filterModel: req.filterModel,
            sortModel: req.sortModel,
            paginationModel: req.paginationModel,
        } : {};

        const response = await http.post<IAZonesPagedResponseDTO>(
            "/zones/authoritative/search", params
        );

        return zonesPagedFromDTO(response.data);
    },

    async get(id: string): Promise<IAZone> {
        const response = await http.get<IAZoneInDTO>(`/zones/authoritative/${id}`);
        return zoneFromDTO(response.data);
    },

    async create(payload: Omit<IAZone, "id">): Promise<IAZone> {
        const dtoPayload = zoneToDTO(payload as IAZone);
        const response = await http.post<IAZoneInDTO>("/zones/authoritative", dtoPayload);
        return zoneFromDTO(response.data);
    },

    async update(id: string, payload: Partial<IAZone>): Promise<IAZone> {
        const dtoPayload = zoneToDTO(payload as IAZone);
        const response = await http.put<IAZoneInDTO>(`/zones/authoritative/${id}`, dtoPayload);
        return zoneFromDTO(response.data);
    },

    async remove(id: string): Promise<void> {
        await http.delete(`/zones/authoritative/${id}`);
    },
};