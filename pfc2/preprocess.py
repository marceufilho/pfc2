"""The preprocessing PFC2 does itself: comments, its own headers, #ifdef/#ifndef/#else/#endif and
object-like `#define NAME value`.

No external preprocessor is run. A comment becomes spaces and a directive an empty line, so every
token keeps the line and column it has in the source; an include is replaced by the header between
line markers. Anything else (function-like macros, #if, other headers, line continuations) is
refused with a rule: this code never guesses what a directive would have done.

`PFC_CHECK` is defined, which selects the branch of `pfc.h` and `pfc_rt.h` that declares instead of
erasing. An ordinary compiler, without it, reads the other branch of the same headers.
"""

import re
from collections.abc import Mapping
from typing import NoReturn

from pfc2.core.config import MAX_PREPROCESSED_BYTES
from pfc2.core.diagnostics import FrontendError, SourceLocation

PREDEFINED = ("PFC_CHECK",)
MAX_INCLUDE_DEPTH = 4
_DIRECTIVE = re.compile(r"\s*#\s*([A-Za-z_]*)\s*(.*?)\s*$")
_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_INCLUDE = re.compile(r'"([^"]+)"|<([^>]+)>')
# Literals and numbers are tokens of their own, so a macro named like a suffix or a hex digit never rewrites one.
_TOKEN = re.compile(
    r'"(?:[^"\\\n]|\\.)*"|\'(?:[^\'\\\n]|\\.)*\'|\.?[0-9](?:[eEpP][+-]|[A-Za-z0-9_.])*|[A-Za-z_][A-Za-z0-9_]*'
)
# Words whose meaning a macro may not change: C's own and the ones PFC2 adds.
KEYWORDS = frozenset(
    """auto break case char const continue default do double else enum extern float for goto if inline int long
    register restrict return short signed sizeof static struct switch typedef union unsigned void volatile while
    _Bool requires ensures result invariant decreases assert where separated law main
    REQUIRES ENSURES INVARIANT ASSERT SEPARATED RESULT""".split()
)


def _fail(rule: str, message: str, filename: str, line: int) -> NoReturn:
    raise FrontendError(rule, message, SourceLocation(filename, line))


def strip_comments(text: str, filename: str) -> str:
    """Replace every comment by spaces, keeping newlines; literals are left alone."""
    output = list(text)
    index, line = 0, 1
    while index < len(text):
        character = text[index]
        if character == "\n":
            line += 1
        elif character in "\"'":
            index += 1
            while index < len(text) and text[index] not in (character, "\n"):
                index += 2 if text[index] == "\\" else 1
        elif text.startswith("//", index):
            end = text.find("\n", index)
            end = len(text) if end < 0 else end
            output[index:end] = " " * (end - index)
            index = end
            continue
        elif text.startswith("/*", index):
            end = text.find("*/", index + 2)
            if end < 0:
                _fail("preprocess-comment", "this comment is never closed", filename, line)
            for position in range(index, end + 2):
                if output[position] != "\n":
                    output[position] = " "
            line += text.count("\n", index, end)
            index = end + 2
            continue
        index += 1
    return "".join(output)


