# nonebot.adapters.feishu.exception

## _class_ `FeishuAdapterException(<auto>)` {#FeishuAdapterException}



- **参数**

  auto

## _class_ `ActionFailed(<auto>)` {#ActionFailed}

- **说明**

  :说明:

  API 请求返回错误信息，包括 HTTP 错误和飞书返回的非零 ``code``。

  :属性:

    * ``info: dict[str, Any]``: 错误信息，通常包含 ``status_code``、``code``、``msg`` 和 ``log_id``

- **参数**

  auto

## _class_ `NetworkError(<auto>)` {#NetworkError}

- **说明**

  :说明:

  网络错误，包括超时。

  :参数:

    * ``msg: Optional[str]``: 错误信息

- **参数**

  auto

## _class_ `ApiNotAvailable(<auto>)` {#ApiNotAvailable}



- **参数**

  auto
