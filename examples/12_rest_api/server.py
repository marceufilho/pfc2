"""A small HTTP server around the certified handlers of api.c. This file is ordinary, unverified code.

It owns the table (two arrays of N slots), turns each request into three numbers (method, id, value),
calls the certified `handle`, and turns the status back into an HTTP response. The proof covers what
`handle` does with any three numbers; it does not cover this file, the HTTP library or the operating system.

    pfc2 build examples/12_rest_api/api.c --output build/api
    clang-19 -std=c11 -O2 -shared -fPIC build/api/api.c -o build/api/libapi.so
    python examples/12_rest_api/server.py build/api/libapi.so --port 8080
"""

import argparse
import ctypes
import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

SLOTS = 8
METHODS = {"GET": 0, "PUT": 1, "DELETE": 2}
UNKNOWN_METHOD = 99
LONG_MAX = 2**63 - 1
_ITEM = re.compile(r"/items/(-?\d{1,19})")


class Api:
    """The certified library and the table it works on. Not thread-safe: one request at a time."""

    def __init__(self, library: Path) -> None:
        self.library = ctypes.CDLL(str(library))
        table = ctypes.c_long * SLOTS
        self.used, self.values = table(), table()
        self.library.handle.restype = ctypes.c_long
        self.library.handle.argtypes = [ctypes.c_long, table, table, ctypes.c_long, ctypes.c_long, ctypes.c_long]
        self.library.last_reply.restype = ctypes.c_long

    def handle(self, method: int, identifier: int, value: int) -> tuple[int, int]:
        """The status the certified code chose and, for a successful GET, the value it returned."""
        status = int(self.library.handle(SLOTS, self.used, self.values, method, identifier, value))
        return status, int(self.library.last_reply())


def handler(api: Api) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def respond(self, status: int, body: dict[str, object] | None = None) -> None:
            data = b"" if status == 204 else json.dumps(body or {}).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def value(self) -> int | None:
            """The integer in a body `{"value": n}`; None when the body is anything else."""
            try:
                length = int(self.headers.get("Content-Length", "0"))
                parsed = json.loads(self.rfile.read(length)) if 0 < length <= 1024 else None
            except (ValueError, UnicodeDecodeError):
                return None
            found = parsed.get("value") if isinstance(parsed, dict) else None
            return found if type(found) is int and -LONG_MAX <= found <= LONG_MAX else None

        def serve(self) -> None:
            path = _ITEM.fullmatch(self.path)
            if path is None or abs(int(path.group(1))) > LONG_MAX:
                self.respond(404, {"error": "not found"})
                return
            value = 0
            if self.command == "PUT":
                sent = self.value()
                if sent is None:
                    self.respond(400, {"error": 'expected a body like {"value": 5}'})
                    return
                value = sent
            status, reply = api.handle(METHODS.get(self.command, UNKNOWN_METHOD), int(path.group(1)), value)
            self.respond(status, {"value": reply} if status == 200 and self.command == "GET" else {"status": status})

        do_GET = do_PUT = do_DELETE = do_POST = do_PATCH = serve  # noqa: N815

        def log_message(self, format: str, *arguments: object) -> None:  # noqa: A002
            return

    return Handler


def serve(library: Path, port: int) -> HTTPServer:
    """A server bound to 127.0.0.1; port 0 picks a free one (see `server_port`)."""
    return HTTPServer(("127.0.0.1", port), handler(Api(library)))


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the certified handlers of api.c over HTTP on 127.0.0.1.")
    parser.add_argument("library", type=Path, help="shared library built from the certified api.c")
    parser.add_argument("--port", type=int, default=8080)
    arguments = parser.parse_args()
    server = serve(arguments.library, arguments.port)
    print(f"http://127.0.0.1:{server.server_port}/items/0")
    server.serve_forever()


if __name__ == "__main__":
    main()
