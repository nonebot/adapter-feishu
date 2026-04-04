# nonebot.adapters.feishu.event

## _class_ `Event(<auto>)` {#Event}

- **说明**

  飞书协议事件。各事件字段参考 `飞书文档`\_

  .. \_飞书文档:
  https://open.feishu.cn/document/ukTMukTMukTM/uYDNxYjL2QTM24iN0EjN/event-list

- **参数**

  auto

### _method_ `get_type()` {#Event-get-type}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_event_name()` {#Event-get-event-name}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_event_description()` {#Event-get-event-description}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_message()` {#Event-get-message}

- **参数**

  empty

- **返回**

  - [Message](message.md#Message)

### _method_ `get_plaintext()` {#Event-get-plaintext}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_user_id()` {#Event-get-user-id}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_session_id()` {#Event-get-session-id}

- **参数**

  empty

- **返回**

  - str

### _method_ `is_tome()` {#Event-is-tome}

- **参数**

  empty

- **返回**

  - bool

## _class_ `MessageEvent(<auto>)` {#MessageEvent}

- **参数**

  auto

### _class-var_ `to_me` {#MessageEvent-to-me}

- **类型:** bool

- **说明**

  :说明: 消息是否与机器人有关

  :类型: `bool`

### _method_ `get_type()` {#MessageEvent-get-type}

- **参数**

  empty

- **返回**

  - Literal['message']

### _method_ `get_event_name()` {#MessageEvent-get-event-name}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_event_description()` {#MessageEvent-get-event-description}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_message()` {#MessageEvent-get-message}

- **参数**

  empty

- **返回**

  - [Message](message.md#Message)

### _method_ `get_plaintext()` {#MessageEvent-get-plaintext}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_user_id()` {#MessageEvent-get-user-id}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_all_user_id()` {#MessageEvent-get-all-user-id}

- **参数**

  empty

- **返回**

  - UserId

### _method_ `get_session_id()` {#MessageEvent-get-session-id}

- **参数**

  empty

- **返回**

  - str

### _method_ `is_tome()` {#MessageEvent-is-tome}

- **参数**

  empty

- **返回**

  - bool

## _class_ `GroupMessageEvent(<auto>)` {#GroupMessageEvent}

- **参数**

  auto

## _class_ `PrivateMessageEvent(<auto>)` {#PrivateMessageEvent}

- **参数**

  auto

## _class_ `NoticeEvent(<auto>)` {#NoticeEvent}

- **参数**

  auto

### _method_ `get_type()` {#NoticeEvent-get-type}

- **参数**

  empty

- **返回**

  - Literal['notice']

### _method_ `get_event_name()` {#NoticeEvent-get-event-name}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_event_description()` {#NoticeEvent-get-event-description}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_message()` {#NoticeEvent-get-message}

- **参数**

  empty

- **返回**

  - [Message](message.md#Message)

### _method_ `get_plaintext()` {#NoticeEvent-get-plaintext}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_user_id()` {#NoticeEvent-get-user-id}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_session_id()` {#NoticeEvent-get-session-id}

- **参数**

  empty

- **返回**

  - str

## _class_ `MessageReadEvent(<auto>)` {#MessageReadEvent}

- **参数**

  auto

## _class_ `GroupDisbandedEvent(<auto>)` {#GroupDisbandedEvent}

- **参数**

  auto

## _class_ `MessageReactionDeletedEvent(<auto>)` {#MessageReactionDeletedEvent}

- **参数**

  auto

## _class_ `MessageReactionCreatedEvent(<auto>)` {#MessageReactionCreatedEvent}

- **参数**

  auto

## _class_ `GroupConfigUpdatedEvent(<auto>)` {#GroupConfigUpdatedEvent}

- **参数**

  auto

## _class_ `GroupMemberBotAddedEvent(<auto>)` {#GroupMemberBotAddedEvent}

- **参数**

  auto

## _class_ `GroupMemberBotDeletedEvent(<auto>)` {#GroupMemberBotDeletedEvent}

- **参数**

  auto

## _class_ `GroupMemberUserAddedEvent(<auto>)` {#GroupMemberUserAddedEvent}

- **参数**

  auto

## _class_ `GroupMemberUserWithdrawnEvent(<auto>)` {#GroupMemberUserWithdrawnEvent}

- **参数**

  auto

## _class_ `GroupMemberUserDeletedEvent(<auto>)` {#GroupMemberUserDeletedEvent}

- **参数**

  auto

## _class_ `ContactUserUpdatedEvent(<auto>)` {#ContactUserUpdatedEvent}

- **参数**

  auto

## _class_ `ContactUserDeletedEvent(<auto>)` {#ContactUserDeletedEvent}

- **参数**

  auto

## _class_ `ContactUserCreatedEvent(<auto>)` {#ContactUserCreatedEvent}

- **参数**

  auto

## _class_ `ContactDepartmentUpdatedEvent(<auto>)` {#ContactDepartmentUpdatedEvent}

- **参数**

  auto

## _class_ `ContactDepartmentDeletedEvent(<auto>)` {#ContactDepartmentDeletedEvent}

- **参数**

  auto

## _class_ `ContactDepartmentCreatedEvent(<auto>)` {#ContactDepartmentCreatedEvent}

- **参数**

  auto

## _class_ `CalendarAclCreatedEvent(<auto>)` {#CalendarAclCreatedEvent}

- **参数**

  auto

## _class_ `CalendarAclDeletedEvent(<auto>)` {#CalendarAclDeletedEvent}

- **参数**

  auto

## _class_ `CalendarChangedEvent(<auto>)` {#CalendarChangedEvent}

- **参数**

  auto

## _class_ `CalendarEventChangedEvent(<auto>)` {#CalendarEventChangedEvent}

- **参数**

  auto

## _class_ `DriveFileReadEvent(<auto>)` {#DriveFileReadEvent}

- **参数**

  auto

## _class_ `DriveFileTitleUpdatedEvent(<auto>)` {#DriveFileTitleUpdatedEvent}

- **参数**

  auto

## _class_ `DriveFilePermissionMemberAddedEvent(<auto>)` {#DriveFilePermissionMemberAddedEvent}

- **参数**

  auto

## _class_ `DriveFilePermissionMemberRemovedEvent(<auto>)` {#DriveFilePermissionMemberRemovedEvent}

- **参数**

  auto

## _class_ `DriveFileTrashedEvent(<auto>)` {#DriveFileTrashedEvent}

- **参数**

  auto

## _class_ `DriveFileDeletedEvent(<auto>)` {#DriveFileDeletedEvent}

- **参数**

  auto

## _class_ `DriveFileEditedEvent(<auto>)` {#DriveFileEditedEvent}

- **参数**

  auto

## _class_ `MeetingRoomCreatedEvent(<auto>)` {#MeetingRoomCreatedEvent}

- **参数**

  auto

## _class_ `MeetingRoomUpdatedEvent(<auto>)` {#MeetingRoomUpdatedEvent}

- **参数**

  auto

## _class_ `MeetingRoomDeletedEvent(<auto>)` {#MeetingRoomDeletedEvent}

- **参数**

  auto

## _class_ `MeetingRoomStatusChangedEvent(<auto>)` {#MeetingRoomStatusChangedEvent}

- **参数**

  auto

## _class_ `VCMeetingStartedEvent(<auto>)` {#VCMeetingStartedEvent}

- **参数**

  auto

## _class_ `VCMeetingEndedEvent(<auto>)` {#VCMeetingEndedEvent}

- **参数**

  auto

## _class_ `VCMeetingJoinedEvent(<auto>)` {#VCMeetingJoinedEvent}

- **参数**

  auto

## _class_ `VCMeetingLeftEvent(<auto>)` {#VCMeetingLeftEvent}

- **参数**

  auto

## _class_ `VCMeetingRecordingStartedEvent(<auto>)` {#VCMeetingRecordingStartedEvent}

- **参数**

  auto

## _class_ `VCMeetingRecordingEndedEvent(<auto>)` {#VCMeetingRecordingEndedEvent}

- **参数**

  auto

## _class_ `VCMeetingRecordingReadyEvent(<auto>)` {#VCMeetingRecordingReadyEvent}

- **参数**

  auto

## _class_ `VCMeetingShareStartedEvent(<auto>)` {#VCMeetingShareStartedEvent}

- **参数**

  auto

## _class_ `VCMeetingShareEndedEvent(<auto>)` {#VCMeetingShareEndedEvent}

- **参数**

  auto

## _class_ `AttendanceUserFlowCreatedEvent(<auto>)` {#AttendanceUserFlowCreatedEvent}

- **参数**

  auto

## _class_ `AttendanceUserTaskUpdatedEvent(<auto>)` {#AttendanceUserTaskUpdatedEvent}

- **参数**

  auto
