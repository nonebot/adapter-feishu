from copy import deepcopy
from datetime import datetime
from typing_extensions import override
from typing import TYPE_CHECKING, Any, Dict, Literal, Optional

from pydantic import Field
from nonebot.utils import escape_tag
from nonebot.compat import model_dump

from nonebot.adapters import Event as BaseEvent

from .message import Message
from .models import (
    Reply,
    UserId,
    EventHeader,
    MessageEventDetail,
    MessageReadEventDetail,
    GroupMessageEventDetail,
    DriveFileReadEventDetail,
    VCMeetingLeftEventDetail,
    GroupDisbandedEventDetail,
    PrivateMessageEventDetail,
    VCMeetingEndedEventDetail,
    DriveFileEditedEventDetail,
    VCMeetingJoinedEventDetail,
    DriveFileDeletedEventDetail,
    DriveFileTrashedEventDetail,
    VCMeetingStartedEventDetail,
    CalendarAclCreatedEventDetail,
    CalendarAclDeletedEventDetail,
    ContactUserCreatedEventDetail,
    ContactUserDeletedEventDetail,
    ContactUserUpdatedEventDetail,
    GroupConfigUpdatedEventDetail,
    MeetingRoomCreatedEventDetail,
    MeetingRoomDeletedEventDetail,
    MeetingRoomUpdatedEventDetail,
    GroupMemberBotAddedEventDetail,
    VCMeetingShareEndedEventDetail,
    CalendarEventChangedEventDetail,
    GroupMemberUserAddedEventDetail,
    DriveFileTitleUpdatedEventDetail,
    GroupMemberBotDeletedEventDetail,
    VCMeetingShareStartedEventDetail,
    GroupMemberUserDeletedEventDetail,
    MessageReactionCreatedEventDetail,
    MessageReactionDeletedEventDetail,
    VCMeetingRecordingEndedEventDetail,
    VCMeetingRecordingReadyEventDetail,
    ContactDepartmentCreatedEventDetail,
    ContactDepartmentDeletedEventDetail,
    ContactDepartmentUpdatedEventDetail,
    GroupMemberUserWithdrawnEventDetail,
    MeetingRoomStatusChangedEventDetail,
    AttendanceUserFlowCreatedEventDetail,
    AttendanceUserTaskUpdatedEventDetail,
    VCMeetingRecordingStartedEventDetail,
    DriveFilePermissionMemberAddedEventDetail,
    DriveFilePermissionMemberRemovedEventDetail,
)


class Event(BaseEvent):
    """
    飞书协议事件。各事件字段参考 `飞书文档`_

    .. _飞书文档:
        https://open.feishu.cn/document/ukTMukTMukTM/uYDNxYjL2QTM24iN0EjN/event-list
    """

    __event__ = ""
    schema_: str = Field("", alias="schema")
    header: EventHeader
    event: Any

    @override
    def get_type(self) -> str:
        return self.header.event_type

    @override
    def get_event_name(self) -> str:
        return self.header.event_type

    @override
    def get_event_description(self) -> str:
        return escape_tag(str(model_dump(self)))

    @override
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @override
    def get_plaintext(self) -> str:
        raise ValueError("Event has no plaintext!")

    @override
    def get_user_id(self) -> str:
        raise ValueError("Event has no user_id!")

    @override
    def get_session_id(self) -> str:
        raise ValueError("Event has no session_id!")

    @override
    def is_tome(self) -> bool:
        return False

    @property
    def time(self) -> datetime:
        return datetime.utcfromtimestamp(int(self.header.create_time) / 1000)


class MessageEvent(Event):
    __event__ = "im.message.receive_v1"
    event: MessageEventDetail

    to_me: bool = False
    """
    :说明: 消息是否与机器人有关

    :类型: ``bool``
    """
    reply: Optional[Reply]

    if TYPE_CHECKING:
        _message: Message
        original_message: Message

    @override
    def get_type(self) -> Literal["message"]:
        return "message"

    @override
    def get_event_name(self) -> str:
        return f"{self.get_type()}.{self.event.message.chat_type}"

    @override
    def get_event_description(self) -> str:
        return (
            f"{self.event.message.message_id} from {self.get_user_id()}"
            f"@[{self.event.message.chat_type}:{self.event.message.chat_id}]"
            f" {escape_tag(str(self.get_message()))}"
        )

    @override
    def get_message(self) -> Message:
        if not hasattr(self, "_message"):
            deserialized = Message.deserialize(
                self.event.message.content,
                self.event.message.mentions,
                self.event.message.message_type,
            )
            setattr(
                self,
                "_message",
                deserialized,
            )
            setattr(
                self,
                "original_message",
                deepcopy(deserialized),
            )

        return getattr(self, "_message")

    @property
    def message_id(self) -> str:
        return self.event.message.message_id

    @override
    def get_plaintext(self) -> str:
        return str(self.get_message())

    @override
    def get_user_id(self) -> str:
        return self.event.sender.sender_id.open_id

    def get_all_user_id(self) -> UserId:
        return self.event.sender.sender_id

    @override
    def get_session_id(self) -> str:
        return (
            f"{self.event.message.chat_type}"
            f"_{self.event.message.chat_id}"
            f"_{self.get_user_id()}"
        )

    @override
    def is_tome(self) -> bool:
        return self.to_me


