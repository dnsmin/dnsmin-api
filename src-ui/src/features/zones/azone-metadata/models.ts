import {ModelBase} from "@app/types/models";

export interface AZoneMetadata extends ModelBase {
    id?: string;
    tenantId?: string | null;
    zoneId: string;
    viewId?: string | null;
    name: string;
    values?: string[] | null;
    createdAt?: string | null;
    updatedAt?: string | null;
}

export interface AZoneMetadataPaged extends ModelBase {
    records: AZoneMetadata[];
    total: number;
    totalFiltered: number;
}

export type IAZoneMetadata = AZoneMetadata;
export type IAZoneMetadataPaged = AZoneMetadataPaged;