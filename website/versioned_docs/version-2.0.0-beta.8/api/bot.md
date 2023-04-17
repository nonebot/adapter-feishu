# nonebot.adapters.feishu.bot

## _async def_ `send(bot, event, message, at_sender=False, **kwargs)` {#send}

- **说明:** 默认回复消息处理函数。

- **参数**

  - `bot` (Bot)

  - `event` ([Event](event.md#Event))

  - `message` (str | [Message](message.md#Message) | [MessageSegment](message.md#MessageSegment))

  - `at_sender` (bool)

  - `**kwargs` (Any)

- **返回**

  - Any

## _class_ `BotInfo(<auto>)` {#BotInfo}

- **参数**

  auto

## _class_ `Bot(adapter, bot_config, bot_info)` {#Bot}

- **说明:** 飞书 协议 Bot 适配。继承属性参考 `BaseBot <./#class-basebot>`\_ 。

- **参数**

  - `adapter` ([Adapter](adapter.md#Adapter))

  - `bot_config` ([BotConfig](config.md#BotConfig))

  - `bot_info` (BotInfo)

### _async method_ `send_handler(event, message, at_sender=False, **kwargs)` {#Bot-send-handler}

- **说明:** 默认回复消息处理函数。

- **参数**

  - `event` ([Event](event.md#Event))

  - `message` (str | [Message](message.md#Message) | [MessageSegment](message.md#MessageSegment))

  - `at_sender` (bool)

  - `**kwargs` (Any)

- **返回**

  - Any

### _async method_ `send(event, message, **kwargs)` {#Bot-send}

- **说明:** 根据 `event` 向触发事件的主体回复消息。

- **参数**

  - `event` ([Event](event.md#Event)): Event 对象

  - `message` (str | [Message](message.md#Message) | [MessageSegment](message.md#MessageSegment)): 要发送的消息

  - `at_sender` (bool): 是否 @ 事件主体

  - `**kwargs` (Any): 其他参数，可以与 [Adapter.custom_send](adapter.md#Adapter-custom-send) 配合使用

- **返回**

  - Any: API 调用返回数据

- **异常**

  - ValueError: 缺少 `user_id`, `group_id`

  - NetworkError: 网络错误

  - ActionFailed: API 调用失败

### _async method_ `call_api(api, **data)` {#Bot-call-api}

- **说明**

  :说明:

  调用 OneBot 协议 API
  :参数:

  - `api: str`: API 名称
  - `**data: Any`: API 参数
    :返回:

  * `Any`: API 调用返回数据
    :异常:
  * `NetworkError`: 网络错误
  * `ActionFailed`: API 调用失败

- **参数**

  - `api` (str)

  - `**data`

- **返回**

  - Any

### _async method_ `handle_event(event)` {#Bot-handle-event}

- **参数**

  - `event` ([Event](event.md#Event))

- **返回**

  - None
