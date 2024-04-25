import json
import base64
from pathlib import Path
from typing import Union, TypeVar

from werkzeug import Request, Response
from werkzeug.datastructures import MultiDict

K = TypeVar("K")
V = TypeVar("V")


def json_safe(string, content_type="application/octet-stream") -> str:
    try:
        string = string.decode("utf-8")
        json.dumps(string)
        return string
    except (ValueError, TypeError):
        return b"".join(
            [
                b"data:",
                content_type.encode("utf-8"),
                b";base64,",
                base64.b64encode(string),
            ]
        ).decode("utf-8")


def flattern(d: "MultiDict[K, V]") -> dict[K, Union[V, list[V]]]:
    return {k: v[0] if len(v) == 1 else v for k, v in d.to_dict(flat=False).items()}


def http_echo(request: Request) -> Response:
    try:
        _json = json.loads(request.data.decode("utf-8"))
    except (ValueError, TypeError):
        _json = None

    return Response(
        json.dumps(
            {
                "url": request.url,
                "method": request.method,
                "origin": request.headers.get("X-Forwarded-For", request.remote_addr),
                "headers": flattern(
                    MultiDict((k, v) for k, v in request.headers.items())
                ),
                "args": flattern(request.args),
                "form": flattern(request.form),
                "data": json_safe(request.data),
                "json": _json,
                "files": flattern(
                    MultiDict(
                        (
                            k,
                            json_safe(
                                v.read(),
                                request.files[k].content_type
                                or "application/octet-stream",
                            ),
                        )
                        for k, v in request.files.items()
                    )
                ),
            }
        ),
        status=200,
        content_type="application/json",
    )


def handle_get_tenant_access_token():
    return Response(
        json.dumps(
            {
                "code": 0,
                "msg": "ok",
                "tenant_access_token": "tenant_access_token",
                "expire": 7200,
            }
        ),
        status=200,
        content_type="application/json",
    )


def handle_get_bot_info():
    with open(Path(__file__).parent.joinpath("data", "bots_info.json")) as f:
        bots_info = json.load(f)

    return Response(
        json.dumps(bots_info),
        status=200,
        content_type="application/json",
    )


@Request.application
def request_handler(request: Request) -> Response:
    if request.url.endswith("/auth/v3/tenant_access_token/internal"):
        return handle_get_tenant_access_token()

    elif request.url.endswith("bot/v3/info"):
        return handle_get_bot_info()

    return http_echo(request)
