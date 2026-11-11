import json
from pathlib import Path
from typing import Any

from nonebug import App
import pytest

import nonebot
from nonebot.adapters.feishu import Adapter
from nonebot.adapters.feishu.bot import Bot, _check_at_me, _check_nickname, _check_reply
from nonebot.adapters.feishu.config import BotConfig
from nonebot.adapters.feishu.event import GroupMessageEvent
from nonebot.adapters.feishu.models import BotInfo
from nonebot.compat import type_validate_python

with (Path(__file__).parent.joinpath("data", "bots.json")).open("r") as f:
    feishu_bots = json.load(f)

test_bot = feishu_bots[1]
bot_id = test_bot["app_id"]

with (Path(__file__).parent.joinpath("data", "bots_info.json")).open("r") as f:
    bots_info = json.load(f)

with (Path(__file__).parent.joinpath("data", "events.json")).open("r", encoding="utf8") as f:
    test_events = json.load(f)


@pytest.mark.anyio
async def test_check_tome(server_url: str):
    event_data = test_events[0]
    event_data.pop("_model", None)
    event = Adapter.json_to_event(event_data)
    assert isinstance(event, GroupMessageEvent)

    adapter = nonebot.get_adapter(Adapter)
    adapter.feishu_config.feishu_api_base = str(server_url)  # type: ignore
    bot = Bot(
        adapter,
        bot_id,
        bot_config=type_validate_python(BotConfig, test_bot),
        bot_info=type_validate_python(BotInfo, bots_info["bot"]),
    )
    _check_at_me(bot, event)
    assert not event.to_me

    event_data = test_events[1]
    event_data.pop("_model", None)
    event = Adapter.json_to_event(event_data)
    _check_at_me(bot, event)
    assert event.to_me


@pytest.mark.anyio
async def test_check_reply(server_url: str):
    event_data = test_events[0]
    event_data.pop("_model", None)
    event = Adapter.json_to_event(event_data)
    assert isinstance(event, GroupMessageEvent)

    adapter = nonebot.get_adapter(Adapter)
    adapter.feishu_config.feishu_api_base = str(server_url)  # type: ignore
    bot = Bot(
        adapter,
        bot_id,
        bot_config=type_validate_python(BotConfig, test_bot),
        bot_info=type_validate_python(BotInfo, bots_info["bot"]),
    )
    await _check_reply(bot, event)
    assert not event.reply


@pytest.mark.anyio
async def test_check_nickname(app: App, server_url: str):
    event_data = test_events[0]
    event_data.pop("_model", None)
    event = Adapter.json_to_event(event_data)
    assert isinstance(event, GroupMessageEvent)

    adapter = nonebot.get_adapter(Adapter)
    adapter.feishu_config.feishu_api_base = str(server_url)  # type: ignore
    bot = Bot(
        adapter,
        bot_id,
        bot_config=type_validate_python(BotConfig, test_bot),
        bot_info=type_validate_python(BotInfo, bots_info["bot"]),
    )
    _check_nickname(bot, event)
    assert event.to_me

    event_data = test_events[1]
    event_data.pop("_model", None)
    event = Adapter.json_to_event(event_data)
    _check_nickname(bot, event)
    assert not event.to_me


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("msg_type", "content"),
    [
        pytest.param(
            "interactive",
            {"title": "卡片标题", "elements": [[{"tag": "text", "text": "卡片内容"}]]},
            id="card",
        ),
        pytest.param("image", {"image_key": "img_1", "added_later": "value"}, id="added field"),
    ],
)
async def test_received_message_reaches_matchers(
    server_url: str, monkeypatch: pytest.MonkeyPatch, msg_type: str, content: dict[str, Any]
):
    event_data = {k: v for k, v in test_events[0].items() if k != "_model"}
    message = {**event_data["event"]["message"], "message_type": msg_type, "content": json.dumps(content)}
    event = Adapter.json_to_event({**event_data, "event": {**event_data["event"], "message": message}})
    assert isinstance(event, GroupMessageEvent)

    handled = []

    async def handle_event(bot: Bot, event: GroupMessageEvent) -> None:
        handled.append(event)

    monkeypatch.setattr("nonebot.adapters.feishu.bot.handle_event", handle_event)

    bot = Bot(
        nonebot.get_adapter(Adapter),
        bot_id,
        bot_config=type_validate_python(BotConfig, test_bot),
        bot_info=type_validate_python(BotInfo, bots_info["bot"]),
    )
    await bot.handle_event(event)

    assert handled == [event]
    assert event.get_message()[0].type == msg_type
    assert event.get_event_description()


@pytest.mark.anyio
async def test_check_tome_in_post():
    """@ 机器人的富文本与文本消息一样去掉开头的 @，命令可以匹配"""
    event_data = {k: v for k, v in test_events[1].items() if k != "_model"}
    content = {
        "title": "",
        "content": [
            [
                {"tag": "at", "user_id": "@_user_1", "user_name": "bot", "style": []},
                {"tag": "text", "text": " /say 34567", "style": []},
            ],
            [{"tag": "img", "image_key": "img_1"}],
        ],
    }
    message = {**event_data["event"]["message"], "message_type": "post", "content": json.dumps(content)}
    event = Adapter.json_to_event({**event_data, "event": {**event_data["event"], "message": message}})
    assert isinstance(event, GroupMessageEvent)

    bot = Bot(
        nonebot.get_adapter(Adapter),
        bot_id,
        bot_config=type_validate_python(BotConfig, test_bot),
        bot_info=type_validate_python(BotInfo, bots_info["bot"]),
    )
    _check_at_me(bot, event)

    assert event.to_me
    assert event.get_message().extract_plain_text() == "/say 34567\n"
    assert [seg.type for seg in event.get_message()] == ["text", "image"]
    assert event.original_message[0].type == "at"
    assert event.original_message[0].data["user_id"] == bots_info["bot"]["open_id"]
