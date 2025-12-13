import {IAZoneRecordInDTO, IAZoneRecordOutDTO, IAZoneRecordsPagedResponseDTO} from "@app/features/zones/azone-records/dto";
import {IAZoneRecord, IAZoneRecordsPaged} from "@app/features/zones/azone-records/models";

export function recordFromDTO(dto: IAZoneRecordInDTO): IAZoneRecord {
    return {
        id: dto.id,
        tenantId: dto.tenant_id,
        zoneId: dto.zone_id,
        viewId: dto.view_id,
        name: dto.name,
        type: dto.type,
        ttl: dto.ttl,
        content: dto.content,
        comment: dto.comment,
        disabled: dto.disabled,
        modifiedAt: dto.modified_at,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
    }
}

export function recordToDTO(record: IAZoneRecord): IAZoneRecordOutDTO {
    return {
        id: record.id,
        tenant_id: record.tenantId,
        zone_id: record.zoneId,
        view_id: record.viewId,
        name: record.name,
        type: record.type,
        ttl: record.ttl,
        content: record.content,
        comment: record.comment,
        disabled: record.disabled,
    }
}

export function recordsPagedFromDTO(dto: IAZoneRecordsPagedResponseDTO): IAZoneRecordsPaged {
    return {
        records: dto.records.map(recordFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}