from fastapi import FastAPI

from dnsmin.lib.config import Config


def install_routers(app: FastAPI, config: Config) -> None:
    """Attach local and global routers"""
    from dnsmin.lib.config.app import EnvironmentEnum
    from dnsmin.routers import root, api, dev

    # Attach API router to root router
    root.router.include_router(api.router)

    # Dev Router
    if config.app.environment.name in (EnvironmentEnum.local, EnvironmentEnum.dev):
        root.router.include_router(dev.router)

    # Attach root router to app
    app.include_router(root.router)
