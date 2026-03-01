"""飞书 WebSocket 长连接相关测试。"""

import asyncio
import json
from unittest.mock import AsyncMock, MagicMock

import pytest

from nonebot.adapters.feishu.ws import frame_pb2
from nonebot.adapters.feishu.ws.client import WsClient
from nonebot.adapters.feishu.ws.models import (
    FrameSegment,
    FrameType,
    MessageType,
    WsEndpointApiResponse,
    WsEndpointClientConfig,
    WsEndpointData,
    WsEndpointResponse,
)


def test_frame_pb2_serialize_deserialize():
    """Frame (frame_pb2) 序列化与反序列化。"""
    frame = frame_pb2.Frame()
    frame.seq_id = 0
    frame.log_id = 0
    frame.service = 1
    frame.method = 0
    header = frame.headers.add()
    header.key = "type"
    header.value = "ping"

    raw = frame.SerializeToString()
    assert isinstance(raw, bytes)

    frame2 = frame_pb2.Frame()
    frame2.ParseFromString(raw)
    assert frame2.seq_id == 0
    assert frame2.service == 1
    assert frame2.method == 0
    assert len(frame2.headers) == 1
    assert frame2.headers[0].key == "type"
    assert frame2.headers[0].value == "ping"


def test_frame_pb2_with_payload():
    """Frame 带 payload 的序列化。"""
    frame = frame_pb2.Frame()
    frame.seq_id = 1
    frame.log_id = 1
    frame.service = 1
    frame.method = FrameType.DATA
    h = frame.headers.add()
    h.key = "type"
    h.value = MessageType.EVENT
    frame.payload = b'{"header":{}}'

    raw = frame.SerializeToString()
    frame2 = frame_pb2.Frame()
    frame2.ParseFromString(raw)
    assert frame2.payload == b'{"header":{}}'


# --- WsClient 单元测试 ---


@pytest.fixture
def mock_adapter():
    adapter = MagicMock()
    adapter.get_api_base.return_value = MagicMock()
    adapter.get_api_base.return_value.joinpath.return_value = "https://open.feishu.cn/callback/ws/endpoint"
    adapter.tasks = set()
    return adapter


@pytest.fixture
def mock_bot():
    bot = MagicMock()
    bot.handle_event = AsyncMock()
    return bot


@pytest.fixture
def mock_bot_config():
    config = MagicMock()
    config.app_id = "test_app_id"
    config.app_secret = "test_app_secret"
    return config


@pytest.fixture
def ws_client(mock_adapter, mock_bot, mock_bot_config):
    return WsClient(mock_adapter, mock_bot, mock_bot_config)


def test_ws_client_get_ws_endpoint_url(ws_client, mock_adapter):
    """_get_ws_endpoint_url 返回正确 URL。"""
    url = ws_client._get_ws_endpoint_url()
    assert url == "https://open.feishu.cn/callback/ws/endpoint"
    mock_adapter.get_api_base.assert_called_once_with(ws_client._bot_config)
    mock_adapter.get_api_base.return_value.joinpath.assert_called_once_with("callback/ws/endpoint")


def test_ws_client_headers_to_dict(ws_client):
    """_headers_to_dict 将 headers 转为 dict。"""

    class H:
        def __init__(self, key, value):
            self.key = key
            self.value = value

    headers = [H("type", "event"), H("message_id", "mid1")]
    result = ws_client._headers_to_dict(headers)
    assert result == {"type": "event", "message_id": "mid1"}


def test_ws_client_retrieve_single_segment(ws_client):
    """_retrieve 单分片直接返回 payload。"""
    seg = FrameSegment(message_id="m1", sum=1, seq=0, data=b"hello")
    out = ws_client._retrieve(seg)
    assert out == b"hello"
    assert "m1" not in ws_client._cache


