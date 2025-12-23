from fastapi import APIRouter, WebSocket

from dnsmin.lib.api.dependencies import get_websocket_user
from dnsmin.routers.root import router_responses

router = APIRouter(
    prefix='/ws',
    tags=['ws'],
    responses=router_responses,
)


@router.websocket('')
async def websocket_endpoint(ws: WebSocket):
    from dnsmin.app import AsyncSessionLocal, ws_cm
    async with AsyncSessionLocal() as db_session:
        user = await get_websocket_user(ws, db_session)
    if not user:
        return
    await ws_cm.connect(ws)
    try:
        while True:
            await ws.receive_text()  # keep alive / pings
    except Exception:
        ws_cm.disconnect(ws)
