"""Source text in, editor facts out: diagnostics, hover texts and symbols. Pure; no editor protocol here.

Everything comes from the one checking path (`frontend.load_text` then `check.check`), so the editor
can never disagree with the command line. Lines and columns are 1-based, as the checker reports them.
"""

import re
from dataclasses import dataclass
from typing import Literal

from pfc2 import frontend, report
from pfc2.check import check
from pfc2.core import ir
from pfc2.core.config import SOLVER_TIMEOUT_MS
from pfc2.core.diagnostics import FrontendError, SourceLocation
from pfc2.core.parse import SpecKind
from pfc2.core.target import Target
from pfc2.elaborate import Unit
from pfc2.gate import Certification, Level

STATIC_TARGET = Target("static LP64 layout (pfc2.lsp; no clang was queried)", "x86_64-pc-linux-gnu", 32, 64)
MARKER = re.compile(r'^\s*#\s*include\s*"pfc\.h"', re.MULTILINE)
_WORD = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
Severity = Literal["error", "warning", "hint"]
_ORDER = {"error": 0, "warning": 1, "hint": 2}


@dataclass(frozen=True)
class Diagnostic:
    line: int
    column: int
    end_column: int  # Exclusive.
    severity: Severity
    code: str
    message: str


@dataclass(frozen=True)
class Hover:
    line: int
    column: int
    end_column: int
    text: str  # Markdown.


@dataclass(frozen=True)
class Symbol:
    name: str
    kind: Literal["function", "law", "global"]
    line: int
    column: int


@dataclass(frozen=True)
class Analysis:
    applicable: bool  # False for a C file that is not a PFC2 source.
    accepted: bool | None  # None when the source itself was refused.
    diagnostics: tuple[Diagnostic, ...] = ()
    hovers: tuple[Hover, ...] = ()
    symbols: tuple[Symbol, ...] = ()


class _Source:
    def __init__(self, text: str) -> None:
        self.lines = text.split("\n")

    def span(self, line: int | None, column: int | None) -> tuple[int, int, int]:
        """The identifier at a position, or one character; whole first word when the column is unknown."""
        row = min(max(line or 1, 1), len(self.lines))
        text = self.lines[row - 1]
        start = column if column is not None else len(text) - len(text.lstrip()) + 1
        start = min(max(start, 1), max(len(text), 1))
        word = _WORD.match(text, start - 1)
        return row, start, (word.end() + 1) if word else start + 1

    def word(self, line: int, name: str) -> tuple[int, int, int]:
        """Where `name` stands on a line, falling back to the start of the line."""
        text = self.lines[line - 1] if 0 < line <= len(self.lines) else ""
        found = re.search(rf"\b{re.escape(name)}\b", text)
        return self.span(line, found.start() + 1 if found else None)


def _at(source: _Source, where: SourceLocation, severity: Severity, code: str, message: str) -> Diagnostic:
    line, column, end = source.span(where.line, where.column)
    return Diagnostic(line, column, end, severity, code, message)


def _refusal(source: _Source, unit: Unit, certification: Certification) -> list[Diagnostic]:
    """Errors of a refused file: its unproved obligations, or the contract that made it refusable."""
    primary = [b for b in certification.blockers if not b.status.startswith("depends")]
    found = []
    for external in certification.proof.external_results:
        if external.consistent != "sat" or external.total == "partial":
            found.append(_at(source, external.query.location, "error", "contract", certification.reason))
    for entry in certification.proof.entry_results:
        if entry.status != "sat":
            found.append(_at(source, entry.query.location, "error", "contract", certification.reason))
    for blocker in primary:
        message = f"{report.MEANING.get(blocker.kind, blocker.kind)} [{blocker.status}]. Cannot prove: {blocker.goal}"
        example = report.values(blocker)
        found.append(
            _at(
                source,
                blocker.location,
                "error",
                blocker.kind,
                message + (f". For example: {example}" if example else ""),
            )
        )
    if not found:
        found.append(_at(source, SourceLocation(unit.filename, 1, 1), "error", "refused", certification.reason))
    return found


def _loops(source: _Source, unit: Unit) -> tuple[list[Diagnostic], list[Hover]]:
    diagnostics, hovers = [], []
    inferred = {(item.function, item.line): item.invariant for item in unit.inferred}
    measured = {(m.function, m.anchor.line): m.predicate for m in unit.measures}
    for site in unit.loop_sites:
        line, column, end = source.span(site.line, None)
        key = (site.function, site.line)
        facts = []
        if key in inferred:
            message = f"inferred and proved: {inferred[key]}"
            diagnostics.append(Diagnostic(line, column, end, "hint", "inferred", message))
            facts.append(f"Inferred invariant, proved: `{inferred[key]}`")
        if key in measured:
            facts.append(f"This loop terminates: the measure `{measured[key]}` is proved to decrease.")
        else:
            message = "termination is not claimed for this loop; add decreases(measure) to prove it"
            diagnostics.append(Diagnostic(line, column, end, "hint", "termination", message))
            facts.append("Loop termination is not claimed (no `decreases`).")
        hovers.append(Hover(line, column, end, "\n\n".join(facts)))
    return diagnostics, hovers


