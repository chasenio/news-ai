import logging
import typing as t
from typing import TYPE_CHECKING
from contextvars import ContextVar
from starlette.datastructures import MutableHeaders
from dataclasses import dataclass

if TYPE_CHECKING:
    from starlette.types import ASGIApp, Message, Receive, Scope, Send

_logger = logging.getLogger(__name__)

connection_ctx = ContextVar('connection_ctx')
took = ContextVar('took', default=0.0)


@dataclass
class ClientInfo:
    ip: str
    port: t.Optional[int] = 0
    country: t.Optional[str] = None


def set_client_by_header(headers: t.Mapping[str, str]) -> t.Optional[ClientInfo]:
    ip_header: str = 'cf-connecting-ip'
    country_header: str = 'cf-ipcountry'
    # 前端转发过来的
    x_connecting_ip = "x-connecting-ip"
    x_ip_country = "x-ipcountry"
    client = None
    # from front end
    if x_ip := headers.get(x_connecting_ip):
        ip = x_ip
        country = headers.get(x_ip_country)
        client = ClientInfo(ip=ip, country=country)
    # from cloudflare
    elif header_value := headers.get(ip_header.lower()):
        ip = header_value
        country = headers.get(country_header)
        client = ClientInfo(ip=ip, country=country)
    # from other
    else:
        x_forwarded_for = headers.get('x-forwarded-for')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
            client = ClientInfo(ip=ip)
    return client


class ConnectMiddleware:
    app: 'ASGIApp'

    def __init__(self, app: 'ASGIApp', default: t.Optional[str] = "127.0.0.1") -> None:
        self.app = app
        self.default = default

    async def __call__(self, scope, receive, send) -> None:
        if scope['type'] != 'http':
            await self.app(scope, receive, send)
            return

        # Try to load request ID from the request headers
        headers: t.Mapping[str, str] = MutableHeaders(scope=scope)
        client = set_client_by_header(headers)
        if client is None:
            ip = scope['client'][0] if scope['client'] else self.default
            port = scope['client'][1] if scope['client'] else 0
            client = ClientInfo(ip=ip, port=port)
        connection_ctx.set(client)

        await self.app(scope, receive, send)
        return
