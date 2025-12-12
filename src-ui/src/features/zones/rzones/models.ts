import {ModelBase} from "@app/types/models";

export interface RZone extends ModelBase {
    id?: string;
    tenantId?: string | null;
    fqdn: string;
    kind: string;
    servers: string[];
    recursionDesired?: boolean | null;
    notifyAllowed?: boolean | null;
    createdAt?: string | null;
    updatedAt?: string | null;
}

export interface RZonesPaged extends ModelBase {
    records: RZone[];
    total: number;
    totalFiltered: number;
}

export type IRZone = RZone;
export type IRZonesPaged = RZonesPaged;