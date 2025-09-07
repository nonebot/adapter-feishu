import json
from pathlib import Path

from nonebug import App
import pytest

import nonebot
from nonebot.adapters.feishu import Adapter

with (Path(__file__).parent.joinpath("data", "bots.json")).open("r") as f:
    feishu_bots = json.load(f)

bot_id = feishu_bots[0]["app_id"]


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
        bots = nonebot.get_bots()
        assert bot_id in bots
        assert bot_id in adapter.bots
        adapter.bot_disconnect(bots[bot_id])
