"""长连接：协议由 larkify 实现，这里验证事件能经过真实的 socket 到达 Bot。"""

import asyncio
from collections.abc import AsyncGenerator
import json
from pathlib import Path

from larkify import AppAuthStrategy, Feishu
from larkify.cache import MemCacheStrategy
from larkify.exception import WebSocketError
from larkify.ws import Frame, WSClient
from larkify.ws.frame import METHOD_DATA
import pytest
import wsproto
from wsproto.events import AcceptConnection, BytesMessage, CloseConnection, Request

import nonebot
from nonebot.adapters.feishu import Adapter, Bot, Event, GroupMessageEvent
from nonebot.adapters.feishu import adapter as adapter_module
from nonebot.adapters.feishu.adapter import Dispatcher
from nonebot.adapters.feishu.config import BotConfig, Config
from nonebot.adapters.feishu.models import BotInfo
from nonebot.compat import type_validate_python
from nonebot.config import Env
from nonebot.drivers.none import Driver as NoneDriver

with (Path(__file__).parent.joinpath("data", "bots.json")).open("r") as f:
    feishu_bots = json.load(f)

with (Path(__file__).parent.joinpath("data", "bots_info.json")).open("r") as f:
    bots_info = json.load(f)

with (Path(__file__).parent.joinpath("data", "events.json")).open("r", encoding="utf8") as f:
    test_events = json.load(f)

SERVICE_ID = 77
bot_config = type_validate_python(BotConfig, feishu_bots[1])
ws_config = BotConfig(app_id="app_id_ws", app_secret="secret", verification_token="token", protocol="ws")


