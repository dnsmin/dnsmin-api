import {ModelBase} from "@app/types/models";

export interface Setting extends ModelBase {
    id?: string;
    tenantId?: string | null;
    userId?: string | null;
    key: string;
    value?: any | null;
    overridable: boolean;
    hidden: boolean;
    readonly: boolean;
    createdAt?: string | null;
    updatedAt?: string | null;
}

export interface SettingsPaged extends ModelBase {
    records: Setting[];
    total: number;
    totalFiltered: number;
}

export type ISetting = Setting;
export type ISettingsPaged = SettingsPaged;