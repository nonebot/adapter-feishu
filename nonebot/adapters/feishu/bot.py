import re
from typing_extensions import override
from typing import TYPE_CHECKING, Any, List, Union, Callable

from nonebot.message import handle_event
from pydantic import Field, HttpUrl, BaseModel

from nonebot.adapters import Bot as BaseBot

from .utils import log
from .config import BotConfig
from .message import At, Message, MessageSegment
from .event import Event, MessageEvent, GroupMessageEvent, PrivateMessageEvent

if TYPE_CHECKING:
    from .adapter import Adapter


def _check_at_me(bot: "Bot", event: "Event"):
    """
    :说明:

      检查消息开头或结尾是否存在 @机器人，去除并赋值 ``event.to_me``

    :参数:

      * ``bot: Bot``: Bot 对象
      * ``event: Event``: Event 对象
    """
    if not isinstance(event, MessageEvent):
        return

    # ensure message not empty
    if not (message := event.get_message()):
        message.append(MessageSegment.text(""))

    if event.event.message.chat_type == "p2p":
        event.to_me = True
        return

    if (
        isinstance(event, GroupMessageEvent)
        and event.event.message.mentions is not None
        and bot.bot_info.open_id
        in [user.id.open_id for user in event.event.message.mentions]
    ):
        event.to_me = True

    def _is_at_me_seg(segment: MessageSegment) -> bool:
        return (
            segment.type == "at" and segment.data.get("user_id") == bot.bot_info.open_id
        )

    deleted = False
    if _is_at_me_seg(message[0]):
        message.pop(0)
        deleted = True
        if message and message[0].type == "text":
            message[0].data["text"] = message[0].data["text"].lstrip()
            if not message[0].data["text"]:
                del message[0]

    if not deleted:
        # wipe out last empty text segment
        i = -1
        last_msg_seg = message[i]
        if (
            last_msg_seg.type == "text"
            and not last_msg_seg.data["text"].strip()
            and len(message) >= 2
        ):
            i -= 1
            last_msg_seg = message[i]

        if _is_at_me_seg(last_msg_seg):
            deleted = True
            del message[i:]

    if not message:
        message.append(MessageSegment.text(""))


def _check_nickname(bot: "Bot", event: "Event"):
    """
    :说明:

      检查消息开头是否存在昵称，去除并赋值 ``event.to_me``

    :参数:

      * ``bot: Bot``: Bot 对象
      * ``event: Event``: Event 对象
    """
    if not isinstance(event, MessageEvent):
        return

    first_msg_seg = event.get_message()[0]
    if first_msg_seg.type != "text":
        return

    first_text = first_msg_seg.data["text"]

    nicknames = set(filter(lambda n: n, bot.config.nickname))
    if nicknames:
        # check if the user is calling me with my nickname
        nickname_regex = "|".join(nicknames)
        m = re.search(rf"^({nickname_regex})([\s,，]*|$)", first_text, re.IGNORECASE)
        if m:
            nickname = m.group(1)
            log("DEBUG", f"User is calling me {nickname}")
            event.to_me = True
            first_msg_seg.data["text"] = first_text[m.end() :]


async def send(
    bot: "Bot",
    event: Event,
    message: Union[str, Message, MessageSegment],
    at_sender: bool = False,
    **kwargs: Any,
) -> Any:
    """默认回复消息处理函数。"""

    message = message if isinstance(message, Message) else Message(message)

    if isinstance(event, GroupMessageEvent):
        receive_id, receive_id_type = event.event.message.chat_id, "chat_id"
    elif isinstance(event, PrivateMessageEvent):
        receive_id, receive_id_type = event.get_user_id(), "open_id"
    else:
        raise ValueError("Cannot guess `receive_id` and `receive_id_type` to reply!")

    full_message = Message()  # create a new message for prepending
    at_sender = at_sender and bool(event.get_user_id())
    if at_sender and receive_id_type == "chat_id":
        full_message += At("at", {"user_id": event.get_user_id()}) + " "
    full_message += message

    msg_type, content = full_message.serialize()

    params = {
        "method": "POST",
        "query": {"receive_id_type": receive_id_type},
        "body": {
            "receive_id": receive_id,
            "content": content,
            "msg_type": msg_type,
        },
    }

    return await bot.call_api("im/v1/messages", **params)


class BotInfo(BaseModel):
    activate_status: int = Field(alias="activate_status")
    app_name: str = Field(alias="app_name")
    avatar_url: HttpUrl = Field(alias="avatar_url")
    ip_white_list: List[str] = Field(alias="ip_white_list")
    open_id: str = Field(alias="open_id")


class Bot(BaseBot):
    send_handler: Callable[
        ["Bot", Event, Union[str, Message, MessageSegment]], Any
    ] = send

    @override
    def __init__(
        self,
        adapter: "Adapter",
        self_id: str,
        *,
        bot_config: BotConfig,
        bot_info: BotInfo,
    ):
        super().__init__(adapter, self_id)
        self.bot_config: BotConfig = bot_config
        self.bot_info: BotInfo = bot_info

    @override
    async def send(
        self,
        event: Event,
        message: Union[str, Message, MessageSegment],
        **kwargs: Any,
    ) -> Any:
        """根据 `event` 向触发事件的主体回复消息。
        参数:
            event: Event 对象
            message: 要发送的消息
            at_sender (bool): 是否 @ 事件主体
            kwargs: 其他参数，可以与 {ref}`nonebot.adapters.feishu.adapter.Adapter.custom_send` 配合使用
        返回:
            API 调用返回数据
        异常:
            ValueError: 缺少 `user_id`, `group_id`
            NetworkError: 网络错误
            ActionFailed: API 调用失败
        """  # noqa: E501
        return await self.__class__.send_handler(self, event, message, **kwargs)

    @override
    async def call_api(self, api: str, **data) -> Any:
        """
        :说明:
          调用 飞书 协议 API
        :参数:
          * ``api: str``: API 名称
          * ``**data: Any``: API 参数
        :返回:
          - ``Any``: API 调用返回数据
        :异常:
          - ``NetworkError``: 网络错误
          - ``ActionFailed``: API 调用失败
        """
        return await super().call_api(api, **data)

    async def handle_event(self, event: Event) -> None:
        if isinstance(event, MessageEvent):
            _check_at_me(self, event)
            _check_nickname(self, event)

        await handle_event(self, event)
