"""The compiler core must still agree with the thesis compiler on every program of that compiler's subset.

`tests/agreement/v5-reference.json` holds what the frozen `pfc` (freeze-v5) produced for 48 programs:
its preprocessed input, every obligation with its status, every decision about a check and the emitted
code without comments. It was recorded once, from the thesis repository, and is never regenerated from
PFC2. Differences PFC2 introduced on purpose are listed in `INTENDED`, each with its reason.
"""

import json
import re
from pathlib import Path
from typing import Any

import pytest

from pfc2.core import emit, lower, parse, smt
from pfc2.core.diagnostics import FrontendError
from pfc2.core.target import Target

REFERENCE = json.loads((Path(__file__).parent / "agreement" / "v5-reference.json").read_text(encoding="utf-8"))
PROGRAMS = REFERENCE["programs"]
TARGET = Target("static LP64 layout (agreement test)", "x86_64-pc-linux-gnu", 32, 64)
COMMENT = re.compile(r"//.*$|/\*.*?\*/", re.MULTILINE | re.DOTALL)
# program -> reason PFC2 is allowed to differ there.
INTENDED: dict[str, str] = {
    "tests/negative/increment.c": "PFC2 accepts ++ as a statement and spells it as an explicit assignment",
    "tests/negative/local-array.c": "still refused (no initializer), by the rule of the new local arrays (0064)",
    "tests/negative/break.c": "PFC2 accepts break inside a loop (decision 0064)",
    "tests/negative/continue.c": "PFC2 accepts continue inside a loop (decision 0064)",
}


def _site(decision: Any) -> list[object]:
    return [decision.kind, decision.location.line, decision.location.column, decision.removed]


def _summary(text: str, filename: str) -> dict[str, object]:
    try:
        program = lower.lower(parse.parse_preprocessed(text, filename))
        report = smt.check(program, TARGET)
        emission = emit.emit(program, TARGET, mode="verified", proof=report)
    except FrontendError as problem:
        location = problem.diagnostic.location
        return {"refused": [problem.diagnostic.rule, location.line, location.column]}
    return {
        "obligations": [
            [
                r.obligation.kind,
                r.obligation.category,
                r.obligation.location.line,
                r.obligation.location.column,
                r.status,
            ]
            for r in report.results
        ],
        "entry": [[r.query.function, r.status] for r in report.entry_results],
        "required_passed": report.required_passed,
        "decisions": [_site(d) for d in emission.decisions],
        "overflow": [_site(d) for d in emission.overflow],
        "c": COMMENT.sub("", emission.c),
    }


def test_the_reference_covers_the_frozen_subset() -> None:
    assert len(PROGRAMS) == 48 and all("summary" in program for program in PROGRAMS)
    assert set(INTENDED) <= {program["name"] for program in PROGRAMS}


@pytest.mark.integration
@pytest.mark.parametrize("program", PROGRAMS, ids=lambda p: p["name"])
def test_core_agrees_with_the_frozen_compiler(program: dict[str, Any]) -> None:
    if program["name"] in INTENDED:
        pytest.skip(INTENDED[program["name"]])
    assert _summary(program["preprocessed"], program["name"]) == program["summary"]
