import {IServerViewInDTO, IServerViewOutDTO, IServerViewsPagedResponseDTO} from "@app/features/servers/views/dto";
import {IServerView, IServerViewsPaged} from "@app/features/servers/views/models";

export function viewFromDTO(dto: IServerViewInDTO): IServerView {
    return {
        id: dto.id,
        serverId: dto.server_id,
        name: dto.name,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
    }
}

export function viewToDTO(view: IServerView): IServerViewOutDTO {
    return {
        id: view.id,
        server_id: view.serverId,
        name: view.name,
    }
}

export function viewsPagedFromDTO(dto: IServerViewsPagedResponseDTO): IServerViewsPaged {
    return {
        records: dto.records.map(viewFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}