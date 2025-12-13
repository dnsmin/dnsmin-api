import {http} from "@app/utils/http";
import {ListResourceParams} from "@app/types/api";
import {recordFromDTO, recordsPagedFromDTO, recordToDTO} from "@app/features/zones/rzone-records/converters";
import {IRZoneRecordInDTO, IRZoneRecordsPagedResponseDTO} from "@app/features/zones/rzone-records/dto";
import {IRZoneRecord, IRZoneRecordsPaged} from "@app/features/zones/rzone-records/models";

export const RZoneRecordsService = {
    async list(zoneId: string, req?: ListResourceParams): Promise<IRZoneRecordsPaged> {
        const params = req !== undefined ? {
            filterModel: req.filterModel,
            sortModel: req.sortModel,
            paginationModel: req.paginationModel,
        } : {};

        const response = await http.post<IRZoneRecordsPagedResponseDTO>(
            `/records/recursive/${zoneId}/records`, params
        );

        return recordsPagedFromDTO(response.data);
    },

    async get(zoneId: string, id: string): Promise<IRZoneRecord> {
        const response = await http.get<IRZoneRecordInDTO>(`/records/recursive/${zoneId}/records/${id}`);
        return recordFromDTO(response.data);
    },

    async create(zoneId: string, payload: Omit<IRZoneRecord, "id">): Promise<IRZoneRecord> {
        const dtoPayload = recordToDTO(payload as IRZoneRecord);
        const response = await http.post<IRZoneRecordInDTO>(`/records/recursive/${zoneId}/records/create`, dtoPayload);
        return recordFromDTO(response.data);
    },

    async update(zoneId: string, id: string, payload: Partial<IRZoneRecord>): Promise<IRZoneRecord> {
        const dtoPayload = recordToDTO(payload as IRZoneRecord);
        const response = await http.put<IRZoneRecordInDTO>(`/records/recursive/${zoneId}/records/${id}`, dtoPayload);
        return recordFromDTO(response.data);
    },

    async remove(zoneId: string, id: string): Promise<void> {
        await http.delete(`/records/recursive/${zoneId}/records/${id}`);
    },
};