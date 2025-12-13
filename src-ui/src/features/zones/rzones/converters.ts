import {IRZoneInDTO, IRZoneOutDTO, IRZonesPagedResponseDTO} from "@app/features/zones/rzones/dto";
import {IRZone, IRZonesPaged} from "@app/features/zones/rzones/models";

export function zoneFromDTO(dto: IRZoneInDTO): IRZone {
    return {
        id: dto.id,
        tenantId: dto.tenant_id,
        fqdn: dto.fqdn,
        kind: dto.kind,
        servers: dto.servers,
        recursionDesired: dto.recursion_desired,
        notifyAllowed: dto.notify_allowed,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
    }
}

export function zoneToDTO(zone: IRZone): IRZoneOutDTO {
    return {
        id: zone.id,
        tenant_id: zone.tenantId,
        fqdn: zone.fqdn,
        kind: zone.kind,
        servers: zone.servers,
        recursion_desired: zone.recursionDesired,
        notify_allowed: zone.notifyAllowed,
    }
}

export function zonesPagedFromDTO(dto: IRZonesPagedResponseDTO): IRZonesPaged {
    return {
        records: dto.records.map(zoneFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}