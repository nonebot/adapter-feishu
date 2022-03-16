from typing import Optional

from pydantic import Field, BaseModel


class Config(BaseModel):
    """
    飞书配置类

    :配置项:

      - ``feishu_app_id``: 飞书开放平台后台“凭证与基础信息”处给出的 App ID
      - ``feishu_app_secret``: 飞书开放平台后台“凭证与基础信息”处给出的 App Secret
      - ``feishu_encrypt_key``: 飞书开放平台后台“事件订阅”处设置的 Encrypt Key
      - ``feishu_verification_token``: 飞书开放平台后台“事件订阅”处设置的 Verification Token
      - ``feishu_is_lark``: 是否使用 Lark（飞书海外版），默认为 false

    """

    feishu_app_id: Optional[str] = Field(default=None)
    feishu_app_secret: Optional[str] = Field(default=None)
    feishu_encrypt_key: Optional[str] = Field(default=None)
    feishu_verification_token: Optional[str] = Field(default=None)
    feishu_is_lark: Optional[str] = Field(default=False)

    class Config:
        extra = "ignore"
