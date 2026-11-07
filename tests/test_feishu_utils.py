from io import BytesIO
import logging
from pathlib import Path

from nonebot.adapters.feishu.utils import f2b
from nonebot.log import LoguruHandler


def test_larkify_logs_go_to_nonebot():
    handlers = logging.getLogger("larkify").handlers

    assert any(isinstance(handler, LoguruHandler) for handler in handlers)


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
