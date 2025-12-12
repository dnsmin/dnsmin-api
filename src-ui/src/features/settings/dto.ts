import {BaseDTO} from "@app/types/dto";

export interface SettingInDTO extends BaseDTO {
    id: string;
    tenant_id: string | null;
    user_id: string | null;
    key: string;
    value: any | null;
    overridable: boolean;
    hidden: boolean;
    readonly: boolean;
    created_at: string;
    updated_at: string | null;
}

export interface SettingOutDTO extends BaseDTO {
    id?: string;
    tenant_id: string | null;
    user_id: string | null;
    key: string;
    value?: any | null;
    overridable: boolean;
    hidden: boolean;
    readonly: boolean;
}

export interface SettingsPagedResponseDTO extends BaseDTO {
    records: SettingInDTO[];
    total: number;
    total_filtered: number;
}

export type ISettingInDTO = SettingInDTO;
export type ISettingOutDTO = SettingOutDTO;
export type ISettingsPagedResponseDTO = SettingsPagedResponseDTO;