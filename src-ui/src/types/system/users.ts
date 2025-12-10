import {ValidationErrors} from '@app/types/service';

export interface User {
    id?: string;
    tenantId?: string | null;
    name?: string | null;
    username: string | null;
    email?: string | null;
    phoneNumber?: string | null;
    status: string | null;
    createdAt?: string;
    updatedAt?: string;
    authenticatedAt?: string;
}

export interface UserValidationErrors extends ValidationErrors {
    id?: string;
    tenantId?: string;
    name?: string;
    username?: string;
    email?: string;
    phoneNumber?: string;
    status?: string;
}

export type IUser = User;
export type IUserValidationErrors = UserValidationErrors;