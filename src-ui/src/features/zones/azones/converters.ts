import {IAZoneInDTO, IAZoneOutDTO, IAZonesPagedResponseDTO} from "@app/features/zones/azones/dto";
import {IAZone, IAZonesPaged} from "@app/features/zones/azones/models";

export function zoneFromDTO(dto: IAZoneInDTO): IAZone {
    return {
        id: dto.id,
        tenantId: dto.tenant_id,
        viewId: dto.view_id,
        fqdn: dto.fqdn,
        kind: dto.kind,
        serial: dto.serial,
        notifiedSerial: dto.notified_serial,
        editedSerial: dto.edited_serial,
        masters: dto.masters,
        dnssec: dto.dnssec,
        nsec3param: dto.nsec3param,
        nsec3narrow: dto.nsec3narrow,
        presigned: dto.presigned,
        soaEdit: dto.soa_edit,
        soaEditApi: dto.soa_edit_api,
        apiRectify: dto.api_rectify,
        zone: dto.zone,
        catalog: dto.catalog,
        account: dto.account,
        masterTsigKeyIds: dto.master_tsig_key_ids,
        slaveTsigKeyIds: dto.slave_tsig_key_ids,
        shared: dto.shared,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
    }
}

export function zoneToDTO(zone: IAZone): IAZoneOutDTO {
    return {
        id: zone.id,
        tenant_id: zone.tenantId,
        view_id: zone.viewId,
        fqdn: zone.fqdn,
        kind: zone.kind,
        serial: zone.serial,
        notified_serial: zone.notifiedSerial,
        edited_serial: zone.editedSerial,
        masters: zone.masters,
        dnssec: zone.dnssec,
        nsec3param: zone.nsec3param,
        nsec3narrow: zone.nsec3narrow,
        presigned: zone.presigned,
        soa_edit: zone.soaEdit,
        soa_edit_api: zone.soaEditApi,
        api_rectify: zone.apiRectify,
        zone: zone.zone,
        catalog: zone.catalog,
        account: zone.account,
        master_tsig_key_ids: zone.masterTsigKeyIds,
        slave_tsig_key_ids: zone.slaveTsigKeyIds,
        shared: zone.shared,
    }
}

export function zonesPagedFromDTO(dto: IAZonesPagedResponseDTO): IAZonesPaged {
    return {
        records: dto.records.map(zoneFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}