import json

import pytest

from nonebot.adapters.feishu import Message, MessageSegment

TEXT_A = {"tag": "text", "text": "a"}
TEXT_B = {"tag": "text", "text": "b"}
IMG = {"tag": "img", "image_key": "ik"}
MEDIA = {"tag": "media", "file_key": "fk"}


def _paragraphs(*segments: MessageSegment) -> list[list[dict[str, str]]]:
    _, content = Message(list(segments)).serialize()
    return json.loads(content)["zh_cn"]["content"]


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
        (MessageSegment.media("fk", "ik", "a.mp4", 2000), {"file_key": "fk", "image_key": "ik"}),
        (MessageSegment.audio("fk"), {"file_key": "fk"}),
        (MessageSegment.audio("fk", 2000), {"file_key": "fk"}),
        (MessageSegment.file("fk"), {"file_key": "fk"}),
        (MessageSegment.file("fk", "a.txt"), {"file_key": "fk"}),
    ],
)
def test_serialize_omits_unset_and_receive_only_fields(seg: MessageSegment, expected: dict[str, str]):
    msg_type, content = Message([seg]).serialize()
    assert msg_type == seg.type
    assert json.loads(content) == expected


def test_to_post_omits_unset_and_receive_only_fields():
    assert MessageSegment.media("fk").to_post() == {"tag": "media", "file_key": "fk"}
    assert MessageSegment.media("fk", "ik", "a.mp4", 2000).to_post() == {
        "tag": "media",
        "file_key": "fk",
        "image_key": "ik",
    }


def test_serialize_keeps_segment_data_of_received_media():
    received = json.dumps({"file_key": "fk", "image_key": "ik", "file_name": "a.mp4", "duration": 2000})
    seg = Message.deserialize(received, None, "media")[0]
    unset = MessageSegment.media("fk")

    Message([seg]).serialize()
    Message([unset]).serialize()

    assert seg.data == {"file_key": "fk", "image_key": "ik", "file_name": "a.mp4", "duration": 2000}
    assert unset.data == {"file_key": "fk", "image_key": None, "file_name": None, "duration": None}


def test_serialize_puts_image_in_own_paragraph():
    paragraphs = _paragraphs(MessageSegment.text("a"), MessageSegment.image("ik"), MessageSegment.text("b"))

    assert paragraphs == [[TEXT_A], [IMG], [TEXT_B]]


def test_serialize_puts_media_in_own_paragraph():
    paragraphs = _paragraphs(MessageSegment.text("a"), MessageSegment.media("fk"), MessageSegment.text("b"))

    assert paragraphs == [[TEXT_A], [MEDIA], [TEXT_B]]


def test_serialize_keeps_each_image_in_separate_paragraphs():
    paragraphs = _paragraphs(MessageSegment.image("ik"), MessageSegment.media("fk"), MessageSegment.image("ik"))

    assert paragraphs == [[IMG], [MEDIA], [IMG]]


def test_serialize_keeps_inline_segments_in_one_paragraph():
    paragraphs = _paragraphs(MessageSegment.at("ou_x"), MessageSegment.text("a"), MessageSegment.text("b"))

    assert paragraphs == [[{"tag": "at", "user_id": "ou_x"}, TEXT_A, TEXT_B]]


def test_serialize_starts_new_paragraph_after_post_ending_with_image():
    post = MessageSegment.post("title", [[TEXT_A], [IMG]])

    assert _paragraphs(post, MessageSegment.text("b")) == [[TEXT_A], [IMG], [TEXT_B]]
    assert post.data["content"] == [[TEXT_A], [IMG]]


def test_serialize_keeps_post_content_as_written():
    post = MessageSegment.post("title", [[TEXT_A, IMG]])

    assert _paragraphs(post, MessageSegment.text("b")) == [[TEXT_A, IMG], [TEXT_B]]


@pytest.mark.parametrize(
    "seg",
    [
        MessageSegment.audio("fk"),
        MessageSegment.file("fk"),
        MessageSegment.sticker("fk"),
        MessageSegment.share_chat("oc_x"),
        MessageSegment.share_user("ou_x"),
        MessageSegment.interactive_template("id", {}),
    ],
    ids=lambda seg: seg.type,
)
def test_serialize_rejects_segment_not_supported_in_post(seg: MessageSegment):
    assert Message([seg]).serialize()[0] == seg.type

    with pytest.raises(ValueError, match=seg.type):
        Message([MessageSegment.text("hi"), seg]).serialize()


