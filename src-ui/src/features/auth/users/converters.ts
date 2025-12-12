import {IUserInDTO, IUserOutDTO, IUsersPagedResponseDTO} from "@app/features/auth/users/dto";
import {IUser, IUsersPaged} from "@app/features/auth/users/models";

export function userFromDTO(dto: IUserInDTO): IUser {
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

export function userToDTO(user: IUser): IUserOutDTO {
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

export function usersPagedFromDTO(dto: IUsersPagedResponseDTO): IUsersPaged {
    return {
        records: dto.records.map(userFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}