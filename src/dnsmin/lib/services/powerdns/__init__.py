from typing import Any, Optional


class PowerDNSApiConfig:
    """Provides a representation of a PowerDNS server API configuration."""
    version: str
    api_url: str
    api_key: str

    def __init__(self, version: str, api_url: str, api_key: str):
        self.version = version
        self.api_url = api_url
        self.api_key = api_key


class PowerDNSApiBase:
    """Provides an abstract class for building product-specific PowerDNS API clients on."""

    _config: PowerDNSApiConfig
    """Stores a reference to a PowerDNS API configuration."""

    @property
    def config(self) -> PowerDNSApiConfig:
        return self._config

    def __init__(self, config: PowerDNSApiConfig):
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
