import {ModelBase} from "@app/types/models";

export interface AclPrincipal extends ModelBase {
    id?: string;
    tenantId?: string | null;
    type: string;
    createdAt?: string | null;
}

export interface AclPrincipalsPaged extends ModelBase {
    records: AclPrincipal[];
    total: number;
    totalFiltered: number;
}

export type IAclPrincipal = AclPrincipal;
export type IAclPrincipalsPaged = AclPrincipalsPaged;