class GroupMessageEvent(MessageEvent):
    __event__ = "im.message.receive_v1.group"
    event: GroupMessageEventDetail


class PrivateMessageEvent(MessageEvent):
    __event__ = "im.message.receive_v1.p2p"
    event: PrivateMessageEventDetail


class NoticeEvent(Event):
    event: Dict[str, Any]

    @override
    def get_type(self) -> Literal["notice"]:
        return "notice"

    @override
    def get_event_name(self) -> str:
        return self.header.event_type

    @override
    def get_event_description(self) -> str:
        return escape_tag(str(model_dump(self)))

    @override
    def get_message(self) -> Message:
        raise ValueError("Event has no message!")

    @override
    def get_plaintext(self) -> str:
        raise ValueError("Event has no plaintext!")

    @override
    def get_user_id(self) -> str:
        raise ValueError("Event has no user_id!")

    @override
    def get_session_id(self) -> str:
        raise ValueError("Event has no session_id!")


class MessageReadEvent(NoticeEvent):
    __event__ = "im.message.message_read_v1"
    event: MessageReadEventDetail


class GroupDisbandedEvent(NoticeEvent):
    __event__ = "im.chat.disbanded_v1"
    event: GroupDisbandedEventDetail


class MessageReactionDeletedEvent(NoticeEvent):
    __event__ = "im.message.reaction.deleted_v1"
    event: MessageReactionDeletedEventDetail


class MessageReactionCreatedEvent(NoticeEvent):
    __event__ = "im.message.reaction.created_v1"
    event: MessageReactionCreatedEventDetail


class GroupConfigUpdatedEvent(NoticeEvent):
    __event__ = "im.chat.updated_v1"
    event: GroupConfigUpdatedEventDetail


class GroupMemberBotAddedEvent(NoticeEvent):
    __event__ = "im.chat.member.bot.added_v1"
    event: GroupMemberBotAddedEventDetail


class GroupMemberBotDeletedEvent(NoticeEvent):
    __event__ = "im.chat.member.bot.deleted_v1"
    event: GroupMemberBotDeletedEventDetail


class GroupMemberUserAddedEvent(NoticeEvent):
    __event__ = "im.chat.member.user.added_v1"
    event: GroupMemberUserAddedEventDetail


class GroupMemberUserWithdrawnEvent(NoticeEvent):
    __event__ = "im.chat.member.user.withdrawn_v1"
    event: GroupMemberUserWithdrawnEventDetail


class GroupMemberUserDeletedEvent(NoticeEvent):
    __event__ = "im.chat.member.user.deleted_v1"
    event: GroupMemberUserDeletedEventDetail


class ContactUserUpdatedEvent(NoticeEvent):
    __event__ = "contact.user.updated_v3"
    event: ContactUserUpdatedEventDetail


class ContactUserDeletedEvent(NoticeEvent):
    __event__ = "contact.user.deleted_v3"
    event: ContactUserDeletedEventDetail


class ContactUserCreatedEvent(NoticeEvent):
    __event__ = "contact.user.created_v3"
    event: ContactUserCreatedEventDetail


class ContactDepartmentUpdatedEvent(NoticeEvent):
    __event__ = "contact.department.updated_v3"
    event: ContactDepartmentUpdatedEventDetail


class ContactDepartmentDeletedEvent(NoticeEvent):
    __event__ = "contact.department.deleted_v3"
    event: ContactDepartmentDeletedEventDetail


class ContactDepartmentCreatedEvent(NoticeEvent):
    __event__ = "contact.department.created_v3"
    event: ContactDepartmentCreatedEventDetail


