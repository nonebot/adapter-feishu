from typing import Literal, Optional

from pydantic import BaseModel

from nonebot.compat import PYDANTIC_V2, ConfigDict


class EventHeader(BaseModel):
    event_id: str
    event_type: str
    create_time: str
    token: str
    app_id: str
    tenant_key: str
    resource_id: Optional[str] = None
    user_list: Optional[list[dict]] = None

    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config(ConfigDict):
            extra = "allow"


class UserId(BaseModel):
    union_id: str
    user_id: str
    open_id: str


class MeetingUser(BaseModel):
    id: UserId
    user_role: Optional[int] = None
    user_type: Optional[int] = None


class Meeting(BaseModel):
    id: str
    topic: str
    meeting_no: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    host_user: Optional[MeetingUser] = None
    owner: MeetingUser


class VCMeetingRecordingReadyEventDetail(BaseModel):
    meeting: Meeting
    url: str
    duration: str


class VCMeetingRecordingEndedEventDetail(BaseModel):
    meeting: Meeting
    operator: MeetingUser


class VCMeetingRecordingStartedEventDetail(BaseModel):
    meeting: Meeting
    operator: MeetingUser


class VCMeetingLeftEventDetail(BaseModel):
    meeting: Meeting
    operator: MeetingUser
    leave_reason: int


class VCMeetingJoinedEventDetail(BaseModel):
    meeting: Meeting
    operator: MeetingUser


class VCMeetingEndedEventDetail(BaseModel):
    meeting: Meeting
    operator: MeetingUser


class Sender(BaseModel):
    sender_id: UserId
    sender_type: str
    tenant_key: str


class ReplySender(BaseModel):
    id: str
    id_type: str
    sender_type: str
    tenant_key: str


class Mention(BaseModel):
    key: str
    id: UserId
    name: str
    tenant_key: str


class ReplyMention(BaseModel):
    id: str
    id_type: str
    key: str
    name: str
    tenant_key: str


class MessageBody(BaseModel):
    content: str


class Reply(BaseModel):
    message_id: str
    root_id: Optional[str] = None
    parent_id: Optional[str] = None
    thread_id: Optional[str] = None
    msg_type: str
    create_time: str
    update_time: str
    deleted: bool
    updated: bool
    chat_id: str
    sender: ReplySender
    body: MessageBody
    mentions: list[ReplyMention] = []
    upper_message_id: Optional[str] = None

    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config(ConfigDict):
            extra = "allow"


class EventMessage(BaseModel):
    message_id: str
    root_id: Optional[str] = None
    parent_id: Optional[str] = None
    create_time: str
    chat_id: str
    chat_type: str
    message_type: str
    content: str
    mentions: Optional[list[Mention]] = None

    if PYDANTIC_V2:
        model_config = ConfigDict(extra="allow")
    else:

        class Config(ConfigDict):
            extra = "allow"


class GroupEventMessage(EventMessage):
    chat_type: Literal["group"]


class PrivateEventMessage(EventMessage):
    chat_type: Literal["p2p"]


class MessageEventDetail(BaseModel):
    sender: Sender
    message: EventMessage


class GroupMessageEventDetail(MessageEventDetail):
    message: GroupEventMessage


class PrivateMessageEventDetail(MessageEventDetail):
    message: PrivateEventMessage


class VCMeetingShareStartedEventDetail(BaseModel):
    meeting: Meeting
    operator: MeetingUser


class VCMeetingShareEndedEventDetail(BaseModel):
    meeting: Meeting
    operator: MeetingUser


class AttendanceUserFlowCreatedEventDetail(BaseModel):
    bssid: str
    check_time: str
    comment: str
    employee_id: str
    employee_no: str
    is_field: bool
    is_wifi: bool
    latitude: float
    location_name: str
    longitude: float
    photo_urls: Optional[list[str]] = None
    record_id: str
    ssid: str
    type: int


class AttendanceUserTaskStatusDiff(BaseModel):
    before_status: str
    before_supplement: str
    current_status: str
    current_supplement: str
    index: int
    work_type: str


class AttendanceUserTaskUpdatedEventDetail(BaseModel):
    date: int
    employee_id: str
    employee_no: str
    group_id: str
    shift_id: str
    status_changes: list[AttendanceUserTaskStatusDiff]
    task_id: str
    time_zone: str


class VCMeetingStartedEventDetail(BaseModel):
    meeting: Meeting
    operator: MeetingUser


class MeetingRoomStatusChangedEventDetail(BaseModel):
    room_id: str
    room_name: str


class MeetingRoomDeletedEventDetail(BaseModel):
    room_id: str
    room_name: str


