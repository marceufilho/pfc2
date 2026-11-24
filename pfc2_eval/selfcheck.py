"""Harness validation: does the reference interpreter agree with the source compiled as plain C?

This experiment involves no decision of PFC2's engine. It runs generated programs on generated inputs through
the interpreter and, for every input the interpreter accepts, through the source built by clang with the
address and undefined-behaviour sanitizers, and compares the complete observation: result, final array
contents and final globals. An input the interpreter rejects is counted by reason and never executed, because
running undefined behaviour proves nothing. A build failure, a sanitizer report or a missing line on an
accepted input is a failure of the harness, never agreement.

It says whether the interpreter can serve as the oracle of the later experiments on this generator's
programs. It says nothing about PFC2.
"""

import tempfile
from collections import Counter
from collections.abc import Callable, Iterable, Mapping
from pathlib import Path

from pfc2_eval import adapter, build, campaign, evidence, generate, interpret, stats
from pfc2_eval.interpret import Observation

EXPERIMENT = "selfcheck"
FUEL = 200_000
OUTCOMES = ("agree", "mismatch", "plain-failed", "rejected", "build-failed")
SCHEMA = evidence.Schema(
    (
        evidence.Column("program_seed", "integer"),
        evidence.Column("case", "integer", nullable=True),
        evidence.Column("defect", "boolean"),
        evidence.Column("outcome", "string", allowed=OUTCOMES),
        evidence.Column("rejection", "string", nullable=True),
        evidence.Column("plain_kind", "string", nullable=True),
        evidence.Column("detail", "string", nullable=True),
    )
)


def _rows(records: tuple[evidence.Record, ...]) -> Iterable[Mapping[str, object]]:
    return [record.data for record in records]


def compare(expected: Observation, outcome: build.Outcome, arrays: list[str], globals_: list[str]) -> str | None:
    """None when the binary observed exactly what the interpreter did; otherwise what differs."""
    if outcome.kind != "ok":
        return f"plain C ended with {outcome.kind} {outcome.detail}"
    if outcome.result != expected.result:
        return f"result {outcome.result} != {expected.result}"
    if outcome.arrays != tuple(expected.arrays[name] for name in arrays):
        return "array contents differ"
    if outcome.globals != tuple(expected.globals[name] for name in globals_):
        return "globals differ"
    return None


def run(
    *,
    output: Path,
    compiler: str,
    seed: int,
    programs: int,
    cases: int,
    dry_run: bool = False,
    progress: Callable[[str], None] = campaign.progress,
) -> bool:
    if programs <= 0 or cases <= 0:
        raise ValueError("programs and cases are positive")
    settings = {"programs": programs, "cases": cases, "generator": generate.GENERATOR, "fuel": FUEL}
    if dry_run:
        progress(f"selfcheck: would run {programs} programs x {cases} cases from seed {seed} into {output}")
        return True
    started = campaign.start(EXPERIMENT, output, compiler=compiler, seed=seed, settings=settings, schema=SCHEMA)
    counts: Counter[str] = Counter()
    rejections: Counter[str] = Counter()
    with tempfile.TemporaryDirectory(prefix="pfc2-eval-") as scratch:
        for number in range(seed, seed + programs):
            generated = generate.program(number)
            unit = adapter.load_text(generated.text, f"g{number}.c")
            program = adapter.released(unit)
            function = next(item for item in program.functions if item.name == "entry")
            drawn = generate.cases(generated, cases)
            references = [
                interpret.run(program, case, target=started.target, function="entry", fuel=FUEL) for case in drawn
            ]
            valid = [index for index, observed in enumerate(references) if isinstance(observed, Observation)]
            outcomes: dict[int, build.Outcome] = {}
            failure = None
            if valid:
                binary = Path(scratch) / f"plain{number}"
                try:
                    text = build.with_driver(adapter.plain_c(unit), program, function)
                    build.compile_c(text, binary, clang=compiler, plain=True)
                    ran = build.run_cases(binary, program, function, [drawn[index] for index in valid])
                    outcomes = dict(zip(valid, ran, strict=True))
                except build.BuildError as error:
                    failure = str(error)[:300]
            arrays = [p.symbol.name for p in function.parameters if p.length is not None]
            globals_ = [item.symbol.name for item in program.globals]
            for index, observed in enumerate(references):
                row: dict[str, object] = {
                    "program_seed": number,
                    "case": index,
                    "defect": generated.defect,
                    "rejection": None,
                    "plain_kind": None,
                    "detail": None,
                }
                if not isinstance(observed, Observation):
                    row.update(outcome="rejected", rejection=observed.kind)
                    rejections[observed.kind] += 1
                elif failure is not None:
                    row.update(outcome="build-failed", detail=failure)
                else:
                    difference = compare(observed, outcomes[index], arrays, globals_)
                    kind = outcomes[index].kind
                    outcome = "agree" if difference is None else ("mismatch" if kind == "ok" else "plain-failed")
                    row.update(outcome=outcome, plain_kind=kind, detail=difference)
                counts[str(row["outcome"])] += 1
                started.evidence.record(f"g{number}", "cases", f"c{index}", row)
            started.evidence.write_text(f"programs/g{number}.c", generated.text)
            if (number - seed + 1) % 25 == 0:
                progress(f"selfcheck: {number - seed + 1}/{programs} programs, {dict(counts)}")
    compared = counts["agree"] + counts["mismatch"] + counts["plain-failed"]
    failures = counts["mismatch"] + counts["plain-failed"] + counts["build-failed"]
    passed = failures == 0 and compared > 0
    bound = stats.binomial_upper_bound(0, compared) if passed else None
    summary = {
        "passed": passed,
        "programs": programs,
        "cases_drawn": programs * cases,
        "compared": compared,
        "outcomes": {name: counts[name] for name in OUTCOMES},
        "rejections": dict(sorted(rejections.items())),
        "upper_bound_95_on_disagreement_rate": bound,
        "scope": "interpreter versus source compiled as plain C; no decision of PFC2 is involved",
    }
    table = "\n".join(
        [
            "# Harness self-check: interpreter versus plain C",
            "",
            "| Outcome | Cases |",
            "| --- | ---: |",
            *[f"| {name} | {counts[name]} |" for name in OUTCOMES],
            "",
            "| Rejection reason | Cases |",
            "| --- | ---: |",
            *[f"| {name} | {count} |" for name, count in sorted(rejections.items())],
            "",
            f"Compared: {compared}. Failures: {failures}."
            + (f" With 0 failures in {compared}, the 95% upper bound on the rate is {bound:.5f}." if bound else ""),
            "",
        ]
    )
    campaign.finish(started, summary, table, _rows)
    progress(f"selfcheck: {'passed' if passed else 'FAILED'}; {dict(counts)}")
    return passed