def _functions(source: _Source, unit: Unit, certification: Certification) -> tuple[list[Hover], list[Symbol]]:
    laws = {law.name for law in unit.laws}
    functions = [f for f in unit.program.functions if not f.name.startswith("pfc2_str_")]
    starts = sorted(f.location.line for f in unit.program.functions)
    hovers, symbols = [], []
    for item in unit.program.globals:
        line, column, _ = source.word(item.symbol.location.line, item.symbol.name)
        symbols.append(Symbol(item.symbol.name, "global", line, column))
    for function in functions:
        if function.location.file != unit.filename:
            continue  # Declared in a header.
        name = "main" if function.name == "pfc2_main" else function.name
        line, column, end = source.word(function.location.line, name)
        symbols.append(Symbol(name, "law" if function.name in laws else "function", line, column))
        after = [start for start in starts if start > function.location.line]
        last = after[0] if after else len(source.lines) + 1
        inside = [
            r
            for r in certification.proof.results
            if r.obligation.location.file == unit.filename
            and function.location.line <= r.obligation.location.line < last
        ]
        words = {SpecKind.REQUIRES: "requires", SpecKind.ENSURES: "ensures"}
        contract = [
            f"{words[c.kind]} `{ir.render_expression(c.condition)}`" for c in function.contracts if c.kind in words
        ]
        kind = (
            "law" if function.name in laws else "declared function (not verified)" if function.external else "function"
        )
        proved = sum(r.status == "proved" for r in inside)
        text = [f"**{name}** — {kind}", *contract]
        if not function.external:
            text.append(f"obligations proved: {proved} of {len(inside)}")
        hovers.append(Hover(line, column, end, "\n\n".join(text)))
    return hovers, symbols


def _sites(source: _Source, certification: Certification) -> list[Hover]:
    names = {
        "bounds": "bounds check",
        "division": "division check",
        "overflow": "overflow check",
        "conversion": "range check",
    }
    hovers = []
    for decision in (*certification.emission.decisions, *certification.emission.overflow):
        line, column, end = source.span(decision.location.line, decision.location.column)
        state = "removed: proved for every input" if decision.removed else f"kept at run time ({decision.reason})"
        hovers.append(Hover(line, column, end, f"{names[decision.kind]} {state}"))
    return hovers


def analyze(
    text: str,
    name: str,
    *,
    level: Level = "full",
    timeout_ms: int = SOLVER_TIMEOUT_MS,
    target: Target = STATIC_TARGET,
) -> Analysis:
    """Check one document. A source the checker refuses is an analysis with one error, never an exception."""
    if not MARKER.search(text):
        return Analysis(False, None)
    source = _Source(text)
    try:
        unit, certification = check(frontend.load_text(text, name), target, level=level, timeout_ms=timeout_ms)
    except FrontendError as error:
        problem = error.diagnostic
        where = problem.location if problem.location.file == name else SourceLocation(name, 1, 1)
        return Analysis(True, None, (_at(source, where, "error", problem.rule, problem.message),))
    diagnostics = [] if certification.accepted else _refusal(source, unit, certification)
    for trap in certification.retained_traps:
        message = "overflow is not proved here; the emitted C keeps a runtime trap"
        diagnostics.append(_at(source, trap.location, "warning", "overflow-trap", message))
    loop_diagnostics, loop_hovers = _loops(source, unit)
    function_hovers, symbols = _functions(source, unit, certification)
    diagnostics += loop_diagnostics
    diagnostics.sort(key=lambda d: _ORDER[d.severity])
    hovers = (*function_hovers, *loop_hovers, *_sites(source, certification))
    return Analysis(True, certification.accepted, tuple(diagnostics), hovers, tuple(symbols))


def hover_at(analysis: Analysis, line: int, column: int) -> Hover | None:
    """The narrowest hover that covers a 1-based position; several facts at one place are joined."""
    covering = [h for h in analysis.hovers if h.line == line and h.column <= column < h.end_column]
    if not covering:
        return None
    width = min(h.end_column - h.column for h in covering)
    narrow = [h for h in covering if h.end_column - h.column == width]
    return Hover(line, narrow[0].column, narrow[0].end_column, "\n\n".join(dict.fromkeys(h.text for h in narrow)))