class _Preprocessor:
    def __init__(self, headers: Mapping[str, str]) -> None:
        self.headers = headers
        self.macros: dict[str, str] = dict.fromkeys(PREDEFINED, "")
        self.output: list[str] = []

    def expand(self, line: str, hidden: frozenset[str] = frozenset()) -> str:
        """Replace macro names, then rescan each replacement with that name disabled, as the C preprocessor does."""

        def replace(match: re.Match[str]) -> str:
            token = match.group()
            if not (token[0].isalpha() or token[0] == "_") or token in hidden or token not in self.macros:
                return token
            return self.expand(self.macros[token], hidden | {token})

        return _TOKEN.sub(replace, line) if self.macros else line

    def define(self, rest: str, filename: str, number: int) -> None:
        name = _NAME.match(rest)
        if name is None:
            _fail("preprocess-unsupported", "#define needs a name", filename, number)
        if rest[name.end() : name.end() + 1] == "(":
            _fail(
                "preprocess-unsupported", "macros with parameters are not supported; write a function", filename, number
            )
        if name.group() in self.macros:
            _fail("preprocess-unsupported", f"{name.group()} is already defined", filename, number)
        if name.group() in KEYWORDS:
            _fail(
                "preprocess-unsupported",
                f"{name.group()} is a word of the language and cannot be a macro",
                filename,
                number,
            )
        self.macros[name.group()] = rest[name.end() :].strip()

    def include(self, rest: str, filename: str, number: int, depth: int) -> None:
        match = _INCLUDE.fullmatch(rest)
        name = (match.group(1) or match.group(2)) if match else None
        if name is None or name not in self.headers:
            known = ", ".join(sorted(self.headers)) or "none"
            _fail("preprocess-include", f"PFC2 reads only its own headers ({known})", filename, number)
        if depth >= MAX_INCLUDE_DEPTH:
            _fail("preprocess-include", "headers are nested too deeply", filename, number)
        self.output.append(f'# 1 "{name}"')
        self.file(self.headers[name], name, depth + 1)
        self.output.append(f'# {number + 1} "{filename}"')

    def file(self, text: str, filename: str, depth: int = 0) -> None:
        if "\\\n" in text:
            continued = text[: text.index("\\\n")].count("\n") + 1
            _fail("preprocess-unsupported", "line continuations are not supported", filename, continued)
        trigraph = re.search(r"\?\?[=/'()!<>-]", text)
        if trigraph is not None:
            where = text.count("\n", 0, trigraph.start()) + 1
            _fail(
                "preprocess-unsupported", "trigraphs are not supported: a C11 compiler replaces them", filename, where
            )
        active: list[bool] = []  # One entry per open conditional: is its current branch read?
        opened: list[int] = []
        for number, line in enumerate(strip_comments(text, filename).split("\n"), 1):
            directive = _DIRECTIVE.fullmatch(line) if line.lstrip().startswith("#") else None
            reading = all(active)
            if directive is None:
                self.output.append(self.expand(line) if reading else "")
                continue
            word, rest = directive.groups()
            included = False
            if word in {"ifdef", "ifndef"}:
                name = _NAME.fullmatch(rest)
                if name is None:
                    _fail("preprocess-conditional", f"#{word} needs one name", filename, number)
                active.append((rest in self.macros) == (word == "ifdef"))
                opened.append(number)
            elif word == "else":
                if not active or rest:
                    _fail("preprocess-conditional", "#else without #ifdef", filename, number)
                active[-1] = not active[-1]
            elif word == "endif":
                if not active or rest:
                    _fail("preprocess-conditional", "#endif without #ifdef", filename, number)
                active.pop()
                opened.pop()
            elif not reading:
                pass  # A directive in a branch that is not read is not interpreted.
            elif word == "define":
                self.define(rest, filename, number)
            elif word == "include":
                self.include(rest, filename, number, depth)
                included = True
            else:
                _fail("preprocess-unsupported", f"#{word or '?'} is not supported", filename, number)
            if not included:
                self.output.append("")
        if opened:
            _fail("preprocess-conditional", "#ifdef without #endif", filename, opened[-1])
        if self.output and self.output[-1] == "" and text.endswith("\n"):
            self.output.pop()  # The empty piece after the final newline.


def preprocess(text: str, filename: str, headers: Mapping[str, str]) -> str:
    """Return the text the surface passes read; positions in it are positions in `filename`."""
    if not all(character.isprintable() or character in "\n\t\r\f\v" for character in filename) or '"' in filename:
        raise FrontendError("preprocess-config", "invalid source name", SourceLocation("<input>"))
    reader = _Preprocessor(headers)
    reader.file(text, filename)
    output = "\n".join(reader.output) + "\n"
    if len(output.encode("utf-8")) > MAX_PREPROCESSED_BYTES:
        raise FrontendError(
            "preprocess-size", "the program with its headers exceeds the size limit", SourceLocation(filename)
        )
    return output
