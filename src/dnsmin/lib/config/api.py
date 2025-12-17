from dnsmin.lib.config.base import BaseConfig


class ApiConfig(BaseConfig):
    """A model that represents a configuration hierarchy for the FastAPI app."""

    class ApiMetadataConfig(BaseConfig):
        class ApiMetadataTagConfig(BaseConfig):
            name: str
            description: str

        tags: list[ApiMetadataTagConfig] = []

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            if not self.tags:
                self.tags = [
                    self.ApiMetadataTagConfig(
                        name='default',
                        description='Provides browser client entrypoint and monitoring functionality.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='user',
                        description='Provides functionality for user-related features (registration, authentication, security, profile management, etc.)',
                    ),
                    self.ApiMetadataTagConfig(
                        name='auth',
                        description='Provides functionality for managing users and clients.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='acl',
                        description='Provides functionality for managing ACL roles and policies.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='settings',
                        description='Provides functionality for managing system, tenant, and user level settings.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='system',
                        description='Provides functionality for managing system resources.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='tenants',
                        description='Provides functionality for managing system tenants.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='servers',
                        description='Provides functionality for managing DNS servers and settings.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='zones',
                        description='Provides functionality for managing DNS zones and records.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='tasks',
                        description='Provides functionality for managing and monitoring task execution.',
                    ),
                    self.ApiMetadataTagConfig(
                        name='dev',
                        description='Provides development mode resources and tools.',
                    ),
                ]

    metadata: ApiMetadataConfig
