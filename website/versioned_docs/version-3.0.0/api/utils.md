# nonebot.adapters.feishu.utils

## _def_ `log(<auto>)` {#log}



- **参数**

  auto

- **返回**

  - untyped

## _def_ `f2b(file)` {#f2b}



- **参数**

  - `file` (str | bytes | BytesIO | Path)

- **返回**

  - bytes

## _def_ `resolve_rest_api(feishu, api)` {#resolve-rest-api}

- **说明:** 根据 `rest.im.v1.message.async_create` 这样的路径找到 larkify 的方法。

- **参数**

  - `feishu` (Feishu)

  - `api` (str)

- **返回**

  - (...) -> Awaitable[Any]

## _class_ `APIContext(bot, parts)` {#APIContext}

- **说明:** 把 `bot.rest.a.b(...)` 转换为 `bot.call_api("rest.a.b", ...)`。

- **参数**

  - `bot` ([Bot](bot.md#Bot))

  - `parts` (tuple[str, ...])
