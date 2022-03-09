import logging

from nonebot.log import LoguruHandler

aiocache_logger = logging.getLogger("aiocache.serializers.serializers")
aiocache_logger.setLevel(logging.DEBUG)
aiocache_logger.handlers.clear()
aiocache_logger.addHandler(LoguruHandler())

from .adapter import Adapter as Adapter
from .bot import Bot as Bot
from .event import *
from .exception import ActionFailed, ApiNotAvailable
from .exception import FeishuAdapterException as FeishuAdapterException
from .exception import NetworkError
from .message import Message as Message
from .message import MessageSegment as MessageSegment
from .utils import log as log
