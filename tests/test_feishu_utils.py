from nonebot.adapters.feishu.utils import AESCipher


def test_aes():
    encrypt = "P37w+VZImNgPEO1RBhJ6RtKl7n6zymIbEG1pReEzghk="
    cipher = AESCipher("test key")

    assert cipher.decrypt_string(encrypt) == "hello world"
