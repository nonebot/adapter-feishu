import json

import pytest

from nonebot.adapters.feishu import Message, MessageSegment


@pytest.mark.anyio
async def test_to_post_does_not_mutate_image_segment():
    seg = MessageSegment.image("img_key_abc")
    assert seg.type == "image"
    assert seg.to_post() == "img"
    assert seg.type == "image"

    msg_type, content = Message([MessageSegment.text("hi"), seg]).serialize()
    assert msg_type == "post"
    data = json.loads(content)
    assert data["zh_cn"]["content"][-1][-1] == {"tag": "img", "image_key": "img_key_abc"}
    assert seg.type == "image"

    single_type, single_content = Message([seg]).serialize()
    assert single_type == "image"
    assert json.loads(single_content) == {"image_key": "img_key_abc"}
