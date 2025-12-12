from fastapi import APIRouter

from routers.root import router_responses

router = APIRouter(
    prefix='/servers',
    tags=['servers'],
    responses=router_responses,
)


from .servers import *
from .autoprimaries import *
from .tsig_keys import *
from .views import *
from .networks import *