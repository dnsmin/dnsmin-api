import {IServerAutoPrimaryInDTO, IServerAutoPrimaryOutDTO, IServerAutoPrimariesPagedResponseDTO} from "@app/features/servers/autoprimaries/dto";
import {IServerAutoPrimary, IServerAutoPrimariesPaged} from "@app/features/servers/autoprimaries/models";

export function autoPrimaryFromDTO(dto: IServerAutoPrimaryInDTO): IServerAutoPrimary {
    return {
        id: dto.id,
        serverId: dto.server_id,
        ip: dto.ip,
        nameserver: dto.nameserver,
        account: dto.account,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
    }
}

export function autoPrimaryToDTO(autoPrimary: IServerAutoPrimary): IServerAutoPrimaryOutDTO {
    return {
        id: autoPrimary.id,
        server_id: autoPrimary.serverId,
        ip: autoPrimary.ip,
        nameserver: autoPrimary.nameserver,
        account: autoPrimary.account,
    }
}

export function autoPrimariesPagedFromDTO(dto: IServerAutoPrimariesPagedResponseDTO): IServerAutoPrimariesPaged {
    return {
        records: dto.records.map(autoPrimaryFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}