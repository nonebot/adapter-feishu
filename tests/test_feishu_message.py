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


def test_serialize_single_at_as_post():
    """`at` 不是合法的 msg_type，只能作为富文本节点发送。"""
    msg_type, content = Message([MessageSegment.at("ou_x")]).serialize()

    assert msg_type == "post"
    assert json.loads(content) == {"zh_cn": {"title": "", "content": [[{"tag": "at", "user_id": "ou_x"}]]}}


def test_serialize_no_leading_empty_paragraph():
    first = MessageSegment.post("title", [[{"tag": "text", "text": "a"}]])
    second = MessageSegment.post("title", [[{"tag": "text", "text": "b"}]])

    _, content = Message([first, second]).serialize()

    assert json.loads(content)["zh_cn"]["content"] == [
        [{"tag": "text", "text": "a"}],
        [{"tag": "text", "text": "b"}],
    ]


def test_serialize_keeps_empty_paragraph_from_post():
    post = MessageSegment.post("title", [[{"tag": "text", "text": "a"}], [], [{"tag": "text", "text": "b"}]])

    _, content = Message([post, MessageSegment.text("c")]).serialize()

    assert json.loads(content)["zh_cn"]["content"] == [
        [{"tag": "text", "text": "a"}],
        [],
        [{"tag": "text", "text": "b"}, {"tag": "text", "text": "c"}],
    ]


@pytest.mark.parametrize(
    ("seg", "expected"),
    [
        (MessageSegment.media("fk"), {"file_key": "fk"}),
        (MessageSegment.media("fk", image_key="ik"), {"file_key": "fk", "image_key": "ik"}),
        (MessageSegment.audio("fk"), {"file_key": "fk"}),
        (MessageSegment.file("fk"), {"file_key": "fk"}),
    ],
)
def test_serialize_omits_unset_optional_fields(seg: MessageSegment, expected: dict[str, str]):
    msg_type, content = Message([seg]).serialize()
    assert msg_type == seg.type
    assert json.loads(content) == expected

    _, post_content = Message([MessageSegment.text("hi"), seg]).serialize()
    assert json.loads(post_content)["zh_cn"]["content"][-1][-1] == {"tag": seg.type, **expected}


def test_serialize_keeps_segment_data_of_received_media():
    received = json.dumps({"file_key": "fk", "image_key": "ik", "file_name": "a.mp4", "duration": 2000})
    seg = Message.deserialize(received, None, "media")[0]
    unset = MessageSegment.media("fk")

    Message([seg]).serialize()
    Message([unset]).serialize()

    assert seg.data == {"file_key": "fk", "image_key": "ik", "file_name": "a.mp4", "duration": 2000}
    assert unset.data == {"file_key": "fk", "image_key": None, "file_name": None, "duration": None}
