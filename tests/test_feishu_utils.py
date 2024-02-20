import pytest

from nonebot.adapters.feishu.utils import AESCipher


@pytest.mark.parametrize("key", ["test key", b"test key"])
def test_aes(key: str):
    encrypt = "P37w+VZImNgPEO1RBhJ6RtKl7n6zymIbEG1pReEzghk="
    cipher = AESCipher(key)

    assert cipher.decrypt_string(encrypt) == "hello world"
