---
sidebar_position: 3
description: 调用 API

options:
  menu:
    - category: guide
      weight: 40
---

# 调用 API

## 类型化的 API

`bot.rest` 提供飞书开放平台的服务端 API，由 [larkify](https://starhearthunt.github.io/larkify/) 生成，参数和响应都有类型标注：

```python
response = await bot.rest.im.v1.message.async_create(
    receive_id_type="chat_id",
    receive_id="oc_xxx",
    msg_type="text",
    content='{"text": "你好"}',
)
print(response.parsed_data.message_id)
```

调用路径与 larkify 的 `feishu.rest.<业务域>.<版本>.<资源>.<方法>` 一致，只能使用 `async_` 开头的方法。这些调用经过 `call_api`，会触发 `on_calling_api` 和 `on_called_api` 钩子。

## 按路径调用

没有收录的接口可以用 `call_api` 调用，路径不包含 `/open-apis/` 前缀，`method` 必须传入：

```python
result = await bot.call_api("bot/v3/info", method="GET")
print(result["bot"]["open_id"])
```

返回值是解码后的完整响应体，文件等非 JSON 响应返回 `bytes`。

| 参数                  | 说明                                  |
| --------------------- | ------------------------------------- |
| `method`              | HTTP 方法                             |
| `params` / `query`    | 查询参数                              |
| `json` / `body`       | JSON 请求体                           |
| `data` / `files`      | 表单和文件                            |
| `content`             | 原始请求体                            |
| `headers` / `cookies` | 请求头和 Cookie                       |
| `_timeout`            | 覆盖本次调用的超时，`None` 表示不限时 |
| `_return_response`    | 返回 `larkify.Response` 而不是响应体  |

## 错误处理

| 异常           | 触发条件                                                                                       |
| -------------- | ---------------------------------------------------------------------------------------------- |
| `ActionFailed` | HTTP 错误，或者飞书返回非零的 `code`。`info` 属性包含 `status_code`、`code`、`msg` 和 `log_id` |
| `NetworkError` | 网络错误和超时                                                                                 |

```python
from nonebot.adapters.feishu import ActionFailed

try:
    await bot.send(event, "你好")
except ActionFailed as e:
    print(e.info["code"], e.info["msg"], e.info["log_id"])
```

被限流的请求和幂等请求遇到的服务端错误会自动重试，`_timeout` 和 `API_TIMEOUT` 对每次尝试分别生效。发送消息这样的 POST 请求不会在服务端错误后重试，避免消息重复发送。

## 使用 larkify 客户端

`bot.feishu` 是当前 Bot 的 larkify 客户端，可以使用分页这样不适合走 `call_api` 的功能：

```python
async for chat in bot.feishu.rest.paginate(bot.feishu.rest.im.v1.chat.async_list):
    print(chat.name)
```

这些调用不会触发钩子，抛出的是 larkify 的异常，详见 [larkify 文档](https://starhearthunt.github.io/larkify/)。
