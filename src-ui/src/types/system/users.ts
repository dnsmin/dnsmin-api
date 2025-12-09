
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

export type IUser = User;
