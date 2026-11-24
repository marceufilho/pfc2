"""Clean clause spelling, restated as the contract markers the core front end reads.

    long f(long n) requires(p) ensures(q) { ... }   ->  `{ __spec_requires((p)); __spec_ensures((q));`
    while (c) invariant(i) { ... }                  ->  `{ __spec_invariant((i));`
    while (c) decreases(e) { ... }                  ->  `{ __spec_assert((0 <= (e)));`, completed by elaboration
    assert(p);                                      ->  `__spec_assert(p);`
    long f(long x) requires(p) ensures(q);          ->  a placeholder body that carries the contract; the
                                                        function is reported as external (declared, not verified)
    "text"                                          ->  `pfc2_str_K()`, an external function that returns the string
    int main(void)                                  ->  `long pfc2_main(void)`; the release adds the C entry point
    result (inside ensures)                         ->  `RESULT`
    separated(a, b) (inside requires)               ->  `__spec_separated(a, b)`; lowering adds the lengths

A clause is blanked where it stands and restated after the `{` on the same line, so every other
token keeps its line and column. The position of each clause is returned, and elaboration gives
it to the contract it became. This pass decides nothing: every marker is an obligation.
"""

import re
from dataclasses import dataclass
from typing import Literal

from pfc2.core.diagnostics import FrontendError, SourceLocation
from pfc2.text import IDENTIFIER, Shift, SourceText

ClauseKind = Literal["requires", "ensures", "invariant", "decreases"]
SIGNATURE = ("requires", "ensures")
LOOP = ("invariant", "decreases")
_RESULT = re.compile(r"\bresult\b")
_SEPARATED = re.compile(r"\bseparated\b(?=\s*\()")


@dataclass(frozen=True)
class Clause:
    kind: ClauseKind
    function: str
    predicate: str
    location: SourceLocation  # The clause word.
    anchor: SourceLocation  # The loop keyword for a loop clause, else the clause itself.


@dataclass(frozen=True)
class Clauses:
    text: str
    clauses: tuple[Clause, ...]
    externals: tuple[str, ...] = ()  # Functions declared and not defined, strings excluded.
    strings: tuple[str, ...] = ()  # String literal tokens; number K is returned by pfc2_str_K.
    entry: bool = False  # The file has `int main(void)`.
    shifts: tuple[Shift, ...] = ()  # Where this pass inserted text; see `text.moved`.


MARKERS = {
    "assert": "__spec_assert",
    "ASSERT": "__spec_assert",
    "REQUIRES": "__spec_requires",
    "ENSURES": "__spec_ensures",
    "INVARIANT": "__spec_invariant",
    "SEPARATED": "__spec_separated",
}
RESERVED = ("pfc2_", "pfc_")  # Names the surface passes and the emitter generate.
ENTRY = "pfc2_main"
STRING = "pfc2_str_"


def _marker(clause: Clause) -> str:
    return f"__spec_{clause.kind}(({clause.predicate}));"


