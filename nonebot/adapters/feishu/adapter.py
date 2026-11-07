import asyncio
from collections.abc import Callable, Coroutine, Generator, Mapping
from contextlib import contextmanager
import inspect
from typing import Any, cast
from typing_extensions import override

import httpx2
from larkify import UNSET, AppAuthStrategy, Feishu
from larkify.exception import (
    AuthCredentialError,
    FeishuException,
    RequestFailed,
    WebhookError,
    WebSocketError,
)
from larkify.webhooks import EventDispatcher
from larkify.ws import WSClient
from pygtrie import StringTrie

from nonebot import get_plugin_config
from nonebot.adapters import Adapter as BaseAdapter
from nonebot.compat import type_validate_python
from nonebot.drivers import URL, ASGIMixin, Driver, HTTPServerSetup, Request, Response
from nonebot.utils import escape_tag

from . import event
from .bot import Bot
from .config import BotConfig, Config
from .event import Event
from .exception import ActionFailed, FeishuAdapterException, NetworkError
from .message import Message, MessageSegment
from .models import BotInfoResponse
from .utils import log, resolve_rest_api

RECONNECT_INTERVAL = 3.0


@contextmanager
def translate_errors() -> Generator[None, None, None]:
    """把 larkify 的异常转换为 NoneBot 的异常。"""
    try:
        yield
    except RequestFailed as e:
        raise ActionFailed(status_code=e.response.status_code, code=e.code, msg=e.msg, log_id=e.log_id) from e
    except AuthCredentialError as e:
        raise ActionFailed(msg=str(e)) from e
    except FeishuException as e:
        raise NetworkError(f"API request failed: {e!r}") from e


class Dispatcher(EventDispatcher):
    """把事件交给 NoneBot。

    Webhook 的校验、解密和长连接的确认都由 larkify 完成，这里收到的事件已通过校验。
    """

    def __init__(self, adapter: "Adapter", bot_config: BotConfig) -> None:
        super().__init__(
            encrypt_key=bot_config.encrypt_key,
            verification_token=bot_config.verification_token,
        )
        self.adapter = adapter
        self.app_id = bot_config.app_id

    @override
    async def adispatch(self, data: Mapping[str, Any]) -> None:
        if not data.get("header"):
            raise WebhookError("Missing `header` in delivery, only accept event V2")

        if (bot := self.adapter.bots.get(self.app_id)) is None:
            raise RuntimeError("Corresponding Bot instance not found")

        # 飞书要求及时确认，事件在单独的任务中处理
        if event := self.adapter.json_to_event(dict(data)):
            self.adapter.create_task(cast("Bot", bot).handle_event(event))


