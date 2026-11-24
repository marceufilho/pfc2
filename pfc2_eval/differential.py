"""E1 (differential), E8 (expected traps) and E9 (replay), in one pass.

For each generated program: the product's own verdict at `memory` (and at `full`); if certified, the proof
file is written and replayed in a fresh process, and the certified C, the checked C and the source as plain C
are built with sanitizers and run on the same inputs as the reference interpreter.

Per input, the interpreter's answer decides what is required:

- accepted (a complete observation): every binary must print exactly that observation (E1);
- rejected for overflow, out of bounds, division or conversion: the checked C must trap; the certified C must
  trap too (E8). If the rejection is anything but overflow, the input satisfied the entry contract of a
  certified program and still reached an operation the proof says is safe: that is recorded as
  `certified-unsafe`, a finding against the engine, whatever the binaries do;
- rejected at the entry contract: the certified C must trap if a rendered entry check is false; when only
  conjuncts the emitter did not render are false the case is `unscored`, counted and never hidden;
- anything the interpreter could not decide: `unscored`.

Plain C is run only on accepted inputs. A build failure, a missing line, a sanitizer report or a signal that is
not the trap counts as a failure of the case.
"""

import ctypes
import json
import signal
import subprocess
import sys
import tempfile
from collections import Counter
from collections.abc import Callable, Iterable, Mapping
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from pfc2 import proof
from pfc2.core import ir
from pfc2.core.parse import SpecKind
from pfc2.core.target import Target, read_target
from pfc2_eval import adapter, build, campaign, evidence, generate, interpret, stats
from pfc2_eval.interpret import Inputs, Observation, Rejection

EXPERIMENT = "differential"
FUEL = 200_000
JUDGING_SECONDS = 600  # Wall-clock budget for the verdicts of one program (amendment 1).


class _OutOfTime(BaseException):
    """Raised by the timer. Not an `Exception`, so no error handler of the engine can take it for a solver error."""


def _alarm(signum: int, frame: object) -> None:
    raise _OutOfTime


VARIANTS = ("certified", "checked", "plain")
CASE_OUTCOMES = ("agree", "differ", "trapped-as-required", "missing-trap", "certified-unsafe", "unscored", "failed")
SCHEMA = evidence.Schema(
    (
        evidence.Column("row", "string", allowed=("program", "case")),
        evidence.Column("program_seed", "integer"),
        evidence.Column("defect", "boolean"),
        evidence.Column("certified_memory", "boolean"),
        evidence.Column("certified_full", "boolean"),
        evidence.Column("refusal", "string", nullable=True),
        evidence.Column("replay", "string", nullable=True, allowed=("reproduced", "differs", "failed")),
        evidence.Column("guards_removed", "integer", nullable=True),
        evidence.Column("traps_kept", "integer", nullable=True),
        evidence.Column("case", "integer", nullable=True),
        evidence.Column("level", "string", nullable=True, allowed=("memory", "full")),
        evidence.Column("reference", "string", nullable=True),
        evidence.Column("outcome", "string", nullable=True, allowed=CASE_OUTCOMES),
        evidence.Column("detail", "string", nullable=True),
    )
)


def conjuncts(function: ir.Function) -> list[ir.Expr]:
    """Top-level conjuncts of the function's `requires`, in order (the harness's own flattening)."""
    found: list[ir.Expr] = []

    def split(expression: ir.Expr) -> None:
        if isinstance(expression, ir.Convert):
            split(expression.operand)
        elif isinstance(expression, ir.Binary) and expression.operator == "&&":
            split(expression.left)
            split(expression.right)
        else:
            found.append(expression)

    for contract in function.contracts:
        if contract.kind is SpecKind.REQUIRES:
            split(contract.condition)
    return found


