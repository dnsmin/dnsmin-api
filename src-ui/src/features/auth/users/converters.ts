import {UserInDTO, UserOutDTO, UsersPagedResponseDTO} from "@app/features/auth/users/dto";
import {User, UsersPaged} from "@app/features/auth/users/models";

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
        totalFiltered: dto.total_filtered,
    }
}