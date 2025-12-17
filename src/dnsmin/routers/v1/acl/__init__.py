from fastapi import APIRouter

from dnsmin.routers.root import router_responses

router = APIRouter(
    prefix='/acl',
    tags=['acl'],
    responses=router_responses,
)

from .metadata import *
from .roles import *
from .policies import *
