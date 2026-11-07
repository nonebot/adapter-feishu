import json
from pathlib import Path

import httpx2
from larkify import Response
import pytest

import nonebot
from nonebot.adapters.feishu import ActionFailed, Adapter, Bot, NetworkError
from nonebot.adapters.feishu.config import BotConfig
from nonebot.adapters.feishu.models import BotInfo, BotInfoResponse
from nonebot.compat import type_validate_python
from nonebot.drivers import URL

with (Path(__file__).parent.joinpath("data", "bots.json")).open("r") as f:
    feishu_bots = json.load(f)

with (Path(__file__).parent.joinpath("data", "bots_info.json")).open("r") as f:
    bots_info = json.load(f)


def make_bot(config: dict) -> Bot:
    return Bot(
        nonebot.get_adapter(Adapter),
        config["app_id"],
        bot_config=type_validate_python(BotConfig, config),
        bot_info=type_validate_python(BotInfo, bots_info["bot"]),
    )


@pytest.fixture
def bot() -> Bot:
    return make_bot(feishu_bots[1])


@pytest.mark.anyio
async def test_call_api_returns_the_decoded_body(bot: Bot):
    result = await bot.call_api("test/echo", method="POST", params={"a": "1"}, json={"k": "v"})

    assert result["url"].endswith("/open-apis/test/echo?a=1")
    assert result["method"] == "POST"
    assert result["json"] == {"k": "v"}
    assert result["headers"]["Authorization"] == "Bearer tenant_access_token"


@pytest.mark.anyio
async def test_call_api_accepts_query_and_body_aliases(bot: Bot):
    result = await bot.call_api("test/echo", method="POST", query={"a": "1"}, body={"k": "v"})

    assert result["args"] == {"a": "1"}
    assert result["json"] == {"k": "v"}


@pytest.mark.anyio
async def test_call_api_returns_files_as_bytes(bot: Bot):
    assert await bot.call_api("test/binary", method="GET") == b"\x89PNG\xff\xfe"


@pytest.mark.anyio
async def test_call_api_can_return_the_response(bot: Bot):
    response = await bot.call_api("test/binary", method="GET", _return_response=True)

    assert response.status_code == 200
    assert response.content == b"\x89PNG\xff\xfe"


@pytest.mark.anyio
async def test_call_api_rejects_empty_responses(bot: Bot):
    with pytest.raises(NetworkError):
        await bot.call_api("test/empty", method="GET")


@pytest.mark.anyio
async def test_http_errors_raise_action_failed(bot: Bot):
    with pytest.raises(ActionFailed) as info:
        await bot.call_api("test/http_error", method="GET")

    assert info.value.info == {"status_code": 400, "code": 230001, "msg": "invalid", "log_id": "log_1"}


@pytest.mark.anyio
async def test_business_errors_raise_action_failed(bot: Bot):
    with pytest.raises(ActionFailed) as info:
        await bot.call_api("test/business_error", method="GET")

    assert info.value.info["status_code"] == 200
    assert info.value.info["code"] == 230002


@pytest.mark.anyio
async def test_timeout_can_be_set_per_call(bot: Bot):
    with pytest.raises(NetworkError):
        await bot.call_api("test/slow", method="GET", _timeout=0.05)

    assert await bot.call_api("test/slow", method="GET", _timeout=5)


@pytest.mark.anyio
async def test_unreachable_server_raises_network_error(bot: Bot, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(nonebot.get_adapter(Adapter), "get_api_base", lambda _: URL("http://127.0.0.1:1"))

    with pytest.raises(NetworkError):
        await make_bot(feishu_bots[1]).call_api("test/echo", method="GET")


@pytest.mark.anyio
async def test_rejected_credentials_raise_action_failed():
    bot = make_bot({**feishu_bots[1], "app_id": "app_id_invalid"})

    with pytest.raises(ActionFailed, match="tenant_access_token"):
        await bot.call_api("test/echo", method="GET")


@pytest.mark.anyio
async def test_post_file_sends_multipart(bot: Bot):
    result = await bot.post_file("stream", "a.bin", b"abc", duration=3)

    assert result["form"] == {"file_type": "stream", "file_name": "a.bin", "duration": "3"}
    assert result["files"] == {"file": "abc"}


@pytest.mark.anyio
async def test_get_bot_info():
    adapter = nonebot.get_adapter(Adapter)

    result = await adapter.get_bot_info(type_validate_python(BotConfig, feishu_bots[1]))

    assert isinstance(result, BotInfoResponse)
    assert result.bot.open_id == bots_info["bot"]["open_id"]


@pytest.mark.anyio
async def test_rest_calls_larkify_through_call_api(bot: Bot, monkeypatch: pytest.MonkeyPatch):
    called: list[tuple[str, dict]] = []

    async def hook(bot: Bot, api: str, data: dict) -> None:
        called.append((api, data))

    monkeypatch.setattr(Bot, "_calling_api_hook", {hook})

    response = await bot.rest.im.v1.message.async_create(
        receive_id_type="chat_id",
        receive_id="oc_1",
        msg_type="text",
        content="{}",
    )

    assert isinstance(response, Response)
    assert response.json()["args"] == {"receive_id_type": "chat_id"}
    assert response.json()["json"] == {"receive_id": "oc_1", "msg_type": "text", "content": "{}"}
    assert [api for api, _ in called] == ["rest.im.v1.message.async_create"]


@pytest.mark.anyio
async def test_rest_accepts_positional_path_parameters(bot: Bot):
    response = await bot.rest.im.v1.message.async_get("om_1", user_id_type="open_id")

    assert response.json()["url"].endswith("/open-apis/im/v1/messages/om_1?user_id_type=open_id")


@pytest.mark.anyio
async def test_rest_errors_raise_action_failed(bot: Bot):
    with pytest.raises(ActionFailed) as info:
        await bot.rest.im.v1.message.async_get("om_invalid")

    assert info.value.info["code"] == 230001


@pytest.mark.anyio
async def test_rest_refuses_sync_methods(bot: Bot):
    with pytest.raises(TypeError, match="async_"):
        await bot.rest.im.v1.message.get(message_id="om_1")  # type: ignore[misc]

    with pytest.raises(TypeError, match="async_"):
        await bot.rest.im.v1.message.get("om_1")  # type: ignore[misc]


@pytest.mark.parametrize(
    ("api_timeout", "expected"),
    [(12.0, httpx2.Timeout(12.0)), (None, httpx2.Timeout(None))],
)
def test_client_uses_the_api_timeout(
    monkeypatch: pytest.MonkeyPatch, api_timeout: float | None, expected: httpx2.Timeout
):
    adapter = nonebot.get_adapter(Adapter)
    monkeypatch.setattr(adapter.config, "api_timeout", api_timeout)

    client = adapter.create_client(type_validate_python(BotConfig, feishu_bots[1]))

    assert client.config.timeout == expected


def test_client_accepts_a_configured_http_address(monkeypatch: pytest.MonkeyPatch):
    adapter = nonebot.get_adapter(Adapter)
    monkeypatch.setattr(adapter, "get_api_base", lambda _: URL("http://feishu.internal:8080"))

    client = adapter.create_client(type_validate_python(BotConfig, feishu_bots[1]))

    assert client.config.base_url.host == "feishu.internal"


def test_bot_client_is_created_on_first_use():
    class FakeAdapter:
        pass

    Bot(
        FakeAdapter(),  # type: ignore[arg-type]
        "fake",
        bot_config=type_validate_python(BotConfig, feishu_bots[1]),
        bot_info=type_validate_python(BotInfo, bots_info["bot"]),
    )
