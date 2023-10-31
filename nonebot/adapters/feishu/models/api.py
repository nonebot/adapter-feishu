from typing import List

from pydantic import HttpUrl, BaseModel


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
    ip_white_list: List[str]
    open_id: str


class BotInfoResponse(BaseResponse):
    bot: BotInfo


__all__ = ["BaseResponse", "TenantAccessTokenResponse", "BotInfo", "BotInfoResponse"]
