from typing import Optional, Union
from dnsmin.lib.config.base import BaseConfig


class DbConfig(BaseConfig):
    """A model that represents a configuration hierarchy for database connection settings."""
    redis_url: Optional[str] = 'redis://redis:6379/0'
    sql_async_url: Optional[str] = 'sqlite+aiosqlite:///./dnsmin.db'
    sql_sync_url: Optional[str] = 'sqlite:///./dnsmin.db'
