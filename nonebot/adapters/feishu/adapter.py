import json
import asyncio
import inspect
from datetime import timedelta
from typing import Any, Dict, List, Type, Union, Callable, Optional, cast

import httpx
from pygtrie import StringTrie
from pydantic import parse_obj_as
from nonebot.typing import overrides
from nonebot.utils import escape_tag
from nonebot.drivers import (
    URL,
    Driver,
    Request,
    Response,
    ReverseDriver,
    HTTPServerSetup,
)

from nonebot.adapters import Adapter as BaseAdapter

from . import event
from .event import Event
from .bot import Bot, BotInfo
from .exception import NetworkError
from .config import Config, BotConfig
from .message import Message, MessageSegment
from .utils import AESCipher, log, cache, _handle_api_result


class Adapter(BaseAdapter):
    # init all event models
    event_models: StringTrie = StringTrie(separator=".")
    """所有事件模型索引"""

    for model_name in dir(event):
        model = getattr(event, model_name)
        if not inspect.isclass(model) or not issubclass(model, Event):
            continue
        event_models["." + model.__event__] = model

    @overrides(BaseAdapter)
    def __init__(self, driver: Driver, **kwargs: Any):
        super().__init__(driver, **kwargs)
        """飞书适配器配置"""
        self.feishu_config: Config = Config(**self.config.dict())
        self.bot_apps: Dict[str, BotConfig] = {}
        self.setup()

    @classmethod
    @overrides(BaseAdapter)
    def get_name(cls) -> str:
        """适配器名称: `Feishu`"""
        return "Feishu"

    def setup(self) -> None:
        if not isinstance(self.driver, ReverseDriver):
            raise RuntimeError(
                f"Current driver {self.config.driver} doesn't support reverse connections!"
                "Feishu Adapter need a ReverseDriver to work."
            )

        @self.driver.on_startup
        async def _():
            async with httpx.AsyncClient() as client:
                for bot_config in self.feishu_config.feishu_bots:
                    try:
                        response = await client.get(
                            self._construct_url(bot_config, "bot/v3/info"),
                            headers={
                                "Authorization": f"Bearer {await self._fetch_tenant_access_token(bot_config)}"
                            },
                        )
                        if 200 <= response.status_code < 300:
                            result = response.json()
                        else:
                            raise NetworkError(
                                f"HTTP request received unexpected "
                                f"status code: {response.status_code}"
                            )
                    except httpx.InvalidURL:
                        raise NetworkError("API root url invalid")
                    except httpx.HTTPError:
                        raise NetworkError("HTTP request failed")

                    self.bot_apps[bot_config.app_id] = bot_config
                    bot_info = parse_obj_as(BotInfo, result.get("bot", {}))

                    bot = self.bots.get(bot_config.app_id)
                    if not bot:
                        bot = Bot(self, bot_config, bot_info)
                        self.bot_connect(bot)
                        log(
                            "INFO",
                            f"<y>Bot {escape_tag(bot_config.app_id)}</y> connected",
                        )
                    setup = HTTPServerSetup(
                        URL(f"/feishu/{bot.self_id}"),
                        "POST",
                        self.get_name(),
                        self._handle_http,
                    )
                    self.setup_http_server(setup)

    def _construct_url(self, bot_config: BotConfig, path: str):
        api_base = (
            self.feishu_config.feishu_lark_api_base
            if bot_config.is_lark
            else self.feishu_config.feishu_api_base
        )

        return api_base + path

    async def _fetch_tenant_access_token(self, bot_config: BotConfig) -> str:
        token_key = f"feishu_tenant_access_token_{bot_config.app_id}"
        cached_token = await cache.get(token_key)
        if cached_token is not None:
            return cached_token

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self._construct_url(
                        bot_config, "auth/v3/tenant_access_token/internal/"
                    ),
                    json={
                        "app_id": bot_config.app_id,
                        "app_secret": bot_config.app_secret,
                    },
                    timeout=self.config.api_timeout,
                )

            if 200 <= response.status_code < 300:
                result = response.json()
                expire = result["expire"]
                # token 有效期为 2 小时，在此期间调用该接口 token 不会改变
                # 当 token 有效期小于 30 分的时候，再次请求获取 token 的时候，会生成一个新的 token，与此同时老的 token 依然有效
                # 在有效期小于 30 分时使 token 过期，确保 token 时效性
                if expire > 30 * 60:
                    expire -= 30 * 60

                await cache.set(token_key, result["tenant_access_token"], expire)  # type: ignore
                return result["tenant_access_token"]
            else:
                raise NetworkError(
                    f"HTTP request received unexpected "
                    f"status code: {response.status_code}"
                )
        except httpx.InvalidURL:
            raise NetworkError("API root url invalid")
        except httpx.HTTPError:
            raise NetworkError("HTTP request failed")

    @overrides(BaseAdapter)
    async def _call_api(self, bot: Bot, api: str, **data: Any) -> Any:
        timeout: float = data.get("_timeout", self.config.api_timeout)
        log("DEBUG", f"Calling API <y>{api}</y>")

        headers = {
            "Authorization": f"Bearer {await self._fetch_tenant_access_token(bot.bot_config)}"
        }

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                request = data.get(
                    "request",
                    httpx.Request(
                        data["method"],
                        self._construct_url(bot.bot_config, api),
                        cookies=data.get("cookies"),
                        content=data.get("content"),
                        data=data.get("data"),
                        files=data.get("files"),
                        json=data.get("body"),
                        params=data.get("query"),
                        headers=headers,
                    ),
                )
                response = await client.send(request)
            if 200 <= response.status_code < 300:
                if response.headers["content-type"].startswith("application/json"):
                    result = response.json()
                    return _handle_api_result(result)
                else:
                    result = response.content
            else:
                raise NetworkError(
                    f"HTTP request received unexpected "
                    f"status code: {response.status_code} "
                    f"response body: {response.text}"
                )
        except httpx.InvalidURL:
            raise NetworkError("API root url invalid")
        except httpx.HTTPError:
            raise NetworkError("HTTP request failed")

    async def _handle_http(self, request: Request) -> Response:
        bot_config = self.bot_apps.get(request.url.parts[-1])
        if bot_config is None:
            raise RuntimeError("Corresponding bot config not found")

        data = request.content
        if data is not None:
            if bot_config.encrypt_key is not None:
                encrypted = json.loads(data).get("encrypt")
                if encrypted is not None:
                    decrypted = AESCipher(bot_config.encrypt_key).decrypt_string(
                        encrypted
                    )
                    data = json.loads(decrypted)
            else:
                data = json.loads(data)

        if not isinstance(data, dict):
            return Response(500, content="Received non-JSON data, cannot cast to dict")

        challenge = data.get("challenge")
        if challenge:
            return Response(200, content=json.dumps({"challenge": challenge}).encode())

        schema = data.get("schema")
        if not schema:
            return Response(
                400,
                content="Missing `schema` in POST body, only accept event of version 2.0",
            )

        headers = data.get("header")
        if headers:
            token = headers.get("token")
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
            event = self.json_to_event(data)
            bot = self.bots.get(bot_config.app_id)
            if not bot:
                raise RuntimeError("Corresponding Bot instance not found")
            bot = cast(Bot, bot)
            if event:
                asyncio.create_task(bot.handle_event(event))

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
            if json_data.get("event"):
                if json_data["event"].get("message"):
                    event_type += f".{json_data['event']['message']['chat_type']}"

            models = cls.get_event_model(event_type)
            for model in models:
                try:
                    event = model.parse_obj(json_data)
                    break
                except Exception as e:
                    log("DEBUG", "Event Parser Error", e)
            else:
                event = Event.parse_obj(json_data)

            return event
        except Exception as e:
            log(
                "ERROR",
                "<r><bg #f8bbd0>Failed to parse event. "
                f"Raw: {escape_tag(str(json_data))}</bg #f8bbd0></r>",
                e,
            )

    @classmethod
    def add_custom_model(cls, model: Type[Event]) -> None:
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
    def get_event_model(cls, event_name: str) -> List[Type[Event]]:
        """根据事件名获取对应 `Event Model` 及 `FallBack Event Model` 列表，不包括基类 `Event`。"""
        return [model.value for model in cls.event_models.prefixes("." + event_name)][
            ::-1
        ]

    @classmethod
    def custom_send(
        cls,
        send_func: Callable[[Bot, Event, Union[str, Message, MessageSegment]], Any],
    ):
        """自定义 Bot 的回复函数。"""
        setattr(Bot, "send_handler", send_func)
