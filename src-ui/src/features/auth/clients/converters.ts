import {IClientInDTO, IClientOutDTO, IClientsPagedResponseDTO} from "@app/features/auth/clients/dto";
import {IClient, IClientsPaged} from "@app/features/auth/clients/models";

export function clientFromDTO(dto: IClientInDTO): IClient {
    return {
        id: dto.id,
        tenantId: dto.tenant_id,
        userId: dto.user_id,
        name: dto.name,
        redirectUri: dto.redirect_uri,
        scopes: dto.scopes,
        enabled: dto.enabled,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
        expiresAt: dto.expires_at,
    }
}

export function clientToDTO(client: IClient): IClientOutDTO {
    return {
        id: client.id,
        tenant_id: client.tenantId,
        user_id: client.userId,
        name: client.name,
        redirect_uri: client.redirectUri,
        scopes: client.scopes,
        enabled: client.enabled,
    }
}

export function clientsPagedFromDTO(dto: IClientsPagedResponseDTO): IClientsPaged {
    return {
        records: dto.records.map(clientFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}