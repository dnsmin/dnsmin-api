import {BaseDTO} from "@app/types/dto";

export interface AZoneInDTO extends BaseDTO {
    id: string;
    tenant_id: string | null;
    view_id: string | null;
    fqdn: string;
    kind: string;
    serial: number;
    notified_serial: number | null;
    edited_serial: number | null;
    masters: string[] | null;
    dnssec: boolean;
    nsec3param: string | null;
    nsec3narrow: boolean | null;
    presigned: boolean | null;
    soa_edit: string | null;
    soa_edit_api: string | null;
    api_rectify: boolean | null;
    zone: string | null;
    catalog: string | null;
    account: string | null;
    master_tsig_key_ids: string[] | null;
    slave_tsig_key_ids: string[] | null;
    shared: boolean;
    created_at: string;
    updated_at: string | null;
}

export interface AZoneOutDTO extends BaseDTO {
    id?: string;
    tenant_id?: string | null;
    view_id?: string | null;
    fqdn: string;
    kind: string;
    serial: number;
    notified_serial?: number | null;
    edited_serial?: number | null;
    masters?: string[] | null;
    dnssec: boolean;
    nsec3param?: string | null;
    nsec3narrow?: boolean | null;
    presigned?: boolean | null;
    soa_edit?: string | null;
    soa_edit_api?: string | null;
    api_rectify?: boolean | null;
    zone?: string | null;
    catalog?: string | null;
    account?: string | null;
    master_tsig_key_ids?: string[] | null;
    slave_tsig_key_ids?: string[] | null;
    shared: boolean;
}

export interface AZonesPagedResponseDTO extends BaseDTO {
    records: AZoneInDTO[];
    total: number;
    total_filtered: number;
}

export type IAZoneInDTO = AZoneInDTO;
export type IAZoneOutDTO = AZoneOutDTO;
export type IAZonesPagedResponseDTO = AZonesPagedResponseDTO;