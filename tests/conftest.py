import json
from pathlib import Path

import pytest
from nonebug import NONEBOT_INIT_KWARGS

import nonebot
import nonebot.adapters

nonebot.adapters.__path__.append(  # type: ignore
    str((Path(__file__).parent.parent / "nonebot" / "adapters").resolve())
)

from nonebot.adapters.feishu import Adapter as FeishuAdapter


def pytest_configure(config: pytest.Config) -> None:
    with (Path(__file__).parent / "bots.json").open("r") as f:
        feishu_bots = json.load(f)

    config.stash[NONEBOT_INIT_KWARGS] = {
        "driver": "~fastapi+~httpx",
        "log_level": "DEBUG",
        "feishu_bots": feishu_bots,
    }


@pytest.fixture(scope="session", autouse=True)
def _init_adapter(nonebug_init: None):
    driver = nonebot.get_driver()
    driver.register_adapter(FeishuAdapter)
