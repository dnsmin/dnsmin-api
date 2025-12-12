import {ModelBase} from "@app/types/models";

export interface RZoneRecord extends ModelBase {
    id?: string;
    tenantId?: string | null;
    zoneId: string;
    name: string;
    type: string;
    ttl: number;
    content?: string | null;
    comment?: string | null;
    disabled: boolean;
    modifiedAt?: number | null;
    createdAt?: string | null;
    updatedAt?: string | null;
}

export interface RZoneRecordsPaged extends ModelBase {
    records: RZoneRecord[];
    total: number;
    totalFiltered: number;
}

export type IRZoneRecord = RZoneRecord;
export type IRZoneRecordsPaged = RZoneRecordsPaged;