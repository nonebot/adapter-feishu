import re
from typing_extensions import override
from typing import TYPE_CHECKING, Any, Dict, List, Union, Literal, Callable, Optional

from nonebot.message import handle_event
from nonebot.compat import type_validate_python

from nonebot.adapters import Bot as BaseBot

from .utils import log
from .config import BotConfig
from .models import BotInfo, ReplyResponse
from .message import At, Message, MessageSegment
from .event import Event, MessageEvent, GroupMessageEvent, PrivateMessageEvent

if TYPE_CHECKING:
    from .adapter import Adapter


async def _check_reply(bot: "Bot", event: "Event"):
    if not isinstance(event, MessageEvent):
        return

    if not event.event.message.parent_id:
        return

    if event.event.message.parent_id != event.event.message.message_id:
        try:
            response = await bot.call_api(
                f"im/v1/messages/{event.event.message.parent_id}",
                method="GET",
            )
            result = type_validate_python(
                ReplyResponse,
                response,
            )
            for message in result.data.items:
                if (
                    message.sender.id_type == "app_id"
                    and message.sender.id == bot.bot_config.app_id
                ):
                    event.to_me = True
                    event.reply = message
                    return

            if not event.reply and len(result.data.items) >= 1:
                event.reply = result.data.items[0]

        except Exception as e:
            log("ERROR", "Failed to get reply message", e)


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
        in {user.id.open_id for user in event.event.message.mentions}
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
        event.to_me = True
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
            del message[i:]
            deleted = True
            event.to_me = True

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

    return await bot.send_msg(receive_id_type, receive_id, content, msg_type)


class Bot(BaseBot):
    send_handler: Callable[["Bot", Event, Union[str, Message, MessageSegment]], Any] = (
        send
    )

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

    async def get_msgs(
        self, container_id_type: Literal["chat"], container_id: str, **params: Any
    ):
        return await self.call_api(
            "im/v1/messages",
            method="GET",
            params={
                "container_id_type": container_id_type,
                "container_id": container_id,
                **params,
            },
        )

    async def get_msg_resource(
        self, message_id: str, file_key: str, type_: Literal["image", "file"]
    ):
        return await self.call_api(
            f"im/v1/messages/{message_id}/resources/{file_key}",
            method="GET",
            params={"type": type_},
        )

    async def get_msg(self, message_id: str):
        return await self.call_api(
            f"im/v1/messages/{message_id}",
            method="GET",
        )

    async def get_msg_read_users(
        self,
        message_id: str,
        user_id_type: str,
        page_size: Optional[int] = None,
        page_token: Optional[str] = None,
    ):
        params: Dict[str, Any] = {"user_id_type": user_id_type}
        if page_size:
            params.update({"page_size": page_size})

        if page_token:
            params.update({"page_token": page_token})

        return await self.call_api(
            f"im/v1/messages/{message_id}/read_users", method="GET", params=params
        )

    async def merge_forward_msg(
        self,
        receive_id_type: str,
        receive_id: str,
        message_id_list: List[str],
        uuid: Optional[str] = None,
    ):
        params = {"receive_id_type": receive_id_type}
        if uuid:
            params.update({"uuid": uuid})

        return await self.call_api(
            "im/v1/messages/merge_forward",
            method="POST",
            params=params,
            json={"receive_id": receive_id, "message_id_list": message_id_list},
        )

    async def forward_msg(
        self,
        message_id: str,
        receive_id: str,
        receive_id_type: str,
        uuid: Optional[str] = None,
    ):
        params = {"receive_id_type": receive_id_type}
        if uuid:
            params.update({"uuid": uuid})

        return await self.call_api(
            f"im/v1/messages/{message_id}/forward",
            method="POST",
            params=params,
            json={"receive_id": receive_id},
        )

    async def delete_msg(self, message_id: str):
        return await self.call_api(f"im/v1/messages/{message_id}", method="DELETE")

    async def edit_msg(self, message_id: str, content: str, msg_type: str):
        return await self.call_api(
            f"im/v1/messages/{message_id}",
            method="PUT",
            json={"msg_type": msg_type, "content": content},
        )

    async def reply_msg(
        self, message_id: str, content: str, msg_type: str, uuid: Optional[str] = None
    ):
        json = {
            "content": content,
            "msg_type": msg_type,
        }

        if uuid:
            json.update({"uuid": uuid})

        return await self.call_api(
            f"im/v1/messages/{message_id}/reply",
            method="POST",
            json=json,
        )

    async def send_msg(
        self,
        receive_id_type: Literal["chat_id", "open_id"],
        receive_id: str,
        content: str,
        msg_type: str,
    ):
        return await self.call_api(
            "im/v1/messages",
            method="POST",
            params={"receive_id_type": receive_id_type},
            json={
                "receive_id": receive_id,
                "content": content,
                "msg_type": msg_type,
            },
        )

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
            await _check_reply(self, event)

        await handle_event(self, event)
