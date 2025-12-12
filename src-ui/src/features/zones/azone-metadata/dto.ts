import {BaseDTO} from "@app/types/dto";

export interface AZoneMetadataInDTO extends BaseDTO {
    id: string;
    tenant_id: string | null;
    zone_id: string;
    view_id: string | null;
    name: string;
    values: string[] | null;
    created_at: string;
    updated_at: string | null;
}

export interface AZoneMetadataOutDTO extends BaseDTO {
    id?: string;
    tenant_id?: string | null;
    zone_id: string;
    view_id?: string | null;
    name: string;
    values?: string[] | null;
}

export interface AZoneMetadataPagedResponseDTO extends BaseDTO {
    records: AZoneMetadataInDTO[];
    total: number;
    total_filtered: number;
}

export type IAZoneMetadataInDTO = AZoneMetadataInDTO;
export type IAZoneMetadataOutDTO = AZoneMetadataOutDTO;
export type IAZoneMetadataPagedResponseDTO = AZoneMetadataPagedResponseDTO;