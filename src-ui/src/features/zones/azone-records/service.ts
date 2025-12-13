import {http} from "@app/utils/http";
import {ListResourceParams} from "@app/types/api";
import {recordFromDTO, recordsPagedFromDTO, recordToDTO} from "@app/features/zones/azone-records/converters";
import {IAZoneRecordInDTO, IAZoneRecordsPagedResponseDTO} from "@app/features/zones/azone-records/dto";
import {IAZoneRecord, IAZoneRecordsPaged} from "@app/features/zones/azone-records/models";

export const AZoneRecordRecordsService = {
    async list(zoneId: string, req?: ListResourceParams): Promise<IAZoneRecordsPaged> {
        const params = req !== undefined ? {
            filterModel: req.filterModel,
            sortModel: req.sortModel,
            paginationModel: req.paginationModel,
        } : {};

        const response = await http.post<IAZoneRecordsPagedResponseDTO>(
            `/records/authoritative/${zoneId}/records`, params
        );

        return recordsPagedFromDTO(response.data);
    },

    async get(zoneId: string, id: string): Promise<IAZoneRecord> {
        const response = await http.get<IAZoneRecordInDTO>(`/records/authoritative/${zoneId}/records/${id}`);
        return recordFromDTO(response.data);
    },

    async create(zoneId: string, payload: Omit<IAZoneRecord, "id">): Promise<IAZoneRecord> {
        const dtoPayload = recordToDTO(payload as IAZoneRecord);
        const response = await http.post<IAZoneRecordInDTO>(`/records/authoritative/${zoneId}/records/create`, dtoPayload);
        return recordFromDTO(response.data);
    },

    async update(zoneId: string, id: string, payload: Partial<IAZoneRecord>): Promise<IAZoneRecord> {
        const dtoPayload = recordToDTO(payload as IAZoneRecord);
        const response = await http.put<IAZoneRecordInDTO>(`/records/authoritative/${zoneId}/records/${id}`, dtoPayload);
        return recordFromDTO(response.data);
    },

    async remove(zoneId: string, id: string): Promise<void> {
        await http.delete(`/records/authoritative/${zoneId}/records/${id}`);
    },
};