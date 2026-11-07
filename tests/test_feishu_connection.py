from collections.abc import Callable
import json
from pathlib import Path

from larkify.webhooks import sign
from larkify.webhooks.crypto import encrypt
from nonebug import App
import pytest

import nonebot
from nonebot.adapters.feishu import Adapter, Bot, Event, GroupMessageEvent
from nonebot.adapters.feishu.models import BotInfo
from nonebot.compat import type_validate_python

with (Path(__file__).parent.joinpath("data", "bots.json")).open("r") as f:
    feishu_bots = json.load(f)

with (Path(__file__).parent.joinpath("data", "bots_info.json")).open("r") as f:
    bots_info = json.load(f)

with (Path(__file__).parent.joinpath("data", "events.json")).open("r", encoding="utf8") as f:
    test_events = json.load(f)

bot_id = feishu_bots[0]["app_id"]
TOKEN = feishu_bots[0]["verification_token"]

encrypted_bot = feishu_bots[2]
ENCRYPT_KEY = encrypted_bot["encrypt_key"]
ENCRYPTED_TOKEN = encrypted_bot["verification_token"]


def message_event(token: str) -> dict:
    event = {k: v for k, v in test_events[0].items() if k != "_model"}
    return {**event, "header": {**event["header"], "token": token}}


def encrypted(payload: dict) -> bytes:
    plaintext = json.dumps(payload).encode()
    return json.dumps({"encrypt": encrypt(ENCRYPT_KEY, plaintext, b"0123456789abcdef")}).encode()


def signed(body: bytes) -> dict[str, str]:
    return {
        "X-Lark-Request-Timestamp": "1700000000",
        "X-Lark-Request-Nonce": "nonce",
        "X-Lark-Signature": sign(ENCRYPT_KEY, "1700000000", "nonce", body),
    }


@pytest.fixture
def handled(monkeypatch: pytest.MonkeyPatch) -> list[Event]:
    events: list[Event] = []

    async def handle_event(self: Bot, event: Event) -> None:
        events.append(event)

    monkeypatch.setattr(Bot, "handle_event", handle_event)
    return events


@pytest.fixture
def connect(monkeypatch: pytest.MonkeyPatch) -> Callable[[str], None]:
    """让路由对应的 Bot 处于已连接状态，不受其他测试断开连接的影响。"""

    def connect(app_id: str) -> None:
        adapter = nonebot.get_adapter(Adapter)
        bot = Bot(
            adapter,
            app_id,
            bot_config=adapter.bot_apps[app_id],
            bot_info=type_validate_python(BotInfo, bots_info["bot"]),
        )
        monkeypatch.setitem(adapter.bots, app_id, bot)

    return connect


@pytest.mark.anyio
@pytest.mark.parametrize("endpoints", [f"/feishu/{bot_id}"])
async def test_http(app: App, endpoints: str):
    with (Path(__file__).parent.joinpath("data", "payloads.json")).open("r") as f:
        test_payloads = json.load(f)

    adapter = nonebot.get_adapter(Adapter)

    async with app.test_server() as ctx:
        client = ctx.get_client()
        payload = test_payloads[0]
        resp = await client.post(endpoints, json=payload)
        assert resp.status_code == 200
        assert resp.json() == {"challenge": payload["challenge"]}
        bots = nonebot.get_bots()
        assert bot_id in bots
        assert bot_id in adapter.bots
        adapter.bot_disconnect(bots[bot_id])


@pytest.mark.anyio
async def test_webhook_events_reach_the_bot(app: App, handled: list[Event], connect: Callable[[str], None]):
    async with app.test_server() as ctx:
        connect(bot_id)
        resp = await ctx.get_client().post(f"/feishu/{bot_id}", json=message_event(TOKEN))

        assert resp.status_code == 200
        assert resp.json() == {"msg": "success"}

    assert len(handled) == 1
    assert isinstance(handled[0], GroupMessageEvent)


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("content", "status_code"),
    [
        pytest.param(json.dumps(message_event("forged")), 401, id="wrong token"),
        pytest.param(
            json.dumps({"challenge": "c", "token": "forged", "type": "url_verification"}), 401, id="challenge"
        ),
        pytest.param(json.dumps({"uuid": "u", "token": TOKEN, "event": {"type": "message"}}), 400, id="event v1"),
        pytest.param("<xml>", 400, id="not json"),
    ],
)
async def test_webhook_rejects_bad_deliveries(
    app: App, handled: list[Event], connect: Callable[[str], None], content: str, status_code: int
):
    async with app.test_server() as ctx:
        connect(bot_id)
        resp = await ctx.get_client().post(f"/feishu/{bot_id}", data=content)

        assert resp.status_code == status_code

    assert not handled


@pytest.mark.anyio
async def test_encrypted_webhook(app: App, handled: list[Event], connect: Callable[[str], None]):
    url = f"/feishu/{encrypted_bot['app_id']}"
    event = encrypted(message_event(ENCRYPTED_TOKEN))
    challenge = encrypted({"challenge": "c", "token": ENCRYPTED_TOKEN, "type": "url_verification"})

    async with app.test_server() as ctx:
        connect(encrypted_bot["app_id"])
        client = ctx.get_client()

        resp = await client.post(url, data=challenge)
        assert resp.json() == {"challenge": "c"}

        resp = await client.post(url, data=event, headers=signed(event))
        assert resp.status_code == 200

    assert len(handled) == 1
    assert isinstance(handled[0], GroupMessageEvent)


@pytest.mark.anyio
@pytest.mark.parametrize(
    "headers",
    [
        pytest.param({}, id="unsigned"),
        pytest.param({**signed(b""), "X-Lark-Signature": "forged"}, id="forged"),
    ],
)
async def test_encrypted_webhook_needs_a_signature(
    app: App, handled: list[Event], connect: Callable[[str], None], headers: dict[str, str]
):
    url = f"/feishu/{encrypted_bot['app_id']}"
    event = encrypted(message_event(ENCRYPTED_TOKEN))

    async with app.test_server() as ctx:
        connect(encrypted_bot["app_id"])
        resp = await ctx.get_client().post(url, data=event, headers=headers)

        assert resp.status_code == 401

    assert not handled
