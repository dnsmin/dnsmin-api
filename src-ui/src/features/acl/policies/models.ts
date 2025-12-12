import {ModelBase} from "@app/types/models";

export interface AclPolicy extends ModelBase {
    id?: string;
    tenantId?: string | null;
    resourceType: string;
    resourceId?: string | null;
    principalType: string;
    principalId?: string | null;
    permission: string;
    deny: boolean;
    createdAt?: string | null;
    updatedAt?: string | null;
}

export interface AclPoliciesPaged extends ModelBase {
    records: AclPolicy[];
    total: number;
    totalFiltered: number;
}

export type IAclPolicy = AclPolicy;
export type IAclPoliciesPaged = AclPoliciesPaged;