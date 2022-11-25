# nonebot.adapters.feishu.message

## _class_ `MessageSegment(type, data=<factory>)` {#MessageSegment}

- **说明**

  飞书 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。

- **参数**

  - `type` (str)

  - `data` (dict[str, Any])

### _property_ `segment_text` {#MessageSegment-segment_text}

- **类型:** dict

### _staticmethod_ `at(user_id)` {#MessageSegment-at}

- **参数**

  - `user_id` (str)

- **返回**

  - MessageSegment

### _staticmethod_ `audio(file_key, duration)` {#MessageSegment-audio}

- **参数**

  - `file_key` (str)

  - `duration` (int)

- **返回**

  - MessageSegment

### _staticmethod_ `file(file_key, file_name)` {#MessageSegment-file}

- **参数**

  - `file_key` (str)

  - `file_name` (str)

- **返回**

  - MessageSegment

### _classmethod_ `get_message_class(cls)` {#MessageSegment-get_message_class}

- **返回**

  - Type[Message]

### _staticmethod_ `image(image_key)` {#MessageSegment-image}

- **参数**

  - `image_key` (str)

- **返回**

  - MessageSegment

### _staticmethod_ `interactive(data)` {#MessageSegment-interactive}

- **参数**

  - `data` (dict)

- **返回**

  - MessageSegment

### _method_ `is_text(self)` {#MessageSegment-is_text}

- **返回**

  - bool

### _staticmethod_ `media(file_key, image_key, file_name, duration)` {#MessageSegment-media}

- **参数**

  - `file_key` (str)

  - `image_key` (str)

  - `file_name` (str)

  - `duration` (int)

- **返回**

  - MessageSegment

### _staticmethod_ `post(title, content)` {#MessageSegment-post}

- **参数**

  - `title` (str)

  - `content` (list)

- **返回**

  - MessageSegment

### _staticmethod_ `share_chat(chat_id)` {#MessageSegment-share_chat}

- **参数**

  - `chat_id` (str)

- **返回**

  - MessageSegment

### _staticmethod_ `share_user(user_id)` {#MessageSegment-share_user}

- **参数**

  - `user_id` (str)

- **返回**

  - MessageSegment

### _staticmethod_ `sticker(file_key)` {#MessageSegment-sticker}

- **参数**

  - `file_key` (str)

- **返回**

  - MessageSegment

### _staticmethod_ `text(text)` {#MessageSegment-text}

- **参数**

  - `text` (str)

- **返回**

  - MessageSegment

## _class_ `Message(message=None)` {#Message}

- **说明**

  飞书 协议 Message 适配。

- **参数**

  - `message` (str | NoneType | Iterable[(~ TMS)] | (~ TMS))

### _method_ `extract_plain_text(self)` {#Message-extract_plain_text}

- **返回**

  - str

### _classmethod_ `get_segment_class(cls)` {#Message-get_segment_class}

- **返回**

  - Type[[MessageSegment](#MessageSegment)]

## _class_ `MessageSerializer(message)` {#MessageSerializer}

- **说明**

  飞书 协议 Message 序列化器。

- **参数**

  - `message` ([Message](#Message))

### _method_ `serialize(self)` {#MessageSerializer-serialize}

- **返回**

  - tuple[str, str]

## _class_ `MessageDeserializer(type, data, mentions)` {#MessageDeserializer}

- **说明**

  飞书 协议 Message 反序列化器。

- **参数**

  - `type` (str)

  - `data` (dict[str, Any])

  - `mentions` (list[dict] | None)

### _method_ `deserialize(self)` {#MessageDeserializer-deserialize}

- **返回**

  - [Message](#Message)
