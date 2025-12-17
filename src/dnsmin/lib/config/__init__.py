from dnsmin.lib.config.app import AppConfig
from dnsmin.lib.config.api import ApiConfig
from dnsmin.lib.config.base import BaseConfig
from dnsmin.lib.config.celery import CeleryConfig
from dnsmin.lib.config.db import DbConfig
from dnsmin.lib.config.logging import LoggingConfig
from dnsmin.lib.config.mail import MailConfig
from dnsmin.lib.config.notifications import NotificationsConfig
from dnsmin.lib.config.paths import PathsConfig
from dnsmin.lib.config.server import ServerConfig
from dnsmin.lib.config.services import ServicesConfig
from dnsmin.lib.config.tasks import TasksConfig


class Config(BaseConfig):
    """A model that represents the root level element of the app configuration hierarchy."""

    api: ApiConfig
    app: AppConfig
    celery: CeleryConfig
    db: DbConfig
    logging: LoggingConfig
    mail: MailConfig
    notifications: NotificationsConfig
    paths: PathsConfig
    server: ServerConfig
    services: ServicesConfig
    tasks: TasksConfig
