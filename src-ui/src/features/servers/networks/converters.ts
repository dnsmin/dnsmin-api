import {IServerNetworkInDTO, IServerNetworkOutDTO, IServerNetworksPagedResponseDTO} from "@app/features/servers/networks/dto";
import {IServerNetwork, IServerNetworksPaged} from "@app/features/servers/networks/models";

export function networkFromDTO(dto: IServerNetworkInDTO): IServerNetwork {
    return {
        id: dto.id,
        serverId: dto.server_id,
        viewId: dto.view_id,
        network: dto.network,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
    }
}

export function networkToDTO(network: IServerNetwork): IServerNetworkOutDTO {
    return {
        id: network.id,
        server_id: network.serverId,
        view_id: network.viewId,
        network: network.network,
    }
}

export function networksPagedFromDTO(dto: IServerNetworksPagedResponseDTO): IServerNetworksPaged {
    return {
        records: dto.records.map(networkFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}