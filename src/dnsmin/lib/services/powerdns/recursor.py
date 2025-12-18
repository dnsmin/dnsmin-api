from typing import Optional

from dnsmin.lib.services.powerdns import PowerDNSApiConfig, PowerDNSApiBase
from dnsmin.lib.services.powerdns.models import ConfigSetting, StatisticItem, CacheFlushResult, RZone


class PowerDNSServersApi(PowerDNSApiBase):
    """Provides an API for managing PowerDNS servers via API."""

    def list(self) -> list[dict]:
        """Returns a list of servers known to the PowerDNS server."""
        return self.make_request('/v1/servers', method='GET')

    def get(self, server_id: str) -> dict:
        """Returns a server with the specified server ID."""
        return self.make_request(f'/v1/servers/{server_id}', method='GET')


class PowerDNSZonesApi(PowerDNSApiBase):
    """Provides an API for managing PowerDNS zones via API."""

    def list(self, server_id: str) -> list[RZone]:
        """Returns a list of zones known to the PowerDNS server."""
        return [RZone(**z) for z in self.make_request(f'/v1/servers/{server_id}/zones', method='GET')]

    def get(self, server_id: str, zone_id: str) -> RZone:
        """Returns a zone with the specified zone ID."""
        data = self.make_request(f'/v1/servers/{server_id}/zones/{zone_id}', method='GET')
        return RZone(**data)

    def create(self, server_id: str, zone: RZone):
        """Creates a new zone in the PowerDNS server."""
        payload = zone.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True)
        data = self.make_request(f'/v1/servers/{server_id}/zones', method='POST', payload=payload)
        return RZone(**data)

    def delete(self, server_id: str, zone_id: str) -> None:
        """Deletes a zone in the PowerDNS server."""
        self.make_request(f'/v1/servers/{server_id}/zones/{zone_id}', method='DELETE')


class PowerDNSConfigurationApi(PowerDNSApiBase):
    """Provides an API for managing PowerDNS configuration via API."""

    def list(self, server_id: str) -> list[ConfigSetting]:
        """Returns a list of configuration settings known to the PowerDNS server."""
        data = self.make_request(f'/v1/servers/{server_id}/config', method='GET')
        return [ConfigSetting(**s) for s in data]

    def get(self, server_id: str, config_setting_name: str) -> ConfigSetting:
        """Returns the configuration setting with the given name."""
        data = self.make_request(f'/v1/servers/{server_id}/config/{config_setting_name}', method='GET')
        return ConfigSetting(**data)

    def create(self, server_id: str, setting: ConfigSetting) -> None:
        """Creates a new configuration setting in the PowerDNS server."""
        raise NotImplementedError('The ability to create a configuration setting is not implemented in PowerDNS.')
        payload = setting.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True)
        self.make_request(f'/v1/servers/{server_id}/config', method='POST', payload=payload)

    def update(self, server_id: str, config_setting: ConfigSetting) -> ConfigSetting:
        """Updates the given configuration setting in the PowerDNS server."""
        if isinstance(config_setting.value, str):
            config_setting.value = [config_setting.value]
        data = self.make_request(
            f'/v1/servers/{server_id}/config/{config_setting.name}',
            method='PUT',
            payload=config_setting.model_dump(mode='json', exclude_none=False, exclude_unset=True),
        )
        return ConfigSetting(**data)


class PowerDNSStatisticsApi(PowerDNSApiBase):
    """Provides an API for retrieving PowerDNS statistics via API."""

    def list(self, server_id: str, statistic: Optional[str] = None) -> list[StatisticItem]:
        """Returns a list of crypto keys known to the PowerDNS server for the given zone ID."""
        data = self.make_request(
            f'/v1/servers/{server_id}/statistics',
            method='GET',
            params={'statistic': statistic} if isinstance(statistic, str) else None,
        )
        return [StatisticItem(**s) for s in data]


class PowerDNSCacheApi(PowerDNSApiBase):
    """Provides an API for managing the PowerDNS cache via API."""

    def flush(self, server_id: str, domain: str, subtree: bool = False, type: Optional[str] = None) -> CacheFlushResult:
        """Flushes the given domain from the PowerDNS server."""
        params = {'domain': domain, 'subtree': subtree}

        if isinstance(type, str):
            params['type'] = type

        data = self.make_request(
            f'/v1/servers/{server_id}/cache/flush',
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

    def __init__(self, config: PowerDNSApiConfig):
        super().__init__(config)
        self.servers = PowerDNSServersApi(config)
        self.zones = PowerDNSZonesApi(config)
        self.configuration = PowerDNSConfigurationApi(config)
        self.statistics = PowerDNSStatisticsApi(config)
        self.cache = PowerDNSCacheApi(config)