class CalendarAclCreatedEvent(NoticeEvent):
    __event__ = "calendar.calendar.acl.created_v4"
    event: CalendarAclCreatedEventDetail


class CalendarAclDeletedEvent(NoticeEvent):
    __event__ = "calendar.calendar.acl.deleted_v4"
    event: CalendarAclDeletedEventDetail


class CalendarChangedEvent(NoticeEvent):
    __event__ = "calendar.calendar.changed_v4"
    event: dict


class CalendarEventChangedEvent(NoticeEvent):
    __event__ = "calendar.calendar.event.changed_v4"
    event: CalendarEventChangedEventDetail


class DriveFileReadEvent(NoticeEvent):
    __event__ = "drive.file.read_v1"
    event: DriveFileReadEventDetail


class DriveFileTitleUpdatedEvent(NoticeEvent):
    __event__ = "drive.file.title_updated_v1"
    event: DriveFileTitleUpdatedEventDetail


class DriveFilePermissionMemberAddedEvent(NoticeEvent):
    __event__ = "drive.file.permission_member_added_v1"
    event: DriveFilePermissionMemberAddedEventDetail


class DriveFilePermissionMemberRemovedEvent(NoticeEvent):
    __event__ = "drive.file.permission_member_removed_v1"
    event: DriveFilePermissionMemberRemovedEventDetail


class DriveFileTrashedEvent(NoticeEvent):
    __event__ = "drive.file.trashed_v1"
    event: DriveFileTrashedEventDetail


class DriveFileDeletedEvent(NoticeEvent):
    __event__ = "drive.file.deleted_v1"
    event: DriveFileDeletedEventDetail


class DriveFileEditedEvent(NoticeEvent):
    __event__ = "drive.file.edit_v1"
    event: DriveFileEditedEventDetail


class MeetingRoomCreatedEvent(NoticeEvent):
    __event__ = "meeting_room.meeting_room.created_v1"
    event: MeetingRoomCreatedEventDetail


class MeetingRoomUpdatedEvent(NoticeEvent):
    __event__ = "meeting_room.meeting_room.updated_v1"
    event: MeetingRoomUpdatedEventDetail


class MeetingRoomDeletedEvent(NoticeEvent):
    __event__ = "meeting_room.meeting_room.deleted_v1"
    event: MeetingRoomDeletedEventDetail


class MeetingRoomStatusChangedEvent(NoticeEvent):
    __event__ = "meeting_room.meeting_room.status_changed_v1"
    event: MeetingRoomStatusChangedEventDetail


class VCMeetingStartedEvent(NoticeEvent):
    __event__ = "vc.meeting.meeting_started_v1"
    event: VCMeetingStartedEventDetail


class VCMeetingEndedEvent(NoticeEvent):
    __event__ = "vc.meeting.meeting_ended_v1"
    event: VCMeetingEndedEventDetail


class VCMeetingJoinedEvent(NoticeEvent):
    __event__ = "vc.meeting.join_meeting_v1"
    event: VCMeetingJoinedEventDetail


class VCMeetingLeftEvent(NoticeEvent):
    __event__ = "vc.meeting.leave_meeting_v1"
    event: VCMeetingLeftEventDetail


class VCMeetingRecordingStartedEvent(NoticeEvent):
    __event__ = "vc.meeting.recording_started_v1"
    event: VCMeetingRecordingStartedEventDetail


class VCMeetingRecordingEndedEvent(NoticeEvent):
    __event__ = "vc.meeting.recording_ended_v1"
    event: VCMeetingRecordingEndedEventDetail


class VCMeetingRecordingReadyEvent(NoticeEvent):
    __event__ = "vc.meeting.recording_ready_v1"
    event: VCMeetingRecordingReadyEventDetail


class VCMeetingShareStartedEvent(NoticeEvent):
    __event__ = "vc.meeting.share_started_v1"
    event: VCMeetingShareStartedEventDetail


class VCMeetingShareEndedEvent(NoticeEvent):
    __event__ = "vc.meeting.share_ended_v1"
    event: VCMeetingShareEndedEventDetail


class AttendanceUserFlowCreatedEvent(NoticeEvent):
    __event__ = "attendance.user_flow.created_v1"
    event: AttendanceUserFlowCreatedEventDetail


class AttendanceUserTaskUpdatedEvent(NoticeEvent):
    __event__ = "attendance.user_task.updated_v1"
    event: AttendanceUserTaskUpdatedEventDetail
