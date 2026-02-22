"""飞书 WebSocket 长连接客户端"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from enum import IntEnum
import json
from typing import TYPE_CHECKING, Optional
from urllib.parse import parse_qs, urlparse

from websockets.asyncio.client import ClientConnection, connect

from .frame import Frame, Header

if TYPE_CHECKING:
    from feishu.adapter import Adapter
    from feishu.bot import Bot
    from feishu.config import BotConfig


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


@dataclass
class WsEndpointResponse:
    """获取 WebSocket 端点 API 的响应。"""

    url: str
    device_id: str
    service_id: int
    ping_interval_ms: int


class WsClient:
    """
    飞书 WebSocket 长连接客户端。

    通过 protobuf Frame 收发，
    支持 ping/pong、分片重组、事件接收与 ack。
    """

    def __init__(
        self,
        adapter: Adapter,
        bot: Bot,
        bot_config: BotConfig,
    ) -> None:
        self._adapter = adapter
        self._bot = bot
        self._bot_config = bot_config
        self._device_id: str = ""
        self._service_id: int = 0
        self._ping_interval_ms: int = 90_000
        self._ping_task: Optional[asyncio.Task[None]] = None
        self._cache: dict[str, list[FrameSegment]] = {}
        self._ws: Optional[ClientConnection] = None
        self._tasks: set[asyncio.Task] = set()

    def _get_ws_endpoint_url(self) -> str:
        """获取「获取 WebSocket 端点」的 HTTP URL"""
        base = self._adapter.get_api_base(self._bot_config)
        return str(base).rstrip("/") + "/callback/ws/endpoint"

    async def _fetch_endpoint(self) -> WsEndpointResponse:
        """请求 WebSocket 端点 URL 与配置。"""
        url = self._get_ws_endpoint_url()
        # 请求体使用 AppID / AppSecret
        body = {
            "AppID": self._bot_config.app_id,
            "AppSecret": self._bot_config.app_secret,
        }
        from nonebot.drivers import Request

        req = Request("POST", url, json=body)
        response = await self._adapter.send_request(req)
        if not isinstance(response, dict):
            raise RuntimeError("Ws endpoint response is not dict")
        code = response.get("code", -1)
        if code != 0:
            msg = response.get("msg", "unknown")
            raise RuntimeError(f"Failed to get gateway url: {code} {msg}")
        data = response.get("data")
        if not data or not isinstance(data, dict):
            raise RuntimeError("Ws endpoint data missing")
        ws_url = data.get("URL")
        if not ws_url or not isinstance(ws_url, str):
            raise RuntimeError("Ws endpoint URL missing")
        parsed = urlparse(ws_url)
        params = parse_qs(parsed.query)
        device_id = (params.get("device_id") or [""])[0]
        service_id_str = (params.get("service_id") or ["0"])[0]
        service_id = int(service_id_str)
        client_config = data.get("ClientConfig") or {}
        if isinstance(client_config, dict):
            ping_interval_sec = client_config.get("PingInterval", 90)
        else:
            ping_interval_sec = 90
        ping_interval_ms = int(ping_interval_sec) * 1000
        return WsEndpointResponse(
            url=ws_url,
            device_id=device_id,
            service_id=service_id,
            ping_interval_ms=ping_interval_ms,
        )

    def _headers_to_dict(self, headers: list[Header]) -> dict[str, str]:
        """将 Frame 的 headers 转为 dict。"""
        return {h.key: h.value for h in headers}

    async def _send_frame_async(self, frame: Frame) -> None:
        if self._ws is None:
            return
        await self._ws.send(bytes(frame))

    def _ping(self) -> None:
        """构造并发送 ping 帧（不 await，由调用方在循环里 send）。"""
        frame = Frame(
            seq_id=0,
            log_id=0,
            service=self._service_id,
            method=FrameType.CONTROL,
            headers=[Header(key="type", value=MessageType.PING)],
        )
        task = asyncio.create_task(self._send_frame_async(frame))
        task.add_done_callback(self._tasks.discard)
        self._tasks.add(task)

    def _retrieve(self, seg: FrameSegment) -> Optional[bytes]:
        """重组分片；若已收齐则返回完整 payload 并清除缓存。"""
        mid, total, data = seg.message_id, seg.sum, seg.data
        if total == 1:
            return data
        if mid not in self._cache:
            self._cache[mid] = []
        self._cache[mid].append(seg)
        if len(self._cache[mid]) != total:
            return None
        parts = sorted(self._cache[mid], key=lambda x: x.seq)
        result = b"".join(p.data for p in parts)
        del self._cache[mid]
        return result

    async def _handle_message(self, raw: bytes) -> None:
        """处理一条二进制消息。"""
        try:
            frame = Frame().parse(raw)
        except Exception:
            return
        headers_dict = self._headers_to_dict(frame.headers)
        msg_type = headers_dict.get("type", "")
        method = frame.method

        if method == FrameType.CONTROL and msg_type == MessageType.PONG:
            return

        if method == FrameType.DATA and msg_type == MessageType.EVENT:
            message_id = headers_dict.get("message_id", "")
            sum_str = headers_dict.get("sum", "1")
            seq_str = headers_dict.get("seq", "0")
            try:
                total = int(sum_str)
                seq = int(seq_str)
            except ValueError:
                return
            seg = FrameSegment(
                message_id=message_id,
                sum=total,
                seq=seq,
                data=frame.payload or b"",
            )
            payload_bytes = self._retrieve(seg)
            if payload_bytes is None:
                return
            try:
                body = json.loads(payload_bytes.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError):
                return
            if not isinstance(body, dict) or not body.get("header"):
                return
            body.setdefault("type", body.get("header", {}).get("event_type", ""))
            event = self._adapter.json_to_event(body)
            if event is not None:
                task = asyncio.create_task(self._bot.handle_event(event))
                task.add_done_callback(self._adapter.tasks.discard)
                self._adapter.tasks.add(task)
            # ack：原样回传 frame，并加上 biz_rt: 0，payload 为 {"code": 200}
            ack_headers = [*list(frame.headers), Header(key="biz_rt", value="0")]
            ack_frame = Frame(
                seq_id=frame.seq_id,
                log_id=frame.log_id,
                service=frame.service,
                method=frame.method,
                headers=ack_headers,
                payload=json.dumps({"code": 200}).encode("utf-8"),
            )
            await self._send_frame_async(ack_frame)

    async def run(self) -> None:
        """拉取端点、连接 WebSocket、循环收发并维持 ping。"""
        resp = await self._fetch_endpoint()
        self._device_id = resp.device_id
        self._service_id = resp.service_id
        self._ping_interval_ms = resp.ping_interval_ms
        url = resp.url

        async def ping_loop() -> None:
            while True:
                await asyncio.sleep(self._ping_interval_ms / 1000.0)
                if self._ws is None:
                    break
                self._ping()

        async with connect(url) as ws:
            self._ws = ws
            self._ping_task = asyncio.create_task(ping_loop())
            try:
                self._ping()
                async for raw in ws:
                    if isinstance(raw, bytes):
                        await self._handle_message(raw)
            finally:
                if self._ping_task is not None:
                    self._ping_task.cancel()
                    try:
                        await self._ping_task
                    except asyncio.CancelledError:
                        pass
                self._ws = None
