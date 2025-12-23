from fastapi import WebSocket
from fastapi.requests import Request


def get_client_ip(request: Request | WebSocket) -> str:
    client_ip = request.headers.get('X-Forwarded-For', None)

    if client_ip is None:
        client_ip = request.headers.get('X-Real-IP', None)

    if client_ip is None:
        client_ip = request.client.host

    return client_ip
