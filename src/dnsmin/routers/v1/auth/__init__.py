from fastapi import APIRouter

from dnsmin.routers.root import router_responses

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
    responses=router_responses,
)

from .users import *
from .clients import *
from .sessions import *
