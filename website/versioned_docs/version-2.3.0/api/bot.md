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

## _class_ `Bot(adapter, self_id, *, bot_config, bot_info)` {#Bot}

- **参数**

  - `adapter` ([Adapter](adapter.md#Adapter))

  - `self_id` (str)

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

### _async method_ `get_msgs(container_id_type, container_id, **params)` {#Bot-get-msgs}

- **参数**

  - `container_id_type` (Literal['chat'])

  - `container_id` (str)

  - `**params` (Any)

- **返回**

  - untyped

### _async method_ `get_msg_resource(message_id, file_key, type_)` {#Bot-get-msg-resource}

- **参数**

  - `message_id` (str)

  - `file_key` (str)

  - `type_` (Literal['image', 'file'])

- **返回**

  - untyped

### _async method_ `get_msg(message_id)` {#Bot-get-msg}

- **参数**

  - `message_id` (str)

- **返回**

  - untyped

### _async method_ `get_msg_read_users(message_id, user_id_type, page_size=None, page_token=None)` {#Bot-get-msg-read-users}

- **参数**

  - `message_id` (str)

  - `user_id_type` (str)

  - `page_size` (int | None)

  - `page_token` (str | None)

- **返回**

  - untyped

### _async method_ `merge_forward_msg(receive_id_type, receive_id, message_id_list, uuid=None)` {#Bot-merge-forward-msg}

- **参数**

  - `receive_id_type` (str)

  - `receive_id` (str)

  - `message_id_list` (list[str])

  - `uuid` (str | None)

- **返回**

  - untyped

### _async method_ `forward_msg(message_id, receive_id, receive_id_type, uuid=None)` {#Bot-forward-msg}

- **参数**

  - `message_id` (str)

  - `receive_id` (str)

  - `receive_id_type` (str)

  - `uuid` (str | None)

- **返回**

  - untyped

### _async method_ `delete_msg(message_id)` {#Bot-delete-msg}

- **参数**

  - `message_id` (str)

- **返回**

  - untyped

### _async method_ `edit_msg(message_id, content, msg_type)` {#Bot-edit-msg}

- **参数**

  - `message_id` (str)

  - `content` (str)

  - `msg_type` (str)

- **返回**

  - untyped

### _async method_ `reply_msg(message_id, content, msg_type, uuid=None)` {#Bot-reply-msg}

- **参数**

  - `message_id` (str)

  - `content` (str)

  - `msg_type` (str)

  - `uuid` (str | None)

- **返回**

  - untyped

### _async method_ `send_msg(receive_id_type, receive_id, content, msg_type)` {#Bot-send-msg}

- **参数**

  - `receive_id_type` (Literal['chat\_id', 'open\_id'])

  - `receive_id` (str)

  - `content` (str)

  - `msg_type` (str)

- **返回**

  - untyped

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

- **说明:** :说明: 调用 飞书 协议 API :参数: _ `api: str`: API 名称 _ `**data: Any`: API 参数 :返回: - `Any`: API 调用返回数据 :异常: - `NetworkError`: 网络错误 - `ActionFailed`: API 调用失败

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