@pytest.mark.parametrize(
    ("seg_type", "data"),
    [
        ("a", {"text": "link", "href": "https://example.com"}),
        ("emotion", {"emoji_type": "SMILE"}),
        ("code_block", {"text": "print()"}),
        ("hr", {}),
        ("md", {"text": "**bold**"}),
    ],
)
def test_serialize_allows_documented_post_tags(seg_type: str, data: dict[str, str]):
    paragraphs = _paragraphs(MessageSegment.text("a"), MessageSegment(seg_type, data))

    assert paragraphs == [[TEXT_A, {"tag": seg_type, **data}]]


@pytest.mark.parametrize(
    ("seg_type", "data"),
    [
        ("a", {"text": "link", "href": "https://example.com"}),
        ("emotion", {"emoji_type": "SMILE"}),
        ("code_block", {"text": "print()"}),
        ("hr", {}),
        ("md", {"text": "**bold**"}),
    ],
)
def test_serialize_sends_lone_post_node_as_post(seg_type: str, data: dict[str, str]):
    msg_type, content = Message([MessageSegment(seg_type, data)]).serialize()

    assert msg_type == "post"
    assert json.loads(content)["zh_cn"]["content"] == [[{"tag": seg_type, **data}]]


@pytest.mark.parametrize(
    "seg",
    [
        MessageSegment.location("name", "0", "0"),
        MessageSegment.hongbao("text"),
        MessageSegment.todo("task", {"title": "", "content": []}, "0"),
        MessageSegment.video_chat("topic", "0"),
        MessageSegment.folder("fk", "name"),
        MessageSegment("vote", {"topic": "topic", "options": []}),
    ],
    ids=lambda seg: seg.type,
)
def test_serialize_rejects_segment_not_supported_for_sending(seg: MessageSegment):
    with pytest.raises(ValueError, match=f"Cannot send '{seg.type}' segment"):
        Message([seg]).serialize()

    with pytest.raises(ValueError, match=f"Cannot send '{seg.type}' segment"):
        Message([MessageSegment.text("hi"), seg]).serialize()


def test_serialize_rejects_empty_message():
    with pytest.raises(ValueError, match="empty message"):
        Message().serialize()


def test_system_divider_matches_documented_format():
    seg = MessageSegment.system_divider("新会话", {"zh_CN": "新会话", "en_US": "New Session"}, need_rollup=True)

    msg_type, content = Message([seg]).serialize()

    assert msg_type == "system"
    assert json.loads(content) == {
        "type": "divider",
        "params": {"divider_text": {"text": "新会话", "i18n_text": {"zh_CN": "新会话", "en_US": "New Session"}}},
        "options": {"need_rollup": True},
    }


def test_system_divider_omits_optional_fields():
    _, content = Message([MessageSegment.system_divider("新会话")]).serialize()

    assert json.loads(content) == {"type": "divider", "params": {"divider_text": {"text": "新会话"}}}


def test_system_divider_cannot_be_combined_with_other_segments():
    with pytest.raises(ValueError, match="'system' segment in a post message"):
        Message([MessageSegment.text("hi"), MessageSegment.system_divider("新会话")]).serialize()


def test_system_divider_str():
    assert str(MessageSegment.system_divider("新会话")) == "[system_divider:'新会话']"


def test_received_system_message_keeps_its_format():
    received = {"template": "template", "from_user": ["a"], "to_chatters": ["b"]}

    seg = Message.deserialize(json.dumps(received), None, "system")[0]

    assert seg.type == "system"
    assert seg.data == received


def test_serialize_rejects_received_system_message():
    received = {"template": "template", "from_user": ["a"], "to_chatters": ["b"]}
    seg = Message.deserialize(json.dumps(received), None, "system")[0]

    with pytest.raises(ValueError, match="system_divider"):
        Message([seg]).serialize()

    with pytest.raises(ValueError, match="system_divider"):
        Message([MessageSegment.text("hi"), seg]).serialize()


def test_serialize_rejects_system_builder_segment():
    with pytest.raises(ValueError, match="system_divider"):
        Message([MessageSegment.system("template", [], [])]).serialize()


def test_serialize_allows_raw_system_segment_in_documented_format():
    data = {"type": "divider", "params": {"divider_text": {"text": "新会话"}}}

    msg_type, content = Message([MessageSegment("system", data)]).serialize()

    assert msg_type == "system"
    assert json.loads(content) == data
