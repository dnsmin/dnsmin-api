from fastapi import APIRouter, WebSocket
from dnsmin.routers.root import router_responses

router = APIRouter(
    prefix='/ws',
    tags=['ws'],
    responses=router_responses,
)


@router.websocket('')
async def websocket_endpoint(ws: WebSocket):
    from dnsmin.app import ws_cm
    await ws_cm.connect(ws)
    try:
        while True:
            await ws.receive_text()  # keep alive / pings
    except Exception:
        ws_cm.disconnect(ws)
