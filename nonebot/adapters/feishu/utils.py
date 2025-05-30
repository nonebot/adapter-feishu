import base64
import hashlib
from io import BytesIO
from pathlib import Path
from typing import Union

from cashews import cache
from Crypto.Cipher import AES

from nonebot.utils import logger_wrapper

log = logger_wrapper("FEISHU")

cache.setup("mem://")


def f2b(file: Union[str, bytes, BytesIO, Path]) -> bytes:
    if isinstance(file, bytes):
        return file

    elif isinstance(file, str):
        return Path(file).resolve().read_bytes()

    elif isinstance(file, BytesIO):
        return file.getvalue()

    elif isinstance(file, Path):
        return file.resolve().read_bytes()


class AESCipher:
    def __init__(self, key):
        self.block_size = AES.block_size
        self.key = hashlib.sha256(AESCipher.str_to_bytes(key)).digest()

    @staticmethod
    def str_to_bytes(data):
        u_type = type(b"".decode("utf8"))
        if isinstance(data, u_type):
            return data.encode("utf8")

        return data

    @staticmethod
    def _unpad(s):
        return s[: -ord(s[len(s) - 1 :])]

    def decrypt(self, enc):
        iv = enc[: AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        return self._unpad(cipher.decrypt(enc[AES.block_size :]))

    def decrypt_string(self, enc):
        enc = base64.b64decode(enc)

        return self.decrypt(enc).decode("utf8")
