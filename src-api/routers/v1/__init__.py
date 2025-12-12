from fastapi import APIRouter

from app import config
from lib.config.app import EnvironmentEnum
from routers.root import router_responses
from routers.v1 import user, auth, acl, settings, system, tenants, servers, zones, tasks, services

router = APIRouter(
    prefix='/v1',
    responses=router_responses,
)

# Setup descendent routers
router.include_router(user.router)
router.include_router(auth.router)
router.include_router(acl.router)
router.include_router(settings.router)
router.include_router(system.router)
router.include_router(tenants.router)
router.include_router(servers.router)
router.include_router(zones.router)
router.include_router(services.router)

if config.app.environment.name in (EnvironmentEnum.local, EnvironmentEnum.dev):
    router.include_router(tasks.router)
