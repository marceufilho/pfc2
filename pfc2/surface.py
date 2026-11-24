"""Surface pass for the two words added to the C subset: `law` and `where(predicate)`.

Input is preprocessed text. Every `where(...)` is recorded with its binder and source position, blanked
in place (so the declaration keeps its line and column) and restated as a marker statement the
frozen frontend already understands:

    parameter  `long n where(p)`         ->  `__spec_requires((p));` after the body's `{`
    result     `long f(...) where(p)`    ->  `__spec_ensures((p));`  after the body's `{`
    local      `long i where(p) = e;`    ->  `__spec_assert((p));`   after the declaration's `;`

A `law name(parameters) { ... }` at file scope is a property proved for every input: its typed
parameters are the hypotheses and its `assert`s the conclusions. It becomes an ordinary function
(`long name(...) { ...; return 0; }`) that the checker verifies and the emitter never prints.

A proof may also arrive as data: one invariant per loop, in source order, written into the loop
body as `__spec_invariant((p));`. It is text checked by `bundle.py`, never code that runs.

Nothing here decides a proof: each marker becomes an obligation that the frozen checker must
discharge. A mistake in this pass can make a proof fail or state a different law; it cannot turn
an unproved formula into a proved one.
"""

from dataclasses import dataclass
from typing import Literal

from pfc2.core.diagnostics import FrontendError, SourceLocation
from pfc2.text import IDENTIFIER as _IDENTIFIER
from pfc2.text import Shift, SourceText

KEYWORD = "where"
LAW = "law"
Kind = Literal["parameter", "result", "local"]
_NOT_A_BINDER = frozenset(
    "auto break case char const continue default do double else enum extern float for goto if inline int long "
    "register restrict return short signed sizeof static struct switch typedef union unsigned void volatile while "
    "_Bool bool".split()
)
_MARKER = {"parameter": "__spec_requires", "result": "__spec_ensures", "local": "__spec_assert"}


@dataclass(frozen=True)
class Where:
    kind: Kind
    function: str
    binder: str
    predicate: str
    location: SourceLocation  # The `where` token.
    binder_line: int


@dataclass(frozen=True)
class Law:
    name: str
    text: str  # Source of the whole law, white space normalized.
    location: SourceLocation


@dataclass(frozen=True)
class Loop:
    function: str
    line: int


@dataclass(frozen=True)
class Surface:
    text: str
    wheres: tuple[Where, ...]
    laws: tuple[Law, ...] = ()
    loops: tuple[Loop, ...] = ()
    shifts: tuple[Shift, ...] = ()  # Where this pass inserted text.