class _Rewriter(SourceText):
    def __init__(self, text: str, filename: str) -> None:
        super().__init__(text, filename)
        self.output = list(text)
        self.insertions: list[tuple[int, str]] = []
        self.clauses: list[Clause] = []
        self.declared: dict[str, list[tuple[Clause, ...]]] = {}
        self.defined: dict[str, tuple[Clause, ...]] = {}
        self.semicolon: dict[str, int] = {}  # Function -> the `;` of its last declaration.
        self.strings: list[str] = []
        self.entry = False

    def blank(self, start: int, end: int) -> None:
        for position in range(start, end + 1):
            if self.output[position] != "\n":
                self.output[position] = " "

    def clause(self, kind: ClauseKind, word: int, function: str, anchor: int) -> tuple[Clause, int]:
        predicate, closing = self.argument(word, len(kind), "clause-syntax", kind)
        if kind == "ensures":
            predicate = _RESULT.sub("RESULT", predicate)
        if kind == "requires":
            predicate = _SEPARATED.sub("__spec_separated", predicate)
        self.blank(word, closing)
        return Clause(kind, function, predicate, self.locate(word), self.locate(anchor)), closing

    def loop_markers(self, pending: list[Clause]) -> list[str]:
        """One invariant marker (the conjunction) first, then the marker that carries the measure."""
        invariants = [item for item in pending if item.kind == "invariant"]
        measures = [item for item in pending if item.kind == "decreases"]
        if len(measures) > 1:
            raise FrontendError("clause-syntax", "a loop has one decreases(measure)", measures[1].location)
        markers = [_marker(item) for item in invariants]
        if len(invariants) > 1:
            joined = " && ".join(f"({item.predicate})" for item in invariants)
            markers = [f"__spec_invariant(({joined}));"]
        return markers + [f"__spec_assert((0 <= ({item.predicate})));" for item in measures]

    def run(self) -> Clauses:
        text = self.text
        braces, parentheses = 0, 0
        function = ""  # Name before the most recent file-scope parameter list.
        signature: list[Clause] = []  # Clauses waiting for the `{` or `;` of their function.
        tail = -1  # Offset of the `)` a clause may follow: end of a signature, a loop head or a clause.
        loop: list[Clause] = []  # Clauses waiting for the `{` of their loop.
        loop_keyword = -1
        headers: list[tuple[int, int]] = []  # (parenthesis depth, keyword offset) of loop heads being read.
        unit, boundary = 0, True  # Start of the file-scope declaration being read.
        index = 0
        while index < len(text):
            character = text[index]
            if character == "#" and self.starts_line(index):
                index = self.skip_directive(index)
                continue
            if boundary and braces == 0 and parentheses == 0 and character not in " \t\n\r\f\v":
                unit, boundary = index, False
            if character in "\"'":
                end = self.skip_literal(index)
                initializer = self.initializes_array(index)
                if character == '"' and braces and not initializer:
                    self.string(index, end, unit)
                index = end
                continue
            word = IDENTIFIER.match(text, index) if character.isalpha() or character == "_" else None
            if word is not None and word.group().startswith(RESERVED):
                self.fail("ir-name", "names starting with pfc_ or pfc2_ are reserved", index)
            if word is not None and word.group() == "int" and braces == 0 and parentheses == 0:
                index = self.main(index, word.end())
                continue
            follows = self.before(index) - 1 == tail and tail >= 0
            if word is not None and word.group() in SIGNATURE and braces == 0 and parentheses == 0 and follows:
                item, tail = self.clause(word.group(), index, function, index)  # type: ignore[arg-type]
                signature.append(item)
                index = tail + 1
                continue
            if word is not None and word.group() in LOOP and braces and parentheses == 0:
                opening = text[word.end() :].lstrip()[:1] == "("
                if follows and loop_keyword >= 0:
                    item, tail = self.clause(word.group(), index, function, loop_keyword)  # type: ignore[arg-type]
                    loop.append(item)
                    index = tail + 1
                    continue
                if opening and text[self.before(index) - 1] in ";{})":
                    self.fail("clause-position", "a loop clause goes between the loop head and its `{`", index)
            if character not in " \t\n\r\f\v":
                if loop and character != "{":
                    raise FrontendError(
                        "clause-position", "a loop with clauses needs its body in braces", loop[0].location
                    )
                if signature and character not in "{;" and not (word and word.group() == "where"):
                    raise FrontendError(
                        "clause-position", "a clause is followed by the function body or `;`", signature[0].location
                    )
            if word is not None:
                if word.group() in {"while", "for"} and braces:
                    headers.append((parentheses, index))
                elif word.group() in MARKERS and braces and text[word.end() :].lstrip()[:1] == "(":
                    # `assert`, and the older REQUIRES/ENSURES/INVARIANT/ASSERT/SEPARATED written in a body.
                    self.output[index : word.end()] = [MARKERS[word.group()]] + [""] * (word.end() - index - 1)
                index = word.end()
                continue
            if character == "(":
                if braces == 0 and parentheses == 0:
                    named = self.identifier_before(index)
                    if named is None or named[0] != "where":
                        function = named[0] if named else ""
                        function = ENTRY if function == "main" and self.entry else function
                parentheses += 1
            elif character == ")":
                parentheses = max(0, parentheses - 1)
                if braces == 0 and parentheses == 0:
                    tail = index
                if headers and headers[-1][0] == parentheses:
                    loop_keyword = headers.pop()[1]
                    tail = index
            elif character == "{":
                pending = signature if braces == 0 else loop
                if pending:
                    markers = [_marker(item) for item in pending]
                    if braces:
                        markers = self.loop_markers(pending)
                    self.insertions.append((index + 1, " " + " ".join(markers)))
                    self.clauses.extend(pending)
                if braces == 0 and function:
                    self.defined[function] = tuple(signature)
                signature, loop, tail = [], [], -1
                braces += 1
            elif character == "}":
                braces = max(0, braces - 1)
                tail = -1
                boundary = braces == 0
            elif character == ";":
                if braces == 0 and parentheses == 0 and function and self.before(index) - 1 == tail:
                    self.declared.setdefault(function, []).append(tuple(signature))
                    self.semicolon[function] = index
                    signature = []
                if parentheses == 0:
                    tail = -1
                    boundary = braces == 0
            index += 1
        if signature or loop:
            unattached = (signature or loop)[0]
            raise FrontendError("clause-position", "a clause is followed by a body in braces", unattached.location)
        externals = self._check_declarations()
        output = self.output
        for offset, inserted in sorted(self.insertions, reverse=True):
            output[offset:offset] = list(inserted)
        shifts = self.shifts(self.insertions)
        return Clauses("".join(output), tuple(self.clauses), externals, tuple(self.strings), self.entry, shifts)

    def initializes_array(self, quote: int) -> bool:
        """Is the string at `quote` the initial value of a declared char array (`char w[6] = "hello";`)?"""
        equals = self.before(quote) - 1
        if equals < 0 or self.text[equals] != "=" or self.text[self.before(equals) - 1 : self.before(equals)] != "]":
            return False
        start = max(self.text.rfind(mark, 0, equals) for mark in ";{}") + 1
        return re.match(r"\s*(const\s+)?char\b", self.text[start:equals]) is not None

    def string(self, start: int, end: int, unit: int) -> None:
        """A string literal in a function body becomes a call to the external function that returns it."""
        token = self.text[start:end]
        if token not in self.strings:
            self.strings.append(token)
            number = len(self.strings)
            self.insertions.append((unit, f"long {STRING}{number}(void) {{ return 0; }} "))
        self.output[start:end] = [f"{STRING}{self.strings.index(token) + 1}()"] + [""] * (end - start - 1)

    def main(self, start: int, end: int) -> int:
        """`int main(void)` is checked as `long pfc2_main(void)`; any other `int` is left for the subset rules."""
        position = end
        while position < len(self.text) and self.text[position] in " \t\n":
            position += 1
        name = IDENTIFIER.match(self.text, position)
        if name is None or name.group() != "main":
            return end
        self.entry = True
        self.output[start:end] = ["long"] + [""] * (end - start - 1)
        self.output[name.start() : name.end()] = [ENTRY] + [""] * (name.end() - name.start() - 1)
        return name.end()

    def _check_declarations(self) -> tuple[str, ...]:
        """Compare declarations with definitions; give each function that is only declared a placeholder body."""
        externals = []
        for function, declarations in self.declared.items():
            if function.startswith("__spec_"):
                continue
            if function not in self.defined:
                contract = declarations[-1]
                for declaration in declarations:
                    if declaration and [(c.kind, c.predicate) for c in declaration] != [
                        (c.kind, c.predicate) for c in contract
                    ]:
                        raise FrontendError(
                            "clause-mismatch",
                            f"the declarations of {function} state different contracts",
                            declaration[0].location,
                        )
                offset = self.semicolon[function]
                self.output[offset] = " "
                self.insertions.append((offset + 1, "{ " + " ".join(_marker(c) for c in contract) + " return 0; }"))
                self.clauses.extend(contract)
                externals.append(function)
                continue
            for declaration in declarations:
                stated = [(item.kind, item.predicate) for item in declaration]
                if stated and stated != [(item.kind, item.predicate) for item in self.defined[function]]:
                    raise FrontendError(
                        "clause-mismatch",
                        f"clauses on the declaration of {function} differ from its definition in this file",
                        declaration[0].location,
                    )
        return tuple(externals)


def rewrite(text: str, filename: str) -> Clauses:
    """Restate requires/ensures/invariant clauses and `assert` as contract markers."""
    return _Rewriter(text, filename).run()
