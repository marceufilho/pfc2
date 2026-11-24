"""One conversation with the real server process over stdio: diagnostics, hover, symbols and a re-check."""

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "examples" / "wrong" / "off_by_one.c").read_text(encoding="utf-8")
URI = "file:///work/off_by_one.c"


class Client:
    def __init__(self) -> None:
        command = [sys.executable, "-m", "pfc2", "lsp"]
        self.process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=ROOT)
        self.serial = 0

    def send(self, method: str, params: Any, *, request: bool = False) -> int:
        message: dict[str, Any] = {"jsonrpc": "2.0", "method": method, "params": params}
        if request:
            self.serial += 1
            message["id"] = self.serial
        body = json.dumps(message).encode("utf-8")
        assert self.process.stdin is not None
        self.process.stdin.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body)
        self.process.stdin.flush()
        return self.serial

    def read(self) -> dict[str, Any]:
        assert self.process.stdout is not None
        length = 0
        while True:
            line = self.process.stdout.readline()
            assert line, "the server closed its output"
            if line in (b"\r\n", b"\n"):
                break
            if line.lower().startswith(b"content-length:"):
                length = int(line.split(b":")[1])
        return json.loads(self.process.stdout.read(length))  # type: ignore[no-any-return]

    def until(self, wanted: Any) -> dict[str, Any]:
        for _ in range(200):
            message = self.read()
            if wanted(message):
                return message
        raise AssertionError("expected message did not arrive")


@pytest.mark.integration
def test_the_server_reports_a_wrong_program_and_answers_hover_and_symbols() -> None:
    client = Client()
    try:
        first = client.send("initialize", {"processId": None, "rootUri": None, "capabilities": {}}, request=True)
        capabilities = client.until(lambda m: m.get("id") == first)["result"]["capabilities"]
        assert capabilities["hoverProvider"] and capabilities["documentSymbolProvider"]
        client.send("initialized", {})
        document = {"uri": URI, "languageId": "c", "version": 1, "text": SOURCE}
        client.send("textDocument/didOpen", {"textDocument": document})
        published = client.until(lambda m: m.get("method") == "textDocument/publishDiagnostics")["params"]
        assert published["uri"] == URI
        errors = [d for d in published["diagnostics"] if d["severity"] == 1]
        # Hand-counted: `a[i] = value;` is line 7 column 9, so the zero-based position is (6, 8).
        assert [(d["range"]["start"]["line"], d["range"]["start"]["character"], d["code"]) for d in errors][0] == (
            6,
            8,
            "bounds",
        )
        assert "n = 0" in errors[0]["message"] and errors[0]["source"] == "pfc2"

        position = {"textDocument": {"uri": URI}, "position": {"line": 3, "character": 6}}  # `fill`
        asked = client.send("textDocument/hover", position, request=True)
        hover = client.until(lambda m: m.get("id") == asked)["result"]
        assert "**fill**" in hover["contents"]["value"]

        asked = client.send("textDocument/documentSymbol", {"textDocument": {"uri": URI}}, request=True)
        listed = client.until(lambda m: m.get("id") == asked)["result"]
        assert [(s["name"], s["range"]["start"]["line"]) for s in listed] == [("fill", 3)]

        fixed = SOURCE.replace("i <= n", "i < n")
        change = {"textDocument": {"uri": URI, "version": 2}, "contentChanges": [{"text": fixed}]}
        client.send("textDocument/didChange", change)
        again = client.until(lambda m: m.get("method") == "textDocument/publishDiagnostics")["params"]
        assert again["version"] == 2 and not [d for d in again["diagnostics"] if d["severity"] == 1]

        last = client.send("shutdown", None, request=True)
        client.until(lambda m: m.get("id") == last)
        client.send("exit", None)
        assert client.process.wait(timeout=20) == 0
    finally:
        if client.process.poll() is None:
            client.process.kill()
