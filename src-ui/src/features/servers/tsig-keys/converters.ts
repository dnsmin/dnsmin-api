import {IServerTsigKeyInDTO, IServerTsigKeyOutDTO, IServerTsigKeysPagedResponseDTO} from "@app/features/servers/tsig-keys/dto";
import {IServerTsigKey, IServerTsigKeysPaged} from "@app/features/servers/tsig-keys/models";

export function tsigKeyFromDTO(dto: IServerTsigKeyInDTO): IServerTsigKey {
    return {
        id: dto.id,
        serverId: dto.server_id,
        internalId: dto.internal_id,
        algorithm: dto.algorithm,
        key: dto.key,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
    }
}

export function tsigKeyToDTO(tsigKey: IServerTsigKey): IServerTsigKeyOutDTO {
    return {
        id: tsigKey.id,
        server_id: tsigKey.serverId,
        algorithm: tsigKey.algorithm,
        key: tsigKey.key,
    }
}

export function tsigKeysPagedFromDTO(dto: IServerTsigKeysPagedResponseDTO): IServerTsigKeysPaged {
    return {
        records: dto.records.map(tsigKeyFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}