from typing import Set

from fastapi import WebSocket
from redis.asyncio.client import Redis


class ConnectionManager:
    def __init__(self):
        self.connections: Set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.add(ws)

    def disconnect(self, ws: WebSocket):
        self.connections.discard(ws)

    async def broadcast(self, message: str):
        for ws in list(self.connections):
            try:
                await ws.send_text(message)
            except Exception:
                self.disconnect(ws)


async def redis_listener(redis: Redis, manager: ConnectionManager):
    pubsub = redis.pubsub()

    await pubsub.subscribe("ws:broadcast")

    async for message in pubsub.listen():
        if message["type"] != "message":
            continue

        await manager.broadcast(message["data"])