class MeetingRoomUpdatedEventDetail(BaseModel):
    room_id: str
    room_name: str


class MeetingRoomCreatedEventDetail(BaseModel):
    room_id: str
    room_name: str


class DriveFileEditedEventDetail(BaseModel):
    file_token: str
    file_type: str
    operator_id_list: list[UserId]
    subscriber_id_list: list[UserId]


class DriveFileDeletedEventDetail(BaseModel):
    file_token: str
    file_type: str
    operator_id: UserId


class DriveFileTrashedEventDetail(BaseModel):
    file_token: str
    file_type: str
    operator_id: UserId


class DriveFilePermissionMemberRemovedEventDetail(BaseModel):
    chat_list: list[str]
    file_token: str
    file_type: str
    operator_id: UserId
    user_list: list[UserId]


class DriveFilePermissionMemberAddedEventDetail(BaseModel):
    chat_list: list[str]
    file_token: str
    file_type: str
    operator_id: UserId
    user_list: list[UserId]


class DriveFileTitleUpdatedEventDetail(BaseModel):
    file_token: str
    file_type: str
    operator_id: UserId


class DriveFileReadEventDetail(BaseModel):
    file_token: str
    file_type: str
    operator_id_list: list[UserId]


class CalendarEventChangedEventDetail(BaseModel):
    calendar_id: str


class CalendarAclScope(BaseModel):
    type: str
    user_id: str


class CalendarAclDeletedEventDetail(BaseModel):
    acl_id: str
    role: str
    scope: CalendarAclScope


class CalendarAclCreatedEventDetail(BaseModel):
    acl_id: str
    role: str
    scope: CalendarAclScope


class ContactDepartmentStatus(BaseModel):
    is_deleted: bool


class ContactDepartment(BaseModel):
    name: str
    parent_department_id: str
    department_id: str
    open_department_id: str
    leader_user_id: str
    chat_id: str
    order: int
    status: ContactDepartmentStatus


class ContactDepartmentCreatedEventDetail(BaseModel):
    object: ContactDepartment


class OldContactDepartment(BaseModel):
    status: ContactDepartmentStatus
    open_department_id: str


class ContactDepartmentDeletedEventDetail(BaseModel):
    object: ContactDepartment
    old_object: OldContactDepartment


class ContactDepartmentUpdatedEventDetail(BaseModel):
    object: ContactDepartment
    old_object: ContactDepartment


class AvatarInfo(BaseModel):
    avatar_72: str
    avatar_240: str
    avatar_640: str
    avatar_origin: str


class UserStatus(BaseModel):
    is_frozen: bool
    is_resigned: bool
    is_activated: bool


class UserOrder(BaseModel):
    department_id: str
    user_order: int
    department_order: int


class UserCustomAttrValue(BaseModel):
    text: str
    url: str
    pc_url: str


class UserCustomAttr(BaseModel):
    type: str
    id: str
    value: UserCustomAttrValue


class ContactUser(BaseModel):
    open_id: str
    user_id: str
    name: str
    en_name: str
    email: str
    mobile: str
    gender: int
    avatar: AvatarInfo
    status: UserStatus
    department_ids: Optional[list[str]] = None
    leader_user_id: str
    city: str
    country: str
    work_station: str
    join_time: int
    employee_no: str
    employee_type: int
    orders: Optional[list[UserOrder]] = None
    custom_attrs: list[UserCustomAttr]


class OldContactUser(BaseModel):
    department_ids: list[str]
    open_id: str


class ContactUserCreatedEventDetail(BaseModel):
    object: ContactUser


class ContactUserDeletedEventDetail(BaseModel):
    object: ContactUser
    old_object: OldContactUser


class ContactUserUpdatedEventDetail(BaseModel):
    object: ContactUser
    old_object: ContactUser


class ChatMemberUser(BaseModel):
    name: str
    tenant_key: str
    user_id: UserId


class GroupMemberUserDeletedEventDetail(BaseModel):
    chat_id: str
    operator_id: UserId
    external: bool
    operator_tenant_key: str
    users: list[ChatMemberUser]


class GroupMemberUserWithdrawnEventDetail(BaseModel):
    chat_id: str
    operator_id: UserId
    external: bool
    operator_tenant_key: str
    users: list[ChatMemberUser]


class GroupMemberUserAddedEventDetail(BaseModel):
    chat_id: str
    operator_id: UserId
    external: bool
    operator_tenant_key: str
    users: list[ChatMemberUser]


class GroupMemberBotDeletedEventDetail(BaseModel):
    chat_id: str
    operator_id: UserId
    external: bool
    operator_tenant_key: str


class GroupMemberBotAddedEventDetail(BaseModel):
    chat_id: str
    operator_id: UserId
    external: bool
    operator_tenant_key: str


