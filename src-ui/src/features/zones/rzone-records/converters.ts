import {IRZoneRecordInDTO, IRZoneRecordOutDTO, IRZoneRecordsPagedResponseDTO} from "@app/features/zones/rzone-records/dto";
import {IRZoneRecord, IRZoneRecordsPaged} from "@app/features/zones/rzone-records/models";

export function recordFromDTO(dto: IRZoneRecordInDTO): IRZoneRecord {
    return {
        id: dto.id,
        tenantId: dto.tenant_id,
        zoneId: dto.zone_id,
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

export function recordToDTO(record: IRZoneRecord): IRZoneRecordOutDTO {
    return {
        id: record.id,
        tenant_id: record.tenantId,
        zone_id: record.zoneId,
        name: record.name,
        type: record.type,
        ttl: record.ttl,
        content: record.content,
        comment: record.comment,
        disabled: record.disabled,
    }
}

export function recordsPagedFromDTO(dto: IRZoneRecordsPagedResponseDTO): IRZoneRecordsPaged {
    return {
        records: dto.records.map(recordFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}