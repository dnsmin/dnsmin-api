import {ISessionInDTO, ISessionsPagedResponseDTO} from "@app/features/auth/sessions/dto";
import {ISession, ISessionsPaged} from "@app/features/auth/sessions/models";

export function sessionFromDTO(dto: ISessionInDTO): ISession {
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

export function sessionsPagedFromDTO(dto: ISessionsPagedResponseDTO): ISessionsPaged {
    return {
        records: dto.records.map(sessionFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}