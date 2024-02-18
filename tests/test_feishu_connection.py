import json
from pathlib import Path

import pytest
from nonebug import App

import nonebot
from nonebot.adapters.feishu import Adapter


@pytest.mark.asyncio
@pytest.mark.parametrize("endpoints", ["/feishu/", "/feishu/http", "/feishu/http/"])
async def test_http(app: App, endpoints: str):
    with (Path(__file__).parent / "events.json").open("r") as f:
        test_events = json.load(f)

    adapter = nonebot.get_adapter(Adapter)

    async with app.test_server() as ctx:
        client = ctx.get_client()
        event = test_events[0]
        event.pop("_model")
        headers = {"X-Self-ID": "0"}
        resp = await client.post(endpoints, json=event, headers=headers)
        assert resp.status_code == 204
        bots = nonebot.get_bots()
        assert "0" in bots
        assert "0" in adapter.bots
        adapter.bot_disconnect(bots["0"])
