import {ClientInDTO, ClientOutDTO, UserInDTO, UserOutDTO, UsersPagedResponseDTO, SessionInDTO} from "@app/types/dto/auth";
import {Client, User, UsersPaged, Session} from "@app/types/models/auth";

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

export function userFromDTO(dto: UserInDTO): User {
    return {
        id: dto.id,
        tenantId: dto.tenant_id,
        username: dto.username,
        email: dto.email,
        phoneNumber: dto.phone_number,
        status: dto.status,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
        authenticatedAt: dto.authenticated_at,
    }
}

export function userToDTO(user: User): UserOutDTO {
    return {
        id: user.id,
        tenant_id: user.tenantId || null,
        username: user.username,
        password: user.password || null,
        email: user.email || null,
        phone_number: user.phoneNumber || null,
        status: user.status,
    }
}

export function usersPagedFromDTO(dto: UsersPagedResponseDTO): UsersPaged {
    return {
        records: dto.records.map(userFromDTO),
        total: dto.total,
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