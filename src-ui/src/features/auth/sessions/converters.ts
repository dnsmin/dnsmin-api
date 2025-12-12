import {SessionInDTO} from "@app/features/auth/sessions/dto";
import {Session} from "@app/features/auth/sessions/models";

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