def test_ws_client_retrieve_multi_segment(ws_client):
    """_retrieve 多分片收齐后重组并清缓存。"""
    seg0 = FrameSegment(message_id="m1", sum=2, seq=0, data=b"hel")
    seg1 = FrameSegment(message_id="m1", sum=2, seq=1, data=b"lo")
    assert ws_client._retrieve(seg0) is None
    out = ws_client._retrieve(seg1)
    assert out == b"hello"
    assert "m1" not in ws_client._cache


def test_ws_client_retrieve_multi_segment_out_of_order(ws_client):
    """_retrieve 分片乱序时按 seq 排序重组。"""
    seg1 = FrameSegment(message_id="m1", sum=2, seq=1, data=b"lo")
    seg0 = FrameSegment(message_id="m1", sum=2, seq=0, data=b"hel")
    assert ws_client._retrieve(seg1) is None
    out = ws_client._retrieve(seg0)
    assert out == b"hello"


@pytest.mark.anyio
async def test_ws_client_send_frame_async_when_ws_none(ws_client):
    """_send_frame_async 在 _ws 为 None 时不发送。"""
    frame = frame_pb2.Frame()
    await ws_client._send_frame_async(frame)
    ws_client._adapter.send_request.assert_not_called()


@pytest.mark.anyio
async def test_ws_client_send_frame_async_when_ws_set(ws_client):
    """_send_frame_async 在 _ws 存在时发送序列化帧。"""
    mock_ws = AsyncMock()
    ws_client._ws = mock_ws
    frame = frame_pb2.Frame()
    frame.seq_id = 1
    frame.log_id = 0
    frame.service = 0
    frame.method = 0
    await ws_client._send_frame_async(frame)
    mock_ws.send.assert_called_once()
    (arg,) = mock_ws.send.call_args[0]
    assert isinstance(arg, bytes)
    frame2 = frame_pb2.Frame()
    frame2.ParseFromString(arg)
    assert frame2.seq_id == 1


@pytest.mark.anyio
async def test_ws_client_fetch_endpoint_success(ws_client, mock_adapter):
    """_fetch_endpoint 成功时返回 WsEndpointResponse。"""
    mock_adapter.send_request = AsyncMock(
        return_value={
            "code": 0,
            "msg": "ok",
            "data": {
                "URL": "wss://gateway.open.feishu.cn?device_id=dev1&service_id=2",
                "ClientConfig": {
                    "PingInterval": 90,
                    "ReconnectCount": -1,
                    "ReconnectInterval": 90,
                    "ReconnectNonce": 25,
                },
            },
        }
    )
    resp = await ws_client._fetch_endpoint()
    assert isinstance(resp, WsEndpointResponse)
    assert resp.url == "wss://gateway.open.feishu.cn?device_id=dev1&service_id=2"
    assert resp.device_id == "dev1"
    assert resp.service_id == 2
    assert resp.ping_interval_seconds == 90


@pytest.mark.anyio
async def test_ws_client_fetch_endpoint_non_dict_raises(ws_client, mock_adapter):
    """_fetch_endpoint 响应非 dict 时抛出 RuntimeError。"""
    mock_adapter.send_request = AsyncMock(return_value="not a dict")
    with pytest.raises(RuntimeError, match="not dict"):
        await ws_client._fetch_endpoint()


@pytest.mark.anyio
async def test_ws_client_fetch_endpoint_code_not_zero_raises(ws_client, mock_adapter):
    """_fetch_endpoint code != 0 时抛出 RuntimeError。"""
    mock_adapter.send_request = AsyncMock(return_value={"code": 1, "msg": "error", "data": None})
    with pytest.raises(RuntimeError, match="Failed to get gateway url"):
        await ws_client._fetch_endpoint()


@pytest.mark.anyio
async def test_ws_client_fetch_endpoint_data_none_raises(ws_client, mock_adapter):
    """_fetch_endpoint data 为 None 时抛出 RuntimeError。"""
    mock_adapter.send_request = AsyncMock(return_value={"code": 0, "msg": "ok", "data": None})
    with pytest.raises(RuntimeError, match="data missing"):
        await ws_client._fetch_endpoint()


