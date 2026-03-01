"""飞书 WebSocket 长连接客户端"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from enum import IntEnum
import json
from typing import TYPE_CHECKING, Optional

from nonebot.drivers import URL, Request, WebSocket
from nonebot.utils import escape_tag

from ..utils import log
from .frame import Frame, Header
from .models import WsEndpointApiResponse, WsEndpointResponse

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
        self._ping_interval_seconds: int = 90
        self._ping_task: Optional[asyncio.Task[None]] = None
        self._cache: dict[str, list[FrameSegment]] = {}
        self._ws: Optional[WebSocket] = None
        self._tasks: set[asyncio.Task] = set()

    def _get_ws_endpoint_url(self) -> str:
        """获取「获取 WebSocket 端点」的 HTTP URL"""
        base = self._adapter.get_api_base(self._bot_config)
        return str(base.joinpath("callback/ws/endpoint"))

    async def _fetch_endpoint(self) -> WsEndpointResponse:
        """请求 WebSocket 端点 URL 与配置。

        响应由 Pydantic 解析；device_id 与 service_id 从 data.URL 的查询参数解析。
        """
        url = self._get_ws_endpoint_url()
        body = {
            "AppID": self._bot_config.app_id,
            "AppSecret": self._bot_config.app_secret,
        }
        req = Request("POST", url, json=body)
        response = await self._adapter.send_request(req)
        if not isinstance(response, dict):
            raise RuntimeError("Ws endpoint response is not dict")
        result = WsEndpointApiResponse.model_validate(response)
        if result.code != 0:
            raise RuntimeError(f"Failed to get gateway url: {result.code} {result.msg}")
        if result.data is None:
            raise RuntimeError("Ws endpoint data missing")
        data = result.data
        # device_id、service_id 从 URL 查询参数读取
        parsed = URL(data.url)
        device_id = parsed.query.get("device_id") or ""
        service_id = int(parsed.query.get("service_id") or "0")

        return WsEndpointResponse(
            url=data.url,
            device_id=device_id,
            service_id=service_id,
            ping_interval_seconds=data.client_config.ping_interval,
            client_config=data.client_config,
        )

    def _headers_to_dict(self, headers: list[Header]) -> dict[str, str]:
        """将 Frame 的 headers 转为 dict。"""
        return {h.key: h.value for h in headers}

    async def _send_frame_async(self, frame: Frame) -> None:
        if self._ws is None:
            return
        await self._ws.send_bytes(bytes(frame))

    def _ping(self) -> None:
        """构造并发送 ping 帧"""
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
        except Exception as e:
            log("WARNING", f"Failed to parse frame: {e!r}, raw_hex={raw.hex()!r}")
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
        """拉取端点、通过 NoneBot Driver 建立 WebSocket 连接，循环收发并维持 ping。"""
        resp = await self._fetch_endpoint()
        self._device_id = resp.device_id
        self._service_id = resp.service_id
        self._ping_interval_seconds = resp.ping_interval_seconds
        url = resp.url

        async def ping_loop() -> None:
            while True:
                await asyncio.sleep(self._ping_interval_seconds)
                if self._ws is None:
                    break
                self._ping()

        request = Request("GET", url, timeout=30.0)
        async with self._adapter.websocket(request) as ws:
            self._ws = ws
            log(
                "INFO",
                f"<y>Bot {escape_tag(self._bot_config.app_id)}</y> WebSocket connected",
            )
            self._ping_task = asyncio.create_task(ping_loop())
            try:
                self._ping()
                while True:
                    raw = await ws.receive()
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
