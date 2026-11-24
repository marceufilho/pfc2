"""PFC2 as one pure function over source text, for callers that cannot spawn a process (the site's playground).

It runs the same path as the command line (`frontend.load_text`, `check.check`, `proof.build`) with one
declared difference: the integer layout is the fixed LP64 one below instead of the one clang reports.
Nothing computed here is evidence of anything; it is a live run on the reader's machine.
"""

import sys
from typing import Any

from pfc2 import frontend, proof, report
from pfc2.check import check
from pfc2.core import ir, smt
from pfc2.core.diagnostics import FrontendError
from pfc2.core.target import Target
from pfc2.gate import LEVELS

ENGINE = "pfc2-web-v1"
STATIC_TARGET = Target("static LP64 layout (pfc2.web; no clang was queried)", "x86_64-pc-linux-gnu", 32, 64)
MAX_SOURCE_BYTES = 16 * 1024
DEFAULT_TIMEOUT_MS = 5_000
MAX_TIMEOUT_MS = 10_000
Result = dict[str, Any]


def provenance(timeout_ms: int) -> Result:
    return {
        "engine": ENGINE,
        "target": {"triple": STATIC_TARGET.triple, "int_bits": 32, "long_bits": 64, "source": STATIC_TARGET.compiler},
        "z3": smt.solver_version(),
        "python": sys.version.split()[0],
        "platform": sys.platform,
        "timeout_ms": timeout_ms,
    }


def _refusal(rule: str, message: str, name: str, line: int | None, column: int | None, timeout_ms: int) -> Result:
    diagnostic = {"rule": rule, "message": message, "file": name, "line": line, "column": column}
    return {"ok": False, "diagnostic": diagnostic, "provenance": provenance(timeout_ms)}


def analyze(
    source: object, *, name: object = "program.c", level: object = "full", timeout_ms: object = DEFAULT_TIMEOUT_MS
) -> Result:
    """Check one program; a refusal of the input is data (`ok: False`), never an exception."""
    budget = timeout_ms if type(timeout_ms) is int and 1 <= timeout_ms <= MAX_TIMEOUT_MS else None
    shown = name if isinstance(name, str) and name.isprintable() and 0 < len(name) <= 100 and "/" not in name else None
    if budget is None or shown is None or level not in LEVELS or not isinstance(source, str):
        return _refusal(
            "engine-usage",
            "expected source text, a short file name, a level and a timeout",
            "<input>",
            None,
            None,
            DEFAULT_TIMEOUT_MS,
        )
    if len(source.encode("utf-8")) > MAX_SOURCE_BYTES:
        return _refusal(
            "engine-size", f"the playground accepts up to {MAX_SOURCE_BYTES} bytes", shown, None, None, budget
        )
    try:
        elaborated = frontend.load_text(source, shown)
        unit, certification = check(elaborated, STATIC_TARGET, level=level, timeout_ms=budget)
    except FrontendError as error:
        where = error.diagnostic.location
        return _refusal(error.diagnostic.rule, error.diagnostic.message, where.file, where.line, where.column, budget)
    record = proof.build(unit, certification)
    blockers = [
        {
            "kind": blocker.kind,
            "meaning": report.MEANING.get(blocker.kind, blocker.kind),
            "line": blocker.location.line,
            "column": blocker.location.column,
            "status": blocker.status,
            "goal": blocker.goal,
            "example": report.values(blocker),
        }
        for blocker in certification.blockers
    ]
    return {
        "ok": True,
        "accepted": certification.accepted,
        "level": certification.level,
        "reason": certification.reason,
        "memory_would_pass": certification.memory_would_pass,
        "report": report.render(unit, certification, record),
        "blockers": blockers,
        "c": certification.c,
        "elaborated": ir.print_c(unit.program),
        "record": record,
        "provenance": provenance(budget),
    }


def summary(result: Result) -> Result:
    """What two runs of the same program must agree on, whatever machine they ran on."""
    if not result["ok"]:
        return {"ok": False, "diagnostic": result["diagnostic"]}
    record = result["record"]
    return {
        "ok": True,
        "accepted": result["accepted"],
        "reason": result["reason"],
        "obligations": [[o["id"], o["status"]] for o in record["obligations"]],
        "entry": [[e["function"], e["status"]] for e in record["entry"]],
        "guards": [[g["line"], g["column"], g["removed"]] for g in record["guards"]],
        "overflow": [[g["line"], g["column"], g["removed"]] for g in record["overflow"]],
        "inferred": record["inferred"],
        "c_sha256": record["c_sha256"],
    }
