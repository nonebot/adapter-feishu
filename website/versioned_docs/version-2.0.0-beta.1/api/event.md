# nonebot.adapters.feishu.event

## _class_ `EventHeader(*, event_id, event_type, create_time, token, app_id, tenant_key, resource_id=None, user_list=None)` {#EventHeader}

- **参数**

  - `event_id` (str)

  - `event_type` (str)

  - `create_time` (str)

  - `token` (str)

  - `app_id` (str)

  - `tenant_key` (str)

  - `resource_id` (str)

  - `user_list` (list[dict])

## _class_ `Event(*, schema='', header, event=None, **extra_data)` {#Event}

- **说明**

  飞书协议事件。各事件字段参考 `飞书文档`\_

  .. \_飞书文档:
  https://open.feishu.cn/document/ukTMukTMukTM/uYDNxYjL2QTM24iN0EjN/event-list

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` (Any)

  - `**extra_data` (Any)

### _method_ `get_event_description(self)` {#Event-get_event_description}

- **返回**

  - str

### _method_ `get_event_name(self)` {#Event-get_event_name}

- **返回**

  - str

### _method_ `get_message(self)` {#Event-get_message}

- **返回**

  - [Message](./message.md#Message)

### _method_ `get_plaintext(self)` {#Event-get_plaintext}

- **返回**

  - str

### _method_ `get_session_id(self)` {#Event-get_session_id}

- **返回**

  - str

### _method_ `get_type(self)` {#Event-get_type}

- **返回**

  - str

### _method_ `get_user_id(self)` {#Event-get_user_id}

- **返回**

  - str

### _method_ `is_tome(self)` {#Event-is_tome}

- **返回**

  - bool

## _class_ `UserId(*, union_id, user_id, open_id)` {#UserId}

- **参数**

  - `union_id` (str)

  - `user_id` (str)

  - `open_id` (str)

## _class_ `Sender(*, sender_id, sender_type, tenant_key)` {#Sender}

- **参数**

  - `sender_id` ([UserId](#UserId))

  - `sender_type` (str)

  - `tenant_key` (str)

## _class_ `ReplySender(*, id, id_type, sender_type, tenant_key)` {#ReplySender}

- **参数**

  - `id` (str)

  - `id_type` (str)

  - `sender_type` (str)

  - `tenant_key` (str)

## _class_ `Mention(*, key, id, name, tenant_key)` {#Mention}

- **参数**

  - `key` (str)

  - `id` ([UserId](#UserId))

  - `name` (str)

  - `tenant_key` (str)

## _class_ `ReplyMention(*, id, id_type, key, name, tenant_key)` {#ReplyMention}

- **参数**

  - `id` (str)

  - `id_type` (str)

  - `key` (str)

  - `name` (str)

  - `tenant_key` (str)

## _class_ `MessageBody(*, content)` {#MessageBody}

- **参数**

  - `content` (str)

## _class_ `Reply(*, message_id, root_id=None, parent_id=None, msg_type, create_time, update_time, deleted, updated, chat_id, sender, body, mentions, upper_message_id=None, **extra_data)` {#Reply}

- **参数**

  - `message_id` (str)

  - `root_id` (str)

  - `parent_id` (str)

  - `msg_type` (str)

  - `create_time` (str)

  - `update_time` (str)

  - `deleted` (bool)

  - `updated` (bool)

  - `chat_id` (str)

  - `sender` ([ReplySender](#ReplySender))

  - `body` ([MessageBody](#MessageBody))

  - `mentions` (list[[ReplyMention](#ReplyMention)])

  - `upper_message_id` (str)

  - `**extra_data` (Any)

## _class_ `EventMessage(*, message_id, root_id=None, parent_id=None, create_time, chat_id, chat_type, message_type, content, mentions=None)` {#EventMessage}

- **参数**

  - `message_id` (str)

  - `root_id` (str)

  - `parent_id` (str)

  - `create_time` (str)

  - `chat_id` (str)

  - `chat_type` (str)

  - `message_type` (str)

  - `content` ([Message](./message.md#Message))

  - `mentions` (list[[Mention](#Mention)])

### _classmethod_ `parse_message(cls, values)` {#EventMessage-parse_message}

- **参数**

  - `values` (dict)

- **返回**

  - Unknown

## _class_ `GroupEventMessage(*, message_id, root_id=None, parent_id=None, create_time, chat_id, chat_type, message_type, content, mentions=None)` {#GroupEventMessage}

- **参数**

  - `message_id` (str)

  - `root_id` (str)

  - `parent_id` (str)

  - `create_time` (str)

  - `chat_id` (str)

  - `chat_type` (Literal['group'])

  - `message_type` (str)

  - `content` ([Message](./message.md#Message))

  - `mentions` (list[[Mention](#Mention)])

## _class_ `PrivateEventMessage(*, message_id, root_id=None, parent_id=None, create_time, chat_id, chat_type, message_type, content, mentions=None)` {#PrivateEventMessage}

- **参数**

  - `message_id` (str)

  - `root_id` (str)

  - `parent_id` (str)

  - `create_time` (str)

  - `chat_id` (str)

  - `chat_type` (Literal['p2p'])

  - `message_type` (str)

  - `content` ([Message](./message.md#Message))

  - `mentions` (list[[Mention](#Mention)])

## _class_ `MessageEventDetail(*, sender, message)` {#MessageEventDetail}

- **参数**

  - `sender` ([Sender](#Sender))

  - `message` ([EventMessage](#EventMessage))

## _class_ `GroupMessageEventDetail(*, sender, message)` {#GroupMessageEventDetail}

- **参数**

  - `sender` ([Sender](#Sender))

  - `message` ([GroupEventMessage](#GroupEventMessage))

## _class_ `PrivateMessageEventDetail(*, sender, message)` {#PrivateMessageEventDetail}

- **参数**

  - `sender` ([Sender](#Sender))

  - `message` ([PrivateEventMessage](#PrivateEventMessage))

## _class_ `MessageEvent(*, schema='', header, event, to_me=False, reply=None, **extra_data)` {#MessageEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([MessageEventDetail](#MessageEventDetail))

  - `to_me` (bool)

  - `reply` ([Reply](#Reply))

  - `**extra_data` (Any)

### _class-var_ `to_me` {#MessageEvent-to_me}

- **类型:** bool

- **说明**

  :说明: 消息是否与机器人有关

  :类型: `bool`

### _method_ `get_all_user_id(self)` {#MessageEvent-get_all_user_id}

- **返回**

  - [UserId](#UserId)

### _method_ `get_event_description(self)` {#MessageEvent-get_event_description}

- **返回**

  - str

### _method_ `get_event_name(self)` {#MessageEvent-get_event_name}

- **返回**

  - str

### _method_ `get_message(self)` {#MessageEvent-get_message}

- **返回**

  - [Message](./message.md#Message)

### _method_ `get_plaintext(self)` {#MessageEvent-get_plaintext}

- **返回**

  - str

### _method_ `get_session_id(self)` {#MessageEvent-get_session_id}

- **返回**

  - str

### _method_ `get_type(self)` {#MessageEvent-get_type}

- **返回**

  - Literal['message', 'notice']

### _method_ `get_user_id(self)` {#MessageEvent-get_user_id}

- **返回**

  - str

### _method_ `is_tome(self)` {#MessageEvent-is_tome}

- **返回**

  - bool

## _class_ `GroupMessageEvent(*, schema='', header, event, to_me=False, reply=None, **extra_data)` {#GroupMessageEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([GroupMessageEventDetail](#GroupMessageEventDetail))

  - `to_me` (bool)

  - `reply` ([Reply](#Reply))

  - `**extra_data` (Any)

## _class_ `PrivateMessageEvent(*, schema='', header, event, to_me=False, reply=None, **extra_data)` {#PrivateMessageEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([PrivateMessageEventDetail](#PrivateMessageEventDetail))

  - `to_me` (bool)

  - `reply` ([Reply](#Reply))

  - `**extra_data` (Any)

## _class_ `NoticeEvent(*, schema='', header, event, **extra_data)` {#NoticeEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` (dict[str, Any])

  - `**extra_data` (Any)

