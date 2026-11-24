"""Host models for the interpreter: Python stand-ins for the unverified C a program is linked with.

`ConsoleHost` models `pfc2/runtime/pfc_rt.c`. It is written from that file's comments and the C library's
documented behaviour, independently of the compiler; a test runs the example programs through both.
"""

import re
from collections.abc import Sequence

from pfc2_eval.interpret import Argument, Host

LINE_BUFFER = 4096  # PFC_RT_LINE: fgets reads at most this many bytes minus one per call.
STRING = re.compile(r"pfc2_str_(\d+)")


def _unescape(token: str) -> str:
    """The text of a C string literal token with the simple escapes."""
    simple = {"n": "\n", "t": "\t", "r": "\r", "0": "\0", "\\": "\\", "'": "'", '"': '"', "a": "\a", "b": "\b"}
    body, out, index = token[1:-1], [], 0
    while index < len(body):
        if body[index] == "\\" and index + 1 < len(body) and body[index + 1] in simple:
            out.append(simple[body[index + 1]])
            index += 2
        else:
            out.append(body[index])
            index += 1
    return "".join(out)


class ConsoleHost(Host):
    """Standard input and output as `pfc_rt.c` uses them. A string is a handle: an index into `self.texts`."""

    def __init__(self, strings: Sequence[str] = (), stdin: str = "") -> None:
        super().__init__()
        self.texts = [""] + [_unescape(token) for token in strings]  # Handle K is literal K; 0 is unused.
        self.pending = stdin

    def _line(self) -> str | None:
        """What one fgets call returns: up to a newline (kept) or the buffer limit; None at end of input."""
        if not self.pending:
            return None
        end = self.pending.find("\n")
        cut = len(self.pending) if end < 0 else end + 1
        cut = min(cut, LINE_BUFFER - 1)
        line, self.pending = self.pending[:cut], self.pending[cut:]
        return line

    def _text(self, handle: Argument) -> str:
        if not isinstance(handle, int) or not 0 < handle < len(self.texts):
            raise ValueError("not a string handle of this run")
        return self.texts[handle]

    def call(self, name: str, arguments: Sequence[Argument]) -> int | None:
        literal = STRING.fullmatch(name)
        if literal is not None:
            return int(literal.group(1))
        if name == "print_int":
            self.output.append(str(arguments[0]))
        elif name == "print_str":
            self.output.append(self._text(arguments[0]))
        elif name == "println":
            self.output.append("\n")
        elif name == "println_str":
            self.output.append(self._text(arguments[0]) + "\n")
        elif name == "read_line":
            line = self._line() or ""
            self.texts.append(re.split(r"[\r\n]", line, maxsplit=1)[0])
            return len(self.texts) - 1
        elif name == "read_int":
            text = self._line()
            if text is None:
                return 0
            # strtol: optional white space, an optional sign, digits. The runtime then accepts the number only
            # if the next character ends the line.
            match = re.match(r"[ \t\n\v\f\r]*([+-]?\d+)", text)
            if match is None or text[match.end() : match.end() + 1] not in {"", "\n", "\r"}:
                return 0
            return max(-(2**63), min(2**63 - 1, int(match.group(1))))  # strtol saturates; errno is not checked.
        elif name == "str_eq":
            return int(self._text(arguments[0]) == self._text(arguments[1]))
        else:
            return None
        return 0