class I18nNames(BaseModel):
    zh_cn: str
    en_us: str
    ja_jp: str


class Emoji(BaseModel):
    emoji_type: str


class ChatChange(BaseModel):
    avatar: str
    name: str
    description: str
    i18n_names: I18nNames
    add_member_permission: str
    share_card_permission: str
    at_all_permission: str
    edit_permission: str
    membership_approval: str
    join_message_visibility: str
    leave_message_visibility: str
    moderation_permission: str
    owner_id: UserId


class EventModerator(BaseModel):
    tenant_key: str
    user_id: UserId


class ModeratorList(BaseModel):
    added_member_list: EventModerator
    removed_member_list: EventModerator


class GroupConfigUpdatedEventDetail(BaseModel):
    chat_id: str
    operator_id: UserId
    external: bool
    operator_tenant_key: str
    after_change: ChatChange
    before_change: ChatChange
    moderator_list: ModeratorList


class MessageReactionCreatedEventDetail(BaseModel):
    message_id: str
    reaction_type: Emoji
    operator_type: str
    user_id: UserId
    action_time: str


class MessageReactionDeletedEventDetail(BaseModel):
    message_id: str
    reaction_type: Emoji
    operator_type: str
    user_id: UserId
    action_time: str


class GroupDisbandedEventDetail(BaseModel):
    chat_id: str
    operator_id: UserId
    external: bool
    operator_tenant_key: str


class MessageReader(BaseModel):
    reader_id: UserId
    read_time: str
    tenant_key: str


class MessageReadEventDetail(BaseModel):
    reader: MessageReader
    message_id_list: list[str]


__all__ = [
    "AttendanceUserFlowCreatedEventDetail",
    "AttendanceUserTaskStatusDiff",
    "AttendanceUserTaskUpdatedEventDetail",
    "AvatarInfo",
    "CalendarAclCreatedEventDetail",
    "CalendarAclDeletedEventDetail",
    "CalendarAclScope",
    "CalendarEventChangedEventDetail",
    "ChatChange",
    "ChatMemberUser",
    "ContactDepartment",
    "ContactDepartmentCreatedEventDetail",
    "ContactDepartmentDeletedEventDetail",
    "ContactDepartmentStatus",
    "ContactDepartmentUpdatedEventDetail",
    "ContactUser",
    "ContactUserCreatedEventDetail",
    "ContactUserDeletedEventDetail",
    "ContactUserUpdatedEventDetail",
    "DriveFileDeletedEventDetail",
    "DriveFileEditedEventDetail",
    "DriveFilePermissionMemberAddedEventDetail",
    "DriveFilePermissionMemberRemovedEventDetail",
    "DriveFileReadEventDetail",
    "DriveFileTitleUpdatedEventDetail",
    "DriveFileTrashedEventDetail",
    "Emoji",
    "EventHeader",
    "EventMessage",
    "EventModerator",
    "GroupConfigUpdatedEventDetail",
    "GroupDisbandedEventDetail",
    "GroupEventMessage",
    "GroupMemberBotAddedEventDetail",
    "GroupMemberBotDeletedEventDetail",
    "GroupMemberUserAddedEventDetail",
    "GroupMemberUserDeletedEventDetail",
    "GroupMemberUserWithdrawnEventDetail",
    "GroupMessageEventDetail",
    "I18nNames",
    "Meeting",
    "MeetingRoomCreatedEventDetail",
    "MeetingRoomDeletedEventDetail",
    "MeetingRoomStatusChangedEventDetail",
    "MeetingRoomUpdatedEventDetail",
    "MeetingUser",
    "Mention",
    "MessageBody",
    "MessageEventDetail",
    "MessageReactionCreatedEventDetail",
    "MessageReactionDeletedEventDetail",
    "MessageReadEventDetail",
    "MessageReader",
    "ModeratorList",
    "OldContactDepartment",
    "OldContactUser",
    "PrivateEventMessage",
    "PrivateMessageEventDetail",
    "Reply",
    "ReplyMention",
    "ReplySender",
    "Sender",
    "UserCustomAttr",
    "UserCustomAttrValue",
    "UserId",
    "UserOrder",
    "UserStatus",
    "VCMeetingEndedEventDetail",
    "VCMeetingJoinedEventDetail",
    "VCMeetingLeftEventDetail",
    "VCMeetingRecordingEndedEventDetail",
    "VCMeetingRecordingReadyEventDetail",
    "VCMeetingRecordingStartedEventDetail",
    "VCMeetingShareEndedEventDetail",
    "VCMeetingShareStartedEventDetail",
    "VCMeetingStartedEventDetail",
]
