import {IAZoneMetadataInDTO, IAZoneMetadataOutDTO, IAZoneMetadataPagedResponseDTO} from "@app/features/zones/azone-metadata/dto";
import {IAZoneMetadata, IAZoneMetadataPaged} from "@app/features/zones/azone-metadata/models";

export function metadataFromDTO(dto: IAZoneMetadataInDTO): IAZoneMetadata {
    return {
        id: dto.id,
        tenantId: dto.tenant_id,
        zoneId: dto.zone_id,
        viewId: dto.view_id,
        name: dto.name,
        values: dto.values,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
    }
}

export function metadataToDTO(metadata: IAZoneMetadata): IAZoneMetadataOutDTO {
    return {
        id: metadata.id,
        tenant_id: metadata.tenantId,
        zone_id: metadata.zoneId,
        view_id: metadata.viewId,
        name: metadata.name,
        values: metadata.values,
    }
}

export function metadataPagedFromDTO(dto: IAZoneMetadataPagedResponseDTO): IAZoneMetadataPaged {
    return {
        records: dto.records.map(metadataFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}