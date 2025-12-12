import {ModelBase} from "@app/types/models";

export interface AZoneRecord extends ModelBase {
    id?: string;
    tenantId?: string | null;
    zoneId: string;
    viewId?: string | null;
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

export interface AZoneRecordsPaged extends ModelBase {
    records: AZoneRecord[];
    total: number;
    totalFiltered: number;
}

export type IAZoneRecord = AZoneRecord;
export type IAZoneRecordsPaged = AZoneRecordsPaged;