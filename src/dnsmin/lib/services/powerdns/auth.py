from typing import Optional

from dnsmin.lib.services.powerdns import PowerDNSApiBase
from dnsmin.lib.services.powerdns.models import AZone, AZoneUpdate


class PowerDNSAuthApi(PowerDNSApiBase):
    """Provides an API for interacting with the PowerDNS authoritative server API."""

    def list_servers(self) -> list[dict]:
        """Returns a list of servers known to the PowerDNS server."""
        return self.make_request('/v1/servers', method='GET')

    def get_server(self, server_id: str) -> dict:
        """Returns a server with the specified server ID."""
        return self.make_request(f'/v1/servers/{server_id}', method='GET')

    def list_zones(self, server_id: str) -> list[dict]:
        """Returns a list of zones known to the PowerDNS server."""
        return self.make_request(f'/v1/servers/{server_id}/zones', method='GET')

    def get_zone(
            self,
            server_id: str,
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

        data = self.make_request(f'/v1/servers/{server_id}/zones/{zone_id}', method='GET', params=params)

        return AZone(**data)

    def create_zone(self, server_id: str, zone: AZone):
        """Creates a new zone in the PowerDNS server."""
        payload = zone.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True)
        data = self.make_request(f'/v1/servers/{server_id}/zones', method='POST', payload=payload)
        return AZone(**data)

    def update_zone(self, server_id: str, zone_id: str, zone: AZoneUpdate) -> None:
        """Updates zone data in the PowerDNS server."""
        payload = zone.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True)
        self.make_request(f'/v1/servers/{server_id}/zones/{zone_id}', method='PUT', payload=payload)

    def update_zone_records(self, server_id: str, zone_id: str, zone: AZone) -> None:
        """Updates zone records in the PowerDNS server."""
        payload = zone.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True)
        self.make_request(f'/v1/servers/{server_id}/zones/{zone_id}', method='PATCH', payload=payload)

    def delete_zone(self, server_id: str, zone_id: str) -> None:
        """Deletes a zone in the PowerDNS server."""
        self.make_request(f'/v1/servers/{server_id}/zones/{zone_id}', method='DELETE')

    def retrieve_zone(self, server_id: str, zone_id: str):
        """Initiates an AXFR request for a zone on a secondary server."""
        self.make_request(f'/v1/servers/{server_id}/zones/{zone_id}/axfr-retrieve', method='PUT')

    def notify_zone(self, server_id: str, zone_id: str):
        """Sends a DNS NOTIFY request for a zone to all secondaries."""
        self.make_request(f'/v1/servers/{server_id}/zones/{zone_id}/notify', method='PUT')

    def rectify_zone(self, server_id: str, zone_id: str):
        """Rectifies a zone."""
        self.make_request(f'/v1/servers/{server_id}/zones/{zone_id}/rectify', method='PUT')

    def export_zone(self, server_id: str, zone_id: str) -> str:
        """Returns a zone in AXFR format."""
        return self.make_request(f'/v1/servers/{server_id}/zones/{zone_id}/export', method='GET')
