from fastapi import APIRouter

from dnsmin.routers.root import router_responses

router = APIRouter(
    prefix='/system',
    tags=['system'],
    responses=router_responses,
)


from .stopgap_domains import *
from .timezones import *
