# nonebot.adapters.feishu.config

## _class_ `BotConfig(<auto>)` {#BotConfig}

- **说明**

  飞书适配器机器人配置类

  :配置项:

  - `app_id`: 飞书开放平台后台“凭证与基础信息”处给出的 App ID
  - `app_secret`: 飞书开放平台后台“凭证与基础信息”处给出的 App Secret
  - `encrypt_key`: 飞书开放平台后台“事件订阅”处设置的 Encrypt Key
  - `verification_token`: 飞书开放平台后台“事件订阅”处设置的 Verification Token
  - `is_lark`: 是否使用 Lark（飞书海外版），默认为 false
  - `protocol`: 连接方式，`http` 为 Webhook 回调，`ws` 为 WebSocket 长连接（仅企业自建应用）

- **参数**

  auto

## _class_ `Config(<auto>)` {#Config}

- **说明**

  飞书适配器全局配置类

  :配置项:

  - `feishu_api_base`: 飞书国内版开放平台 API Endpoint
  - `feishu_lark_api_base`: 飞书海外版（lark）开放平台 API Endpoint
  - `feishu_bots`: 飞书适配器 Bot 配置列表，具体配置项参阅 BotConfig 类

- **参数**

  auto
