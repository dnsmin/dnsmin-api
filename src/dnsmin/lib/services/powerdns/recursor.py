from dnsmin.lib.services.powerdns import PowerDNSApiConfig, PowerDNSApiBase
from dnsmin.lib.services.powerdns.models import RZone


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


class PowerDNSRecursorApi(PowerDNSApiBase):
    """Provides an API for interacting with the PowerDNS recursor server API."""

    servers: PowerDNSServersApi

    zones: PowerDNSZonesApi

    def __init__(self, config: PowerDNSApiConfig):
        super().__init__(config)
        self.servers = PowerDNSServersApi(config)
        self.zones = PowerDNSZonesApi(config)
