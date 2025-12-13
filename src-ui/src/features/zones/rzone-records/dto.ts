import {BaseDTO} from "@app/types/dto";

export interface RZoneRecordInDTO extends BaseDTO {
    id: string;
    tenant_id: string | null;
    zone_id: string;
    name: string;
    type: string;
    ttl: number;
    content: string | null;
    comment: string | null;
    disabled: boolean;
    modified_at: number | null;
    created_at: string;
    updated_at: string | null;
}

export interface RZoneRecordOutDTO extends BaseDTO {
    id?: string;
    tenant_id?: string | null;
    zone_id: string;
    name: string;
    type: string;
    ttl: number;
    content?: string | null;
    comment?: string | null;
    disabled: boolean;
}

export interface RZoneRecordsPagedResponseDTO extends BaseDTO {
    records: RZoneRecordInDTO[];
    total: number;
    total_filtered: number;
}

export type IRZoneRecordInDTO = RZoneRecordInDTO;
export type IRZoneRecordOutDTO = RZoneRecordOutDTO;
export type IRZoneRecordsPagedResponseDTO = RZoneRecordsPagedResponseDTO;