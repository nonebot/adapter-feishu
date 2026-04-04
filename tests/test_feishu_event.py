import json
from pathlib import Path
from typing import Any

import pytest

from nonebot.adapters.feishu import Adapter, Message
from nonebot.adapters.feishu.models import Mention, UserId


@pytest.mark.anyio
async def test_event():
    with (Path(__file__).parent.joinpath("data", "events.json")).open("r") as f:
        test_events: list[dict[str, Any]] = json.load(f)

    for event_data in test_events:
        model_name: str = event_data.pop("_model", None)
        event = Adapter.json_to_event(event_data)
        assert model_name == event.__class__.__name__


def test_deserialize_text_with_at_symbol_no_mentions():
    """Text containing @ symbol should not be parsed as at segment
    when there are no mentions. (GitHub issue #149)"""
    content = json.dumps({"text": "/cmd email@example.com"})
    msg = Message.deserialize(content, None, "text")

    assert len(msg) == 1
    assert msg[0].type == "text"
    assert msg[0].data["text"] == "/cmd email@example.com"


def test_deserialize_text_with_real_mention():
    """Real mentions from Feishu should still be parsed correctly."""
    content = json.dumps({"text": "@_user_1 hello"})
    mentions = [
        Mention(
            key="@_user_1",
            id=UserId(open_id="ou_123", user_id="uid", union_id="uid"),
            name="TestUser",
            tenant_key="tk",
        )
    ]
    msg = Message.deserialize(content, mentions, "text")

    assert len(msg) == 2
    assert msg[0].type == "at"
    assert msg[0].data["user_id"] == "ou_123"
    assert msg[1].type == "text"
    assert msg[1].data["text"] == " hello"


def test_deserialize_text_with_mention_and_at_symbol():
    """Real mention + email-like @ in the same message should only
    parse the real mention as at segment."""
    content = json.dumps({"text": "@_user_1 send to user@example.com"})
    mentions = [
        Mention(
            key="@_user_1",
            id=UserId(open_id="ou_123", user_id="uid", union_id="uid"),
            name="Bot",
            tenant_key="tk",
        )
    ]
    msg = Message.deserialize(content, mentions, "text")

    assert len(msg) == 2
    assert msg[0].type == "at"
    assert msg[0].data["user_id"] == "ou_123"
    assert msg[1].type == "text"
    assert msg[1].data["text"] == " send to user@example.com"
