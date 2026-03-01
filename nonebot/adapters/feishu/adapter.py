import asyncio
import inspect
import json
from typing import Any, Callable, Optional, Union, cast
from typing_extensions import override

from pygtrie import StringTrie

from nonebot import get_plugin_config
from nonebot.adapters import Adapter as BaseAdapter
from nonebot.compat import type_validate_python
from nonebot.drivers import (
    URL,
    ASGIMixin,
    Driver,
    HTTPClientMixin,
    HTTPServerSetup,
    Request,
    Response,
    WebSocketClientMixin,
)
from nonebot.exception import WebSocketClosed
from nonebot.utils import escape_tag

from . import event
from .bot import Bot
from .config import BotConfig, Config
from .event import Event
from .exception import ApiNotAvailable, FeishuAdapterException, NetworkError
from .message import Message, MessageSegment
from .models import BotInfoResponse, TenantAccessTokenResponse
from .utils import AESCipher, cache, log
from .ws import WsClient

RECONNECT_INTERVAL = 3.0


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
            result = await self.get_bot_info(bot_config)
            if result.code != 0:
                log(
                    "ERROR",
                    "<r><bg #f8bbd0>Failed to get bot info.</bg #f8bbd0></r> "
                    f"Skipped Bot {bot_config.app_id} registration",
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
            self.bot_connect(bot)
            log(
                "INFO",
                f"<y>Bot {escape_tag(bot_config.app_id)}</y> connected",
            )

            if bot_config.protocol == "ws":
                if not isinstance(self.driver, WebSocketClientMixin):
                    log(
                        "WARNING",
                        f"Current driver does not support WebSocket client. "
                        f"Skipped WS for Bot {escape_tag(bot_config.app_id)}.",
                    )
                else:
                    client = WsClient(self, bot, bot_config)
                    task = asyncio.create_task(self._run_ws(client, bot_config))
                    task.add_done_callback(self.tasks.discard)
                    self.tasks.add(task)
            else:
                setup = HTTPServerSetup(
                    URL(f"/feishu/{bot.self_id}"),
                    "POST",
                    self.get_name(),
                    self._handle_http,
                )
                self.setup_http_server(setup)

    def setup(self) -> None:
        if not isinstance(self.driver, ASGIMixin):
            raise RuntimeError(
                f"Current driver {self.config.driver} "
                "doesn't support reverse connections!"
                f"{self.get_name()} Adapter needs a ASGI Driver to work."
            )

        if not isinstance(self.driver, HTTPClientMixin):
            raise RuntimeError(
                f"Current driver {self.config.driver} "
                "doesn't support http client requests!"
                f"{self.get_name()} Adapter needs a HTTPClient Driver to work."
            )

        self.driver.on_startup(self.startup)
        self.driver.on_shutdown(self._stop)

    async def _stop(self) -> None:
        """取消所有 WS 任务并等待结束（shutdown 时调用）。"""
        for task in self.tasks:
            if not task.done():
                task.cancel()
        await asyncio.gather(
            *(asyncio.wait_for(task, timeout=10) for task in self.tasks),
            return_exceptions=True,
        )

    async def _run_ws(self, client: WsClient, bot_config: BotConfig) -> None:
        """单 Bot 的 WebSocket 长连接循环：异常时记录并按间隔重连。"""
        app_id = bot_config.app_id
        while True:
            try:
                await client.run()
            except WebSocketClosed as e:
                log(
                    "WARNING",
                    f"Feishu WebSocket for Bot <y>{escape_tag(app_id)}</y> closed by peer",
                    e,
                )
            except Exception as e:
                log(
                    "ERROR",
                    "<r><bg #f8bbd0>Error while processing Feishu WebSocket for bot "
                    f"<y>{escape_tag(app_id)}</y>. Trying to reconnect...</bg #f8bbd0></r>",
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

    def get_api_url(self, bot_config: BotConfig, path: str):
        return self.get_api_base(bot_config).joinpath("open-apis", path)

    async def get_bot_info(self, bot_config: BotConfig):
        token = await self.get_tenant_access_token(bot_config)

        response = await self.send_request(
            Request(
                "GET",
                self.get_api_url(bot_config, "bot/v3/info"),
                headers={
                    "Authorization": f"Bearer {token}",
                },
            ),
        )
        result = type_validate_python(BotInfoResponse, response)

        return result

    async def get_tenant_access_token(self, bot_config: BotConfig):
        key = f"feishu_tenant_access_token_{bot_config.app_id}"

        if token := await cache.get(key):
            return cast("str", token)

        response = await self.send_request(
            Request(
                "POST",
                self.get_api_url(bot_config, "auth/v3/tenant_access_token/internal"),
                json={
                    "app_id": bot_config.app_id,
                    "app_secret": bot_config.app_secret,
                },
            ),
        )
        result = type_validate_python(TenantAccessTokenResponse, response)

        expire = result.expire
        if expire > 30 * 60:
            expire -= 30 * 60

        await cache.set(key, result.tenant_access_token, expire)

        return result.tenant_access_token

    async def send_request(self, request: Request, **data: Any):
        return_response = data.get("_return_response", False)
        timeout: float = data.get("_timeout", self.config.api_timeout)
        request.timeout = timeout

        if not isinstance(self.driver, HTTPClientMixin):
            raise ApiNotAvailable

        try:
            response = await self.driver.request(request)

            if 200 <= response.status_code < 300:
                if not response.content:
                    raise ValueError("Empty response")

                if return_response:
                    return response

                if response.headers["Content-Type"].find("application/json") != -1:
                    result = json.loads(response.content)
                    return result
                else:
                    return response.content

            raise NetworkError(
                f"HTTP request received unexpected "
                f"status code: {response.status_code}, "
                f"response content: {response.content}"
            )

        except FeishuAdapterException:
            raise

        except Exception as e:
            raise NetworkError("HTTP request failed") from e

    @override
    async def _call_api(self, bot, api: str, **data: Any) -> Any:
        bot = cast("Bot", bot)
        token = await self.get_tenant_access_token(bot.bot_config)
        headers = {**data.get("headers", {}), "Authorization": f"Bearer {token}"}

        request = Request(
            data["method"],
            self.get_api_url(bot.bot_config, api),
            cookies=data.get("cookies"),
            content=data.get("content"),
            data=data.get("data"),
            files=data.get("files"),
            json=data.get("json") or data.get("body"),
            params=data.get("params") or data.get("query"),
            headers=headers,
        )

        return await self.send_request(request, **data)

    async def _handle_http(self, request: Request) -> Response:
        bot_config = self.bot_apps.get(request.url.parts[-1])
        if bot_config is None:
            raise RuntimeError("Corresponding bot config not found")

        if (data := request.content) is not None:
            if bot_config.encrypt_key is not None:
                if (encrypted := json.loads(data).get("encrypt")) is not None:
                    decrypted = AESCipher(bot_config.encrypt_key).decrypt_string(encrypted)
                    data = json.loads(decrypted)
            else:
                data = json.loads(data)

        if not isinstance(data, dict):
            return Response(500, content="Received non-JSON data, cannot cast to dict")

        if challenge := data.get("challenge"):
            return Response(200, content=json.dumps({"challenge": challenge}).encode())

        if not data.get("schema"):
            return Response(
                400,
                content=("Missing `schema` in POST body, only accept event V2"),
            )

        if headers := data.get("header"):
            token: str = headers.get("token")
        else:
            log("WARNING", "Missing `header` in POST body")
            return Response(
                400,
                content="Missing `header` in POST body",
            )

        if not token:
            log("WARNING", "Missing `verification token` in POST body")
            return Response(
                400,
                content="Missing `verification token` in POST body",
            )
        else:
            if token != bot_config.verification_token:
                log("WARNING", "Verification token check failed")
                return Response(
                    403,
                    content="Verification token check failed",
                )

        if data is not None:
            if not (bot := self.bots.get(bot_config.app_id)):
                raise RuntimeError("Corresponding Bot instance not found")

            if event := self.json_to_event(data):
                bot = cast("Bot", bot)
                task = asyncio.create_task(bot.handle_event(event))
                task.add_done_callback(self.tasks.discard)
                self.tasks.add(task)

        return Response(200)

    @classmethod
    def json_to_event(cls, json_data: Any) -> Optional[Event]:
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
        send_func: Callable[[Bot, Event, Union[str, Message, MessageSegment]], Any],
    ):
        """自定义 Bot 的回复函数。"""
        setattr(Bot, "send_handler", send_func)
