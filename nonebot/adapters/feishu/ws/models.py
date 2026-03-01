"""WebSocket 相关 API 响应模型。"""

from dataclasses import dataclass
from enum import IntEnum

from pydantic import BaseModel, Field

from nonebot.compat import PYDANTIC_V2, ConfigDict


class FrameType(IntEnum):
    """帧类型。"""

    CONTROL = 0
    DATA = 1


class MessageType:
    """消息类型字符串。"""

    EVENT = "event"
    CARD = "card"
    PING = "ping"
    PONG = "pong"


@dataclass
class FrameSegment:
    """分片消息片段，用于重组。"""

    message_id: str
    sum: int
    seq: int
    data: bytes


class WsEndpointClientConfig(BaseModel):
    """WebSocket 端点返回的 ClientConfig，字段与 API 驼峰命名一致。"""

    if PYDANTIC_V2:
        model_config = ConfigDict(populate_by_name=True)
    else:

        class Config:
            allow_population_by_field_name = True

    ping_interval: int = Field(default=90, alias="PingInterval")
    reconnect_count: int = Field(default=-1, alias="ReconnectCount")
    reconnect_interval: int = Field(default=90, alias="ReconnectInterval")
    reconnect_nonce: int = Field(default=25, alias="ReconnectNonce")


class WsEndpointData(BaseModel):
    """WebSocket 端点 API 的 data 字段。"""

    url: str = Field(alias="URL")
    client_config: WsEndpointClientConfig = Field(
        default_factory=WsEndpointClientConfig,
        alias="ClientConfig",
    )


class WsEndpointApiResponse(BaseModel):
    """获取 WebSocket 端点 API 的完整响应。"""

    code: int
    msg: str = ""
    data: WsEndpointData | None = None


class WsEndpointResponse(BaseModel):
    """解析后的 WebSocket 端点结果，供客户端使用。

    device_id 与 service_id 从 data.URL 的查询参数中解析得到。
    """

    url: str
    device_id: str
    service_id: int
    ping_interval_seconds: int
    client_config: WsEndpointClientConfig
