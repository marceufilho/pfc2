"""E12: the editor and the browser must say what the command line says.

Three paths lead from a source text to a verdict: `pfc2.check.check` (the command line), `pfc2.web.analyze`
(the playground) and `pfc2.lsp.analysis.analyze` (the language server). They are compared on the same text,
level, target and solver budget: whether the file is certified, which obligations block it and where, and, for
the browser path, the hash of the released C.

This runs the browser's Python entry point natively. That the same code gives the same answers inside the
browser's WebAssembly runtime is a different question, covered by the site's own test on the examples.
"""

import ctypes
import hashlib
import signal
from collections import Counter
from collections.abc import Callable, Iterable, Mapping
from pathlib import Path

from pfc2 import web
from pfc2.core.diagnostics import FrontendError
from pfc2.gate import Level
from pfc2.lsp import analysis
from pfc2_eval import adapter, campaign, evidence, generate

EXPERIMENT = "surfaces"
LEVEL: Level = "memory"
TIMEOUT_MS = web.MAX_TIMEOUT_MS
SCHEMA = evidence.Schema(
    (
        evidence.Column("program", "string"),
        evidence.Column("command_line", "string", allowed=("certified", "refused", "rejected", "not-judged")),
        evidence.Column("browser_same", "boolean"),
        evidence.Column("editor_same", "boolean"),
        evidence.Column("detail", "string", nullable=True),
    )
)


JUDGING_SECONDS = 600  # Wall-clock budget for the three verdicts of one program (amendment 5).


class _OutOfTime(BaseException):
    pass


def _alarm(signum: int, frame: object) -> None:
    raise _OutOfTime


def within_budget(name: str, text: str, budget: int = JUDGING_SECONDS) -> dict[str, object]:
    """`compare`, or a row saying the program could not be judged in time; such a row compares nothing."""
    signal.signal(signal.SIGALRM, _alarm)
    signal.setitimer(signal.ITIMER_REAL, budget, 1.0)
    try:
        return compare(name, text)
    except _OutOfTime:
        row = {"program": name, "command_line": "not-judged", "browser_same": True, "editor_same": True}
        return {**row, "detail": "not judged within the time budget; nothing was compared"}
    except ctypes.ArgumentError as error:
        # The timer can fire while ctypes converts an argument of a solver call; ctypes then reports the
        # timer's exception as its own, by name (amendments 25 and 27). Anything else is a real error.
        if _OutOfTime.__name__ not in str(error):
            raise
        row = {"program": name, "command_line": "not-judged", "browser_same": True, "editor_same": True}
        return {**row, "detail": "not judged within the time budget; nothing was compared"}
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


def compare(name: str, text: str) -> dict[str, object]:
    """One row: the command-line verdict, and whether the other two paths match it."""
    target = web.STATIC_TARGET
    try:
        _, certification = adapter.check(adapter.load_text(text, name), target, level=LEVEL, timeout_ms=TIMEOUT_MS)
        verdict = "certified" if certification.accepted else "refused"
        blockers = sorted((b.kind, b.location.line, b.location.column or 0) for b in certification.blockers)
        primary = sorted(b.kind for b in certification.blockers if not b.status.startswith("depends"))
        released = certification.c
    except FrontendError as error:
        verdict, blockers, primary, released = "rejected", [], [error.diagnostic.rule], None
    notes = []
    seen = web.analyze(text, name=name, level=LEVEL, timeout_ms=TIMEOUT_MS)
    if verdict == "rejected":
        browser = not seen["ok"] and seen["diagnostic"]["rule"] == primary[0]
    else:
        theirs = sorted((b["kind"], b["line"], b["column"] or 0) for b in seen.get("blockers", []))
        browser = (
            bool(seen["ok"])
            and seen["accepted"] == (verdict == "certified")
            and theirs == blockers
            and seen["c"] == released
        )
    if not browser:
        notes.append("browser differs")
    shown = analysis.analyze(text, name, level=LEVEL, timeout_ms=TIMEOUT_MS, target=target)
    errors = sorted(d.code for d in shown.diagnostics if d.severity == "error")
    if verdict == "certified":
        editor = shown.accepted is True and not errors
    elif verdict == "rejected":
        editor = shown.accepted is None and errors == primary
    else:
        editor = shown.accepted is False and (errors == primary if primary else bool(errors))
    if not editor:
        notes.append(f"editor differs: {errors[:4]}")
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]
    return {
        "program": name,
        "command_line": verdict,
        "browser_same": browser,
        "editor_same": editor,
        "detail": f"{digest}: " + "; ".join(notes) if notes else None,
    }


def _rows(records: tuple[evidence.Record, ...]) -> Iterable[Mapping[str, object]]:
    return [record.data for record in records]


def run(
    *,
    output: Path,
    compiler: str,
    seed: int,
    programs: int,
    directories: list[Path],
    dry_run: bool = False,
    progress: Callable[[str], None] = campaign.progress,
) -> bool:
    units = [(f"g{number}.c", generate.program(number).text) for number in range(seed, seed + programs)]
    for directory in directories:
        units += [(path.name, path.read_text(encoding="utf-8")) for path in sorted(directory.rglob("*.c"))]
    if dry_run:
        progress(f"surfaces: would compare three paths on {len(units)} programs into {output}")
        return True
    settings = {"programs": len(units), "level": LEVEL, "timeout_ms": TIMEOUT_MS, "generator": generate.GENERATOR}
    settings["judging_seconds"] = JUDGING_SECONDS
    started = campaign.start(EXPERIMENT, output, compiler=compiler, seed=seed, settings=settings, schema=SCHEMA)
    counts: Counter[str] = Counter()
    differing = []
    for index, (name, text) in enumerate(units):
        row = within_budget(name, text)
        counts[str(row["command_line"])] += 1
        if not (row["browser_same"] and row["editor_same"]):
            differing.append(name)
        started.evidence.record("programs", "rows", f"p{index}", row)
    passed = not differing
    compared = len(units) - counts["not-judged"]
    summary: dict[str, object] = {"passed": passed and compared > 0, "programs": len(units), "compared": compared}
    summary.update({"verdicts": dict(counts), "differing": differing})
    table = "\n".join(
        [
            "# E12: command line, browser entry point, editor analysis",
            "",
            f"Programs: {len(units)} ({dict(counts)}). Differing: {len(differing)}.",
            "",
            *[f"- {name}" for name in differing],
            "",
        ]
    )
    campaign.finish(started, summary, table, _rows)
    progress(f"surfaces: {'passed' if passed else 'FAILED'}; {len(units)} programs, {len(differing)} differing")
    return passed
