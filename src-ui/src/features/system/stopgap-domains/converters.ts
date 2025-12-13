import {IStopgapDomainInDTO, IStopgapDomainOutDTO, IStopgapDomainsPagedResponseDTO} from "@app/features/system/stopgap-domains/dto";
import {IStopgapDomain, IStopgapDomainsPaged} from "@app/features/system/stopgap-domains/models";

export function stopgapDomainFromDTO(dto: IStopgapDomainInDTO): IStopgapDomain {
    return {
        id: dto.id,
        name: dto.name,
        fqdn: dto.fqdn,
        restrictedHosts: dto.restricted_hosts,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
    }
}

export function stopgapDomainToDTO(stopgapDomain: IStopgapDomain): IStopgapDomainOutDTO {
    return {
        id: stopgapDomain.id,
        name: stopgapDomain.name,
        fqdn: stopgapDomain.fqdn,
        restricted_hosts: stopgapDomain.restrictedHosts,
    }
}

export function stopgapDomainsPagedFromDTO(dto: IStopgapDomainsPagedResponseDTO): IStopgapDomainsPaged {
    return {
        records: dto.records.map(stopgapDomainFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}