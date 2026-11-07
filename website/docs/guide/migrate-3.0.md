---
sidebar_position: 4
description: 从 2.x 迁移

options:
  menu:
    - category: guide
      weight: 50
---

# 从 2.x 迁移

3.0 把与飞书的通信层替换为 [larkify](https://github.com/StarHeartHunt/larkify)，事件、消息和 `Bot` 的方法保持不变。

## 环境

- 需要 pydantic 2.11 及以上，不再支持 pydantic v1。
- 不再需要正向驱动器。使用 Webhook 时配置 `DRIVER=~fastapi` 这样的 ASGI 驱动器即可，全部使用长连接时可以配置 `DRIVER=~none`。
- 不再依赖 `protobuf`、`cashews` 和 `pycryptodome`。

## 异常

API 调用失败时的异常变了，捕获 `NetworkError` 或者检查返回值中 `code` 的代码需要调整：

| 情况                    | 2.x            | 3.0            |
| ----------------------- | -------------- | -------------- |
| HTTP 4xx、5xx           | `NetworkError` | `ActionFailed` |
| HTTP 200 且 `code` 非零 | 返回响应体     | `ActionFailed` |
| Token 获取失败          | `NetworkError` | `ActionFailed` |
| 网络错误和超时          | `NetworkError` | `NetworkError` |

启动时无法获取机器人信息不再中断启动，该 Bot 会被跳过并记录错误日志。

`_return_response=True` 返回的是 `larkify.Response`，`status_code`、`headers` 和 `content` 的用法不变。

## Webhook

校验比之前严格，飞书正常发送的请求不受影响：

- URL 校验（challenge）请求也会校验 Verification Token。
- 配置了 `encrypt_key` 时会校验 `X-Lark-Signature` 签名，缺失或者不匹配的请求返回 401。
- 校验失败的状态码统一为 401，请求体不是 JSON 时返回 400。

成功时的响应体从空变为 `{"msg": "success"}`。

## 长连接

- 重连间隔使用飞书下发的配置，不再固定为 3 秒。
- 遇到无法恢复的错误（例如凭证错误或者连接数超限）时不再重试，Bot 会断开连接并记录错误日志。

## 重试

被限流的请求和幂等请求遇到的服务端错误会自动重试，详见[错误处理](./call-api.md#错误处理)。

## 移除的接口

| 移除                                      | 替代                                    |
| ----------------------------------------- | --------------------------------------- |
| `Adapter.send_request`                    | `bot.call_api` 或 `bot.feishu.arequest` |
| `Adapter.get_api_url`                     | 无                                      |
| `Adapter.get_tenant_access_token`         | 由 larkify 管理                         |
| `nonebot.adapters.feishu.ws`              | `larkify.ws`                            |
| `nonebot.adapters.feishu.utils.AESCipher` | `larkify.webhooks.decrypt`              |
| `nonebot.adapters.feishu.utils.cache`     | 无                                      |
| `models.TenantAccessTokenResponse`        | 无                                      |
