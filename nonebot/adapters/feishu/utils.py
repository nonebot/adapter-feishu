from collections.abc import Awaitable, Callable
import inspect
from io import BytesIO
import logging
from pathlib import Path
from typing import TYPE_CHECKING, Any

from nonebot.log import LoguruHandler
from nonebot.utils import logger_wrapper

if TYPE_CHECKING:
    from larkify import Feishu

    from .bot import Bot

log = logger_wrapper("FEISHU")

# larkify 使用标准库 logging，交给 NoneBot 统一输出，级别由 LOG_LEVEL 控制
_larkify_logger = logging.getLogger("larkify")
_larkify_logger.setLevel(logging.DEBUG)
_larkify_logger.addHandler(LoguruHandler())


def f2b(file: str | bytes | BytesIO | Path) -> bytes:
    if isinstance(file, bytes):
        return file

    elif isinstance(file, str):
        return Path(file).resolve().read_bytes()

    elif isinstance(file, BytesIO):
        return file.getvalue()

    elif isinstance(file, Path):
        return file.resolve().read_bytes()


def resolve_rest_api(feishu: "Feishu", api: str) -> Callable[..., Awaitable[Any]]:
    """根据 `rest.im.v1.message.async_create` 这样的路径找到 larkify 的方法。"""
    func: Any = feishu
    for part in api.split("."):
        func = getattr(func, part)

    if not inspect.iscoroutinefunction(func):
        raise TypeError(f"{api} is invalid, only the `async_` methods can be called")

    return func


class APIContext:
    """把 `bot.rest.a.b(...)` 转换为 `bot.call_api("rest.a.b", ...)`。"""

    __slots__ = ("bot", "parts")

    def __init__(self, bot: "Bot", parts: tuple[str, ...]) -> None:
        self.bot = bot
        self.parts = parts

    def __getattr__(self, name: str) -> "APIContext":
        return APIContext(self.bot, (*self.parts, name))

    async def __call__(self, *args: Any, **kwargs: Any) -> Any:
        api = ".".join(self.parts)
        if args:
            # `call_api` 只接受关键字参数，而路径参数可以按位置传入
            signature = inspect.signature(resolve_rest_api(self.bot.feishu, api))
            kwargs = {**signature.bind_partial(*args).arguments, **kwargs}

        return await self.bot.call_api(api, **kwargs)