def _make_control_frame(msg_type: str) -> bytes:
    frame = frame_pb2.Frame()
    frame.seq_id = 0
    frame.log_id = 0
    frame.service = 0
    frame.method = FrameType.CONTROL
    h = frame.headers.add()
    h.key = "type"
    h.value = msg_type
    return frame.SerializeToString()


def _make_data_event_frame(
    seq_id: int, payload: bytes, message_id: str = "mid1", sum_val: int = 1, seq: int = 0
) -> bytes:
    frame = frame_pb2.Frame()
    frame.seq_id = seq_id
    frame.log_id = 0
    frame.service = 1
    frame.method = FrameType.DATA
    for k, v in [("type", MessageType.EVENT), ("message_id", message_id), ("sum", str(sum_val)), ("seq", str(seq))]:
        h = frame.headers.add()
        h.key = k
        h.value = v
    frame.payload = payload
    return frame.SerializeToString()


@pytest.mark.anyio
async def test_ws_client_handle_message_pong_no_op(ws_client, mock_adapter):
    """CONTROL + PONG 消息不处理、不报错。"""
    raw = _make_control_frame(MessageType.PONG)
    await ws_client._handle_message(raw)
    mock_adapter.json_to_event.assert_not_called()
    ws_client._bot.handle_event.assert_not_called()


@pytest.mark.anyio
async def test_ws_client_handle_message_parse_error(ws_client):
    """无效 protobuf 时记录并返回，不抛异常。"""
    await ws_client._handle_message(b"invalid\x00\x01")
    ws_client._bot.handle_event.assert_not_called()


@pytest.mark.anyio
async def test_ws_client_handle_message_event_dispatch_and_ack(ws_client, mock_adapter):
    """DATA + EVENT 有效 body 时派发事件并发送 ack。"""
    event_payload = json.dumps(
        {
            "schema": "2.0",
            "header": {
                "event_id": "e1",
                "event_type": "im.message.receive_v1",
                "create_time": "0",
                "token": "",
                "app_id": "",
            },
            "event": {},
        }
    ).encode("utf-8")
    raw = _make_data_event_frame(seq_id=42, payload=event_payload)
    mock_event = MagicMock()
    mock_adapter.json_to_event.return_value = mock_event
    ws_client._ws = AsyncMock()

    await ws_client._handle_message(raw)

    mock_adapter.json_to_event.assert_called_once()
    ws_client._bot.handle_event.assert_called_once_with(mock_event)
    ws_client._ws.send.assert_called_once()
    ack_bytes = ws_client._ws.send.call_args[0][0]
    ack_frame = frame_pb2.Frame()
    ack_frame.ParseFromString(ack_bytes)
    assert ack_frame.seq_id == 42
    headers_dict = {h.key: h.value for h in ack_frame.headers}
    assert headers_dict.get("biz_rt") == "0"
    assert ack_frame.payload == json.dumps({"code": 200}).encode("utf-8")


@pytest.mark.anyio
async def test_ws_client_handle_message_event_no_header_skipped(ws_client, mock_adapter):
    """body 无 header 时不派发、不 ack。"""
    payload = json.dumps({"foo": "bar"}).encode("utf-8")
    raw = _make_data_event_frame(seq_id=1, payload=payload)
    ws_client._ws = AsyncMock()
    await ws_client._handle_message(raw)
    mock_adapter.json_to_event.assert_not_called()
    ws_client._ws.send.assert_not_called()


@pytest.mark.anyio
async def test_ws_client_handle_message_event_invalid_json(ws_client):
    """payload 非合法 JSON 时不派发。"""
    raw = _make_data_event_frame(seq_id=1, payload=b"not json")
    ws_client._ws = AsyncMock()
    await ws_client._handle_message(raw)
    ws_client._bot.handle_event.assert_not_called()
    ws_client._ws.send.assert_not_called()


