import json
from pathlib import Path

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

with (Path(__file__).parent.joinpath("data", "events.json")).open(
    "r", encoding="utf8"
) as f:
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
