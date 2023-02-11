# nonebot.adapters.feishu.event

## _class_ `EventHeader(<auto>)` {#EventHeader}

- **参数**

  auto

## _class_ `Event(<auto>)` {#Event}

- **说明**

  飞书协议事件。各事件字段参考 `飞书文档`\_

  .. \_飞书文档:
  https://open.feishu.cn/document/ukTMukTMukTM/uYDNxYjL2QTM24iN0EjN/event-list

- **参数**

  auto

### _method_ `get_type()` {#Event-get_type}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_event_name()` {#Event-get_event_name}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_event_description()` {#Event-get_event_description}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_message()` {#Event-get_message}

- **参数**

  empty

- **返回**

  - [Message](message.md#Message)

### _method_ `get_plaintext()` {#Event-get_plaintext}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_user_id()` {#Event-get_user_id}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_session_id()` {#Event-get_session_id}

- **参数**

  empty

- **返回**

  - str

### _method_ `is_tome()` {#Event-is_tome}

- **参数**

  empty

- **返回**

  - bool

## _class_ `UserId(<auto>)` {#UserId}

- **参数**

  auto

## _class_ `Sender(<auto>)` {#Sender}

- **参数**

  auto

## _class_ `ReplySender(<auto>)` {#ReplySender}

- **参数**

  auto

## _class_ `Mention(<auto>)` {#Mention}

- **参数**

  auto

## _class_ `ReplyMention(<auto>)` {#ReplyMention}

- **参数**

  auto

## _class_ `MessageBody(<auto>)` {#MessageBody}

- **参数**

  auto

## _class_ `Reply(<auto>)` {#Reply}

- **参数**

  auto

## _class_ `EventMessage(<auto>)` {#EventMessage}

- **参数**

  auto

### _classmethod_ `parse_message(values)` {#EventMessage-parse_message}

- **参数**

  - `values` (dict)

- **返回**

  - untyped

## _class_ `GroupEventMessage(<auto>)` {#GroupEventMessage}

- **参数**

  auto

## _class_ `PrivateEventMessage(<auto>)` {#PrivateEventMessage}

- **参数**

  auto

## _class_ `MessageEventDetail(<auto>)` {#MessageEventDetail}

- **参数**

  auto

## _class_ `GroupMessageEventDetail(<auto>)` {#GroupMessageEventDetail}

- **参数**

  auto

## _class_ `PrivateMessageEventDetail(<auto>)` {#PrivateMessageEventDetail}

- **参数**

  auto

## _class_ `MessageEvent(<auto>)` {#MessageEvent}

- **参数**

  auto

### _class-var_ `to_me` {#MessageEvent-to_me}

- **类型:** bool

- **说明**

  :说明: 消息是否与机器人有关

  :类型: `bool`

### _method_ `get_type()` {#MessageEvent-get_type}

- **参数**

  empty

- **返回**

  - Literal['message', 'notice']

### _method_ `get_event_name()` {#MessageEvent-get_event_name}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_event_description()` {#MessageEvent-get_event_description}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_message()` {#MessageEvent-get_message}

- **参数**

  empty

- **返回**

  - [Message](message.md#Message)

### _method_ `get_plaintext()` {#MessageEvent-get_plaintext}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_user_id()` {#MessageEvent-get_user_id}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_all_user_id()` {#MessageEvent-get_all_user_id}

- **参数**

  empty

- **返回**

  - UserId

### _method_ `get_session_id()` {#MessageEvent-get_session_id}

- **参数**

  empty

- **返回**

  - str

### _method_ `is_tome()` {#MessageEvent-is_tome}

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

### _method_ `get_type()` {#NoticeEvent-get_type}

- **参数**

  empty

- **返回**

  - Literal['message', 'notice']

### _method_ `get_event_name()` {#NoticeEvent-get_event_name}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_event_description()` {#NoticeEvent-get_event_description}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_message()` {#NoticeEvent-get_message}

- **参数**

  empty

- **返回**

  - [Message](message.md#Message)

### _method_ `get_plaintext()` {#NoticeEvent-get_plaintext}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_user_id()` {#NoticeEvent-get_user_id}

- **参数**

  empty

- **返回**

  - str

### _method_ `get_session_id()` {#NoticeEvent-get_session_id}

- **参数**

  empty

- **返回**

  - str

## _class_ `MessageReader(<auto>)` {#MessageReader}

- **参数**

  auto

## _class_ `MessageReadEventDetail(<auto>)` {#MessageReadEventDetail}

- **参数**

  auto

## _class_ `MessageReadEvent(<auto>)` {#MessageReadEvent}

- **参数**

  auto

## _class_ `GroupDisbandedEventDetail(<auto>)` {#GroupDisbandedEventDetail}

- **参数**

  auto

## _class_ `GroupDisbandedEvent(<auto>)` {#GroupDisbandedEvent}

- **参数**

  auto

## _class_ `Emoji(<auto>)` {#Emoji}

- **参数**

  auto

## _class_ `MessageReactionDeletedEventDetail(<auto>)` {#MessageReactionDeletedEventDetail}

- **参数**

  auto

## _class_ `MessageReactionDeletedEvent(<auto>)` {#MessageReactionDeletedEvent}

- **参数**

  auto

## _class_ `MessageReactionCreatedEventDetail(<auto>)` {#MessageReactionCreatedEventDetail}

- **参数**

  auto

## _class_ `MessageReactionCreatedEvent(<auto>)` {#MessageReactionCreatedEvent}

- **参数**

  auto

## _class_ `I18nNames(<auto>)` {#I18nNames}

- **参数**

  auto

## _class_ `ChatChange(<auto>)` {#ChatChange}

- **参数**

  auto

## _class_ `EventModerator(<auto>)` {#EventModerator}

- **参数**

  auto

## _class_ `ModeratorList(<auto>)` {#ModeratorList}

- **参数**

  auto

## _class_ `GroupConfigUpdatedEventDetail(<auto>)` {#GroupConfigUpdatedEventDetail}

- **参数**

  auto

## _class_ `GroupConfigUpdatedEvent(<auto>)` {#GroupConfigUpdatedEvent}

- **参数**

  auto

## _class_ `GroupMemberBotAddedEventDetail(<auto>)` {#GroupMemberBotAddedEventDetail}

- **参数**

  auto

## _class_ `GroupMemberBotAddedEvent(<auto>)` {#GroupMemberBotAddedEvent}

- **参数**

  auto

## _class_ `GroupMemberBotDeletedEventDetail(<auto>)` {#GroupMemberBotDeletedEventDetail}

- **参数**

  auto

## _class_ `GroupMemberBotDeletedEvent(<auto>)` {#GroupMemberBotDeletedEvent}

- **参数**

  auto

## _class_ `ChatMemberUser(<auto>)` {#ChatMemberUser}

- **参数**

  auto

## _class_ `GroupMemberUserAddedEventDetail(<auto>)` {#GroupMemberUserAddedEventDetail}

- **参数**

  auto

## _class_ `GroupMemberUserAddedEvent(<auto>)` {#GroupMemberUserAddedEvent}

- **参数**

  auto

## _class_ `GroupMemberUserWithdrawnEventDetail(<auto>)` {#GroupMemberUserWithdrawnEventDetail}

- **参数**

  auto

## _class_ `GroupMemberUserWithdrawnEvent(<auto>)` {#GroupMemberUserWithdrawnEvent}

- **参数**

  auto

## _class_ `GroupMemberUserDeletedEventDetail(<auto>)` {#GroupMemberUserDeletedEventDetail}

- **参数**

  auto

## _class_ `GroupMemberUserDeletedEvent(<auto>)` {#GroupMemberUserDeletedEvent}

- **参数**

  auto

## _class_ `AvatarInfo(<auto>)` {#AvatarInfo}

- **参数**

  auto

## _class_ `UserStatus(<auto>)` {#UserStatus}

- **参数**

  auto

## _class_ `UserOrder(<auto>)` {#UserOrder}

- **参数**

  auto

## _class_ `UserCustomAttrValue(<auto>)` {#UserCustomAttrValue}

- **参数**

  auto

## _class_ `UserCustomAttr(<auto>)` {#UserCustomAttr}

- **参数**

  auto

## _class_ `ContactUser(<auto>)` {#ContactUser}

- **参数**

  auto

## _class_ `OldContactUser(<auto>)` {#OldContactUser}

- **参数**

  auto

## _class_ `ContactUserUpdatedEventDetail(<auto>)` {#ContactUserUpdatedEventDetail}

- **参数**

  auto

## _class_ `ContactUserUpdatedEvent(<auto>)` {#ContactUserUpdatedEvent}

- **参数**

  auto

## _class_ `ContactUserDeletedEventDetail(<auto>)` {#ContactUserDeletedEventDetail}

- **参数**

  auto

## _class_ `ContactUserDeletedEvent(<auto>)` {#ContactUserDeletedEvent}

- **参数**

  auto

## _class_ `ContactUserCreatedEventDetail(<auto>)` {#ContactUserCreatedEventDetail}

- **参数**

  auto

## _class_ `ContactUserCreatedEvent(<auto>)` {#ContactUserCreatedEvent}

- **参数**

  auto

## _class_ `ContactDepartmentStatus(<auto>)` {#ContactDepartmentStatus}

- **参数**

  auto

## _class_ `ContactDepartment(<auto>)` {#ContactDepartment}

- **参数**

  auto

## _class_ `ContactDepartmentUpdatedEventDetail(<auto>)` {#ContactDepartmentUpdatedEventDetail}

- **参数**

  auto

## _class_ `ContactDepartmentUpdatedEvent(<auto>)` {#ContactDepartmentUpdatedEvent}

- **参数**

  auto

## _class_ `OldContactDepartment(<auto>)` {#OldContactDepartment}

- **参数**

  auto

## _class_ `ContactDepartmentDeletedEventDetail(<auto>)` {#ContactDepartmentDeletedEventDetail}

- **参数**

  auto

## _class_ `ContactDepartmentDeletedEvent(<auto>)` {#ContactDepartmentDeletedEvent}

- **参数**

  auto

## _class_ `ContactDepartmentCreatedEventDetail(<auto>)` {#ContactDepartmentCreatedEventDetail}

- **参数**

  auto

## _class_ `ContactDepartmentCreatedEvent(<auto>)` {#ContactDepartmentCreatedEvent}

- **参数**

  auto

## _class_ `CalendarAclScope(<auto>)` {#CalendarAclScope}

- **参数**

  auto

## _class_ `CalendarAclCreatedEventDetail(<auto>)` {#CalendarAclCreatedEventDetail}

- **参数**

  auto

## _class_ `CalendarAclCreatedEvent(<auto>)` {#CalendarAclCreatedEvent}

- **参数**

  auto

## _class_ `CalendarAclDeletedEventDetail(<auto>)` {#CalendarAclDeletedEventDetail}

- **参数**

  auto

## _class_ `CalendarAclDeletedEvent(<auto>)` {#CalendarAclDeletedEvent}

- **参数**

  auto

## _class_ `CalendarChangedEvent(<auto>)` {#CalendarChangedEvent}

- **参数**

  auto

## _class_ `CalendarEventChangedEventDetail(<auto>)` {#CalendarEventChangedEventDetail}

- **参数**

  auto

## _class_ `CalendarEventChangedEvent(<auto>)` {#CalendarEventChangedEvent}

- **参数**

  auto

## _class_ `DriveFileReadEventDetail(<auto>)` {#DriveFileReadEventDetail}

- **参数**

  auto

## _class_ `DriveFileReadEvent(<auto>)` {#DriveFileReadEvent}

- **参数**

  auto

## _class_ `DriveFileTitleUpdatedEventDetail(<auto>)` {#DriveFileTitleUpdatedEventDetail}

- **参数**

  auto

## _class_ `DriveFileTitleUpdatedEvent(<auto>)` {#DriveFileTitleUpdatedEvent}

- **参数**

  auto

## _class_ `DriveFilePermissionMemberAddedEventDetail(<auto>)` {#DriveFilePermissionMemberAddedEventDetail}

- **参数**

  auto

## _class_ `DriveFilePermissionMemberAddedEvent(<auto>)` {#DriveFilePermissionMemberAddedEvent}

- **参数**

  auto

## _class_ `DriveFilePermissionMemberRemovedEventDetail(<auto>)` {#DriveFilePermissionMemberRemovedEventDetail}

- **参数**

  auto

## _class_ `DriveFilePermissionMemberRemovedEvent(<auto>)` {#DriveFilePermissionMemberRemovedEvent}

- **参数**

  auto

## _class_ `DriveFileTrashedEventDetail(<auto>)` {#DriveFileTrashedEventDetail}

- **参数**

  auto

## _class_ `DriveFileTrashedEvent(<auto>)` {#DriveFileTrashedEvent}

- **参数**

  auto

## _class_ `DriveFileDeletedEventDetail(<auto>)` {#DriveFileDeletedEventDetail}

- **参数**

  auto

## _class_ `DriveFileDeletedEvent(<auto>)` {#DriveFileDeletedEvent}

- **参数**

  auto

## _class_ `DriveFileEditedEventDetail(<auto>)` {#DriveFileEditedEventDetail}

- **参数**

  auto

## _class_ `DriveFileEditedEvent(<auto>)` {#DriveFileEditedEvent}

- **参数**

  auto

## _class_ `MeetingRoomCreatedEventDetail(<auto>)` {#MeetingRoomCreatedEventDetail}

- **参数**

  auto

## _class_ `MeetingRoomCreatedEvent(<auto>)` {#MeetingRoomCreatedEvent}

- **参数**

  auto

## _class_ `MeetingRoomUpdatedEventDetail(<auto>)` {#MeetingRoomUpdatedEventDetail}

- **参数**

  auto

## _class_ `MeetingRoomUpdatedEvent(<auto>)` {#MeetingRoomUpdatedEvent}

- **参数**

  auto

## _class_ `MeetingRoomDeletedEventDetail(<auto>)` {#MeetingRoomDeletedEventDetail}

- **参数**

  auto

## _class_ `MeetingRoomDeletedEvent(<auto>)` {#MeetingRoomDeletedEvent}

- **参数**

  auto

## _class_ `MeetingRoomStatusChangedEventDetail(<auto>)` {#MeetingRoomStatusChangedEventDetail}

- **参数**

  auto

## _class_ `MeetingRoomStatusChangedEvent(<auto>)` {#MeetingRoomStatusChangedEvent}

- **参数**

  auto

## _class_ `MeetingUser(<auto>)` {#MeetingUser}

- **参数**

  auto

## _class_ `Meeting(<auto>)` {#Meeting}

- **参数**

  auto

## _class_ `VCMeetingStartedEventDetail(<auto>)` {#VCMeetingStartedEventDetail}

- **参数**

  auto

## _class_ `VCMeetingStartedEvent(<auto>)` {#VCMeetingStartedEvent}

- **参数**

  auto

## _class_ `VCMeetingEndedEventDetail(<auto>)` {#VCMeetingEndedEventDetail}

- **参数**

  auto

## _class_ `VCMeetingEndedEvent(<auto>)` {#VCMeetingEndedEvent}

- **参数**

  auto

## _class_ `VCMeetingJoinedEventDetail(<auto>)` {#VCMeetingJoinedEventDetail}

- **参数**

  auto

## _class_ `VCMeetingJoinedEvent(<auto>)` {#VCMeetingJoinedEvent}

- **参数**

  auto

## _class_ `VCMeetingLeftEventDetail(<auto>)` {#VCMeetingLeftEventDetail}

- **参数**

  auto

## _class_ `VCMeetingLeftEvent(<auto>)` {#VCMeetingLeftEvent}

- **参数**

  auto

## _class_ `VCMeetingRecordingStartedEventDetail(<auto>)` {#VCMeetingRecordingStartedEventDetail}

- **参数**

  auto

## _class_ `VCMeetingRecordingStartedEvent(<auto>)` {#VCMeetingRecordingStartedEvent}

- **参数**

  auto

## _class_ `VCMeetingRecordingEndedEventDetail(<auto>)` {#VCMeetingRecordingEndedEventDetail}

- **参数**

  auto

## _class_ `VCMeetingRecordingEndedEvent(<auto>)` {#VCMeetingRecordingEndedEvent}

- **参数**

  auto

## _class_ `VCMeetingRecordingReadyEventDetail(<auto>)` {#VCMeetingRecordingReadyEventDetail}

- **参数**

  auto

## _class_ `VCMeetingRecordingReadyEvent(<auto>)` {#VCMeetingRecordingReadyEvent}

- **参数**

  auto

## _class_ `VCMeetingShareStartedEventDetail(<auto>)` {#VCMeetingShareStartedEventDetail}

- **参数**

  auto

## _class_ `VCMeetingShareStartedEvent(<auto>)` {#VCMeetingShareStartedEvent}

- **参数**

  auto

## _class_ `VCMeetingShareEndedEventDetail(<auto>)` {#VCMeetingShareEndedEventDetail}

- **参数**

  auto

## _class_ `VCMeetingShareEndedEvent(<auto>)` {#VCMeetingShareEndedEvent}

- **参数**

  auto

## _class_ `AttendanceUserFlowCreatedEventDetail(<auto>)` {#AttendanceUserFlowCreatedEventDetail}

- **参数**

  auto

## _class_ `AttendanceUserFlowCreatedEvent(<auto>)` {#AttendanceUserFlowCreatedEvent}

- **参数**

  auto

## _class_ `AttendanceUserTaskStatusDiff(<auto>)` {#AttendanceUserTaskStatusDiff}

- **参数**

  auto

## _class_ `AttendanceUserTaskUpdatedEventDetail(<auto>)` {#AttendanceUserTaskUpdatedEventDetail}

- **参数**

  auto

## _class_ `AttendanceUserTaskUpdatedEvent(<auto>)` {#AttendanceUserTaskUpdatedEvent}

- **参数**

  auto
