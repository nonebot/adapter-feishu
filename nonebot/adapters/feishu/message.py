import json
import itertools
from dataclasses import dataclass
from typing import Any, Dict, List, Type, Tuple, Union, Mapping, Iterable, Optional

from nonebot.typing import overrides

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment


class MessageSegment(BaseMessageSegment["Message"]):
    """
    飞书 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。
    """

    @classmethod
    @overrides(BaseMessageSegment)
    def get_message_class(cls) -> Type["Message"]:
        return Message

    @property
    def segment_text(self) -> dict:
        return {
            "image": "[图片]",
            "file": "[文件]",
            "folder": "[文件夹]",
            "audio": "[音频]",
            "media": "[视频]",
            "sticker": "[表情包]",
            "interactive": "[消息卡片]",
            "hongbao": "[红包]",
            "share_calendar_event": "[日程分享卡片]",
            "calendar": "[日程邀请卡片]",
            "general_calendar": "[日程转让卡片]",
            "share_chat": "[群名片]",
            "share_user": "[个人名片]",
            "system": "[系统消息]",
            "location": "[位置]",
            "video_chat": "[视频通话]",
            "todo": "[任务]",
            "vote": "[投票]",
        }

    def __str__(self) -> str:
        if self.type in ["text", "hongbao", "a"]:
            return self.data["text"]
        elif self.type == "at":
            return f"@{self.data['user_name']}"
        else:
            return self.segment_text.get(self.type, "[未知消息类型]")

    @overrides(BaseMessageSegment)
    def __add__(
        self, other: Union[str, "MessageSegment", Iterable["MessageSegment"]]
    ) -> "Message":
        return Message(self) + (
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @overrides(BaseMessageSegment)
    def __radd__(
        self, other: Union[str, "MessageSegment", Iterable["MessageSegment"]]
    ) -> "Message":
        return (
            MessageSegment.text(other) if isinstance(other, str) else Message(other)
        ) + self

    @overrides(BaseMessageSegment)
    def is_text(self) -> bool:
        return self.type == "text"

    # 发送消息
    @staticmethod
    def text(text: str) -> "MessageSegment":
        return MessageSegment("text", {"text": text})

    @staticmethod
    def post(title: str, content: List[Any]) -> "MessageSegment":
        return MessageSegment("post", {"title": title, "content": content})

    @staticmethod
    def image(image_key: str) -> "MessageSegment":
        return MessageSegment("image", {"image_key": image_key})

    @staticmethod
    def interactive(data: Dict[str, Any]) -> "MessageSegment":
        return MessageSegment("interactive", data)

    # 接收消息
    @staticmethod
    def at(user_id: str) -> "MessageSegment":
        return MessageSegment("at", {"user_id": user_id})

    @staticmethod
    def share_chat(chat_id: str) -> "MessageSegment":
        return MessageSegment("share_chat", {"chat_id": chat_id})

    @staticmethod
    def share_user(user_id: str) -> "MessageSegment":
        return MessageSegment("share_user", {"user_id": user_id})

    @staticmethod
    def audio(file_key: str) -> "MessageSegment":
        return MessageSegment("audio", {"file_key": file_key})

    @staticmethod
    def media(file_key: str, image_key: Optional[str]) -> "MessageSegment":
        return MessageSegment(
            "media",
            {
                "file_key": file_key,
                "image_key": image_key,
            },
        )

    @staticmethod
    def file(file_key: str) -> "MessageSegment":
        return MessageSegment("file", {"file_key": file_key})

    @staticmethod
    def sticker(file_key: str) -> "MessageSegment":
        return MessageSegment("sticker", {"file_key": file_key})


class Message(BaseMessage[MessageSegment]):
    """
    飞书 协议 Message 适配。
    """

    @classmethod
    @overrides(BaseMessage)
    def get_segment_class(cls) -> Type[MessageSegment]:
        return MessageSegment

    @overrides(BaseMessage)
    def __add__(
        self, other: Union[str, "MessageSegment", Iterable["MessageSegment"]]
    ) -> "Message":
        return super().__add__(
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @overrides(BaseMessage)
    def __radd__(
        self, other: Union[str, "MessageSegment", Iterable["MessageSegment"]]
    ) -> "Message":
        return super().__radd__(
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @staticmethod
    @overrides(BaseMessage)
    def _construct(
        msg: Union[str, Mapping, Iterable[Mapping]]
    ) -> Iterable[MessageSegment]:
        if isinstance(msg, Mapping) and not isinstance(msg, Iterable):
            yield MessageSegment(msg["type"], msg.get("data") or {})
            return
        elif isinstance(msg, str):
            yield MessageSegment.text(msg)
        elif isinstance(msg, Iterable):
            for seg in msg:
                if isinstance(seg, MessageSegment):
                    yield seg
                else:
                    yield MessageSegment(seg["type"], seg.get("data") or {})

    def _merge(self) -> "Message":
        msg: List[MessageSegment] = []
        for i, seg in enumerate(self):
            if seg.type == "text" and i != 0 and msg[-1].type == "text":
                msg[-1] = MessageSegment(
                    "text", {"text": msg[-1].data["text"] + seg.data["text"]}
                )
            else:
                msg.append(seg)
        return Message(msg)

    @overrides(BaseMessage)
    def extract_plain_text(self) -> str:
        return "".join(seg.data["text"] for seg in self if seg.is_text())


@dataclass
class MessageSerializer:
    """
    飞书 协议 Message 序列化器。
    """

    message: Message

    def serialize(self) -> Tuple[str, str]:
        segments = list(self.message)
        last_segment_type: str = ""
        if len(segments) > 1:
            msg = {"title": "", "content": [[]]}
            for segment in segments:
                if segment == "image":
                    if last_segment_type != "image":
                        msg["content"].append([])
                else:
                    if last_segment_type == "image":
                        msg["content"].append([])
                msg["content"][-1].append(
                    {
                        "tag": segment.type if segment.type != "image" else "img",
                        **segment.data,
                    }
                )
                last_segment_type = segment.type
            return "post", json.dumps({"zh_cn": {**msg}})

        else:
            return self.message[0].type, json.dumps(self.message[0].data)


@dataclass
class MessageDeserializer:
    """
    飞书 协议 Message 反序列化器。
    """

    type: str
    data: Dict[str, Any]
    mentions: Optional[List[dict]]

    def deserialize(self) -> Message:
        dict_mention = {}
        if self.mentions:
            for mention in self.mentions:
                dict_mention[mention["key"]] = mention

        if self.type == "post":
            msg = Message()
            if self.data["title"] != "":
                msg += MessageSegment("text", {"text": self.data["title"]})

            for seg in itertools.chain(*self.data["content"]):
                if (tag := seg.pop("tag")) == "at":
                    seg["user_name"] = dict_mention[seg["user_id"]]["name"]
                    seg["user_id"] = dict_mention[seg["user_id"]]["id"]["open_id"]

                msg += MessageSegment(tag if tag != "img" else "image", seg)

            return msg._merge()
        elif self.type == "text":
            for key, mention in dict_mention.items():
                self.data["text"] = self.data["text"].replace(
                    key, f"@{mention['name']}"
                )
            self.data["mentions"] = dict_mention

            return Message(MessageSegment(self.type, self.data))

        else:
            return Message(MessageSegment(self.type, self.data))
