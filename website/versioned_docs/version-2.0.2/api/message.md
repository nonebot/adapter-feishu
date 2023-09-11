# nonebot.adapters.feishu.message

## _class_ `MessageSegment(<auto>)` {#MessageSegment}

- **说明:** 飞书 协议 MessageSegment 适配。具体方法参考协议消息段类型或源码。

- **参数**

  auto

### _classmethod_ `get_message_class()` {#MessageSegment-get-message-class}

- **参数**

  empty

- **返回**

  - type[Message]

### _method_ `is_text()` {#MessageSegment-is-text}

- **参数**

  empty

- **返回**

  - bool

### _staticmethod_ `text(text)` {#MessageSegment-text}

- **参数**

  - `text` (str)

- **返回**

  - MessageSegment

### _staticmethod_ `post(title, content)` {#MessageSegment-post}

- **参数**

  - `title` (str)

  - `content` (list[Any])

- **返回**

  - MessageSegment

### _staticmethod_ `image(image_key)` {#MessageSegment-image}

- **参数**

  - `image_key` (str)

- **返回**

  - MessageSegment

### _staticmethod_ `interactive(data)` {#MessageSegment-interactive}

- **参数**

  - `data` (dict[str, Any])

- **返回**

  - MessageSegment

### _staticmethod_ `at(user_id)` {#MessageSegment-at}

- **参数**

  - `user_id` (str)

- **返回**

  - MessageSegment

### _staticmethod_ `share_chat(chat_id)` {#MessageSegment-share-chat}

- **参数**

  - `chat_id` (str)

- **返回**

  - MessageSegment

### _staticmethod_ `share_user(user_id)` {#MessageSegment-share-user}

- **参数**

  - `user_id` (str)

- **返回**

  - MessageSegment

### _staticmethod_ `audio(file_key)` {#MessageSegment-audio}

- **参数**

  - `file_key` (str)

- **返回**

  - MessageSegment

### _staticmethod_ `media(file_key, image_key)` {#MessageSegment-media}

- **参数**

  - `file_key` (str)

  - `image_key` (str | None)

- **返回**

  - MessageSegment

### _staticmethod_ `file(file_key)` {#MessageSegment-file}

- **参数**

  - `file_key` (str)

- **返回**

  - MessageSegment

### _staticmethod_ `sticker(file_key)` {#MessageSegment-sticker}

- **参数**

  - `file_key` (str)

- **返回**

  - MessageSegment

## _class_ `Message(<auto>)` {#Message}

- **说明:** 飞书 协议 Message 适配。

- **参数**

  auto

### _classmethod_ `get_segment_class()` {#Message-get-segment-class}

- **参数**

  empty

- **返回**

  - type[MessageSegment]

### _method_ `extract_plain_text()` {#Message-extract-plain-text}

- **参数**

  empty

- **返回**

  - str

## _class_ `MessageSerializer(<auto>)` {#MessageSerializer}

- **说明:** 飞书 协议 Message 序列化器。

- **参数**

  auto

### _method_ `serialize()` {#MessageSerializer-serialize}

- **参数**

  empty

- **返回**

  - tuple[str, str]

## _class_ `MessageDeserializer(<auto>)` {#MessageDeserializer}

- **说明:** 飞书 协议 Message 反序列化器。

- **参数**

  auto

### _method_ `deserialize()` {#MessageDeserializer-deserialize}

- **参数**

  empty

- **返回**

  - Message