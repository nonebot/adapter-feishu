"""飞书 WebSocket 长连接相关测试。"""

from nonebot.adapters.feishu.ws.frame import Frame, Header


def test_frame_encode_decode():
    """Frame 序列化与反序列化"""
    f = Frame(
        seq_id=0,
        log_id=0,
        service=1,
        method=0,
        headers=[Header(key="type", value="ping")],
    )
    raw = bytes(f)
    assert isinstance(raw, bytes)
    f2 = Frame().parse(raw)
    assert f2.seq_id == 0
    assert f2.service == 1
    assert f2.method == 0
    assert len(f2.headers) == 1
    assert f2.headers[0].key == "type"
    assert f2.headers[0].value == "ping"
