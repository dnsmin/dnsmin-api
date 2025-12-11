import {ModelBase} from "@app/types/models";

export interface Session extends ModelBase {
    id?: string;
    tenantId?: string | null;
    userId?: string | null;
    clientIp: string;
    token: string;
    data: object | null;
    createdAt?: string | null;
    updatedAt?: string | null;
    expiresAt?: string | null;
}

export type ISession = Session;