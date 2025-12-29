import json
from typing import Any, Optional

import aiohttp
from loguru import logger


class PowerDNSApiConfig:
    """Provides a representation of a PowerDNS server API configuration."""
    server_id: str
    version: str
    api_url: str
    api_key: str

    def __init__(self, server_id: str, version: str, api_url: str, api_key: str):
        self.server_id = server_id
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

    async def make_request(
            self,
            endpoint: str,
            method: str = 'GET',
            params: Optional[dict[str, Any]] = None,
            payload: Optional[dict[str, Any] | tuple | bytes] = None,
            headers: Optional[dict] = None,
    ) -> list[dict] | dict | str | None:
        """Makes a request to the configured PowerDNS server API."""

        request_headers = {
            'Accept': 'application/json',
            'X-API-Key': self.config.api_key,
        }

        if isinstance(headers, dict):
            request_headers.update(headers)

        request_kwargs: dict[str, Any] = {
            'headers': request_headers,
        }

        if isinstance(params, dict):
            request_kwargs['params'] = params

        if method.lower() in ['post', 'put', 'patch']:
            request_kwargs['json'] = payload

        logger.trace(f'Sending {method} request to {self.config.api_url}{endpoint}...')
        logger.trace(json.dumps(request_kwargs, indent=2))

        async with aiohttp.ClientSession() as session:
            request_method = getattr(session, method.lower())

            async with request_method(f'{self.config.api_url}{endpoint}', **request_kwargs) as res:

                if res.status < 200 or res.status >= 300:
                    logger.warning(await res.json())

                res.raise_for_status()

                if res.status == 204:
                    return None

                return await res.json()
