from nonebot.exception import ActionFailed as BaseActionFailed
from nonebot.exception import AdapterException
from nonebot.exception import ApiNotAvailable as BaseApiNotAvailable
from nonebot.exception import NetworkError as BaseNetworkError


class FeishuAdapterException(AdapterException):
    def __init__(self):
        super().__init__("feishu")


class ActionFailed(BaseActionFailed, FeishuAdapterException):
    """
    :说明:

      API 请求返回错误信息，包括 HTTP 错误和飞书返回的非零 ``code``。

    :属性:

      * ``info: dict[str, Any]``: 错误信息，通常包含 ``status_code``、``code``、``msg`` 和 ``log_id``
    """

    def __init__(self, **kwargs):
        super().__init__()
        self.info = kwargs

    def __repr__(self):
        return "<ActionFailed " + ", ".join(f"{k}={v}" for k, v in self.info.items()) + ">"

    def __str__(self):
        return self.__repr__()


class NetworkError(BaseNetworkError, FeishuAdapterException):
    """
    :说明:

      网络错误，包括超时。

    :参数:

      * ``msg: Optional[str]``: 错误信息
    """

    def __init__(self, msg: str | None = None):
        super().__init__()
        self.msg = msg

    def __repr__(self):
        return f"<NetWorkError message={self.msg}>"

    def __str__(self):
        return self.__repr__()


class ApiNotAvailable(BaseApiNotAvailable, FeishuAdapterException):
    pass
