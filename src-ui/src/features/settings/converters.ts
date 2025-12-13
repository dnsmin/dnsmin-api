import {ISettingInDTO, ISettingOutDTO, ISettingsPagedResponseDTO} from "@app/features/settings/dto";
import {ISetting, ISettingsPaged} from "@app/features/settings/models";

export function settingFromDTO(dto: ISettingInDTO): ISetting {
    return {
        id: dto.id,
        tenantId: dto.tenant_id,
        userId: dto.user_id,
        key: dto.key,
        value: dto.value,
        overridable: dto.overridable,
        hidden: dto.hidden,
        readonly: dto.readonly,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
    }
}

export function settingToDTO(setting: ISetting): ISettingOutDTO {
    return {
        id: setting.id,
        tenant_id: setting.tenantId,
        user_id: setting.userId,
        key: setting.key,
        value: setting.value,
        overridable: setting.overridable,
        hidden: setting.hidden,
        readonly: setting.readonly,
    }
}

export function settingsPagedFromDTO(dto: ISettingsPagedResponseDTO): ISettingsPaged {
    return {
        records: dto.records.map(settingFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}