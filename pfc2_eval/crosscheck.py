"""E6: every query of the engine, answered again by a second solver.

For each program the obligations are generated as the product judges them (with its inferred loop bounds). Each
query, hypotheses and negated goal, or the entry hypotheses alone, is built with the engine's own encoder,
printed as SMT-LIB 2 and given to cvc5 with the same time budget. The engine's answer is the status its own
check recorded.

A disagreement is one solver saying the formula is unsatisfiable and the other saying it is satisfiable. An
answer of `unknown`, a timeout or an error on either side is inconclusive and counted apart; it is never
agreement. The second solver shares the encoding with the first: this checks the solver, not the encoder.
It grants nothing: no verdict of cvc5 changes what PFC2 certifies.
"""

import subprocess
from collections import Counter
from collections.abc import Callable, Iterable, Mapping
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import z3

from pfc2 import infer
from pfc2.core import smt
from pfc2.core.config import SOLVER_TIMEOUT_MS
from pfc2.core.target import read_target
from pfc2_eval import adapter, campaign, evidence, generate

EXPERIMENT = "crosscheck"
ANSWERS = ("unsat", "sat", "unknown", "timeout", "error")
AGREEMENT = ("agree", "disagree", "inconclusive")
SCHEMA = evidence.Schema(
    (
        evidence.Column("program", "string"),
        evidence.Column("query", "string"),
        evidence.Column("kind", "string"),
        evidence.Column("z3", "string", allowed=ANSWERS),
        evidence.Column("cvc5", "string", allowed=ANSWERS),
        evidence.Column("agreement", "string", allowed=AGREEMENT),
    )
)
_Z3 = {"proved": "unsat", "failed": "sat", "timeout": "timeout", "unknown": "unknown", "error": "error"}


def smtlib(formulas: list[z3.BoolRef]) -> str:
    solver = z3.Solver()
    solver.add(*formulas)
    return "(set-logic ALL)\n" + str(solver.to_smt2())


def ask(cvc5: Path, text: str, timeout_ms: int) -> str:
    """cvc5's answer to one SMT-LIB text; anything that is not a clear answer is not one."""
    try:
        result = subprocess.run(
            [str(cvc5), "--lang=smt2", f"--tlimit={timeout_ms}", "-"],
            input=text,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_ms / 1000 + 30,
        )
    except subprocess.TimeoutExpired:
        return "timeout"
    except OSError:
        return "error"
    first = result.stdout.strip().splitlines()[:1]
    if first in (["unsat"], ["sat"], ["unknown"]):
        return first[0]
    return "timeout" if "timeout" in (result.stdout + result.stderr).lower() else "error"


def agreement(first: str, second: str) -> str:
    if {first, second} <= {"sat", "unsat"}:
        return "agree" if first == second else "disagree"
    return "inconclusive"


def one_program(arguments: tuple[str, str, str, str, int]) -> list[dict[str, object]]:
    name, text, compiler, cvc5, timeout_ms = arguments
    target = read_target(compiler)
    unit = infer.apply(adapter.load_text(text, f"{name}.c"), target, timeout_ms=timeout_ms)
    report = smt.check(unit.program, target, timeout_ms=timeout_ms)
    rows: list[dict[str, object]] = []
    for result in report.results:
        obligation = result.obligation
        encoder = smt.Encoder(target)
        formulas = [encoder.boolean(encoder.encode(item.formula)) for item in obligation.hypotheses]
        formulas.append(z3.Not(encoder.boolean(encoder.encode(obligation.goal))))
        ours = _Z3[str(result.status)]
        theirs = ask(Path(cvc5), smtlib(formulas), timeout_ms)
        rows.append(
            {
                "program": name,
                "query": obligation.id[:40],
                "kind": obligation.kind,
                "z3": ours,
                "cvc5": theirs,
                "agreement": agreement(ours, theirs),
            }
        )
    for entry in report.entry_results:
        encoder = smt.Encoder(target)
        formulas = [encoder.boolean(encoder.encode(item.formula)) for item in entry.query.hypotheses]
        theirs = ask(Path(cvc5), smtlib(formulas), timeout_ms)
        row = {"program": name, "query": f"entry-{entry.query.function}", "kind": "entry-consistency"}
        rows.append({**row, "z3": str(entry.status), "cvc5": theirs, "agreement": agreement(str(entry.status), theirs)})
    return rows


def _rows(records: tuple[evidence.Record, ...]) -> Iterable[Mapping[str, object]]:
    return [record.data for record in records]


def run(
    *,
    output: Path,
    compiler: str,
    cvc5: Path,
    seed: int,
    programs: int,
    directories: list[Path],
    workers: int = 1,
    timeout_ms: int = SOLVER_TIMEOUT_MS,
    dry_run: bool = False,
    progress: Callable[[str], None] = campaign.progress,
) -> bool:
    if not cvc5.is_file():
        raise ValueError(f"cvc5 not found at {cvc5}")
    version = subprocess.run([str(cvc5), "--version"], capture_output=True, text=True, check=False).stdout.splitlines()
    units = [(f"g{number}", generate.program(number).text) for number in range(seed, seed + programs)]
    for directory in directories:
        for path in sorted(directory.rglob("*.c")):
            if "wrong" not in path.parts:
                units.append((path.stem, path.read_text(encoding="utf-8")))
    if dry_run:
        progress(f"crosscheck: would check {len(units)} programs with {version[:1]} into {output}")
        return True
    settings = {
        "programs": len(units),
        "generated": programs,
        "cvc5": version[0] if version else None,
        "timeout_ms": timeout_ms,
        "workers": workers,
        "generator": generate.GENERATOR,
    }
    started = campaign.start(EXPERIMENT, output, compiler=compiler, seed=seed, settings=settings, schema=SCHEMA)
    jobs = [(name, text, compiler, str(cvc5), timeout_ms) for name, text in units]
    counts: Counter[str] = Counter()
    pairs: Counter[str] = Counter()
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for done, rows in enumerate(pool.map(one_program, jobs), 1):
            for index, row in enumerate(rows):
                counts[str(row["agreement"])] += 1
                pairs[f"z3 {row['z3']} / cvc5 {row['cvc5']}"] += 1
                started.evidence.record(str(row["program"]), "queries", f"q{index}", row)
            if done % 25 == 0:
                progress(f"crosscheck: {done}/{len(units)} programs; {dict(counts)}")
    passed = counts["disagree"] == 0 and counts["agree"] > 0
    summary = {
        "passed": passed,
        "queries": sum(counts.values()),
        "agreement": dict(counts),
        "pairs": dict(sorted(pairs.items())),
    }
    lines = [
        "# E6: second solver",
        "",
        "| Z3 / cvc5 | Queries |",
        "| --- | ---: |",
        *[f"| {name} | {count} |" for name, count in sorted(pairs.items())],
        "",
        f"Agree: {counts['agree']}. Disagree: {counts['disagree']}. Inconclusive: {counts['inconclusive']}.",
        "",
    ]
    campaign.finish(started, summary, "\n".join(lines), _rows)
    progress(f"crosscheck: {'passed' if passed else 'FAILED'}; {dict(counts)}")
    return passed
