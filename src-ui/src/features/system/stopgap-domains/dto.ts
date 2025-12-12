import {BaseDTO} from "@app/types/dto";

export interface StopgapDomainInDTO extends BaseDTO {
    id: string;
    name: string;
    fqdn: string;
    restricted_hosts: string[] | null;
    created_at: string;
    updated_at: string | null;
}

export interface StopgapDomainOutDTO extends BaseDTO {
    id?: string;
    name: string;
    fqdn: string;
    restricted_hosts?: string[] | null;
}

export interface StopgapDomainsPagedResponseDTO extends BaseDTO {
    records: StopgapDomainInDTO[];
    total: number;
    total_filtered: number;
}

export type IStopgapDomainInDTO = StopgapDomainInDTO;
export type IStopgapDomainOutDTO = StopgapDomainOutDTO;
export type IStopgapDomainsPagedResponseDTO = StopgapDomainsPagedResponseDTO;