@pytest.mark.anyio
async def test_ws_client_handle_message_event_json_to_event_none(ws_client, mock_adapter):
    """json_to_event 返回 None 时不调用 handle_event，但仍发送 ack。"""
    event_payload = json.dumps(
        {
            "schema": "2.0",
            "header": {"event_id": "e1", "event_type": "unknown", "create_time": "0", "token": "", "app_id": ""},
            "event": {},
        }
    ).encode("utf-8")
    raw = _make_data_event_frame(seq_id=1, payload=event_payload)
    mock_adapter.json_to_event.return_value = None
    ws_client._ws = AsyncMock()
    await ws_client._handle_message(raw)
    ws_client._bot.handle_event.assert_not_called()
    ws_client._ws.send.assert_called_once()


@pytest.mark.anyio
async def test_ws_client_run_connects_and_sets_device_service_id(ws_client, mock_adapter):
    """run() 拉取端点、建立 ws，并正确设置 device_id/service_id。"""
    mock_adapter.send_request = AsyncMock(
        return_value={
            "code": 0,
            "msg": "ok",
            "data": {
                "URL": "wss://test/?device_id=d&service_id=1",
                "ClientConfig": {"PingInterval": 90},
            },
        }
    )
    received: asyncio.Queue = asyncio.Queue()

    async def fake_receive():
        return await received.get()

    mock_ws = AsyncMock()
    mock_ws.receive = fake_receive
    mock_ws.send = AsyncMock()

    class Ctx:
        async def __aenter__(self):
            return mock_ws

        async def __aexit__(self, *args):
            pass

    mock_adapter.websocket = MagicMock(return_value=Ctx())

    async def run_client():
        await ws_client.run()

    task = asyncio.create_task(run_client())
    await asyncio.sleep(0.05)
    assert ws_client._device_id == "d"
    assert ws_client._service_id == 1
    mock_adapter.websocket.assert_called_once()
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task


# --- ws/models 测试 ---


def test_ws_endpoint_data_parse_with_alias():
    """WsEndpointData 使用 URL、ClientConfig 别名解析。"""
    data = WsEndpointData.model_validate(
        {
            "URL": "wss://gateway.open.feishu.cn?device_id=x&service_id=1",
            "ClientConfig": {
                "PingInterval": 60,
                "ReconnectCount": 3,
                "ReconnectInterval": 30,
                "ReconnectNonce": 10,
            },
        }
    )
    assert data.url == "wss://gateway.open.feishu.cn?device_id=x&service_id=1"
    assert data.client_config.ping_interval == 60
    assert data.client_config.reconnect_count == 3


def test_ws_endpoint_api_response():
    """WsEndpointApiResponse 解析完整响应。"""
    resp = WsEndpointApiResponse.model_validate(
        {
            "code": 0,
            "msg": "ok",
            "data": {
                "URL": "wss://test/",
                "ClientConfig": {"PingInterval": 90},
            },
        }
    )
    assert resp.code == 0
    assert resp.data is not None
    assert resp.data.url == "wss://test/"


def test_ws_endpoint_response_construction():
    """WsEndpointResponse 可正确构造。"""
    config = WsEndpointClientConfig(ping_interval=90)
    resp = WsEndpointResponse(
        url="wss://test/",
        device_id="dev",
        service_id=1,
        ping_interval_seconds=90,
        client_config=config,
    )
    assert resp.device_id == "dev"
    assert resp.service_id == 1
    assert resp.ping_interval_seconds == 90


def test_frame_type_and_message_type():
    """FrameType 与 MessageType 常量。"""
    assert FrameType.CONTROL == 0
    assert FrameType.DATA == 1
    assert MessageType.PING == "ping"
    assert MessageType.PONG == "pong"
    assert MessageType.EVENT == "event"
