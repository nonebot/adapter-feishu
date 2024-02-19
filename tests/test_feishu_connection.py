import json
from pathlib import Path

import pytest
from nonebug import App

import nonebot
from nonebot.adapters.feishu import Adapter

with (Path(__file__).parent / "bots.json").open("r") as f:
    feishu_bots = json.load(f)

test_bot = feishu_bots[0]
bot_id = test_bot["app_id"]


@pytest.mark.asyncio
@pytest.mark.parametrize("endpoints", [f"/feishu/{bot_id}"])
async def test_http(app: App, endpoints: str):
    with (Path(__file__).parent / "events.json").open("r") as f:
        test_events = json.load(f)

    adapter = nonebot.get_adapter(Adapter)

    async with app.test_server() as ctx:
        client = ctx.get_client()
        event = test_events[0]
        resp = await client.post(endpoints, json=event)
        assert resp.status_code == 200
        bots = nonebot.get_bots()
        assert bot_id in bots
        assert bot_id in adapter.bots
        adapter.bot_disconnect(bots[bot_id])
