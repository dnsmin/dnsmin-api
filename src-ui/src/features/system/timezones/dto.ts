import {BaseDTO} from "@app/types/dto";

export interface TimezoneInDTO extends BaseDTO {
    id: string;
    name: string;
    offset: number;
    offset_dst: number;
    created_at: string;
    updated_at: string | null;
}

export interface TimezoneOutDTO extends BaseDTO {
    id?: string;
    name: string;
    offset: number;
    offset_dst: number;
}

export interface TimezonesPagedResponseDTO extends BaseDTO {
    records: TimezoneInDTO[];
    total: number;
    total_filtered: number;
}

export type ITimezoneInDTO = TimezoneInDTO;
export type ITimezoneOutDTO = TimezoneOutDTO;
export type ITimezonesPagedResponseDTO = TimezonesPagedResponseDTO;