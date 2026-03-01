from io import BytesIO
from pathlib import Path

import pytest

from nonebot.adapters.feishu.utils import AESCipher, f2b


@pytest.mark.parametrize("key", ["test key", b"test key"])
def test_aes(key: str):
    encrypt = "P37w+VZImNgPEO1RBhJ6RtKl7n6zymIbEG1pReEzghk="
    cipher = AESCipher(key)

    assert cipher.decrypt_string(encrypt) == "hello world"


def test_f2b_bytes():
    """f2b 传入 bytes 原样返回。"""
    data = b"hello"
    assert f2b(data) is data


def test_f2b_str(tmp_path: Path):
    """f2b 传入文件路径时读取文件内容。"""
    f = tmp_path / "f.txt"
    f.write_bytes(b"content")
    assert f2b(str(f)) == b"content"


def test_f2b_path(tmp_path: Path):
    """f2b 传入 Path 时读取文件内容。"""
    f = tmp_path / "f.txt"
    f.write_bytes(b"path_content")
    assert f2b(f) == b"path_content"


def test_f2b_bytes_io():
    """f2b 传入 BytesIO 时返回 getvalue()。"""
    bio = BytesIO(b"bytesio_content")
    assert f2b(bio) == b"bytesio_content"
