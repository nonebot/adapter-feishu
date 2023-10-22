import re
import json
import itertools
from dataclasses import dataclass
from typing_extensions import override
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Type,
    Tuple,
    Union,
    Literal,
    Iterable,
    Optional,
    TypedDict,
)

from nonebot.adapters import Message as BaseMessage
from nonebot.adapters import MessageSegment as BaseMessageSegment

from .models import MessageEventDetail


class MessageSegment(BaseMessageSegment["Message"]):
    """
    飞书 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。
    """

    @classmethod
    @override
    def get_message_class(cls) -> Type["Message"]:
        return Message

    @override
    def is_text(self) -> bool:
        return self.type == "text"

    @override
    def __str__(self) -> str:
        if self.is_text():
            return self.data.get("text", "")
        return ""

    @override
    def __add__(
        self, other: Union[str, "MessageSegment", Iterable["MessageSegment"]]
    ) -> "Message":
        return Message(self) + (
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @override
    def __radd__(
        self, other: Union[str, "MessageSegment", Iterable["MessageSegment"]]
    ) -> "Message":
        return (
            MessageSegment.text(other) if isinstance(other, str) else Message(other)
        ) + self

    @staticmethod
    def text(text: str) -> "Text":
        return Text("text", {"text": str(text)})

    @staticmethod
    def post(
        title: str, content: List[List["PostMessageNode"]], language: str = "zh_cn"
    ) -> "Post":
        return Post("post", data={language: {"title": title, "content": content}})

    @staticmethod
    def image(image_key: str) -> "Image":
        return Image("image", {"image_key": image_key})

    @staticmethod
    def interactive(
        header: "InteractiveHeader",
        config: "InteractiveConfig",
        elements: Optional[List[Dict[str, Any]]] = None,
        i18n_elements: Optional[List[Dict[str, Any]]] = None,
    ):
        elements_key = "elements" if elements else "i18n_elements"
        elements_value = elements or i18n_elements

        return Interactive(
            "interactive",
            {
                "header": header,
                elements_key: elements_value,
                "config": config,
            },
        )

    @staticmethod
    def interactive_template(
        template_id: str, template_variable: Dict[str, Any]
    ) -> "InteractiveTemplate":
        return InteractiveTemplate(
            "interactive",
            {
                "template_id": template_id,
                "template_variable": template_variable,
            },
        )

    @staticmethod
    def share_chat(chat_id: str) -> "MessageSegment":
        return ShareChat("share_chat", {"chat_id": chat_id})

    @staticmethod
    def share_user(user_id: str) -> "MessageSegment":
        return ShareUser("share_user", {"user_id": user_id})

    @staticmethod
    def audio(file_key: str, duration: Optional[int] = None) -> "MessageSegment":
        return Audio("audio", {"file_key": file_key, "duration": duration})

    @staticmethod
    def media(
        file_key: str,
        image_key: Optional[str],
        file_name: Optional[str] = None,
        duration: Optional[int] = None,
    ) -> "MessageSegment":
        return Media(
            "media",
            {
                "file_key": file_key,
                "image_key": image_key,
                "file_name": file_name,
                "duration": duration,
            },
        )

    @staticmethod
    def file(file_key: str, file_name: Optional[str] = None) -> "MessageSegment":
        return File("file", {"file_key": file_key, "file_name": file_name})

    @staticmethod
    def sticker(file_key: str) -> "MessageSegment":
        return Sticker("sticker", {"file_key": file_key})


class _TextData(TypedDict):
    text: str


@dataclass
class Text(MessageSegment):
    if TYPE_CHECKING:
        data: _TextData

    @override
    def __str__(self) -> str:
        return self.data["text"]


class _AtData(TypedDict):
    user_id: str


@dataclass
class At(MessageSegment):
    if TYPE_CHECKING:
        data: _AtData

    @override
    def __str__(self) -> str:
        return f"@{self.data['user_id']}"


class _AtAllData(TypedDict):
    user_id: Literal["all"]


@dataclass
class AtAll(MessageSegment):
    if TYPE_CHECKING:
        data: _AtAllData

    @override
    def __str__(self) -> str:
        return "@all"


class _ImageData(TypedDict):
    image_key: str


@dataclass
class Image(MessageSegment):
    if TYPE_CHECKING:
        data: _ImageData

    @override
    def __str__(self) -> str:
        return f"<image:{self.data['image_key']!r}>"


class InteractiveHeaderTitle(TypedDict):
    tag: Literal["plain_text"]
    content: Optional[str]
    i18n: Optional[Dict[str, str]]
    template: Optional[str]


class InteractiveHeader(TypedDict):
    title: InteractiveHeaderTitle


class InteractiveConfig(TypedDict):
    enable_forward: Optional[bool]
    update_multi: Optional[bool]


class _InteractiveData(TypedDict):
    header: InteractiveHeader
    elements: Optional[List[Dict[str, Any]]]
    i18n_elements: Optional[List[Dict[str, Any]]]
    config: InteractiveConfig


class Interactive(MessageSegment):
    if TYPE_CHECKING:
        data: _InteractiveData

    @override
    def __str__(self) -> str:
        return f"<interactive:{self.data!r}>"


class _InteractiveTemplateData(TypedDict):
    template_id: str
    template_variable: Dict[str, Any]


@dataclass
class InteractiveTemplate(MessageSegment):
    if TYPE_CHECKING:
        data: _InteractiveTemplateData

    @override
    def __str__(self) -> str:
        return f"<interactive_template:{self.data!r}>"


class _ShareChatData(TypedDict):
    chat_id: str


@dataclass
class ShareChat(MessageSegment):
    if TYPE_CHECKING:
        data: _ShareChatData

    @override
    def __str__(self) -> str:
        return f"<share_chat:{self.data['chat_id']!r}>"


class _ShareUserData(TypedDict):
    user_id: str


@dataclass
class ShareUser(MessageSegment):
    if TYPE_CHECKING:
        data: _ShareUserData

    @override
    def __str__(self) -> str:
        return f"<share_user:{self.data['user_id']!r}>"


class _AudioData(TypedDict):
    file_key: str
    duration: Optional[int]


@dataclass
class Audio(MessageSegment):
    if TYPE_CHECKING:
        data: _AudioData

    @override
    def __str__(self) -> str:
        return f"<audio:{self.data!r}>"


class _MediaData(TypedDict):
    file_key: str
    image_key: Optional[str]
    file_name: Optional[str]
    duration: Optional[int]


@dataclass
class Media(MessageSegment):
    if TYPE_CHECKING:
        data: _MediaData

    @override
    def __str__(self) -> str:
        return f"<media:{self.data['file_key']!r}>"


class _FileData(TypedDict):
    file_key: str
    file_name: Optional[str]


@dataclass
class File(MessageSegment):
    if TYPE_CHECKING:
        data: _FileData

    @override
    def __str__(self) -> str:
        return f"<file:{self.data!r}>"


class _StickerData(TypedDict):
    file_key: str


@dataclass
class Sticker(MessageSegment):
    if TYPE_CHECKING:
        data: _StickerData

    @override
    def __str__(self) -> str:
        return f"<sticker:{self.data['file_key']!r}>"


class PostMessageNode(TypedDict):
    tag: str


class PostMessageNodeStylable(TypedDict):
    style: Optional[List[Literal["bold", "underline", "lineThrough", "italic"]]]


class PostText(PostMessageNode, PostMessageNodeStylable):
    text: str
    un_escape: Optional[bool]


class PostA(PostMessageNode, PostMessageNodeStylable):
    text: str
    href: str


class PostAt(PostMessageNode, PostMessageNodeStylable):
    user_id: str
    user_name: Optional[str]


class PostImg(PostMessageNode):
    image_key: str


class PostMedia(PostMessageNode):
    file_key: str
    image_key: Optional[str]


class PostEmotion(PostMessageNode):
    emoji_type: str


class _PostData(TypedDict):
    title: str
    content: List[List[PostMessageNode]]


@dataclass
class Post(MessageSegment):
    if TYPE_CHECKING:
        data: Dict[str, _PostData]  # i18n

    @override
    def __str__(self) -> str:
        return f"<post:{self.data!r}>"


class _SystemData(TypedDict):
    template: str
    from_user: List[str]
    to_chatters: List[str]


@dataclass
class System(MessageSegment):
    if TYPE_CHECKING:
        data: _SystemData

    @override
    def __str__(self) -> str:
        return f"<system:{self.data!r}>"


class _LocationData(TypedDict):
    name: str
    longitude: str
    latitude: str


@dataclass
class Location(MessageSegment):
    if TYPE_CHECKING:
        data: _LocationData

    @override
    def __str__(self) -> str:
        return f"<location:{self.data!r}>"


class _VideoChatData(TypedDict):
    topic: str
    start_time: str


@dataclass
class VideoChat(MessageSegment):
    if TYPE_CHECKING:
        data: _VideoChatData

    @override
    def __str__(self) -> str:
        return f"<video_chat:{self.data!r}>"


class _TodoData(TypedDict):
    task_id: str
    summary: _PostData
    due_time: str


@dataclass
class Todo(MessageSegment):
    if TYPE_CHECKING:
        data: _TodoData

    @override
    def __str__(self) -> str:
        return f"<todo:{self.data!r}>"


class _VoteData(TypedDict):
    topic: str
    options: List[str]


@dataclass
class Vote(MessageSegment):
    if TYPE_CHECKING:
        data: _VoteData

    @override
    def __str__(self) -> str:
        return f"<vote:{self.data!r}>"


class _HongbaoData(TypedDict):
    text: str


@dataclass
class Hongbao(MessageSegment):
    if TYPE_CHECKING:
        data: _HongbaoData

    @override
    def __str__(self) -> str:
        return f"<hongbao:{self.data['text']!r}>"


class _CalendarData(TypedDict):
    summary: str
    start_time: str
    end_time: str


@dataclass
class ShareCalendarEvent(MessageSegment):
    if TYPE_CHECKING:
        data: _CalendarData

    @override
    def __str__(self) -> str:
        return f"<share_calendar_event:{self.data!r}>"


class Calendar:
    if TYPE_CHECKING:
        data: _CalendarData

    @override
    def __str__(self) -> str:
        return f"<calendar:{self.data!r}>"


class GeneralCalendar:
    if TYPE_CHECKING:
        data: _CalendarData

    @override
    def __str__(self) -> str:
        return f"<general_calendar:{self.data!r}>"


class Message(BaseMessage[MessageSegment]):
    """
    飞书 协议 Message 适配。
    """

    @classmethod
    @override
    def get_segment_class(cls) -> Type[MessageSegment]:
        return MessageSegment

    @override
    def __add__(
        self, other: Union[str, "MessageSegment", Iterable["MessageSegment"]]
    ) -> "Message":
        return super().__add__(
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @override
    def __radd__(
        self, other: Union[str, "MessageSegment", Iterable["MessageSegment"]]
    ) -> "Message":
        return super().__radd__(
            MessageSegment.text(other) if isinstance(other, str) else other
        )

    @staticmethod
    @override
    def _construct(msg: str) -> Iterable[MessageSegment]:
        yield Text("text", {"text": msg})

    def serialize(self) -> Tuple[str, str]:
        combined = {"zh_cn": {"title": "", "content": [[]]}}
        if len(self) >= 2:
            for seg in self:
                if seg.type != "post":
                    combined["zh_cn"]["content"][-1].append(
                        {"tag": seg.type, **seg.data}
                    )
                else:
                    zh_cn_data = seg.data.pop("zh_cn", None)
                    if zh_cn_data:
                        combined["zh_cn"]["title"] = zh_cn_data["title"]
                        combined["zh_cn"]["content"] = [
                            *combined["zh_cn"]["content"],
                            *zh_cn_data["content"],
                        ]
                    combined.update(seg.data)

            return "post", json.dumps(combined, ensure_ascii=False)
        else:
            return self[0].type, json.dumps(self[0].data, ensure_ascii=False)

    @classmethod
    def from_event_message(cls, event: MessageEventDetail) -> "Message":
        msg = Message()
        content = json.loads(event.message.content)
        mentions = {
            # wipeout @ at the start of key
            mention.key[1:]: mention.id.open_id
            for mention in (event.message.mentions or [])
        }

        if event.message.message_type == "text":
            text = content["text"]
            text_begin = 0

            for embed in re.finditer(
                r"(?P<type>(?:@))(?P<key>\w+)",
                text,
            ):
                matched = text[text_begin : embed.pos + embed.start()]
                if matched:
                    msg.extend(Message(Text("text", matched)))

                text_begin = embed.pos + embed.end()
                if embed.group("type") == "@":
                    msg.extend(
                        Message(
                            At("at", {"user_id": mentions.get(embed.group("key"), "")})
                        )
                    )

            matched = text[text_begin:]
            if matched:
                msg.extend(Message(Text("text", {"text": text[text_begin:]})))

        elif event.message.message_type == "post":
            msg.append(Post("post", content))

        return msg

    @override
    def extract_plain_text(self) -> str:
        text_list: List[str] = []
        for seg in self:
            if seg.is_text():
                text_list.append(str(seg))

            elif seg.type == "post":
                text_list.append(seg.data["title"])
                for node in itertools.chain.from_iterable(seg.data["content"]):
                    if node["tag"] == "text":
                        text_list.append(node["text"])

        return "".join(text_list)
