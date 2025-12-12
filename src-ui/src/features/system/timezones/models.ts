import {ModelBase} from "@app/types/models";

export interface Timezone extends ModelBase {
    id?: string;
    name: string;
    offset: number;
    offsetDst: number;
    createdAt?: string | null;
    updatedAt?: string | null;
}

export interface TimezonesPaged extends ModelBase {
    records: Timezone[];
    total: number;
    totalFiltered: number;
}

export type ITimezone = Timezone;
export type ITimezonesPaged = TimezonesPaged;