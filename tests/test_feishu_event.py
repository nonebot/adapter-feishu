import json
from pathlib import Path
from typing import Any

import pytest

from nonebot.adapters.feishu import Adapter


@pytest.mark.asyncio
async def test_event():
    with (Path(__file__).parent.joinpath("data", "events.json")).open("r") as f:
        test_events: list[dict[str, Any]] = json.load(f)

    for event_data in test_events:
        model_name: str = event_data.pop("_model", None)
        event = Adapter.json_to_event(event_data)
        assert model_name == event.__class__.__name__
