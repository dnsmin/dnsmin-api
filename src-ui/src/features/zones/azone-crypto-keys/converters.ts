import {ICryptoKeyInDTO, ICryptoKeyOutDTO, ICryptoKeysPagedResponseDTO} from "@app/features/zones/azone-crypto-keys/dto";
import {IAZoneCryptoKey, IAZoneCryptoKeysPaged} from "@app/features/zones/azone-crypto-keys/models";

export function cryptoKeyFromDTO(dto: ICryptoKeyInDTO): IAZoneCryptoKey {
    return {
        id: dto.id,
        tenantId: dto.tenant_id,
        zoneId: dto.zone_id,
        internalId: dto.internal_id,
        type: dto.type,
        active: dto.active,
        published: dto.published,
        dnsKey: dto.dns_key,
        ds: dto.ds,
        cds: dto.cds,
        privateKey: dto.private_key,
        algorithm: dto.algorithm,
        bits: dto.bits,
        createdAt: dto.created_at,
        updatedAt: dto.updated_at,
    }
}

export function cryptoKeyToDTO(cryptoKey: IAZoneCryptoKey): ICryptoKeyOutDTO {
    return {
        id: cryptoKey.id,
        tenant_id: cryptoKey.tenantId,
        zone_id: cryptoKey.zoneId,
        type: cryptoKey.type,
        active: cryptoKey.active,
        published: cryptoKey.published,
        dns_key: cryptoKey.dnsKey,
        ds: cryptoKey.ds,
        cds: cryptoKey.cds,
        private_key: cryptoKey.privateKey,
        algorithm: cryptoKey.algorithm,
        bits: cryptoKey.bits,
    }
}

export function cryptoKeysPagedFromDTO(dto: ICryptoKeysPagedResponseDTO): IAZoneCryptoKeysPaged {
    return {
        records: dto.records.map(cryptoKeyFromDTO),
        total: dto.total,
        totalFiltered: dto.total_filtered,
    }
}