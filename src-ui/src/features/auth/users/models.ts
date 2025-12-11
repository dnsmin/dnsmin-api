import {ModelBase} from "@app/types/models";

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
    totalFiltered: number;
}

export type IUser = User;
export type IUsersPaged = UsersPaged;