from typing import Optional

from dnsmin.lib.services.powerdns import PowerDNSApiConfig, PowerDNSApiBase
from dnsmin.lib.services.powerdns.models import (
    StatisticItem, MapStatisticItem, RingStatisticItem, SimpleStatisticItem, CacheFlushResult,
    ServerAutoPrimary, ServerTSIGKey, ServerView, ServerNetwork,
    AZone, AZoneUpdate, AZoneMetadata, AZoneCryptoKey
)


class PowerDNSServersApi(PowerDNSApiBase):
    """Provides an API for managing PowerDNS servers via API."""

    async def list(self) -> list[dict]:
        """Returns a list of servers known to the PowerDNS server."""
        return await self.make_request('/v1/servers', method='GET')

    async def get(self) -> dict:
        """Returns a server with the specified server ID."""
        return await self.make_request(f'/v1/servers/{self.config.server_id}', method='GET')


class PowerDNSAutoPrimariesApi(PowerDNSApiBase):
    """Provides an API for managing PowerDNS auto-primaries via API."""

    async def list(self) -> list[ServerAutoPrimary]:
        """Returns a list of auto-primaries known to the PowerDNS server."""
        data = await self.make_request(f'/v1/servers/{self.config.server_id}/autoprimaries', method='GET')
        return [ServerAutoPrimary(**ck) for ck in data]

    async def create(self, auto_primary: ServerAutoPrimary):
        """Creates an auto-primary in the PowerDNS server."""
        data = await self.make_request(
            f'/v1/servers/{self.config.server_id}/autoprimaries',
            method='POST',
            payload=auto_primary.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True),
        )
        return ServerAutoPrimary(**data)

    async def delete(self, ip: str, nameserver: str) -> None:
        """Deletes an auto-primary for the given IP address and nameserver in the PowerDNS server."""
        await self.make_request(f'/v1/servers/{self.config.server_id}/autoprimaries/{ip}/{nameserver}', method='DELETE')


class PowerDNSTSIGKeysApi(PowerDNSApiBase):
    """Provides an API for managing PowerDNS TSIG keys via API."""

    async def list(self) -> list[ServerTSIGKey]:
        """Returns a list of TSIG keys known to the PowerDNS server."""
        data = await self.make_request(f'/v1/servers/{self.config.server_id}/tsigkeys', method='GET')
        return [ServerTSIGKey(**ck) for ck in data]

    async def get(self, tsig_key_id: str) -> ServerTSIGKey:
        """Returns a TSIG key with the specified TSIG key ID."""
        data = await self.make_request(f'/v1/servers/{self.config.server_id}/tsigkeys/{tsig_key_id}', method='GET')
        return ServerTSIGKey(**data)

    async def create(self, tsig_key: ServerTSIGKey):
        """Creates a TSIG key in the PowerDNS server."""
        data = await self.make_request(
            f'/v1/servers/{self.config.server_id}/tsigkeys',
            method='POST',
            payload=tsig_key.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True),
        )
        return ServerTSIGKey(**data)

    async def update(self, tsig_key_id: str, tsig_key: ServerTSIGKey) -> None:
        """Updates a TSIG key for the given TSIG key ID in the PowerDNS server."""
        await self.make_request(
            f'/v1/servers/{self.config.server_id}/tsigkeys/{tsig_key_id}',
            method='PUT',
            payload=tsig_key.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True),
        )

    async def delete(self, tsig_key_id: str) -> None:
        """Deletes a TSIG key for the given TSIG key ID in the PowerDNS server."""
        await self.make_request(f'/v1/servers/{self.config.server_id}/tsigkeys/{tsig_key_id}', method='DELETE')