def entry_violation(
    program: ir.Program, function: ir.Function, case: Inputs, rendered: list[bool], target: Target
) -> str | None:
    """None if the entry contract holds; "rendered" if an emitted entry check is false; else "skipped"."""
    parts = conjuncts(function)
    truths = [
        interpret.evaluate_condition(program, case, part, target=target, function=function.name) for part in parts
    ]
    if all(truth is True for truth in truths):
        return None
    if len(rendered) != len(parts):
        return "skipped"  # The emitter's list does not line up with the contract: nothing can be required.
    return (
        "rendered"
        if any(truth is False and shown for truth, shown in zip(truths, rendered, strict=True))
        else "skipped"
    )


def judge(
    reference: Observation | Rejection,
    outcomes: Mapping[str, build.Outcome | None],
    arrays: list[str],
    globals_: list[str],
    violation: str | None,
) -> tuple[str, str | None]:
    """Outcome of one case for one certified build: what was required, and whether it happened."""
    certified, checked, plain = outcomes["certified"], outcomes["checked"], outcomes["plain"]
    assert certified is not None and checked is not None
    if isinstance(reference, Observation):
        expected = build.Outcome(
            "ok",
            reference.result,
            tuple(reference.arrays[name] for name in arrays),
            tuple(reference.globals[name] for name in globals_),
        )
        assert plain is not None
        seen = {"certified": certified, "checked": checked, "plain": plain}
        wrong = [name for name, outcome in seen.items() if outcome != expected]
        if not wrong:
            return "agree", None
        # A line that never arrived is the harness failing; anything else is the binary doing something different.
        lost = all(seen[name].kind == "missing" for name in wrong)
        return ("failed" if lost else "differ"), ",".join(f"{name}:{seen[name].kind}" for name in wrong)
    if reference.kind in interpret.TRAPPING:
        if violation is not None:  # The run was outside the entry contract before it reached this operation.
            return _entry(violation, certified)
        if reference.kind != "Overflow":
            return "certified-unsafe", f"{reference.kind}: {reference.message}"
        missing = [name for name, seen in (("certified", certified), ("checked", checked)) if seen.kind != "trap"]
        return ("missing-trap", ",".join(missing)) if missing else ("trapped-as-required", None)
    if reference.kind == "PreconditionViolated":
        if violation is None:
            return "certified-unsafe", f"a callee's contract is violated inside the entry contract: {reference.message}"
        return _entry(violation, certified)
    return "unscored", reference.kind


def _entry(violation: str, certified: build.Outcome) -> tuple[str, str | None]:
    if violation != "rendered":
        return "unscored", "only conjuncts without an entry check are false"
    return ("trapped-as-required", None) if certified.kind == "trap" else ("missing-trap", "certified (entry check)")


def _replay(record: object, scratch: Path, name: str) -> str:
    path = scratch / f"{name}.proof.json"
    path.write_text(json.dumps(record, sort_keys=True), encoding="utf-8")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pfc2", "replay", str(path)],
            capture_output=True,
            text=True,
            check=False,
            timeout=600,
        )
    except (OSError, subprocess.SubprocessError):
        return "failed"
    if result.returncode == 0 and "reproduced" in result.stdout:
        return "reproduced"
    return "differs" if result.returncode == 1 else "failed"