class Adapter(BaseAdapter):
    # init all event models
    event_models: StringTrie = StringTrie(separator=".")
    """所有事件模型索引"""

    for model_name in dir(event):
        model = getattr(event, model_name)
        if not inspect.isclass(model) or not issubclass(model, Event):
            continue
        event_models["." + model.__event__] = model

    @override
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        """飞书适配器配置"""
        self.feishu_config: Config = get_plugin_config(Config)
        self.bot_apps: dict[str, BotConfig] = {}
        self.dispatchers: dict[str, Dispatcher] = {}
        self.tasks: set["asyncio.Task"] = set()
        self.setup()

    @classmethod
    @override
    def get_name(cls) -> str:
        """适配器名称: `Feishu`"""
        return "Feishu"

    async def startup(self):
        for bot_config in self.feishu_config.feishu_bots:
            self.bot_apps[bot_config.app_id] = bot_config
            try:
                result = await self.get_bot_info(bot_config)
            except FeishuAdapterException as e:
                log(
                    "ERROR",
                    "<r><bg #f8bbd0>Failed to get bot info.</bg #f8bbd0></r> "
                    f"Skipped Bot {escape_tag(bot_config.app_id)} registration",
                    e,
                )
                continue

            if self.bots.get(bot_config.app_id):
                continue

            bot = Bot(
                self,
                bot_config.app_id,
                bot_config=bot_config,
                bot_info=result.bot,
            )
            dispatcher = self.dispatchers[bot_config.app_id] = Dispatcher(self, bot_config)
            self.bot_connect(bot)
            log(
                "INFO",
                f"<y>Bot {escape_tag(bot_config.app_id)}</y> connected",
            )

            if bot_config.protocol == "ws":
                self.create_task(self._run_ws(WSClient(bot.feishu, dispatcher), bot))
            else:
                setup = HTTPServerSetup(
                    URL(f"/feishu/{bot.self_id}"),
                    "POST",
                    self.get_name(),
                    self._handle_http,
                )
                self.setup_http_server(setup)

    def setup(self) -> None:
        if not isinstance(self.driver, ASGIMixin) and any(
            bot_config.protocol == "http" for bot_config in self.feishu_config.feishu_bots
        ):
            raise RuntimeError(
                f"Current driver {self.config.driver} "
                "doesn't support reverse connections!"
                f"{self.get_name()} Adapter needs a ASGI Driver to receive webhooks."
            )

        self.driver.on_startup(self.startup)
        self.driver.on_shutdown(self._stop)

    def create_task(self, coroutine: Coroutine[Any, Any, None]) -> None:
        """运行后台任务，并持有其引用直至结束。"""
        task = asyncio.create_task(coroutine)
        task.add_done_callback(self.tasks.discard)
        self.tasks.add(task)

    async def _stop(self) -> None:
        """取消所有 WS 任务并等待结束（shutdown 时调用）。"""
        for task in self.tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(
            *(asyncio.wait_for(task, timeout=10) for task in self.tasks),
            return_exceptions=True,
        )

    async def _run_ws(self, client: WSClient, bot: Bot) -> None:
        """单 Bot 的 WebSocket 长连接：重连节奏由 larkify 按飞书下发的配置控制。"""
        app_id = escape_tag(bot.self_id)
        while True:
            try:
                await client.arun()
            except WebSocketError as e:
                # 只有无法恢复时才会抛出，例如凭证错误，此后收不到事件
                log("ERROR", f"Feishu WebSocket for Bot <y>{app_id}</y> gave up", e)
                if bot.self_id in self.bots:
                    self.bot_disconnect(bot)
                return
            except Exception as e:
                log(
                    "ERROR",
                    "<r><bg #f8bbd0>Error while processing Feishu WebSocket for bot "
                    f"<y>{app_id}</y>. Trying to reconnect...</bg #f8bbd0></r>",
                    e,
                )
            await asyncio.sleep(RECONNECT_INTERVAL)

    def get_api_base(self, bot_config: BotConfig) -> URL:
        if bot_config.api_base:
            return URL(str(bot_config.api_base))

        if bot_config.is_lark:
            return URL(str(self.feishu_config.feishu_lark_api_base))
        else:
            return URL(str(self.feishu_config.feishu_api_base))

    def create_client(self, bot_config: BotConfig) -> Feishu[AppAuthStrategy]:
        api_timeout = self.config.api_timeout
        return Feishu(
            AppAuthStrategy(bot_config.app_id, bot_config.app_secret, tenant_token_api="legacy"),
            base_url=str(self.get_api_base(bot_config)),
            timeout=httpx2.Timeout(None) if api_timeout is None else api_timeout,
            # 默认地址都是 https，http 只可能来自部署者的显式配置
            insecure_allow_http=True,
        )

    async def get_bot_info(self, bot_config: BotConfig) -> BotInfoResponse:
        with translate_errors():
            # 该接口不在 larkify 的生成范围内，字段也不在 `data` 下
            response = await self.create_client(bot_config).arequest(
                "GET",
                "/open-apis/bot/v3/info",
                response_model=BotInfoResponse,
                data_key=None,
            )
        return response.parsed_data

    @override
    async def _call_api(self, bot, api: str, **data: Any) -> Any:
        bot = cast("Bot", bot)

        if api.startswith("rest."):
            func = resolve_rest_api(bot.feishu, api)
            with translate_errors():
                return await func(**data)

        with translate_errors():
            response = await bot.feishu.arequest(
                data["method"],
                f"/open-apis/{api}",
                params=data.get("params") or data.get("query"),
                content=data.get("content"),
                data=data.get("data"),
                files=data.get("files"),
                json=data.get("json") or data.get("body"),
                headers=data.get("headers"),
                cookies=data.get("cookies"),
                timeout=data.get("_timeout", UNSET),
                # 下载的文件不必尝试按 JSON 解析
                response_model=bytes,
            )

        if not response.content:
            raise NetworkError("Empty response")

        if data.get("_return_response"):
            return response

        if "application/json" in response.headers.get("content-type", ""):
            return response.json()

        return response.content

    async def _handle_http(self, request: Request) -> Response:
        dispatcher = self.dispatchers.get(request.url.parts[-1])
        if dispatcher is None:
            raise RuntimeError("Corresponding bot config not found")

        content = request.content
        body = content.encode() if isinstance(content, str) else content or b""
        result = await dispatcher.ahandle(body, request.headers)

        return Response(
            result.status_code,
            headers={"Content-Type": result.content_type},
            content=result.body,
        )

    @classmethod
    def json_to_event(cls, json_data: Any) -> Event | None:
        """将 json 数据转换为 Event 对象。
        参数:
            json_data: json 数据
            self_id: 当前 Event 对应的 Bot
        返回:
            Event 对象，如果解析失败则返回 None
        """
        if not isinstance(json_data, dict):
            return

        if json_data.get("type") == "url_verification":
            return

        try:
            header = json_data["header"]
            event_type = header.get("event_type", "")
            if json_data.get("event", {}).get("message"):
                event_type += f".{json_data['event']['message']['chat_type']}"

            models = cls.get_event_model(event_type)
            for model in models:
                try:
                    event = type_validate_python(model, json_data)
                    break
                except Exception as e:
                    log("DEBUG", "Event Parser Error", e)
            else:
                event = type_validate_python(Event, json_data)

            return event

        except Exception as e:
            log(
                "ERROR",
                f"<r><bg #f8bbd0>Failed to parse event. Raw: {escape_tag(str(json_data))}</bg #f8bbd0></r>",
                e,
            )

    @classmethod
    def add_custom_model(cls, model: type[Event]) -> None:
        """插入或覆盖一个自定义的 Event 类型。
        需提供 `__event__` 属性，进行事件模型索引，
        格式为 `{post_type}[.{sub_type}]`，如: `message.private`。
        参数:
            model: 自定义的 Event 类型
        """
        if not hasattr(model, "__event__"):
            raise ValueError("Event model's `__event__` attribute must be set")
        cls.event_models["." + model.__event__] = model

    @classmethod
    def get_event_model(cls, event_name: str) -> list[type[Event]]:
        """根据事件名获取对应 `Event Model` 及 `FallBack Event Model` 列表，
        不包括基类 `Event`。
        """
        return [model.value for model in cls.event_models.prefixes("." + event_name)][::-1]

    @classmethod
    def custom_send(
        cls,
        send_func: Callable[[Bot, Event, str | Message | MessageSegment], Any],
    ):
        """自定义 Bot 的回复函数。"""
        setattr(Bot, "send_handler", send_func)
