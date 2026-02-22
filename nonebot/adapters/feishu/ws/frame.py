"""飞书 WebSocket Frame 的 protobuf 定义"""

from dataclasses import dataclass

from betterproto import (
    Message,
    bytes_field,
    int32_field,
    message_field,
    string_field,
    uint64_field,
)


@dataclass
class Header(Message):
    """Frame 头部键值对。"""

    key: str = string_field(1)
    value: str = string_field(2)


@dataclass
class Frame(Message):
    """
    WebSocket 单帧消息，与飞书/ Lark 长连接协议一致。
    """

    seq_id: int = uint64_field(1)
    log_id: int = uint64_field(2)
    service: int = int32_field(3)
    method: int = int32_field(4)
    headers: list[Header] = message_field(5)  # noqa: RUF009
    payload_encoding: str = string_field(6)
    payload_type: str = string_field(7)
    payload: bytes = bytes_field(8)
    log_id_new: str = string_field(9)