def one_program(arguments: tuple[int, int, str, int]) -> list[dict[str, object]]:
    """All rows of one generated program. Runs in a worker process and touches no shared state."""
    seed, count, compiler, budget = arguments
    target = read_target(compiler)
    generated = generate.program(seed)
    base: dict[str, object] = {
        "program_seed": seed,
        "defect": generated.defect,
        "case": None,
        "level": None,
        "reference": None,
        "outcome": None,
        "detail": None,
    }
    unit = adapter.load_text(generated.text, f"g{seed}.c")
    signal.signal(signal.SIGALRM, _alarm)
    signal.setitimer(signal.ITIMER_REAL, budget, 1.0)  # Repeats, in case one delivery lands in a handler.
    not_judged: list[dict[str, object]] = [
        {
            **base,
            "row": "program",
            "certified_memory": False,
            "certified_full": False,
            "refusal": "not judged within the time budget",
            "replay": None,
            "guards_removed": None,
            "traps_kept": None,
        }
    ]
    try:
        judged, memory = adapter.check(unit, target, level="memory")
        full = adapter.check(unit, target, level="full")[1]
    except _OutOfTime:
        return not_judged
    except ctypes.ArgumentError as error:
        # The timer can fire while ctypes converts an argument of a solver call; ctypes then reports the
        # timer's exception as its own, by name. Anything else is a real error and is not swallowed.
        if _OutOfTime.__name__ not in str(error):
            raise
        return not_judged
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
    refusal = None
    if not memory.accepted:
        kinds = sorted({b.kind for b in memory.blockers if not b.status.startswith("depends")})
        refusal = ",".join(kinds) or memory.reason[:80]
    rows: list[dict[str, object]] = []
    summary: dict[str, object] = {
        **base,
        "row": "program",
        "certified_memory": memory.accepted,
        "certified_full": full.accepted,
        "refusal": refusal,
        "replay": None,
        "guards_removed": None,
        "traps_kept": None,
    }
    if not memory.accepted or memory.c is None:
        return [summary]
    summary["guards_removed"] = sum(decision.removed for decision in memory.emission.decisions)
    summary["traps_kept"] = len(memory.retained_traps)
    program = adapter.released(judged)
    function = next(item for item in program.functions if item.name == "entry")
    arrays = [p.symbol.name for p in function.parameters if p.length is not None]
    globals_ = [item.symbol.name for item in program.globals]
    drawn = generate.cases(generated, count)
    references = [interpret.run(program, case, target=target, function="entry", fuel=FUEL) for case in drawn]
    valid = [index for index, reference in enumerate(references) if isinstance(reference, Observation)]
    with tempfile.TemporaryDirectory(prefix="pfc2-eval-") as directory:
        scratch = Path(directory)
        summary["replay"] = _replay(proof.build(judged, memory), scratch, f"g{seed}")
        levels = [("memory", memory)] + ([("full", full)] if full.accepted and full.c is not None else [])
        ran: dict[str, list[build.Outcome] | None] = {}
        failures: dict[str, str] = {}
        texts = {"checked": adapter.checked_c(judged, target), "plain": adapter.plain_c(judged)}
        for level, certification in levels:
            assert certification.c is not None
            texts[f"certified-{level}"] = certification.c
        for name, text in texts.items():
            try:
                binary = scratch / name
                build.compile_c(
                    build.with_driver(text, program, function), binary, clang=compiler, plain=name == "plain"
                )
                cases = [drawn[index] for index in valid] if name == "plain" else drawn
                ran[name] = build.run_cases(binary, program, function, cases)
            except build.BuildError as error:
                ran[name], failures[name] = None, str(error)[:200]
        for level, certification in levels:
            shown = [
                check.rendered is not None
                for check in certification.emission.requires_checks
                if check.function == "entry"
            ]
            for index, reference in enumerate(references):
                row = {**summary, "row": "case", "case": index, "level": level, "replay": None}
                row["reference"] = "ok" if isinstance(reference, Observation) else reference.kind
                key = f"certified-{level}"
                if ran[key] is None or ran["checked"] is None or (ran["plain"] is None and index in valid):
                    row.update(outcome="failed", detail="build: " + "; ".join(f"{k}: {v}" for k, v in failures.items()))
                else:
                    plain = ran["plain"][valid.index(index)] if index in valid and ran["plain"] is not None else None
                    outcomes = {"certified": ran[key][index], "checked": ran["checked"][index], "plain": plain}  # type: ignore[index]
                    violation = (
                        None
                        if isinstance(reference, Observation)
                        else entry_violation(program, function, drawn[index], shown, target)
                    )
                    outcome, detail = judge(reference, outcomes, arrays, globals_, violation)
                    row.update(outcome=outcome, detail=detail)
                rows.append(row)
    return [summary, *rows]


def _rows(records: tuple[evidence.Record, ...]) -> Iterable[Mapping[str, object]]:
    return [record.data for record in records]


