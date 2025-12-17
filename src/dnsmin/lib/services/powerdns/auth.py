from typing import Any, Optional

from dnsmin.lib.services.powerdns.models import AZone, AZoneUpdate


class PowerDNSAPIConfig:
    """Provides a representation of a PowerDNS server API configuration."""
    version: str
    api_url: str
    api_key: str

    def __init__(self, version: str, api_url: str, api_key: str):
        self.version = version
        self.api_url = api_url
        self.api_key = api_key


class PowerDNSAuthAPI:
    """Provides an API for interacting with the PowerDNS authoritative server API."""

    _config: PowerDNSAPIConfig
    """Stores a reference to a PowerDNS API configuration."""

    @property
    def config(self) -> PowerDNSAPIConfig:
        return self._config

    def __init__(self, config: PowerDNSAPIConfig):
        self._config = config

    def make_request(
            self,
            endpoint: str,
            method: str = 'GET',
            params: Optional[dict[str, Any]] = None,
            payload: Optional[dict[str, Any] | tuple | bytes] = None,
            headers: Optional[dict] = None,
    ) -> list[dict] | dict | str:
        """Makes a request to the configured PowerDNS server API."""
        import json
        import requests
        from loguru import logger

        request_headers = {
            'Accept': 'application/json',
            'X-API-Key': self.config.api_key,
        }

        if isinstance(headers, dict):
            request_headers.update(headers)

        request_method = getattr(requests, method.lower())

        request_kwargs: dict[str, Any] = {
            'headers': request_headers,
        }

        if isinstance(params, dict):
            request_kwargs['params'] = params

        if method.lower() in ['post', 'put', 'patch']:
            request_kwargs['json'] = payload

        logger.trace(f'Sending request to {self.config.api_url}{endpoint}...')
        logger.trace(json.dumps(request_kwargs, indent=2))

        r = request_method(f'{self.config.api_url}{endpoint}', **request_kwargs)

        if r.status_code < 200 or r.status_code >= 300:
            logger.warning(r.json())

        r.raise_for_status()

        return r.json()

    def list_servers(self) -> list[dict]:
        """Returns a list of servers known to the PowerDNS authoritative server."""
        return self.make_request('/v1/servers')

    def get_server(self, server_id: str) -> dict:
        """Returns a server with the specified server ID."""
        return self.make_request(f'/v1/servers/{server_id}')

    def list_zones(self, server_id: str) -> list[dict]:
        """Returns a list of zones known to the PowerDNS authoritative server."""
        return self.make_request(f'/v1/servers/{server_id}/zones')

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
        """Creates a new zone in the PowerDNS authoritative server."""
        payload = zone.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True)
        data = self.make_request(f'/v1/servers/{server_id}/zones', method='POST', payload=payload)
        return AZone(**data)

    def update_zone(self, server_id: str, zone_id: str, zone: AZoneUpdate) -> None:
        """Updates zone data in the PowerDNS authoritative server."""
        payload = zone.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True)
        self.make_request(f'/v1/servers/{server_id}/zones/{zone_id}', method='PUT', payload=payload)

    def update_zone_records(self, server_id: str, zone_id: str, zone: AZone) -> None:
        """Updates zone records in the PowerDNS authoritative server."""
        payload = zone.model_dump(mode='json', exclude_none=False, exclude_unset=True, by_alias=True)
        self.make_request(f'/v1/servers/{server_id}/zones/{zone_id}', method='PATCH', payload=payload)

    def delete_zone(self, server_id: str, zone_id: str) -> None:
        """Deletes a zone in the PowerDNS authoritative server."""
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
