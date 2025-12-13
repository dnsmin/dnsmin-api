import {BaseDTO} from "@app/types/dto";

export interface AZoneRecordInDTO extends BaseDTO {
    id: string;
    tenant_id: string | null;
    zone_id: string;
    view_id: string | null;
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

export interface AZoneRecordOutDTO extends BaseDTO {
    id?: string;
    tenant_id?: string | null;
    zone_id: string;
    view_id?: string | null;
    name: string;
    type: string;
    ttl: number;
    content?: string | null;
    comment?: string | null;
    disabled: boolean;
}

export interface AZoneRecordsPagedResponseDTO extends BaseDTO {
    records: AZoneRecordInDTO[];
    total: number;
    total_filtered: number;
}

export type IAZoneRecordInDTO = AZoneRecordInDTO;
export type IAZoneRecordOutDTO = AZoneRecordOutDTO;
export type IAZoneRecordsPagedResponseDTO = AZoneRecordsPagedResponseDTO;