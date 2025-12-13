import {ITimezoneInDTO, ITimezoneOutDTO, ITimezonesPagedResponseDTO} from "@app/features/system/timezones/dto";
import {ITimezone, ITimezonesPaged} from "@app/features/system/timezones/models";

export function timezoneFromDTO(dto: ITimezoneInDTO): ITimezone {
    return {
        id: dto.id,
        name: dto.name,
        offset: dto.offset,
        offsetDst: dto.offset_dst,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
    }
}

export function timezoneToDTO(timezone: ITimezone): ITimezoneOutDTO {
    return {
        id: timezone.id,
        name: timezone.name,
        offset: timezone.offset,
        offset_dst: timezone.offsetDst,
    }
}

export function timezonesPagedFromDTO(dto: ITimezonesPagedResponseDTO): ITimezonesPaged {
    return {
        records: dto.records.map(timezoneFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}