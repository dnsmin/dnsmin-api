from fastapi import APIRouter
from dnsmin.routers.root import router_responses
from dnsmin.routers.v1.services import mail

router = APIRouter(
    prefix='/services',
    tags=['services'],
    responses=router_responses,
)

# Setup descendent routers
router.include_router(mail.router)
