import {http} from "@app/utils/http";
import {ListResourceParams} from "@app/types/api";
import {timezoneFromDTO, timezonesPagedFromDTO, timezoneToDTO} from "@app/features/system/timezones/converters";
import {ITimezoneInDTO, ITimezonesPagedResponseDTO} from "@app/features/system/timezones/dto";
import {ITimezone, ITimezonesPaged} from "@app/features/system/timezones/models";

export const SystemTimezonesService = {
    async list(req?: ListResourceParams): Promise<ITimezonesPaged> {
        const params = req !== undefined ? {
            filterModel: req.filterModel,
            sortModel: req.sortModel,
            paginationModel: req.paginationModel,
        } : {};

        const response = await http.post<ITimezonesPagedResponseDTO>(
            "/system/timezones", params
        );

        return timezonesPagedFromDTO(response.data);
    },

    async get(id: string): Promise<ITimezone> {
        const response = await http.get<ITimezoneInDTO>(`/system/timezones/${id}`);
        return timezoneFromDTO(response.data);
    },

    async create(payload: Omit<ITimezone, "id">): Promise<ITimezone> {
        const dtoPayload = timezoneToDTO(payload as ITimezone);
        const response = await http.post<ITimezoneInDTO>("/system/timezones/create", dtoPayload);
        return timezoneFromDTO(response.data);
    },

    async update(id: string, payload: Partial<ITimezone>): Promise<ITimezone> {
        const dtoPayload = timezoneToDTO(payload as ITimezone);
        const response = await http.put<ITimezoneInDTO>(`/system/timezones/${id}`, dtoPayload);
        return timezoneFromDTO(response.data);
    },

    async remove(id: string): Promise<void> {
        await http.delete(`/system/timezones/${id}`);
    },
};