"""飞书 WebSocket 长连接模块。"""

from .client import WsClient
from .frame import Frame, Header

__all__ = ["Frame", "Header", "WsClient"]
