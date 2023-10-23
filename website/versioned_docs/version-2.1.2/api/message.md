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

  - Text

### _staticmethod_ `post(title, content, language="zh_cn")` {#MessageSegment-post}

- **参数**

  - `title` (str)

  - `content` (list[list[PostMessageNode]])

  - `language` (str)

- **返回**

  - Post

### _staticmethod_ `image(image_key)` {#MessageSegment-image}

- **参数**

  - `image_key` (str)

- **返回**

  - Image

### _staticmethod_ `interactive(header, config, elements=None, i18n_elements=None)` {#MessageSegment-interactive}

- **参数**

  - `header` (InteractiveHeader)

  - `config` (InteractiveConfig)

  - `elements` (list[dict[str, Any]] | None)

  - `i18n_elements` (list[dict[str, Any]] | None)

- **返回**

  - untyped

### _staticmethod_ `interactive_template(template_id, template_variable)` {#MessageSegment-interactive-template}

- **参数**

  - `template_id` (str)

  - `template_variable` (dict[str, Any])

- **返回**

  - InteractiveTemplate

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

### _staticmethod_ `audio(file_key, duration=None)` {#MessageSegment-audio}

- **参数**

  - `file_key` (str)

  - `duration` (int | None)

- **返回**

  - MessageSegment

### _staticmethod_ `media(file_key, image_key, file_name=None, duration=None)` {#MessageSegment-media}

- **参数**

  - `file_key` (str)

  - `image_key` (str | None)

  - `file_name` (str | None)

  - `duration` (int | None)

- **返回**

  - MessageSegment

### _staticmethod_ `file(file_key, file_name=None)` {#MessageSegment-file}

- **参数**

  - `file_key` (str)

  - `file_name` (str | None)

- **返回**

  - MessageSegment

### _staticmethod_ `sticker(file_key)` {#MessageSegment-sticker}

- **参数**

  - `file_key` (str)

- **返回**

  - MessageSegment

### _method_ `to_post()` {#MessageSegment-to-post}

- **参数**

  empty

- **返回**

  - untyped

## _class_ `Text(<auto>)` {#Text}

- **说明:** Text(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `At(<auto>)` {#At}

- **说明:** At(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `AtAll(<auto>)` {#AtAll}

- **说明:** AtAll(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `Image(<auto>)` {#Image}

- **说明:** Image(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `InteractiveHeaderTitle(<auto>)` {#InteractiveHeaderTitle}

- **参数**

  auto

## _class_ `InteractiveHeader(<auto>)` {#InteractiveHeader}

- **参数**

  auto

## _class_ `InteractiveConfig(<auto>)` {#InteractiveConfig}

- **参数**

  auto

## _class_ `Interactive(<auto>)` {#Interactive}

- **参数**

  auto

## _class_ `InteractiveTemplate(<auto>)` {#InteractiveTemplate}

- **说明:** InteractiveTemplate(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `ShareChat(<auto>)` {#ShareChat}

- **说明:** ShareChat(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `ShareUser(<auto>)` {#ShareUser}

- **说明:** ShareUser(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `Audio(<auto>)` {#Audio}

- **说明:** Audio(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `Media(<auto>)` {#Media}

- **说明:** Media(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `File(<auto>)` {#File}

- **说明:** File(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `Sticker(<auto>)` {#Sticker}

- **说明:** Sticker(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `PostMessageNode(<auto>)` {#PostMessageNode}

- **参数**

  auto

## _class_ `PostMessageNodeStylable(<auto>)` {#PostMessageNodeStylable}

- **参数**

  auto

## _class_ `PostText(<auto>)` {#PostText}

- **参数**

  auto

## _class_ `PostA(<auto>)` {#PostA}

- **参数**

  auto

## _class_ `PostAt(<auto>)` {#PostAt}

- **参数**

  auto

## _class_ `PostImg(<auto>)` {#PostImg}

- **参数**

  auto

## _class_ `PostMedia(<auto>)` {#PostMedia}

- **参数**

  auto

## _class_ `PostEmotion(<auto>)` {#PostEmotion}

- **参数**

  auto

## _class_ `Post(<auto>)` {#Post}

- **说明:** Post(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `System(<auto>)` {#System}

- **说明:** System(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `Location(<auto>)` {#Location}

- **说明:** Location(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `VideoChat(<auto>)` {#VideoChat}

- **说明:** VideoChat(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `Todo(<auto>)` {#Todo}

- **说明:** Todo(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `Vote(<auto>)` {#Vote}

- **说明:** Vote(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `Hongbao(<auto>)` {#Hongbao}

- **说明:** Hongbao(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `ShareCalendarEvent(<auto>)` {#ShareCalendarEvent}

- **说明:** ShareCalendarEvent(type: str, data: Dict[str, Any] = )

- **参数**

  auto

## _class_ `Calendar(<auto>)` {#Calendar}

- **参数**

  auto

## _class_ `GeneralCalendar(<auto>)` {#GeneralCalendar}

- **参数**

  auto

## _class_ `Message(<auto>)` {#Message}

- **说明:** 飞书 协议 Message 适配。

- **参数**

  auto

### _classmethod_ `get_segment_class()` {#Message-get-segment-class}

- **参数**

  empty

- **返回**

  - type[MessageSegment]

### _method_ `serialize()` {#Message-serialize}

- **参数**

  empty

- **返回**

  - tuple[str, str]

### _classmethod_ `from_event_message(event)` {#Message-from-event-message}

- **参数**

  - `event` (MessageEventDetail)

- **返回**

  - Message

### _method_ `extract_plain_text()` {#Message-extract-plain-text}

- **参数**

  empty

- **返回**

  - str