class _Scanner(SourceText):
    def __init__(self, text: str, filename: str, invariants: tuple[str, ...] | None = None) -> None:
        super().__init__(text, filename)
        self.invariants = invariants
        self.loops: list[Loop] = []
        self.output = list(text)
        self.insertions: list[tuple[int, str]] = []
        self.definitions: list[Where] = []
        self.prototypes: list[Where] = []
        self.laws: list[Law] = []

    def _function_of(self, closing: int) -> tuple[str, int] | None:
        """Name before the parenthesis matching the `)` at `closing`."""
        depth, index = 0, closing
        while index >= 0:
            if self.text[index] == ")":
                depth += 1
            elif self.text[index] == "(":
                depth -= 1
                if depth == 0:
                    return self.identifier_before(index)
            index -= 1
        return None

    def _loop(self, keyword: int, closing: int, function: str) -> None:
        """Record the loop whose header ends at `closing`; place its supplied invariant in the body."""
        self.loops.append(Loop(function, self.locate(keyword).line))
        if self.invariants is None:
            return
        body = closing + 1
        while body < len(self.text) and self.text[body] in " \t\n":
            body += 1
        if body >= len(self.text) or self.text[body] != "{":
            self.fail("proof-shape", "a supplied invariant needs a loop body in braces", keyword)
        if self.text[body + 1 :].lstrip().startswith("__spec_invariant"):
            self.fail(
                "proof-shape", "this loop already has a handwritten INVARIANT; the proof cannot replace it", keyword
            )
        if len(self.loops) > len(self.invariants):
            self.fail(
                "proof-shape", f"the proof has {len(self.invariants)} invariant(s) but there are more loops", keyword
            )
        self.insertions.append((body + 1, f" __spec_invariant(({self.invariants[len(self.loops) - 1]}));"))

    def run(self) -> Surface:
        text = self.text
        braces = 0
        parentheses: list[int] = []
        function = ""  # Name before the most recent file-scope parameter list.
        signature: list[Where] = []  # Parameter/result types waiting for `{` or `;`.
        locals_: list[tuple[Where, int]] = []  # Local types waiting for the declaration's `;`.
        law: tuple[str, int] | None = None  # Name and start offset of the law being read.
        law_open = False
        headers: list[tuple[int, int]] = []  # (parenthesis depth, keyword offset) of loop headers being read.
        index = 0
        while index < len(text):
            character = text[index]
            if character == "#" and (index == 0 or text[index - 1] == "\n"):
                index = text.find("\n", index)
                index = len(text) if index < 0 else index
                continue
            if character in "\"'":
                index = self.skip_literal(index)
                continue
            if character == "(":
                if braces == 0 and not parentheses:
                    named = self.identifier_before(index)
                    function = named[0] if named else ""
                parentheses.append(index)
            elif character == ")":
                if parentheses:
                    parentheses.pop()
                if headers and headers[-1][0] == len(parentheses):
                    self._loop(headers.pop()[1], index, function)
            elif character == "{":
                if locals_:
                    self.fail("where-position", "a typed local must be one declaration ending in ';'", index)
                if braces == 0 and parentheses and signature:
                    self.fail("where-syntax", "unbalanced parentheses before the function body", parentheses[-1])
                if braces == 0 and signature:
                    markers = sorted(signature, key=lambda item: item.kind != "parameter")
                    self.insertions.append(
                        (index + 1, "".join(f" {_MARKER[item.kind]}(({item.predicate}));" for item in markers))
                    )
                    self.definitions.extend(signature)
                    signature = []
                if braces == 0 and law is not None:
                    law_open = True
                braces += 1
            elif character == "}":
                if locals_:
                    self.fail("where-position", "a typed local must be one declaration ending in ';'", index)
                braces = max(0, braces - 1)
                if braces == 0 and law is not None and law_open:
                    self.insertions.append((index, " return 0; "))
                    source = " ".join(text[law[1] : index + 1].split())
                    self.laws.append(Law(law[0], source, self.locate(law[1])))
                    law, law_open = None, False
            elif character == ";":
                if braces == 0 and not parentheses and law is not None:
                    self.fail("law-syntax", "a law has a body: law name(parameters) { ... }", law[1])
                if braces == 0 and not parentheses and signature:
                    self.prototypes.extend(signature)
                    signature = []
                ready = [item for item, depth in locals_ if depth == braces] if not parentheses else []
                if ready:
                    self.insertions.append(
                        (index + 1, "".join(f" {_MARKER['local']}(({item.predicate}));" for item in ready))
                    )
                    self.definitions.extend(ready)
                    locals_ = []
            elif character.isalpha() or character == "_":
                match = _IDENTIFIER.match(text, index)
                assert match is not None
                if match.group() in {"while", "for"} and braces:
                    headers.append((len(parentheses), index))
                elif match.group() == LAW:
                    start = match.end()
                    while start < len(text) and text[start] in " \t\n":
                        start += 1
                    following = _IDENTIFIER.match(text, start)
                    misplaced = braces or parentheses or law is not None
                    if misplaced or following is None or following.group() in _NOT_A_BINDER:
                        self.fail("law-syntax", "`law` is reserved: write law name(parameters) { ... }", index)
                    law = (following.group(), index)
                    self.output[index : match.end()] = ["l", "o", "ng"]
                elif match.group() == KEYWORD:
                    predicate, closing = self.argument(index, len(KEYWORD), "where-syntax", KEYWORD)
                    item = self._where(index, predicate, braces, parentheses, function)
                    if item.kind == "local":
                        locals_.append((item, braces))
                    else:
                        signature.append(item)
                    for position in range(index, closing + 1):
                        if self.output[position] != "\n":
                            self.output[position] = " "
                    index = closing + 1
                    continue
                index = match.end()
                continue
            index += 1
        if signature or locals_:
            pending = signature[0] if signature else locals_[0][0]
            raise FrontendError("where-position", "where() is not attached to a complete declaration", pending.location)
        if law is not None:
            self.fail("law-syntax", "a law has a body: law name(parameters) { ... }", law[1])
        if self.invariants is not None and len(self.invariants) != len(self.loops):
            raise FrontendError(
                "proof-shape",
                f"the proof has {len(self.invariants)} invariant(s) for {len(self.loops)} loop(s)",
                SourceLocation(self.filename),
            )
        self._check_prototypes()
        output = self.output
        for offset, inserted in sorted(self.insertions, reverse=True):
            output[offset:offset] = list(inserted)
        shifts = self.shifts(self.insertions)
        return Surface("".join(output), tuple(self.definitions), tuple(self.laws), tuple(self.loops), shifts)

    def _where(self, offset: int, predicate: str, braces: int, parentheses: list[int], function: str) -> Where:
        location = self.locate(offset)
        before = offset
        while before > 0 and self.text[before - 1] in " \t\n\r\f\v":
            before -= 1
        previous = self.text[before - 1] if before else ""
        if previous == ")":
            named = self._function_of(before - 1)
            if braces or parentheses or named is None or named[0] in _NOT_A_BINDER:
                self.fail("where-position", "after ')' where() is a result type and belongs to a function", offset)
            return Where("result", named[0], named[0], predicate, location, self.locate(named[1]).line)
        binder = self.identifier_before(offset)
        if binder is None or binder[0] in _NOT_A_BINDER:
            message = "where() follows the name it types: `long n where(0 <= n)`"
            if previous == "]":
                message = "element types on arrays are not supported yet; state the property on a scalar"
            self.fail("where-position", message, offset)
        name, start = binder
        line = self.locate(start).line
        if braces == 0:
            if not parentheses or not function or function in _NOT_A_BINDER:
                self.fail("where-position", "file-scope variables are outside the subset", offset)
            if len(parentheses) != 1:
                self.fail("where-position", "where() types a parameter, not part of an expression", offset)
            return Where("parameter", function, name, predicate, location, line)
        if parentheses:
            self.fail("where-position", "declare the typed variable before the loop, not inside for(...)", offset)
        return Where("local", function, name, predicate, location, line)

    def _check_prototypes(self) -> None:
        def key(items: list[Where], function: str) -> list[tuple[str, str, str]]:
            return sorted((w.kind, w.binder, w.predicate) for w in items if w.function == function)

        for item in self.prototypes:
            if key(self.prototypes, item.function) != key(
                [w for w in self.definitions if w.kind != "local"], item.function
            ):
                raise FrontendError(
                    "where-mismatch",
                    f"types on the declaration of {item.function} differ from its definition in this file",
                    item.location,
                )


def extract(text: str, filename: str, *, invariants: tuple[str, ...] | None = None) -> Surface:
    """Restate laws, types and supplied invariants as contract marker statements."""
    return _Scanner(text, filename, invariants).run()
