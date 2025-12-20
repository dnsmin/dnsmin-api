from typing import Optional

from dnsmin.lib.services.powerdns import PowerDNSApiConfig, PowerDNSApiBase
from dnsmin.lib.services.powerdns.models import ConfigSetting, StatisticItem, CacheFlushResult, RZone


class PowerDNSServersApi(PowerDNSApiBase):
    """Provides an API for managing PowerDNS servers via API."""

    async def list(self) -> list[dict]:
        """Returns a list of servers known to the PowerDNS server."""
        return await self.make_request('/v1/servers', method='GET')

    async def get(self) -> dict:
        """Returns a server with the specified server ID."""
        return await self.make_request(f'/v1/servers/{self.config.server_id}', method='GET')


class PowerDNSZonesApi(PowerDNSApiBase):
    """Provides an API for managing PowerDNS zones via API."""

    async def list(self) -> list[RZone]:
        """Returns a list of zones known to the PowerDNS server."""
        return [RZone(**z) for z in await self.make_request(f'/v1/servers/{self.config.server_id}/zones', method='GET')]

    async def get(self, zone_id: str) -> RZone:
        """Returns a zone with the specified zone ID."""
        data = await self.make_request(f'/v1/servers/{self.config.server_id}/zones/{zone_id}', method='GET')
        return RZone(**data)

    async def create(self, zone: RZone):
        """Creates a new zone in the PowerDNS server."""
        payload = zone.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True)
        data = await self.make_request(f'/v1/servers/{self.config.server_id}/zones', method='POST', payload=payload)
        return RZone(**data)

    async def delete(self, zone_id: str) -> None:
        """Deletes a zone in the PowerDNS server."""
        await self.make_request(f'/v1/servers/{self.config.server_id}/zones/{zone_id}', method='DELETE')


class PowerDNSConfigurationApi(PowerDNSApiBase):
    """Provides an API for managing PowerDNS configuration via API."""

    async def list(self) -> list[ConfigSetting]:
        """Returns a list of configuration settings known to the PowerDNS server."""
        data = await self.make_request(f'/v1/servers/{self.config.server_id}/config', method='GET')
        return [ConfigSetting(**s) for s in data]

    async def get(self, config_setting_name: str) -> ConfigSetting:
        """Returns the configuration setting with the given name."""
        data = await self.make_request(f'/v1/servers/{self.config.server_id}/config/{config_setting_name}', method='GET')
        return ConfigSetting(**data)

    async def create(self, setting: ConfigSetting) -> None:
        """Creates a new configuration setting in the PowerDNS server."""
        raise NotImplementedError('The ability to create a configuration setting is not implemented in PowerDNS.')
        payload = setting.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True)
        await self.make_request(f'/v1/servers/{self.config.server_id}/config', method='POST', payload=payload)

    async def update(self, config_setting: ConfigSetting) -> ConfigSetting:
        """Updates the given configuration setting in the PowerDNS server."""
        if isinstance(config_setting.value, str):
            config_setting.value = [config_setting.value]
        data = await self.make_request(
            f'/v1/servers/{self.config.server_id}/config/{config_setting.name}',
            method='PUT',
            payload=config_setting.model_dump(mode='json', exclude_none=False, exclude_unset=True),
        )
        return ConfigSetting(**data)


class PowerDNSStatisticsApi(PowerDNSApiBase):
    """Provides an API for retrieving PowerDNS statistics via API."""

    async def list(self, statistic: Optional[str] = None) -> list[StatisticItem]:
        """Returns a list of crypto keys known to the PowerDNS server for the given zone ID."""
        data = await self.make_request(
            f'/v1/servers/{self.config.server_id}/statistics',
            method='GET',
            params={'statistic': statistic} if isinstance(statistic, str) else None,
        )
        return [StatisticItem(**s) for s in data]


class PowerDNSCacheApi(PowerDNSApiBase):
    """Provides an API for managing the PowerDNS cache via API."""

    async def flush(self, domain: str, subtree: bool = False, type: Optional[str] = None) -> CacheFlushResult:
        """Flushes the given domain from the PowerDNS server."""
        params = {'domain': domain, 'subtree': subtree}

        if isinstance(type, str):
            params['type'] = type

        data = await self.make_request(
            f'/v1/servers/{self.config.server_id}/cache/flush',
            method='PUT',
            params=params,
        )
        return CacheFlushResult(**data)


class PowerDNSRecursorApi(PowerDNSApiBase):
    """Provides an API for interacting with the PowerDNS recursor server API."""

    servers: PowerDNSServersApi

    zones: PowerDNSZonesApi

    configuration: PowerDNSConfigurationApi

    statistics: PowerDNSStatisticsApi

    cache: PowerDNSCacheApi

    # XXX: Consider implementing Query Tracing API
    # XXX: Consider implementing Failure Logging API
    # XXX: Consider implementing RPZ Statistics API
    # XXX: Consider implementing JSON Statistics API

    def __init__(self, config: PowerDNSApiConfig):
        super().__init__(config)
        self.servers = PowerDNSServersApi(config)
        self.zones = PowerDNSZonesApi(config)
        self.configuration = PowerDNSConfigurationApi(config)
        self.statistics = PowerDNSStatisticsApi(config)
        self.cache = PowerDNSCacheApi(config)
