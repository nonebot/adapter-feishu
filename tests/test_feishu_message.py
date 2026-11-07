import json

import pytest

from nonebot.adapters.feishu import Message, MessageSegment


@pytest.mark.anyio
async def test_to_post_does_not_mutate_image_segment():
    seg = MessageSegment.image("img_key_abc")
    assert seg.type == "image"
    assert seg.to_post() == {"tag": "img", "image_key": "img_key_abc"}
    assert seg.type == "image"

    msg_type, content = Message([MessageSegment.text("hi"), seg]).serialize()
    assert msg_type == "post"
    data = json.loads(content)
    assert data["zh_cn"]["content"][-1][-1] == {"tag": "img", "image_key": "img_key_abc"}
    assert seg.type == "image"

    single_type, single_content = Message([seg]).serialize()
    assert single_type == "image"
    assert json.loads(single_content) == {"image_key": "img_key_abc"}


def test_to_post_keeps_tag_for_other_segments():
    assert MessageSegment.text("hi").to_post() == {"tag": "text", "text": "hi"}
    assert MessageSegment.at("ou_x").to_post() == {"tag": "at", "user_id": "ou_x"}


def test_serialize_does_not_mutate_post_segment():
    post = MessageSegment.post("title", [[{"tag": "text", "text": "body"}]])
    msg = Message([post, MessageSegment.text("footer")])

    first = msg.serialize()
    second = msg.serialize()

    assert first == second
    assert post.data["content"] == [[{"tag": "text", "text": "body"}]]
    assert json.loads(first[1])["zh_cn"]["content"][-1] == [
        {"tag": "text", "text": "body"},
        {"tag": "text", "text": "footer"},
    ]