class PowerDNSViewsApi(PowerDNSApiBase):
    """Provides an API for managing PowerDNS views via API."""

    async def list(self) -> list[ServerView]:
        """Returns a list of views known to the PowerDNS server."""
        data = await self.make_request(f'/v1/servers/{self.config.server_id}/views', method='GET')
        return [ServerView(name=v) for v in data['views']]

    async def get(self, view: str) -> ServerView:
        """Returns a view with the specified name."""
        data = await self.make_request(f'/v1/servers/{self.config.server_id}/views/{view}', method='GET')
        return ServerView(name=view, zones=data['zones'])

    async def create(self, view: str, zone: str) -> None:
        """Creates a view or adds to a view in the PowerDNS server."""
        data = await self.make_request(
            f'/v1/servers/{self.config.server_id}/views/{view}',
            method='POST',
            payload={'name': f'{zone}.{view}'},
        )

    async def delete(self, view: str, zone: str) -> None:
        """Deletes the given zone from the given view in the PowerDNS server."""
        await self.make_request(f'/v1/servers/{self.config.server_id}/views/{view}/{zone}', method='DELETE')


class PowerDNSNetworksApi(PowerDNSApiBase):
    """Provides an API for managing PowerDNS networks via API."""

    async def list(self) -> list[ServerNetwork]:
        """Returns a list of networks known to the PowerDNS server."""
        data: dict[str, list[dict[str, str]]] = await self.make_request(
            f'/v1/servers/{self.config.server_id}/networks',
            method='GET',
        )
        return [ServerNetwork(network=n['network'], view=n['view']) for n in data['networks']]

    async def get(self, network: str) -> ServerNetwork:
        """Returns a network with the specified network."""
        data: dict[str, list[dict[str, str]]] = await self.make_request(
            f'/v1/servers/{self.config.server_id}/networks/{network}',
            method='GET',
        )
        return ServerNetwork(network=data['networks'][0]['network'], view=data['networks'][0]['view'])

    async def create(self, network: str, view: str) -> None:
        """Add the given network to the given view in the PowerDNS server."""
        await self.make_request(
            f'/v1/servers/{self.config.server_id}/networks/{network}',
            method='PUT',
            payload={'view': view},
        )

    async def delete(self, network: str, view: str) -> None:
        """Deletes the given network from the given view in the PowerDNS server."""
        await self.make_request(
            f'/v1/servers/{self.config.server_id}/networks/{network}',
            method='DELETE',
            payload={'view': view},
        )


class PowerDNSZonesApi(PowerDNSApiBase):
    """Provides an API for managing PowerDNS zones via API."""

    async def list(self, zone: Optional[str] = None, dnssec: Optional[bool] = None) -> list[AZone]:
        """Returns a list of zones known to the PowerDNS server."""
        params = {}

        if isinstance(zone, str):
            params['zone'] = zone

        if isinstance(dnssec, bool):
            params['dnssec'] = dnssec

        return [AZone(**z) for z in await self.make_request(
            f'/v1/servers/{self.config.server_id}/zones', method='GET', params=params,
        )]

    async def get(
            self,
            zone_id: str,
            rrsets: bool = True,
            rrset_name: Optional[str] = None,
            rrset_type: Optional[str] = None,
            include_disabled: bool = True,
    ) -> AZone:
        """Returns a zone with the specified zone ID."""
        params = {
            'rrsets': 'true' if rrsets else 'false',
            'include_disabled': 'true' if include_disabled else 'false',
        }

        if isinstance(rrset_name, str):
            params['rrset_name'] = rrset_name

        if isinstance(rrset_type, str):
            params['rrset_type'] = rrset_type

        data = await self.make_request(f'/v1/servers/{self.config.server_id}/zones/{zone_id}', method='GET',
                                       params=params)

        return AZone(**data)

    async def create(self, zone: AZone):
        """Creates a new zone in the PowerDNS server."""
        payload = zone.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True)
        data = await self.make_request(f'/v1/servers/{self.config.server_id}/zones', method='POST', payload=payload)
        return AZone(**data)

    async def update(self, zone_id: str, zone: AZoneUpdate) -> None:
        """Updates zone data in the PowerDNS server."""
        payload = zone.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True)
        await self.make_request(f'/v1/servers/{self.config.server_id}/zones/{zone_id}', method='PUT', payload=payload)

    async def update_records(self, zone_id: str, zone: AZone) -> None:
        """Updates zone records in the PowerDNS server."""
        payload = zone.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True)
        await self.make_request(f'/v1/servers/{self.config.server_id}/zones/{zone_id}', method='PATCH', payload=payload)

    async def delete(self, zone_id: str) -> None:
        """Deletes a zone in the PowerDNS server."""
        await self.make_request(f'/v1/servers/{self.config.server_id}/zones/{zone_id}', method='DELETE')

    async def retrieve(self, zone_id: str):
        """Initiates an AXFR request for a zone on a secondary server."""
        await self.make_request(f'/v1/servers/{self.config.server_id}/zones/{zone_id}/axfr-retrieve', method='PUT')

    async def notify(self, zone_id: str):
        """Sends a DNS NOTIFY request for a zone to all secondaries."""
        await self.make_request(f'/v1/servers/{self.config.server_id}/zones/{zone_id}/notify', method='PUT')

    async def rectify(self, zone_id: str):
        """Rectifies a zone."""
        await self.make_request(f'/v1/servers/{self.config.server_id}/zones/{zone_id}/rectify', method='PUT')

    async def export(self, zone_id: str) -> str:
        """Returns a zone in AXFR format."""
        return await self.make_request(f'/v1/servers/{self.config.server_id}/zones/{zone_id}/export', method='GET')


