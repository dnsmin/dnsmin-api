from enum import Enum
from typing import Optional
from lib.config.base import BaseConfig


class EnvironmentEnum(str, Enum):
    """Defines the possible environment names."""
    prod = 'prod'
    qa = 'qa'
    dev = 'dev'
    local = 'local'


class AppConfig(BaseConfig):
    """A model that represents a configuration hierarchy shared across descendant apps."""

    class AuthorConfig(BaseConfig):
        name: str = 'Matt Scott'
        email: str = 'matt@dnsmin.org'
        url: str = 'https://dnsmin.org'

    class EnvironmentConfig(BaseConfig):
        class EnvironmentUrlsConfig(BaseConfig):
            api: str = None
            web: str = None

        name: EnvironmentEnum = EnvironmentEnum.prod
        prefix: str = 'DNSMIN'
        file: str = 'config/.app.env'
        urls: EnvironmentUrlsConfig

    class MetadataConfig(BaseConfig):
        description: str = '''The API provides a backend interface for core functionality and support of the UI.'''

    name: str = 'dnsmin'
    version: str = '0.1.0'
    summary: str = 'An advanced management and monitoring tool for the PowerDNS software suite.'
    timezone: str = 'Etc/UTC'
    timezone_code: str = 'UTC'
    author: AuthorConfig
    environment: EnvironmentConfig
    metadata: MetadataConfig
    secret_key: Optional[str] = None
