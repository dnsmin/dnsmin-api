import {http} from "@app/utils/http";
import {ListResourceParams} from "@app/types/api";
import {metadataFromDTO, metadataPagedFromDTO, metadataToDTO} from "@app/features/zones/azone-metadata/converters";
import {IAZoneMetadataInDTO, IAZoneMetadataPagedResponseDTO} from "@app/features/zones/azone-metadata/dto";
import {IAZoneMetadata, IAZoneMetadataPaged} from "@app/features/zones/azone-metadata/models";

export const AZoneMetadataService = {
    async search(zoneId: string, req?: ListResourceParams): Promise<IAZoneMetadataPaged> {
        const params = req !== undefined ? {
            filterModel: req.filterModel,
            sortModel: req.sortModel,
            paginationModel: req.paginationModel,
        } : {};

        const response = await http.post<IAZoneMetadataPagedResponseDTO>(
            `/metadata/authoritative/${zoneId}/metadata/search`, params
        );

        return metadataPagedFromDTO(response.data);
    },

    async get(zoneId: string, id: string): Promise<IAZoneMetadata> {
        const response = await http.get<IAZoneMetadataInDTO>(`/metadata/authoritative/${zoneId}/metadata/${id}`);
        return metadataFromDTO(response.data);
    },

    async create(zoneId: string, payload: Omit<IAZoneMetadata, "id">): Promise<IAZoneMetadata> {
        const dtoPayload = metadataToDTO(payload as IAZoneMetadata);
        const response = await http.post<IAZoneMetadataInDTO>(`/metadata/authoritative/${zoneId}/metadata`, dtoPayload);
        return metadataFromDTO(response.data);
    },

    async update(zoneId: string, id: string, payload: Partial<IAZoneMetadata>): Promise<IAZoneMetadata> {
        const dtoPayload = metadataToDTO(payload as IAZoneMetadata);
        const response = await http.put<IAZoneMetadataInDTO>(`/metadata/authoritative/${zoneId}/metadata/${id}`, dtoPayload);
        return metadataFromDTO(response.data);
    },

    async remove(zoneId: string, id: string): Promise<void> {
        await http.delete(`/metadata/authoritative/${zoneId}/metadata/${id}`);
    },
};