import {ModelBase} from "@app/types/models";

export interface AclRole extends ModelBase {
    id?: string;
    tenantId?: string | null;
    slug: string;
    name: string;
    description: string;
    createdAt?: string | null;
    updatedAt?: string | null;
}

export interface AclRolesPaged extends ModelBase {
    records: AclRole[];
    total: number;
    totalFiltered: number;
}

export type IAclRole = AclRole;
export type IAclRolesPaged = AclRolesPaged;