class PowerDNSMetadataApi(PowerDNSApiBase):
    """Provides an API for managing PowerDNS zone metadata via API."""

    async def list(self, zone_id: str) -> list[AZoneMetadata]:
        """Returns a list of crypto keys known to the PowerDNS server for the given zone ID."""
        data = await self.make_request(f'/v1/servers/{self.config.server_id}/zones/{zone_id}/metadata', method='GET')
        return [AZoneMetadata(**ck) for ck in data]

    async def get(self, zone_id: str, metadata_name: str) -> AZoneMetadata:
        """Returns a single metadata entry with the specified zone ID and metadata name / kind."""
        data = await self.make_request(
            f'/v1/servers/{self.config.server_id}/zones/{zone_id}/metadata/{metadata_name}',
            method='GET',
        )
        return AZoneMetadata(**data)

    async def create(self, zone_id: str, metadata: AZoneMetadata):
        """Creates a new metadata entry for the given zone ID in the PowerDNS server."""
        data = await self.make_request(
            f'/v1/servers/{self.config.server_id}/zones/{zone_id}/metadata',
            method='POST',
            payload=metadata.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True),
        )
        return AZoneMetadata(**data)

    async def update(self, zone_id: str, metadata: AZoneMetadata) -> None:
        """Updates a single metadata kind for the given zone ID in the PowerDNS server."""
        await self.make_request(
            f'/v1/servers/{self.config.server_id}/zones/{zone_id}/metadata/{metadata.name}',
            method='PUT',
            payload=metadata.model_dump(mode='json', exclude_none=False, exclude_unset=True),
        )

    async def delete(self, zone_id: str, metadata_name: str) -> None:
        """Deletes a single metadata kind for the given zone ID and metadata name / kind in the PowerDNS server."""
        await self.make_request(f'/v1/servers/{self.config.server_id}/zones/{zone_id}/metadata/{metadata_name}',
                                method='DELETE')


