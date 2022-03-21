# nonebot.adapters.feishu.adapter

## _class_ `Adapter(driver, **kwargs)` {#Adapter}

- **参数**

  - `driver` (nonebot.internal.driver.driver.Driver)

  - `**kwargs` (Any)

### _property_ `api_root` {#Adapter-api_root}

- **类型:** str

### _class-var_ `event_models` {#Adapter-event_models}

- **类型:** pygtrie.StringTrie

- **说明:** 所有事件模型索引

### _classmethod_ `add_custom_model(cls, model)` {#Adapter-add_custom_model}

- **说明**

  插入或覆盖一个自定义的 Event 类型。
  需提供 `__event__` 属性，进行事件模型索引，
  格式为 `{post_type}[.{sub_type}]`，如: `message.private`。

- **参数**

  - `model` (Type[[Event](./event.md#Event)]): 自定义的 Event 类型

- **返回**

  - None

### _classmethod_ `custom_send(cls, send_func)` {#Adapter-custom_send}

- **说明**

  自定义 Bot 的回复函数。

- **参数**

  - `send_func` (([Bot](./bot.md#Bot), [Event](./event.md#Event), str | [Message](./message.md#Message) | [MessageSegment](./message.md#MessageSegment)) -> Any)

- **返回**

  - Unknown

### _classmethod_ `get_event_model(cls, event_name)` {#Adapter-get_event_model}

- **说明**

  根据事件名获取对应 `Event Model` 及 `FallBack Event Model` 列表，不包括基类 `Event`。

- **参数**

  - `event_name` (str)

- **返回**

  - list[Type[[Event](./event.md#Event)]]

### _classmethod_ `get_name(cls)` {#Adapter-get_name}

- **说明**

  适配器名称: `Feishu`

- **返回**

  - str

### _classmethod_ `json_to_event(cls, json_data)` {#Adapter-json_to_event}

- **说明**

  将 json 数据转换为 Event 对象。

- **参数**

  - `json_data` (Any): json 数据

  - `self_id`: 当前 Event 对应的 Bot

- **返回**

  - [Event](./event.md#Event) | None: Event 对象，如果解析失败则返回 None

### _method_ `model(_func=None, *, pre=False, allow_reuse=False, skip_on_failure=False)` {#Adapter-model}

- **说明**

  Decorate methods on a model indicating that they should be used to validate (and perhaps modify) data either
  before or after standard model parsing/validation is performed.

- **参数**

  - `_func` ((\*Any, \*\*Any) -> Any | None)

  - `pre` (bool)

  - `allow_reuse` (bool)

  - `skip_on_failure` (bool)

- **返回**

  - AnyClassMethod | ((\*Any, \*\*Any) -> Any) -> AnyClassMethod
