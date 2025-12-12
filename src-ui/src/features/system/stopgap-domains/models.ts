import {ModelBase} from "@app/types/models";

export interface StopgapDomain extends ModelBase {
    id?: string;
    name: string;
    fqdn: string;
    restrictedHosts?: string[] | null;
    createdAt?: string | null;
    updatedAt?: string | null;
}

export interface StopgapDomainsPaged extends ModelBase {
    records: StopgapDomain[];
    total: number;
    totalFiltered: number;
}

export type IStopgapDomain = StopgapDomain;
export type IStopgapDomainsPaged = StopgapDomainsPaged;