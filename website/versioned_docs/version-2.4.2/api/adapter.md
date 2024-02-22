# nonebot.adapters.feishu.adapter

## _class_ `Adapter(driver, **kwargs)` {#Adapter}

- **参数**

  - `driver` (Driver)

  - `**kwargs` (Any)

### _class-var_ `event_models` {#Adapter-event-models}

- **类型:** StringTrie

- **说明:** 所有事件模型索引

### _classmethod_ `get_name()` {#Adapter-get-name}

- **说明:** 适配器名称: `Feishu`

- **参数**

  empty

- **返回**

  - str

### _async method_ `startup()` {#Adapter-startup}

- **参数**

  empty

- **返回**

  - untyped

### _method_ `setup()` {#Adapter-setup}

- **参数**

  empty

- **返回**

  - None

### _method_ `get_api_base(bot_config)` {#Adapter-get-api-base}

- **参数**

  - `bot_config` ([BotConfig](config.md#BotConfig))

- **返回**

  - URL

### _method_ `get_api_url(bot_config, path)` {#Adapter-get-api-url}

- **参数**

  - `bot_config` ([BotConfig](config.md#BotConfig))

  - `path` (str)

- **返回**

  - untyped

### _async method_ `get_bot_info(bot_config)` {#Adapter-get-bot-info}

- **参数**

  - `bot_config` ([BotConfig](config.md#BotConfig))

- **返回**

  - untyped

### _async method_ `get_tenant_access_token(bot_config)` {#Adapter-get-tenant-access-token}

- **参数**

  - `bot_config` ([BotConfig](config.md#BotConfig))

- **返回**

  - untyped

### _async method_ `send_request(request, **data)` {#Adapter-send-request}

- **参数**

  - `request` (Request)

  - `**data` (Any)

- **返回**

  - untyped

### _classmethod_ `json_to_event(json_data)` {#Adapter-json-to-event}

- **说明:** 将 json 数据转换为 Event 对象。

- **参数**

  - `json_data` (Any): json 数据

  - `self_id`: 当前 Event 对应的 Bot

- **返回**

  - [Event](event.md#Event) | None: Event 对象，如果解析失败则返回 None

### _classmethod_ `add_custom_model(model)` {#Adapter-add-custom-model}

- **说明:** 插入或覆盖一个自定义的 Event 类型。 需提供 `__event__` 属性，进行事件模型索引， 格式为 `{post_type}[.{sub_type}]`，如: `message.private`。

- **参数**

  - `model` (type[[Event](event.md#Event)]): 自定义的 Event 类型

- **返回**

  - None

### _classmethod_ `get_event_model(event_name)` {#Adapter-get-event-model}

- **说明:** 根据事件名获取对应 `Event Model` 及 `FallBack Event Model` 列表， 不包括基类 `Event`。

- **参数**

  - `event_name` (str)

- **返回**

  - list[type[[Event](event.md#Event)]]

### _classmethod_ `custom_send(send_func)` {#Adapter-custom-send}

- **说明:** 自定义 Bot 的回复函数。

- **参数**

  - `send_func` (([Bot](bot.md#Bot), [Event](event.md#Event), str | [Message](message.md#Message) | [MessageSegment](message.md#MessageSegment)) -> Any)

- **返回**

  - untyped
