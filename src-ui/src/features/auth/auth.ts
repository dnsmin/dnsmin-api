import {ClientInDTO, ClientOutDTO} from "@app/features/auth/clients/dto";
import {SessionInDTO} from "@app/features/auth/sessions/dto";
import {Client} from "@app/features/auth/clients/models";
import {Session} from "@app/features/auth/sessions/models";

export function clientFromDTO(dto: ClientInDTO): Client {
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

export function clientToDTO(client: Client): ClientOutDTO {
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

export function sessionFromDTO(dto: SessionInDTO): Session {
    return {
        id: dto.id,
        tenantId: dto.tenant_id,
        userId: dto.user_id,
        clientIp: dto.client_ip,
        token: dto.token,
        data: dto.data,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
        expiresAt: dto.expires_at,
    }
}