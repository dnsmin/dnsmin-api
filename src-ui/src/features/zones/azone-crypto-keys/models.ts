import {ModelBase} from "@app/types/models";

export interface AZoneCryptoKey extends ModelBase {
    id?: string;
    tenantId?: string | null;
    zoneId: string;
    internalId?: number | null;
    type: string;
    active: boolean;
    published: boolean;
    dnsKey: string;
    ds: string[];
    cds: string[];
    privateKey: string;
    algorithm: string;
    bits: number;
    createdAt?: string | null;
    updatedAt?: string | null;
}

export interface AZoneCryptoKeysPaged extends ModelBase {
    records: AZoneCryptoKey[];
    total: number;
    totalFiltered: number;
}

export type IAZoneCryptoKey = AZoneCryptoKey;
export type IAZoneCryptoKeysPaged = AZoneCryptoKeysPaged;