def run(
    *,
    output: Path,
    compiler: str,
    seed: int,
    programs: int,
    cases: int,
    workers: int = 1,
    budget: int = JUDGING_SECONDS,
    dry_run: bool = False,
    progress: Callable[[str], None] = campaign.progress,
) -> bool:
    if programs <= 0 or cases <= 0 or workers <= 0:
        raise ValueError("programs, cases and workers are positive")
    settings = {"programs": programs, "cases": cases, "generator": generate.GENERATOR, "fuel": FUEL, "workers": workers}
    settings["judging_seconds"] = budget
    if dry_run:
        progress(f"differential: would run {programs} programs x {cases} cases from seed {seed} into {output}")
        return True
    started = campaign.start(EXPERIMENT, output, compiler=compiler, seed=seed, settings=settings, schema=SCHEMA)
    jobs = [(number, cases, compiler, budget) for number in range(seed, seed + programs)]
    counts: Counter[str] = Counter()
    by_level: Counter[tuple[str, str]] = Counter()
    programs_with: dict[str, set[int]] = {name: set() for name in CASE_OUTCOMES}
    certified = certified_full = replayed = replay_bad = 0
    refusals: Counter[str] = Counter()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for done, rows in enumerate(pool.map(one_program, jobs), 1):
            for row in rows:
                number = int(str(row["program_seed"]))
                if row["row"] == "program":
                    certified += bool(row["certified_memory"])
                    certified_full += bool(row["certified_full"])
                    if row["refusal"] is not None:
                        refusals[str(row["refusal"])] += 1
                    if row["replay"] is not None:
                        replayed += 1
                        replay_bad += row["replay"] != "reproduced"
                    started.evidence.record(f"g{number}", "program", "verdict", row)
                else:
                    outcome = str(row["outcome"])
                    counts[outcome] += 1
                    by_level[(str(row["level"]), outcome)] += 1
                    programs_with[outcome].add(number)
                    started.evidence.record(f"g{number}", f"cases-{row['level']}", f"c{row['case']}", row)
            if done % 50 == 0:
                progress(f"differential: {done}/{programs}; certified {certified}; {dict(counts)}")
    bad = ("differ", "missing-trap", "certified-unsafe", "failed")
    failures = sum(counts[name] for name in bad) + replay_bad
    compared = counts["agree"] + counts["differ"]
    trap_cases = counts["trapped-as-required"] + counts["missing-trap"]
    powered = certified >= 300
    passed = failures == 0 and compared > 0
    failing_programs = set().union(*(programs_with[name] for name in bad))
    summary = {
        "passed": passed,
        "powered": powered,
        "programs": programs,
        "certified_memory": certified,
        "certified_full": certified_full,
        "refusals": dict(sorted(refusals.items())),
        "cases": {name: counts[name] for name in CASE_OUTCOMES},
        "cases_by_level": {f"{level}:{name}": value for (level, name), value in sorted(by_level.items())},
        "programs_with_a_failing_case": sorted(failing_programs),
        "e1_compared_cases": compared,
        "e8_trap_cases": trap_cases,
        "e9_replayed": replayed,
        "e9_not_reproduced": replay_bad,
        "upper_bound_95_per_program": stats.binomial_upper_bound(0, certified) if passed and certified else None,
        "upper_bound_95_per_case_not_independent": stats.binomial_upper_bound(0, compared) if passed else None,
    }
    lines = [
        "# E1, E8, E9: differential, expected traps, replay",
        "",
        f"Programs: {programs}. Certified at `memory`: {certified}; at `full`: {certified_full}.",
        "",
        "| Case outcome | Cases | Programs |",
        "| --- | ---: | ---: |",
        *[f"| {name} | {counts[name]} | {len(programs_with[name])} |" for name in CASE_OUTCOMES],
        "",
        f"Replay: {replayed} proof files, {replay_bad} not reproduced.",
        "",
        "| Refused at `memory` for | Programs |",
        "| --- | ---: |",
        *[f"| {name} | {count} |" for name, count in sorted(refusals.items())],
        "",
    ]
    campaign.finish(started, summary, "\n".join(lines), _rows)
    progress(f"differential: {'passed' if passed else 'FAILED'}; certified {certified}/{programs}; {dict(counts)}")
    return passed
