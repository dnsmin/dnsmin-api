import {ModelBase} from "@app/types/models/base";
import {IValidationErrors} from "@app/types/service";

export interface Client extends ModelBase {
    id?: string;
    tenantId?: string | null;
    userId?: string | null;
    name: string;
    redirectUri: string | null;
    scopes: string[] | null;
    enabled: boolean;
    createdAt?: string | null;
    updatedAt?: string | null;
    expiresAt?: string | null;
}

export interface User extends ModelBase {
    id?: string;
    tenantId?: string | null;
    username: string;
    password?: string | null;
    email: string | null;
    phoneNumber: string | null;
    status: string;
    createdAt?: string | null;
    updatedAt?: string | null;
    authenticatedAt?: string | null;
}

export interface UsersPaged extends ModelBase {
    records: User[];
    total: number;
}

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

export interface UserValidationErrors extends IValidationErrors {
    id?: string;
    tenantId?: string;
    name?: string;
    username?: string;
    password?: string;
    email?: string;
    phoneNumber?: string;
    status?: string;
}

export type IClient = Client;
export type IUser = User;
export type ISession = Session;
export type IUserValidationErrors = UserValidationErrors;