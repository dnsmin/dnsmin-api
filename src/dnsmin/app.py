from __future__ import annotations
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI
from jinja2 import Environment, FileSystemLoader, select_autoescape
from redis.asyncio import Redis
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from dnsmin.lib import AppSettings
from dnsmin.lib.api.websockets import ConnectionManager, redis_listener
from dnsmin.lib.config import Config
from dnsmin.lib.config.app import AppConfig
from dnsmin.lib.config.tasks import TaskSchedule
from dnsmin.lib.notifications.config import NotificationConfig
from dnsmin.lib.services.zabbix import ZabbixReporter

DB_PREFIX = 'dnsmin'
INIT_INTERVAL_DEFAULT = 300
INIT_INTERVAL_THRESHOLD = 0.5
INIT_DB_INTERVAL_DEFAULT = 300
INIT_DB_INTERVAL_THRESHOLD = 0.5

settings: Optional[AppSettings] = None
config: Optional[Config] = None
notifications: Optional[list[NotificationConfig]] = None
schedules: Optional[list[TaskSchedule]] = None
j2: Optional[Environment] = None
db_engine: Optional[AsyncEngine] = None
db_engine_sync = Optional[Engine]
AsyncSessionLocal: Optional[async_sessionmaker[AsyncSession]] = None
SessionLocal: Optional[sessionmaker[Session]] = None
redis: Optional[Redis] = None
zabbix: Optional[ZabbixReporter] = None
ws_cm: Optional[ConnectionManager] = None


def app_startup(use_sync: bool = False):
    """Executes appropriate app startup tasks."""
    from dnsmin.lib import load_environment, load_settings, init_logging, init_redis, init_sql
    from dnsmin.lib.jinja import JinjaFilters

    global settings, config, notifications, schedules, redis, db_engine, db_engine_sync, AsyncSessionLocal, \
        SessionLocal, ws_cm, j2, zabbix

    # Initialize logging configuration with defaults
    init_logging()

    # Get the environment variable prefix from the default configuration
    env_prefix = AppConfig.EnvironmentConfig.model_fields['prefix'].default

    # Load the environment settings from the file system
    load_environment(env_prefix)

    # Load the application settings model based on default environment settings
    settings = load_settings(env_prefix=env_prefix)
    # Reload the application settings model based on prefix loaded from the environment if different from the default
    if settings.env_prefix != env_prefix:
        settings = load_settings(env_prefix=settings.env_prefix)

    # Load app configuration into a statically typed object mimicking the hierarchy
    config = settings.config

    # Load app notifications configuration
    notifications = settings.notifications

    # Load app scheduling configuration
    schedules = settings.schedules

    # Re-initialize logging configuration with loaded environment and configuration settings
    init_logging(config=config, settings=settings)

    # Initialize Redis connection
    redis = init_redis(config=config)

    # Initialize SQL connection
    db_engine, AsyncSessionLocal = init_sql(config=config, use_sync=False)
    if use_sync:
        db_engine_sync, SessionLocal = init_sql(config=config, use_sync=True)

    # Set up websocket connection manager
    ws_cm = ConnectionManager()

    # Set up Jinja2 template rendering
    j2 = Environment(
        loader=FileSystemLoader(config.paths.templates),
        autoescape=select_autoescape(),
    )

    j2.globals['settings'] = settings
    j2.globals['config'] = config
    j2.filters = JinjaFilters.implement_filters(j2.filters)

    # Initialize Zabbix Reporter
    zabbix = ZabbixReporter(config=config.services.zabbix)
    zabbix.start()

    return config


async def app_shutdown(use_sync: bool = False):
    """Executes appropriate app shutdown tasks."""
    global db_engine, db_engine_sync, redis, zabbix

    # Dispose of SQL connection pool
    await db_engine.dispose()

    if use_sync:
        db_engine_sync.dispose()

    # Dispose of Redis connection pool
    await redis.close()

    # Stop Zabbix Reporter worker
    await zabbix.stop_async()


STARTUP_TASKS = []
RUNNING_TASKS = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    import asyncio
    from dnsmin.routers import install_routers

    config = app_startup()

    # Create the redis listener for websockets as a background task
    STARTUP_TASKS.append(lambda: redis_listener(redis, ws_cm))

    # Initialize all tasks defined in STARTUP_TASKS list
    for task in STARTUP_TASKS:
        RUNNING_TASKS.append(asyncio.create_task(task()))

    # Set up FastAPI routers
    install_routers(app, config)

    yield

    # Cancel all tasks defined in the RUNNING_TASKS list
    for task in RUNNING_TASKS:
        task.cancel()

    await app_shutdown()
