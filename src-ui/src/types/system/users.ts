import {IRecord, IValidationErrors} from '@app/types/service';

export interface User extends IRecord {
    id?: string;
    tenantId?: string | null;
    name?: string | null;
    username: string | null;
    password?: string;
    email?: string | null;
    phoneNumber?: string | null;
    status: string | null;
    createdAt?: string;
    updatedAt?: string;
    authenticatedAt?: string;
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

export type IUser = User;
export type IUserValidationErrors = UserValidationErrors;