class PowerDNSCryptoKeysApi(PowerDNSApiBase):
    """Provides an API for managing PowerDNS crypto keys via API."""

    async def list(self, zone_id: str) -> list[AZoneCryptoKey]:
        """Returns a list of crypto keys known to the PowerDNS server for the given zone ID."""
        data = await self.make_request(f'/v1/servers/{self.config.server_id}/zones/{zone_id}/cryptokeys', method='GET')
        return [AZoneCryptoKey(**ck) for ck in data]

    async def get(self, zone_id: str, crypto_key_id: str) -> AZoneCryptoKey:
        """Returns a crypto key with the specified zone and crypto key ID."""
        data = await self.make_request(
            f'/v1/servers/{self.config.server_id}/zones/{zone_id}/cryptokeys/{crypto_key_id}',
            method='GET',
        )
        return AZoneCryptoKey(**data)

    async def create(self, zone_id: str, crypto_key: AZoneCryptoKey):
        """Creates a new crypto key for the given zone ID in the PowerDNS server."""
        data = await self.make_request(
            f'/v1/servers/{self.config.server_id}/zones/{zone_id}/cryptokeys',
            method='POST',
            payload=crypto_key.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True),
        )
        return AZoneCryptoKey(**data)

    async def activate(self, zone_id: str, crypto_key_id: str) -> None:
        """Activates / deactivates a crypto key for the given zone and crypto key ID in the PowerDNS server."""
        await self.make_request(f'/v1/servers/{self.config.server_id}/zones/{zone_id}/cryptokeys/{crypto_key_id}',
                                method='PUT')

    async def delete(self, zone_id: str, crypto_key_id: str) -> None:
        """Deletes a crypto key for the given zone and crypto key ID in the PowerDNS server."""
        await self.make_request(
            f'/v1/servers/{self.config.server_id}/zones/{zone_id}/cryptokeys/{crypto_key_id}',
            method='DELETE',
        )


class PowerDNSStatisticsApi(PowerDNSApiBase):
    """Provides an API for retrieving PowerDNS statistics via API."""

    async def list(self, statistic: Optional[str] = None, include_rings: bool = True) \
            -> list[StatisticItem | MapStatisticItem | RingStatisticItem | SimpleStatisticItem]:
        """Returns a list of crypto keys known to the PowerDNS server for the given zone ID."""
        params: dict[str, bool | str] = {'includerings': include_rings}
        if isinstance(statistic, str):
            params['statistic'] = statistic
        data = await self.make_request(f'/v1/servers/{self.config.server_id}/statistics', method='GET', params=params)
        stats = []

        for stat in data:
            if stat['type'] == 'StatisticItem':
                stats.append(StatisticItem(**stat))
            elif stat['type'] == 'MapStatisticItem':
                stats.append(MapStatisticItem(**stat))
            elif stat['type'] == 'RingStatisticItem':
                stats.append(RingStatisticItem(**stat))
            elif stat['type'] == 'SimpleStatisticItem':
                stats.append(SimpleStatisticItem(**stat))

        return stats


class PowerDNSCacheApi(PowerDNSApiBase):
    """Provides an API for managing the PowerDNS cache via API."""

    async def flush(self, domain: str) -> CacheFlushResult:
        """Flushes the given domain from the PowerDNS server."""
        data = await self.make_request(
            f'/v1/servers/{self.config.server_id}/cache/flush',
            method='PUT',
            params={'domain': domain},
        )
        return CacheFlushResult(**data)


class PowerDNSAuthApi(PowerDNSApiBase):
    """Provides an API for interacting with the PowerDNS authoritative server API."""

    servers: PowerDNSServersApi

    auto_primaries: PowerDNSAutoPrimariesApi

    tsig_keys: PowerDNSTSIGKeysApi

    views: PowerDNSViewsApi

    networks: PowerDNSNetworksApi

    zones: PowerDNSZonesApi

    metadata: PowerDNSMetadataApi

    crypto_keys: PowerDNSCryptoKeysApi

    statistics: PowerDNSStatisticsApi

    cache: PowerDNSCacheApi

    def __init__(self, config: PowerDNSApiConfig):
        super().__init__(config)
        self.servers = PowerDNSServersApi(config)
        self.auto_primaries = PowerDNSAutoPrimariesApi(config)
        self.tsig_keys = PowerDNSTSIGKeysApi(config)
        self.views = PowerDNSViewsApi(config)
        self.networks = PowerDNSNetworksApi(config)
        self.zones = PowerDNSZonesApi(config)
        self.metadata = PowerDNSMetadataApi(config)
        self.crypto_keys = PowerDNSCryptoKeysApi(config)
        self.statistics = PowerDNSStatisticsApi(config)
        self.cache = PowerDNSCacheApi(config)
