# nonebot.adapters.feishu.ws.client

飞书 WebSocket 长连接客户端

## _class_ `WsClient(adapter, bot, bot_config)` {#WsClient}

- **说明**

  飞书 WebSocket 长连接客户端。

  通过 protobuf Frame 收发，
  支持 ping/pong、分片重组、事件接收与 ack。

- **参数**

  - `adapter` ([Adapter](../adapter.md#Adapter))

  - `bot` ([Bot](../bot.md#Bot))

  - `bot_config` ([BotConfig](../config.md#BotConfig))

### _async method_ `run()` {#WsClient-run}

- **说明:** 拉取端点、通过 NoneBot Driver 建立 WebSocket 连接，循环收发并维持 ping。

- **参数**

  empty

- **返回**

  - None
