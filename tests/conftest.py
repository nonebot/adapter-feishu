from collections.abc import Generator
import json
from pathlib import Path
import threading
from typing import TypeVar
from typing_extensions import ParamSpec

from nonebug import NONEBOT_INIT_KWARGS
import pytest
from werkzeug.serving import BaseWSGIServer, make_server

from fake_server import request_handler
import nonebot
import nonebot.adapters
from nonebot.drivers import URL

nonebot.adapters.__path__.append(  # type: ignore
    str((Path(__file__).parent.parent / "nonebot" / "adapters").resolve())
)

from nonebot.adapters.feishu import Adapter as FeishuAdapter

P = ParamSpec("P")
R = TypeVar("R")


def pytest_configure(config: pytest.Config) -> None:
    with (Path(__file__).parent.joinpath("data", "bots.json")).open("r") as f:
        feishu_bots = json.load(f)

    config.stash[NONEBOT_INIT_KWARGS] = {
        "driver": "~fastapi+~httpx",
        "log_level": "DEBUG",
        "feishu_bots": feishu_bots,
        "nickname": ["bot"],
    }

# pytest.param("trio"): not supported
@pytest.fixture(scope="session", params=[pytest.param("asyncio")])
def anyio_backend(request: pytest.FixtureRequest):
    return request.param


@pytest.fixture(scope="session", autouse=True)
def server() -> Generator[BaseWSGIServer, None, None]:
    server = make_server("127.0.0.1", 0, app=request_handler)
    thread = threading.Thread(target=server.serve_forever)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        thread.join()


@pytest.fixture(scope="session")
def server_url(server: BaseWSGIServer) -> URL:
    return URL(f"http://{server.host}:{server.port}")


@pytest.fixture(scope="session", autouse=True)
async def after_nonebot_init(after_nonebot_init: None, server_url: URL):
    with pytest.MonkeyPatch.context() as m:

        def _get_api_base(*args, **kwargs):
            return server_url

        m.setattr(FeishuAdapter, "get_api_base", _get_api_base)
        driver = nonebot.get_driver()
        driver.register_adapter(FeishuAdapter)
        yield
