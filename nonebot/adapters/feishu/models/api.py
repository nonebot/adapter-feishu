from pydantic import BaseModel, HttpUrl

from .common import Reply


class BaseResponse(BaseModel):
    code: int
    msg: str


class TenantAccessTokenResponse(BaseResponse):
    tenant_access_token: str
    expire: int


class BotInfo(BaseModel):
    activate_status: int
    app_name: str
    avatar_url: HttpUrl
    ip_white_list: list[str]
    open_id: str


class BotInfoResponse(BaseResponse):
    bot: BotInfo


class ReplyResponseItems(BaseModel):
    items: list[Reply]


class ReplyResponse(BaseResponse):
    data: ReplyResponseItems


__all__ = [
    "BaseResponse",
    "BotInfo",
    "BotInfoResponse",
    "ReplyResponse",
    "ReplyResponseItems",
    "TenantAccessTokenResponse",
]
