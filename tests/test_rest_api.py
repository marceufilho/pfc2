"""The REST API example end to end: certified handlers in a shared library, served over real HTTP.

The expected statuses are written from the API's table in api.c, not taken from a run.
"""

import importlib.util
import json
import subprocess
import threading
import urllib.error
import urllib.request
from pathlib import Path

import pytest

from pfc2 import frontend
from pfc2.check import check
from pfc2.core.target import read_target

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "12_rest_api"
# (method, path, body, expected status, expected body) in order: the table starts empty.
CONVERSATION = [
    ("GET", "/items/2", None, 404, {"status": 404}),
    ("PUT", "/items/2", {"value": 5}, 201, {"status": 201}),
    ("GET", "/items/2", None, 200, {"value": 5}),
    ("PUT", "/items/2", {"value": 9}, 200, {"status": 200}),
    ("GET", "/items/2", None, 200, {"value": 9}),
    ("PUT", "/items/2", {"value": 1000001}, 400, {"status": 400}),
    ("PUT", "/items/2", {"value": -1}, 400, {"status": 400}),
    ("GET", "/items/-1", None, 404, {"status": 404}),
    ("GET", "/items/8", None, 404, {"status": 404}),
    ("PUT", "/items/9223372036854775807", {"value": 1}, 404, {"status": 404}),
    ("POST", "/items/2", {"value": 1}, 405, {"status": 405}),
    ("DELETE", "/items/2", None, 204, None),
    ("DELETE", "/items/2", None, 404, {"status": 404}),
    ("GET", "/items/2", None, 404, {"status": 404}),
    ("GET", "/items/7", None, 404, {"status": 404}),
    ("PUT", "/items/7", {"value": 0}, 201, {"status": 201}),
    ("GET", "/items/7", None, 200, {"value": 0}),
]


def _request(base: str, method: str, path: str, body: object) -> tuple[int, object]:
    data = None if body is None else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(base + path, data=data, method=method)
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            text = response.read()
            return response.status, json.loads(text) if text else None
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read())


@pytest.mark.integration
def test_the_certified_handlers_answer_real_http_requests_as_the_api_table_says(tmp_path: Path) -> None:
    unit, certification = check(frontend.load(EXAMPLE / "api.c"), read_target("clang-19"))
    assert certification.accepted and certification.c is not None, certification.reason
    assert [law.name for law in unit.laws] == ["negative_id_is_not_found"]
    assert certification.emission.decisions and all(d.removed for d in certification.emission.decisions)
    source, library = tmp_path / "api.c", tmp_path / "libapi.so"
    source.write_text(certification.c, encoding="utf-8")
    command = ["clang-19", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-shared", "-fPIC", str(source)]
    built = subprocess.run([*command, "-o", str(library)], capture_output=True, text=True, check=False)
    assert built.returncode == 0, built.stderr

    spec = importlib.util.spec_from_file_location("rest_api_server", EXAMPLE / "server.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    server = module.serve(library, 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base = f"http://127.0.0.1:{server.server_port}"
        for method, path, body, status, answer in CONVERSATION:
            assert _request(base, method, path, body) == (status, answer), (method, path, body)
        assert _request(base, "GET", "/elsewhere", None)[0] == 404  # Refused by the host, before the handlers.
        assert _request(base, "PUT", "/items/1", "not an object")[0] == 400
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=10)