### _method_ `get_event_description(self)` {#NoticeEvent-get_event_description}

- **返回**

  - str

### _method_ `get_event_name(self)` {#NoticeEvent-get_event_name}

- **返回**

  - str

### _method_ `get_message(self)` {#NoticeEvent-get_message}

- **返回**

  - [Message](./message.md#Message)

### _method_ `get_plaintext(self)` {#NoticeEvent-get_plaintext}

- **返回**

  - str

### _method_ `get_session_id(self)` {#NoticeEvent-get_session_id}

- **返回**

  - str

### _method_ `get_type(self)` {#NoticeEvent-get_type}

- **返回**

  - Literal['message', 'notice']

### _method_ `get_user_id(self)` {#NoticeEvent-get_user_id}

- **返回**

  - str

## _class_ `MessageReader(*, reader_id, read_time, tenant_key)` {#MessageReader}

- **参数**

  - `reader_id` ([UserId](#UserId))

  - `read_time` (str)

  - `tenant_key` (str)

## _class_ `MessageReadEventDetail(*, reader, message_id_list)` {#MessageReadEventDetail}

- **参数**

  - `reader` ([MessageReader](#MessageReader))

  - `message_id_list` (list[str])

## _class_ `MessageReadEvent(*, schema='', header, event, **extra_data)` {#MessageReadEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([MessageReadEventDetail](#MessageReadEventDetail))

  - `**extra_data` (Any)

## _class_ `GroupDisbandedEventDetail(*, chat_id, operator_id, external, operator_tenant_key)` {#GroupDisbandedEventDetail}

- **参数**

  - `chat_id` (str)

  - `operator_id` ([UserId](#UserId))

  - `external` (bool)

  - `operator_tenant_key` (str)

## _class_ `GroupDisbandedEvent(*, schema='', header, event, **extra_data)` {#GroupDisbandedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([GroupDisbandedEventDetail](#GroupDisbandedEventDetail))

  - `**extra_data` (Any)

## _class_ `I18nNames(*, zh_cn, en_us, ja_jp)` {#I18nNames}

- **参数**

  - `zh_cn` (str)

  - `en_us` (str)

  - `ja_jp` (str)

## _class_ `ChatChange(*, avatar, name, description, i18n_names, add_member_permission, share_card_permission, at_all_permission, edit_permission, membership_approval, join_message_visibility, leave_message_visibility, moderation_permission, owner_id)` {#ChatChange}

- **参数**

  - `avatar` (str)

  - `name` (str)

  - `description` (str)

  - `i18n_names` ([I18nNames](#I18nNames))

  - `add_member_permission` (str)

  - `share_card_permission` (str)

  - `at_all_permission` (str)

  - `edit_permission` (str)

  - `membership_approval` (str)

  - `join_message_visibility` (str)

  - `leave_message_visibility` (str)

  - `moderation_permission` (str)

  - `owner_id` ([UserId](#UserId))

## _class_ `EventModerator(*, tenant_key, user_id)` {#EventModerator}

- **参数**

  - `tenant_key` (str)

  - `user_id` ([UserId](#UserId))

## _class_ `ModeratorList(*, added_member_list, removed_member_list)` {#ModeratorList}

- **参数**

  - `added_member_list` ([EventModerator](#EventModerator))

  - `removed_member_list` ([EventModerator](#EventModerator))

## _class_ `GroupConfigUpdatedEventDetail(*, chat_id, operator_id, external, operator_tenant_key, after_change, before_change, moderator_list)` {#GroupConfigUpdatedEventDetail}

- **参数**

  - `chat_id` (str)

  - `operator_id` ([UserId](#UserId))

  - `external` (bool)

  - `operator_tenant_key` (str)

  - `after_change` ([ChatChange](#ChatChange))

  - `before_change` ([ChatChange](#ChatChange))

  - `moderator_list` ([ModeratorList](#ModeratorList))

## _class_ `GroupConfigUpdatedEvent(*, schema='', header, event, **extra_data)` {#GroupConfigUpdatedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([GroupConfigUpdatedEventDetail](#GroupConfigUpdatedEventDetail))

  - `**extra_data` (Any)

## _class_ `GroupMemberBotAddedEventDetail(*, chat_id, operator_id, external, operator_tenant_key)` {#GroupMemberBotAddedEventDetail}

- **参数**

  - `chat_id` (str)

  - `operator_id` ([UserId](#UserId))

  - `external` (bool)

  - `operator_tenant_key` (str)

## _class_ `GroupMemberBotAddedEvent(*, schema='', header, event, **extra_data)` {#GroupMemberBotAddedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([GroupMemberBotAddedEventDetail](#GroupMemberBotAddedEventDetail))

  - `**extra_data` (Any)

## _class_ `GroupMemberBotDeletedEventDetail(*, chat_id, operator_id, external, operator_tenant_key)` {#GroupMemberBotDeletedEventDetail}

- **参数**

  - `chat_id` (str)

  - `operator_id` ([UserId](#UserId))

  - `external` (bool)

  - `operator_tenant_key` (str)

## _class_ `GroupMemberBotDeletedEvent(*, schema='', header, event, **extra_data)` {#GroupMemberBotDeletedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([GroupMemberBotDeletedEventDetail](#GroupMemberBotDeletedEventDetail))

  - `**extra_data` (Any)

## _class_ `ChatMemberUser(*, name, tenant_key, user_id)` {#ChatMemberUser}

- **参数**

  - `name` (str)

  - `tenant_key` (str)

  - `user_id` ([UserId](#UserId))

## _class_ `GroupMemberUserAddedEventDetail(*, chat_id, operator_id, external, operator_tenant_key, users)` {#GroupMemberUserAddedEventDetail}

- **参数**

  - `chat_id` (str)

  - `operator_id` ([UserId](#UserId))

  - `external` (bool)

  - `operator_tenant_key` (str)

  - `users` (list[[ChatMemberUser](#ChatMemberUser)])

## _class_ `GroupMemberUserAddedEvent(*, schema='', header, event, **extra_data)` {#GroupMemberUserAddedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([GroupMemberUserAddedEventDetail](#GroupMemberUserAddedEventDetail))

  - `**extra_data` (Any)

## _class_ `GroupMemberUserWithdrawnEventDetail(*, chat_id, operator_id, external, operator_tenant_key, users)` {#GroupMemberUserWithdrawnEventDetail}

- **参数**

  - `chat_id` (str)

  - `operator_id` ([UserId](#UserId))

  - `external` (bool)

  - `operator_tenant_key` (str)

  - `users` (list[[ChatMemberUser](#ChatMemberUser)])

## _class_ `GroupMemberUserWithdrawnEvent(*, schema='', header, event, **extra_data)` {#GroupMemberUserWithdrawnEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([GroupMemberUserWithdrawnEventDetail](#GroupMemberUserWithdrawnEventDetail))

  - `**extra_data` (Any)

## _class_ `GroupMemberUserDeletedEventDetail(*, chat_id, operator_id, external, operator_tenant_key, users)` {#GroupMemberUserDeletedEventDetail}

- **参数**

  - `chat_id` (str)

  - `operator_id` ([UserId](#UserId))

  - `external` (bool)

  - `operator_tenant_key` (str)

  - `users` (list[[ChatMemberUser](#ChatMemberUser)])

## _class_ `GroupMemberUserDeletedEvent(*, schema='', header, event, **extra_data)` {#GroupMemberUserDeletedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([GroupMemberUserDeletedEventDetail](#GroupMemberUserDeletedEventDetail))

  - `**extra_data` (Any)

## _class_ `AvatarInfo(*, avatar_72, avatar_240, avatar_640, avatar_origin)` {#AvatarInfo}

- **参数**

  - `avatar_72` (str)

  - `avatar_240` (str)

  - `avatar_640` (str)

  - `avatar_origin` (str)

## _class_ `UserStatus(*, is_frozen, is_resigned, is_activated)` {#UserStatus}

- **参数**

  - `is_frozen` (bool)

  - `is_resigned` (bool)

  - `is_activated` (bool)

## _class_ `UserOrder(*, department_id, user_order, department_order)` {#UserOrder}

- **参数**

  - `department_id` (str)

  - `user_order` (int)

  - `department_order` (int)

## _class_ `UserCustomAttrValue(*, text, url, pc_url)` {#UserCustomAttrValue}

- **参数**

  - `text` (str)

  - `url` (str)

  - `pc_url` (str)

## _class_ `UserCustomAttr(*, type, id, value)` {#UserCustomAttr}

- **参数**

  - `type` (str)

  - `id` (str)

  - `value` ([UserCustomAttrValue](#UserCustomAttrValue))

## _class_ `ContactUser(*, open_id, user_id, name, en_name, email, mobile, gender, avatar, status, department_ids=None, leader_user_id, city, country, work_station, join_time, employee_no, employee_type, orders=None, custom_attrs)` {#ContactUser}

- **参数**

  - `open_id` (str)

  - `user_id` (str)

  - `name` (str)

  - `en_name` (str)

  - `email` (str)

  - `mobile` (str)

  - `gender` (int)

  - `avatar` ([AvatarInfo](#AvatarInfo))

  - `status` ([UserStatus](#UserStatus))

  - `department_ids` (list[str])

  - `leader_user_id` (str)

  - `city` (str)

  - `country` (str)

  - `work_station` (str)

  - `join_time` (int)

  - `employee_no` (str)

  - `employee_type` (int)

  - `orders` (list[[UserOrder](#UserOrder)])

  - `custom_attrs` (list[[UserCustomAttr](#UserCustomAttr)])

## _class_ `OldContactUser(*, department_ids, open_id)` {#OldContactUser}

- **参数**

  - `department_ids` (list[str])

  - `open_id` (str)

## _class_ `ContactUserUpdatedEventDetail(*, object, old_object)` {#ContactUserUpdatedEventDetail}

- **参数**

  - `object` ([ContactUser](#ContactUser))

  - `old_object` ([ContactUser](#ContactUser))

## _class_ `ContactUserUpdatedEvent(*, schema='', header, event, **extra_data)` {#ContactUserUpdatedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([ContactUserUpdatedEventDetail](#ContactUserUpdatedEventDetail))

  - `**extra_data` (Any)

## _class_ `ContactUserDeletedEventDetail(*, schema='', header, event, object, old_object, **extra_data)` {#ContactUserDeletedEventDetail}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` (dict[str, Any])

  - `object` ([ContactUser](#ContactUser))

  - `old_object` ([OldContactUser](#OldContactUser))

  - `**extra_data` (Any)

## _class_ `ContactUserDeletedEvent(*, schema='', header, event, **extra_data)` {#ContactUserDeletedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([ContactUserDeletedEventDetail](#ContactUserDeletedEventDetail))

  - `**extra_data` (Any)

## _class_ `ContactUserCreatedEventDetail(*, object)` {#ContactUserCreatedEventDetail}

- **参数**

  - `object` ([ContactUser](#ContactUser))

## _class_ `ContactUserCreatedEvent(*, schema='', header, event, **extra_data)` {#ContactUserCreatedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([ContactUserCreatedEventDetail](#ContactUserCreatedEventDetail))

  - `**extra_data` (Any)

## _class_ `ContactDepartmentStatus(*, is_deleted)` {#ContactDepartmentStatus}

- **参数**

  - `is_deleted` (bool)

## _class_ `ContactDepartment(*, name, parent_department_id, department_id, open_department_id, leader_user_id, chat_id, order, status)` {#ContactDepartment}

- **参数**

  - `name` (str)

  - `parent_department_id` (str)

  - `department_id` (str)

  - `open_department_id` (str)

  - `leader_user_id` (str)

  - `chat_id` (str)

  - `order` (int)

  - `status` ([ContactDepartmentStatus](#ContactDepartmentStatus))

## _class_ `ContactDepartmentUpdatedEventDetail(*, object, old_object)` {#ContactDepartmentUpdatedEventDetail}

- **参数**

  - `object` ([ContactDepartment](#ContactDepartment))

  - `old_object` ([ContactDepartment](#ContactDepartment))

## _class_ `ContactDepartmentUpdatedEvent(*, schema='', header, event, **extra_data)` {#ContactDepartmentUpdatedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([ContactDepartmentUpdatedEventDetail](#ContactDepartmentUpdatedEventDetail))

  - `**extra_data` (Any)

## _class_ `OldContactDepartment(*, status, open_department_id)` {#OldContactDepartment}

- **参数**

  - `status` ([ContactDepartmentStatus](#ContactDepartmentStatus))

  - `open_department_id` (str)

## _class_ `ContactDepartmentDeletedEventDetail(*, schema='', header, event, object, old_object, **extra_data)` {#ContactDepartmentDeletedEventDetail}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` (dict[str, Any])

  - `object` ([ContactDepartment](#ContactDepartment))

  - `old_object` ([OldContactDepartment](#OldContactDepartment))

  - `**extra_data` (Any)

## _class_ `ContactDepartmentDeletedEvent(*, schema='', header, event, **extra_data)` {#ContactDepartmentDeletedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([ContactDepartmentDeletedEventDetail](#ContactDepartmentDeletedEventDetail))

  - `**extra_data` (Any)

## _class_ `ContactDepartmentCreatedEventDetail(*, object)` {#ContactDepartmentCreatedEventDetail}

- **参数**

  - `object` ([ContactDepartment](#ContactDepartment))

## _class_ `ContactDepartmentCreatedEvent(*, schema='', header, event, **extra_data)` {#ContactDepartmentCreatedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([ContactDepartmentCreatedEventDetail](#ContactDepartmentCreatedEventDetail))

  - `**extra_data` (Any)

## _class_ `CalendarAclScope(*, type, user_id)` {#CalendarAclScope}

- **参数**

  - `type` (str)

  - `user_id` (str)

## _class_ `CalendarAclCreatedEventDetail(*, acl_id, role, scope)` {#CalendarAclCreatedEventDetail}

- **参数**

  - `acl_id` (str)

  - `role` (str)

  - `scope` ([CalendarAclScope](#CalendarAclScope))

## _class_ `CalendarAclCreatedEvent(*, schema='', header, event, **extra_data)` {#CalendarAclCreatedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([CalendarAclCreatedEventDetail](#CalendarAclCreatedEventDetail))

  - `**extra_data` (Any)

## _class_ `CalendarAclDeletedEventDetail(*, acl_id, role, scope)` {#CalendarAclDeletedEventDetail}

- **参数**

  - `acl_id` (str)

  - `role` (str)

  - `scope` ([CalendarAclScope](#CalendarAclScope))

## _class_ `CalendarAclDeletedEvent(*, schema='', header, event, **extra_data)` {#CalendarAclDeletedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([CalendarAclDeletedEventDetail](#CalendarAclDeletedEventDetail))

  - `**extra_data` (Any)

## _class_ `CalendarChangedEvent(*, schema='', header, event, **extra_data)` {#CalendarChangedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` (dict)

  - `**extra_data` (Any)

## _class_ `CalendarEventChangedEventDetail(*, calendar_id)` {#CalendarEventChangedEventDetail}

- **参数**

  - `calendar_id` (str)

## _class_ `CalendarEventChangedEvent(*, schema='', header, event, **extra_data)` {#CalendarEventChangedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([CalendarEventChangedEventDetail](#CalendarEventChangedEventDetail))

  - `**extra_data` (Any)

## _class_ `DriveFileReadEventDetail(*, file_token, file_type, operator_id_list)` {#DriveFileReadEventDetail}

- **参数**

  - `file_token` (str)

  - `file_type` (str)

  - `operator_id_list` (list[[UserId](#UserId)])

## _class_ `DriveFileReadEvent(*, schema='', header, event, **extra_data)` {#DriveFileReadEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([DriveFileReadEventDetail](#DriveFileReadEventDetail))

  - `**extra_data` (Any)

## _class_ `DriveFileTitleUpdatedEventDetail(*, file_token, file_type, operator_id)` {#DriveFileTitleUpdatedEventDetail}

- **参数**

  - `file_token` (str)

  - `file_type` (str)

  - `operator_id` ([UserId](#UserId))

## _class_ `DriveFileTitleUpdatedEvent(*, schema='', header, event, **extra_data)` {#DriveFileTitleUpdatedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([DriveFileTitleUpdatedEventDetail](#DriveFileTitleUpdatedEventDetail))

  - `**extra_data` (Any)

## _class_ `DriveFilePermissionMemberAddedEventDetail(*, chat_list, file_token, file_type, operator_id, user_list)` {#DriveFilePermissionMemberAddedEventDetail}

- **参数**

  - `chat_list` (list[str])

  - `file_token` (str)

  - `file_type` (str)

  - `operator_id` ([UserId](#UserId))

  - `user_list` (list[[UserId](#UserId)])

## _class_ `DriveFilePermissionMemberAddedEvent(*, schema='', header, event, **extra_data)` {#DriveFilePermissionMemberAddedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([DriveFilePermissionMemberAddedEventDetail](#DriveFilePermissionMemberAddedEventDetail))

  - `**extra_data` (Any)

## _class_ `DriveFilePermissionMemberRemovedEventDetail(*, chat_list, file_token, file_type, operator_id, user_list)` {#DriveFilePermissionMemberRemovedEventDetail}

- **参数**

  - `chat_list` (list[str])

  - `file_token` (str)

  - `file_type` (str)

  - `operator_id` ([UserId](#UserId))

  - `user_list` (list[[UserId](#UserId)])

## _class_ `DriveFilePermissionMemberRemovedEvent(*, schema='', header, event, **extra_data)` {#DriveFilePermissionMemberRemovedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([DriveFilePermissionMemberRemovedEventDetail](#DriveFilePermissionMemberRemovedEventDetail))

  - `**extra_data` (Any)

## _class_ `DriveFileTrashedEventDetail(*, file_token, file_type, operator_id)` {#DriveFileTrashedEventDetail}

- **参数**

  - `file_token` (str)

  - `file_type` (str)

  - `operator_id` ([UserId](#UserId))

## _class_ `DriveFileTrashedEvent(*, schema='', header, event, **extra_data)` {#DriveFileTrashedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([DriveFileTrashedEventDetail](#DriveFileTrashedEventDetail))

  - `**extra_data` (Any)

## _class_ `DriveFileDeletedEventDetail(*, file_token, file_type, operator_id)` {#DriveFileDeletedEventDetail}

- **参数**

  - `file_token` (str)

  - `file_type` (str)

  - `operator_id` ([UserId](#UserId))

## _class_ `DriveFileDeletedEvent(*, schema='', header, event, **extra_data)` {#DriveFileDeletedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([DriveFileDeletedEventDetail](#DriveFileDeletedEventDetail))

  - `**extra_data` (Any)

## _class_ `DriveFileEditedEventDetail(*, file_token, file_type, operator_id_list, subscriber_id_list)` {#DriveFileEditedEventDetail}

- **参数**

  - `file_token` (str)

  - `file_type` (str)

  - `operator_id_list` (list[[UserId](#UserId)])

  - `subscriber_id_list` (list[[UserId](#UserId)])

## _class_ `DriveFileEditedEvent(*, schema='', header, event, **extra_data)` {#DriveFileEditedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([DriveFileEditedEventDetail](#DriveFileEditedEventDetail))

  - `**extra_data` (Any)

## _class_ `MeetingRoomCreatedEventDetail(*, room_id, room_name)` {#MeetingRoomCreatedEventDetail}

- **参数**

  - `room_id` (str)

  - `room_name` (str)

## _class_ `MeetingRoomCreatedEvent(*, schema='', header, event, **extra_data)` {#MeetingRoomCreatedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([MeetingRoomCreatedEventDetail](#MeetingRoomCreatedEventDetail))

  - `**extra_data` (Any)

## _class_ `MeetingRoomUpdatedEventDetail(*, room_id, room_name)` {#MeetingRoomUpdatedEventDetail}

- **参数**

  - `room_id` (str)

  - `room_name` (str)

## _class_ `MeetingRoomUpdatedEvent(*, schema='', header, event, **extra_data)` {#MeetingRoomUpdatedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([MeetingRoomUpdatedEventDetail](#MeetingRoomUpdatedEventDetail))

  - `**extra_data` (Any)

## _class_ `MeetingRoomDeletedEventDetail(*, room_id, room_name)` {#MeetingRoomDeletedEventDetail}

- **参数**

  - `room_id` (str)

  - `room_name` (str)

## _class_ `MeetingRoomDeletedEvent(*, schema='', header, event, **extra_data)` {#MeetingRoomDeletedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([MeetingRoomDeletedEventDetail](#MeetingRoomDeletedEventDetail))

  - `**extra_data` (Any)

## _class_ `MeetingRoomStatusChangedEventDetail(*, room_id, room_name)` {#MeetingRoomStatusChangedEventDetail}

- **参数**

  - `room_id` (str)

  - `room_name` (str)

## _class_ `MeetingRoomStatusChangedEvent(*, schema='', header, event, **extra_data)` {#MeetingRoomStatusChangedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([MeetingRoomStatusChangedEventDetail](#MeetingRoomStatusChangedEventDetail))

  - `**extra_data` (Any)

## _class_ `MeetingUser(*, id, user_role=None, user_type=None)` {#MeetingUser}

- **参数**

  - `id` ([UserId](#UserId))

  - `user_role` (int)

  - `user_type` (int)

## _class_ `Meeting(*, id, topic, meeting_no, start_time=None, end_time=None, host_user=None, owner)` {#Meeting}

- **参数**

  - `id` (str)

  - `topic` (str)

  - `meeting_no` (str)

  - `start_time` (str)

  - `end_time` (str)

  - `host_user` ([MeetingUser](#MeetingUser))

  - `owner` ([MeetingUser](#MeetingUser))

## _class_ `VCMeetingStartedEventDetail(*, meeting, operator)` {#VCMeetingStartedEventDetail}

- **参数**

  - `meeting` ([Meeting](#Meeting))

  - `operator` ([MeetingUser](#MeetingUser))

## _class_ `VCMeetingStartedEvent(*, schema='', header, event, **extra_data)` {#VCMeetingStartedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([VCMeetingStartedEventDetail](#VCMeetingStartedEventDetail))

  - `**extra_data` (Any)

## _class_ `VCMeetingEndedEventDetail(*, meeting, operator)` {#VCMeetingEndedEventDetail}

- **参数**

  - `meeting` ([Meeting](#Meeting))

  - `operator` ([MeetingUser](#MeetingUser))

## _class_ `VCMeetingEndedEvent(*, schema='', header, event, **extra_data)` {#VCMeetingEndedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([VCMeetingEndedEventDetail](#VCMeetingEndedEventDetail))

  - `**extra_data` (Any)

## _class_ `VCMeetingJoinedEventDetail(*, meeting, operator)` {#VCMeetingJoinedEventDetail}

- **参数**

  - `meeting` ([Meeting](#Meeting))

  - `operator` ([MeetingUser](#MeetingUser))

## _class_ `VCMeetingJoinedEvent(*, schema='', header, event, **extra_data)` {#VCMeetingJoinedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([VCMeetingJoinedEventDetail](#VCMeetingJoinedEventDetail))

  - `**extra_data` (Any)

## _class_ `VCMeetingLeftEventDetail(*, meeting, operator, leave_reason)` {#VCMeetingLeftEventDetail}

- **参数**

  - `meeting` ([Meeting](#Meeting))

  - `operator` ([MeetingUser](#MeetingUser))

  - `leave_reason` (int)

## _class_ `VCMeetingLeftEvent(*, schema='', header, event, **extra_data)` {#VCMeetingLeftEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([VCMeetingLeftEventDetail](#VCMeetingLeftEventDetail))

  - `**extra_data` (Any)

## _class_ `VCMeetingRecordingStartedEventDetail(*, meeting, operator)` {#VCMeetingRecordingStartedEventDetail}

- **参数**

  - `meeting` ([Meeting](#Meeting))

  - `operator` ([MeetingUser](#MeetingUser))

## _class_ `VCMeetingRecordingStartedEvent(*, schema='', header, event, **extra_data)` {#VCMeetingRecordingStartedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([VCMeetingRecordingStartedEventDetail](#VCMeetingRecordingStartedEventDetail))

  - `**extra_data` (Any)

## _class_ `VCMeetingRecordingEndedEventDetail(*, meeting, operator)` {#VCMeetingRecordingEndedEventDetail}

- **参数**

  - `meeting` ([Meeting](#Meeting))

  - `operator` ([MeetingUser](#MeetingUser))

## _class_ `VCMeetingRecordingEndedEvent(*, schema='', header, event, **extra_data)` {#VCMeetingRecordingEndedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([VCMeetingRecordingEndedEventDetail](#VCMeetingRecordingEndedEventDetail))

  - `**extra_data` (Any)

## _class_ `VCMeetingRecordingReadyEventDetail(*, meeting, url, duration)` {#VCMeetingRecordingReadyEventDetail}

- **参数**

  - `meeting` ([Meeting](#Meeting))

  - `url` (str)

  - `duration` (str)

## _class_ `VCMeetingRecordingReadyEvent(*, schema='', header, event, **extra_data)` {#VCMeetingRecordingReadyEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([VCMeetingRecordingReadyEventDetail](#VCMeetingRecordingReadyEventDetail))

  - `**extra_data` (Any)

## _class_ `VCMeetingShareStartedEventDetail(*, meeting, operator)` {#VCMeetingShareStartedEventDetail}

- **参数**

  - `meeting` ([Meeting](#Meeting))

  - `operator` ([MeetingUser](#MeetingUser))

## _class_ `VCMeetingShareStartedEvent(*, schema='', header, event, **extra_data)` {#VCMeetingShareStartedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([VCMeetingShareStartedEventDetail](#VCMeetingShareStartedEventDetail))

  - `**extra_data` (Any)

## _class_ `VCMeetingShareEndedEventDetail(*, meeting, operator)` {#VCMeetingShareEndedEventDetail}

- **参数**

  - `meeting` ([Meeting](#Meeting))

  - `operator` ([MeetingUser](#MeetingUser))

## _class_ `VCMeetingShareEndedEvent(*, schema='', header, event, **extra_data)` {#VCMeetingShareEndedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([VCMeetingShareEndedEventDetail](#VCMeetingShareEndedEventDetail))

  - `**extra_data` (Any)

## _class_ `AttendanceUserFlowCreatedEventDetail(*, bssid, check_time, comment, employee_id, employee_no, is_field, is_wifi, latitude, location_name, longitude, photo_urls=None, record_id, ssid, type)` {#AttendanceUserFlowCreatedEventDetail}

- **参数**

  - `bssid` (str)

  - `check_time` (str)

  - `comment` (str)

  - `employee_id` (str)

  - `employee_no` (str)

  - `is_field` (bool)

  - `is_wifi` (bool)

  - `latitude` (float)

  - `location_name` (str)

  - `longitude` (float)

  - `photo_urls` (list[str])

  - `record_id` (str)

  - `ssid` (str)

  - `type` (int)

## _class_ `AttendanceUserFlowCreatedEvent(*, schema='', header, event, **extra_data)` {#AttendanceUserFlowCreatedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([AttendanceUserFlowCreatedEventDetail](#AttendanceUserFlowCreatedEventDetail))

  - `**extra_data` (Any)

## _class_ `AttendanceUserTaskStatusDiff(*, before_status, before_supplement, current_status, current_supplement, index, work_type)` {#AttendanceUserTaskStatusDiff}

- **参数**

  - `before_status` (str)

  - `before_supplement` (str)

  - `current_status` (str)

  - `current_supplement` (str)

  - `index` (int)

  - `work_type` (str)

## _class_ `AttendanceUserTaskUpdatedEventDetail(*, date, employee_id, employee_no, group_id, shift_id, status_changes, task_id, time_zone)` {#AttendanceUserTaskUpdatedEventDetail}

- **参数**

  - `date` (int)

  - `employee_id` (str)

  - `employee_no` (str)

  - `group_id` (str)

  - `shift_id` (str)

  - `status_changes` (list[[AttendanceUserTaskStatusDiff](#AttendanceUserTaskStatusDiff)])

  - `task_id` (str)

  - `time_zone` (str)

## _class_ `AttendanceUserTaskUpdatedEvent(*, schema='', header, event, **extra_data)` {#AttendanceUserTaskUpdatedEvent}

- **参数**

  - `schema` (str)

  - `header` ([EventHeader](#EventHeader))

  - `event` ([AttendanceUserTaskUpdatedEventDetail](#AttendanceUserTaskUpdatedEventDetail))

  - `**extra_data` (Any)
