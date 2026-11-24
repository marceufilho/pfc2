"""The editor protocol around `analysis.py`: diagnostics as you type, hover and document symbols, over stdio.

A change is analysed after a short pause; if a newer change arrives meanwhile, the older result is dropped.
Analyses run one at a time on a worker thread, because the solver's default context is not thread-safe.
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import PurePosixPath
from typing import Any
from urllib.parse import unquote, urlparse

from lsprotocol import types
from pygls.lsp.server import LanguageServer

from pfc2.core.config import MAX_SOLVER_TIMEOUT_MS, MAX_SOURCE_BYTES
from pfc2.gate import LEVELS
from pfc2.lsp.analysis import Analysis, Diagnostic, analyze, hover_at

NAME, VERSION = "pfc2-lsp", "0.1.0"
DEBOUNCE_SECONDS = 0.4
DEFAULT_TIMEOUT_MS = 3_000
_SEVERITY = {
    "error": types.DiagnosticSeverity.Error,
    "warning": types.DiagnosticSeverity.Warning,
    "hint": types.DiagnosticSeverity.Hint,
}
_KIND = {
    "function": types.SymbolKind.Function,
    "law": types.SymbolKind.Event,
    "global": types.SymbolKind.Variable,
}


class Pfc2Server(LanguageServer):
    def __init__(self) -> None:
        super().__init__(NAME, VERSION)
        self.level = "full"
        self.timeout_ms = DEFAULT_TIMEOUT_MS
        self.analyses: dict[str, tuple[int | None, Analysis]] = {}
        self.worker = ThreadPoolExecutor(max_workers=1, thread_name_prefix="pfc2-check")

    def configure(self, options: Any) -> None:
        """Read `{"level": "full"|"memory", "timeoutMs": n}`; anything else keeps the defaults."""
        if not isinstance(options, dict):
            return
        if options.get("level") in LEVELS:
            self.level = options["level"]
        budget = options.get("timeoutMs")
        if type(budget) is int and 1 <= budget <= MAX_SOLVER_TIMEOUT_MS:
            self.timeout_ms = budget


server = Pfc2Server()


def _range(line: int, column: int, end_column: int) -> types.Range:
    return types.Range(types.Position(line - 1, column - 1), types.Position(line - 1, end_column - 1))


def _diagnostic(item: Diagnostic) -> types.Diagnostic:
    return types.Diagnostic(
        range=_range(item.line, item.column, item.end_column),
        message=item.message,
        severity=_SEVERITY[item.severity],
        code=item.code,
        source="pfc2",
    )


def _name(uri: str) -> str:
    name = PurePosixPath(unquote(urlparse(uri).path)).name
    return name if name and name.isprintable() and '"' not in name else "document.c"


async def refresh(ls: Pfc2Server, uri: str) -> None:
    document = ls.workspace.get_text_document(uri)
    version, text = document.version, document.source
    await asyncio.sleep(DEBOUNCE_SECONDS)
    if ls.workspace.get_text_document(uri).version != version:
        return  # A newer edit is on its way.
    if len(text.encode("utf-8")) > MAX_SOURCE_BYTES:
        return
    loop = asyncio.get_running_loop()
    analysis = await loop.run_in_executor(
        ls.worker, lambda: analyze(text, _name(uri), level=ls.level, timeout_ms=ls.timeout_ms)  # type: ignore[arg-type]
    )
    if ls.workspace.get_text_document(uri).version != version:
        return
    ls.analyses[uri] = (version, analysis)
    ls.text_document_publish_diagnostics(
        types.PublishDiagnosticsParams(uri, [_diagnostic(item) for item in analysis.diagnostics], version)
    )


@server.feature(types.INITIALIZE)
def initialize(ls: Pfc2Server, params: types.InitializeParams) -> None:
    ls.configure(params.initialization_options)


@server.feature(types.TEXT_DOCUMENT_DID_OPEN)
async def did_open(ls: Pfc2Server, params: types.DidOpenTextDocumentParams) -> None:
    await refresh(ls, params.text_document.uri)


@server.feature(types.TEXT_DOCUMENT_DID_CHANGE)
async def did_change(ls: Pfc2Server, params: types.DidChangeTextDocumentParams) -> None:
    await refresh(ls, params.text_document.uri)


@server.feature(types.TEXT_DOCUMENT_DID_SAVE)
async def did_save(ls: Pfc2Server, params: types.DidSaveTextDocumentParams) -> None:
    await refresh(ls, params.text_document.uri)


@server.feature(types.TEXT_DOCUMENT_DID_CLOSE)
def did_close(ls: Pfc2Server, params: types.DidCloseTextDocumentParams) -> None:
    ls.analyses.pop(params.text_document.uri, None)
    ls.text_document_publish_diagnostics(types.PublishDiagnosticsParams(params.text_document.uri, []))


@server.feature(types.TEXT_DOCUMENT_HOVER)
def hover(ls: Pfc2Server, params: types.HoverParams) -> types.Hover | None:
    known = ls.analyses.get(params.text_document.uri)
    found = hover_at(known[1], params.position.line + 1, params.position.character + 1) if known else None
    if found is None:
        return None
    contents = types.MarkupContent(types.MarkupKind.Markdown, found.text)
    return types.Hover(contents, _range(found.line, found.column, found.end_column))


@server.feature(types.TEXT_DOCUMENT_DOCUMENT_SYMBOL)
def symbols(ls: Pfc2Server, params: types.DocumentSymbolParams) -> list[types.DocumentSymbol]:
    known = ls.analyses.get(params.text_document.uri)
    result = []
    for item in known[1].symbols if known else ():
        where = _range(item.line, item.column, item.column + len(item.name))
        result.append(types.DocumentSymbol(item.name, _KIND[item.kind], where, where))
    return result


def main() -> None:
    """Serve one editor over standard input and output until it disconnects."""
    server.start_io()
