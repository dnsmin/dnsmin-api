import {ModelBase} from "@app/types/models";

export interface AZone extends ModelBase {
    id?: string;
    tenantId?: string | null;
    viewId?: string | null;
    fqdn: string;
    kind: string;
    serial: number;
    notifiedSerial?: number | null;
    editedSerial?: number | null;
    masters?: string[] | null;
    dnssec: boolean;
    nsec3param?: string | null;
    nsec3narrow?: boolean | null;
    presigned?: boolean | null;
    soaEdit?: string | null;
    soaEditApi?: string | null;
    apiRectify?: boolean | null;
    zone?: string | null;
    catalog?: string | null;
    account?: string | null;
    masterTsigKeyIds?: string[] | null;
    slaveTsigKeyIds?: string[] | null;
    shared: boolean;
    createdAt?: string | null;
    updatedAt?: string | null;
}

export interface AZonesPaged extends ModelBase {
    records: AZone[];
    total: number;
    totalFiltered: number;
}

export type IAZone = AZone;
export type IAZonesPaged = AZonesPaged;