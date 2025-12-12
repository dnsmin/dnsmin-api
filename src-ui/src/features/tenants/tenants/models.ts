import {ModelBase} from "@app/types/models";

export interface Tenant extends ModelBase {
    id?: string;
    name: string;
    fqdn: string | null;
    stopgapDomainId?: string | null;
    stopgapHostname?: string | null;
    createdAt?: string | null;
    updatedAt?: string | null;
}

export interface TenantsPaged extends ModelBase {
    records: Tenant[];
    total: number;
    totalFiltered: number;
}

export type ITenant = Tenant;
export type ITenantsPaged = TenantsPaged;