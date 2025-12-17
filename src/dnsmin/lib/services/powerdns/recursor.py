from dnsmin.lib.services.powerdns import PowerDNSApiBase
from dnsmin.lib.services.powerdns.models import RZone


class PowerDNSRecursorApi(PowerDNSApiBase):
    """Provides an API for interacting with the PowerDNS recursor server API."""

    def list_servers(self) -> list[dict]:
        """Returns a list of servers known to the PowerDNS server."""
        return self.make_request('/v1/servers', method='GET')

    def get_server(self, server_id: str) -> dict:
        """Returns a server with the specified server ID."""
        return self.make_request(f'/v1/servers/{server_id}', method='GET')

    def list_zones(self, server_id: str) -> list[dict]:
        """Returns a list of zones known to the PowerDNS server."""
        return self.make_request(f'/v1/servers/{server_id}/zones', method='GET')

    def get_zone(self, server_id: str, zone_id: str) -> RZone:
        """Returns a zone with the specified zone ID."""
        data = self.make_request(f'/v1/servers/{server_id}/zones/{zone_id}', method='GET')
        return RZone(**data)

    def create_zone(self, server_id: str, zone: RZone):
        """Creates a new zone in the PowerDNS server."""
        payload = zone.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True)
        data = self.make_request(f'/v1/servers/{server_id}/zones', method='POST', payload=payload)
        return RZone(**data)

    def delete_zone(self, server_id: str, zone_id: str) -> None:
        """Deletes a zone in the PowerDNS server."""
        self.make_request(f'/v1/servers/{server_id}/zones/{zone_id}', method='DELETE')