class FakeGateway:
    """在同一端口上应答长连接端点和 WebSocket 升级。"""

    def __init__(self) -> None:
        self.port = 0
        self.frames: list[bytes] = []
        self.received: asyncio.Queue[Frame] = asyncio.Queue()

    async def serve(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        try:
            head = await reader.readuntil(b"\r\n\r\n")
            if head.startswith(b"POST"):
                await self._endpoint(head, reader, writer)
            else:
                await self._websocket(head, reader, writer)
        except (asyncio.IncompleteReadError, ConnectionError):
            pass
        finally:
            writer.close()

    async def _endpoint(self, head: bytes, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        length = next(int(line.split(b":")[1]) for line in head.split(b"\r\n") if line.lower().startswith(b"content-l"))
        await reader.readexactly(length)
        url = f"ws://127.0.0.1:{self.port}/ws?device_id=d1&service_id={SERVICE_ID}"
        body = json.dumps({"code": 0, "msg": "ok", "data": {"URL": url}}).encode()
        writer.write(
            b"HTTP/1.1 200 OK\r\ncontent-type: application/json\r\n"
            + f"content-length: {len(body)}\r\nconnection: close\r\n\r\n".encode()
            + body
        )
        await writer.drain()

    async def _websocket(self, head: bytes, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        connection = wsproto.WSConnection(wsproto.ConnectionType.SERVER)
        connection.receive_data(head)
        for event in connection.events():
            if isinstance(event, Request):
                writer.write(connection.send(AcceptConnection()))
        for frame in self.frames:
            writer.write(connection.send(BytesMessage(data=frame)))
        await writer.drain()

        while data := await reader.read(65536):
            connection.receive_data(data)
            for event in connection.events():
                if isinstance(event, BytesMessage):
                    await self.received.put(Frame.decode(bytes(event.data)))
                elif isinstance(event, CloseConnection):
                    return

    async def next_delivery_answer(self) -> Frame:
        while True:
            frame = await asyncio.wait_for(self.received.get(), 5)
            if frame.method == METHOD_DATA:
                return frame


@pytest.fixture
async def gateway() -> AsyncGenerator[FakeGateway, None]:
    fake = FakeGateway()
    server = await asyncio.start_server(fake.serve, "127.0.0.1", 0)
    fake.port = server.sockets[0].getsockname()[1]
    async with server:
        yield fake


@pytest.fixture
def adapter(monkeypatch: pytest.MonkeyPatch) -> Adapter:
    adapter = nonebot.get_adapter(Adapter)
    monkeypatch.setattr(adapter, "bots", {})
    monkeypatch.setattr(adapter, "bot_apps", {})
    monkeypatch.setattr(adapter, "dispatchers", {})
    monkeypatch.setattr(adapter, "bot_connect", lambda bot: adapter.bots.__setitem__(bot.self_id, bot))
    monkeypatch.setattr(adapter, "bot_disconnect", lambda bot: adapter.bots.pop(bot.self_id))
    return adapter


@pytest.fixture
def bot(adapter: Adapter) -> Bot:
    bot = Bot(
        adapter,
        bot_config.app_id,
        bot_config=bot_config,
        bot_info=type_validate_python(BotInfo, bots_info["bot"]),
    )
    adapter.bots[bot.self_id] = bot
    return bot


def event_frames(payload: dict, parts: int = 1) -> list[bytes]:
    raw = json.dumps(payload).encode()
    size = len(raw) // parts + 1
    return [
        Frame(
            seq_id=5,
            log_id=6,
            service=SERVICE_ID,
            method=METHOD_DATA,
            headers=[("type", "event"), ("message_id", "m1"), ("sum", str(parts)), ("seq", str(index))],
            payload=raw[index * size : (index + 1) * size],
        ).encode()
        for index in range(parts)
    ]


def client_for(gateway: FakeGateway, adapter: Adapter) -> WSClient:
    feishu = Feishu(
        AppAuthStrategy("app_id", "secret"),
        base_url=f"http://127.0.0.1:{gateway.port}",
        cache_strategy=MemCacheStrategy(),
        trust_env=False,
    )
    return WSClient(feishu, Dispatcher(adapter, bot_config))


@pytest.mark.anyio
@pytest.mark.parametrize("parts", [pytest.param(1, id="whole"), pytest.param(3, id="split")])
async def test_events_reach_the_bot_and_are_acknowledged(
    gateway: FakeGateway, adapter: Adapter, bot: Bot, monkeypatch: pytest.MonkeyPatch, parts: int
):
    handled: list[Event] = []

    async def handle_event(self: Bot, event: Event) -> None:
        handled.append(event)

    monkeypatch.setattr(Bot, "handle_event", handle_event)
    payload = {k: v for k, v in test_events[0].items() if k != "_model"}
    gateway.frames = event_frames(payload, parts)[::-1]

    adapter.create_task(adapter._run_ws(client_for(gateway, adapter), bot))
    answer = await gateway.next_delivery_answer()
    await asyncio.sleep(0)
    await adapter._stop()

    assert json.loads(answer.payload or b"") == {"code": 200}
    assert answer.service == SERVICE_ID
    assert len(handled) == 1
    assert isinstance(handled[0], GroupMessageEvent)
    assert not adapter.tasks


@pytest.mark.anyio
async def test_slow_handlers_do_not_delay_the_acknowledgement(
    gateway: FakeGateway, adapter: Adapter, bot: Bot, monkeypatch: pytest.MonkeyPatch
):
    release = asyncio.Event()

    async def handle_event(self: Bot, event: Event) -> None:
        await release.wait()

    monkeypatch.setattr(Bot, "handle_event", handle_event)
    gateway.frames = event_frames({k: v for k, v in test_events[0].items() if k != "_model"})

    adapter.create_task(adapter._run_ws(client_for(gateway, adapter), bot))
    answer = await gateway.next_delivery_answer()
    release.set()
    await adapter._stop()

    assert json.loads(answer.payload or b"") == {"code": 200}


@pytest.mark.anyio
async def test_gives_up_when_larkify_cannot_recover(adapter: Adapter, bot: Bot):
    class Client:
        async def arun(self) -> None:
            raise WebSocketError(403, "forbidden", retryable=False)

    await adapter._run_ws(Client(), bot)  # type: ignore[arg-type]

    assert bot.self_id not in adapter.bots


@pytest.mark.anyio
async def test_unexpected_errors_reconnect(adapter: Adapter, bot: Bot, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(adapter_module, "RECONNECT_INTERVAL", 0)

    class Client:
        runs = 0

        async def arun(self) -> None:
            self.runs += 1
            if self.runs == 1:
                raise RuntimeError("unexpected")
            raise WebSocketError(403, "forbidden", retryable=False)

    client = Client()
    await adapter._run_ws(client, bot)  # type: ignore[arg-type]

    assert client.runs == 2


@pytest.mark.anyio
async def test_startup_starts_the_long_connection(adapter: Adapter, monkeypatch: pytest.MonkeyPatch):
    started: list[Bot] = []

    async def run_ws(client: WSClient, bot: Bot) -> None:
        started.append(bot)

    monkeypatch.setattr(adapter, "_run_ws", run_ws)
    monkeypatch.setattr(adapter.feishu_config, "feishu_bots", [ws_config])

    await adapter.startup()
    await asyncio.sleep(0)
    await adapter._stop()

    assert [bot.self_id for bot in started] == [ws_config.app_id]


@pytest.mark.anyio
async def test_startup_skips_bots_that_fail(adapter: Adapter, monkeypatch: pytest.MonkeyPatch):
    invalid = BotConfig(app_id="app_id_invalid", app_secret="secret", verification_token="token", protocol="ws")
    monkeypatch.setattr(adapter.feishu_config, "feishu_bots", [invalid, ws_config])
    monkeypatch.setattr(adapter, "_run_ws", lambda client, bot: asyncio.sleep(0))

    await adapter.startup()
    await adapter._stop()

    assert list(adapter.bots) == [ws_config.app_id]


def test_webhooks_need_an_asgi_driver():
    driver = nonebot.get_driver()

    with pytest.raises(RuntimeError, match="ASGI"):
        Adapter(NoneDriver(Env(environment=driver.env), driver.config))


def test_long_connections_work_without_an_asgi_driver(monkeypatch: pytest.MonkeyPatch):
    driver = nonebot.get_driver()
    monkeypatch.setattr(adapter_module, "get_plugin_config", lambda _: Config(feishu_bots=[ws_config]))

    Adapter(NoneDriver(Env(environment=driver.env), driver.config))
