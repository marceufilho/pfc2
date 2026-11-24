"""E3: a false loop invariant must never be admitted.

For each certified program, the invariant PFC2 relied on at each loop (written, or inferred and proved) is the
baseline. One loop at a time, the baseline is replaced by a damaged candidate from a fixed family of
operators, while the other loops keep theirs, and the whole list is judged through `adapter.admit`: the same
gate, with inference switched off, that any proposer of invariants goes through.

Whether a candidate is *false* is decided without the solver: the program is run in the interpreter with the
candidate written at its loop, on the inputs of the generator, and the candidate is false if some arrival at
the loop head violates it. A candidate with no observed violation is not called true; it is "not refuted".

The criterion concerns false candidates only: none may be certified. What happens to the others (a weaker
invariant that still suffices, one that no longer does) is counted and reported, not scored.
"""

import ctypes
import re
import signal
from collections import Counter
from collections.abc import Callable, Iterable, Mapping
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from random import Random

from pfc2.core.diagnostics import FrontendError
from pfc2.core.target import read_target
from pfc2_eval import adapter, campaign, evidence, generate, interpret
from pfc2_eval.interpret import Inputs

EXPERIMENT = "inject"
OPERATORS = ("literal-false", "off-by-one", "reversed", "dropped", "wrong-variable")
MAX_CANDIDATES = 20
INPUTS = 200
FUEL = 200_000
JUDGING_SECONDS = 600
CLASSES = ("false", "not-refuted", "unparseable")
SCHEMA = evidence.Schema(
    (
        evidence.Column("row", "string", allowed=("program", "candidate")),
        evidence.Column("program", "string"),
        evidence.Column("status", "string", nullable=True),
        evidence.Column("loop", "integer", nullable=True),
        evidence.Column("operator", "string", nullable=True, allowed=OPERATORS),
        evidence.Column("candidate", "string", nullable=True),
        evidence.Column("class", "string", nullable=True, allowed=CLASSES),
        evidence.Column("admitted", "boolean", nullable=True),
    )
)
_CLAUSE = re.compile(r"\binvariant\s*\(")
_NAME = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")


class _OutOfTime(BaseException):
    pass


def _alarm(signum: int, frame: object) -> None:
    raise _OutOfTime


def strip_invariants(text: str) -> tuple[str, list[tuple[int, str]]]:
    """The source without its `invariant(...)` clauses, and each removed predicate with its line number."""
    removed: list[tuple[int, str]] = []
    out, index = [], 0
    while True:
        match = _CLAUSE.search(text, index)
        if match is None:
            out.append(text[index:])
            return "".join(out), removed
        depth, end = 0, match.end() - 1
        while end < len(text):
            depth += (text[end] == "(") - (text[end] == ")")
            if depth == 0:
                break
            end += 1
        removed.append((text.count("\n", 0, match.start()) + 1, text[match.end() : end]))
        out.append(text[index : match.start()])
        out.append(" " * (end + 1 - match.start()) if "\n" not in text[match.start() : end + 1] else "")
        index = end + 1


def conjuncts(predicate: str) -> list[str]:
    """Top-level `&&` operands of a predicate text."""
    parts, depth, start = [], 0, 0
    for index, character in enumerate(predicate):
        depth += (character == "(") - (character == ")")
        if depth == 0 and predicate.startswith("&&", index):
            parts.append(predicate[start:index].strip())
            start = index + 2
    parts.append(predicate[start:].strip())
    return [part for part in parts if part]


def candidates(baseline: str, scalars: list[str], rng: Random) -> list[tuple[str, str]]:
    """Up to MAX_CANDIDATES damaged versions of one invariant, as (operator, text), without duplicates."""
    parts = conjuncts(baseline)
    found: list[tuple[str, str]] = [("literal-false", "0 == 1")]

    def joined(items: list[str]) -> str:
        return " && ".join(f"({item})" for item in items) if items else "1 == 1"

    for position, part in enumerate(parts):
        rest = parts[:position] + parts[position + 1 :]
        if len(parts) > 1:
            found.append(("dropped", joined(rest)))
        for strict, loose in (("<", "<="), (">", ">=")):
            if loose in part:
                found.append(("off-by-one", joined([*rest, part.replace(loose, strict, 1)])))
            elif re.search(rf"[^<>=!]{strict}[^=]", part):
                found.append(("off-by-one", joined([*rest, re.sub(rf"{strict}(?!=)", loose, part, count=1)])))
        swapped = part.translate(str.maketrans("<>", "><"))
        if swapped != part:
            found.append(("reversed", joined([*rest, swapped])))
        names = [name for name in dict.fromkeys(_NAME.findall(part)) if name in scalars]
        for name in names:
            others = [other for other in scalars if other != name]
            if others:
                other = rng.choice(others)
                found.append(("wrong-variable", joined([*rest, re.sub(rf"\b{name}\b", other, part)])))
    unique = list(dict.fromkeys(item for item in found if item[1] != baseline))
    if len(unique) > MAX_CANDIDATES:
        unique = [unique[0], *rng.sample(unique[1:], MAX_CANDIDATES - 1)]
    return unique


def refuted(
    text: str, name: str, invariants: tuple[str, ...], loop: int, inputs: list[Inputs], compiler: str, entry: str
) -> bool:
    """Does some run reach the head of loop number `loop` in a state where its candidate is false?"""
    target = read_target(compiler)
    unit = adapter.load_text(text, name, invariants=invariants)
    line = unit.loop_sites[loop].line
    for case in inputs:
        observed = interpret.run(adapter.released(unit), case, target=target, function=entry, fuel=FUEL)
        if any(
            v.startswith("INVARIANT at ") and int(v.split()[2].split(":")[0]) == line
            for v in observed.annotation_violations
        ):
            return True
    return False


def one_program(arguments: tuple[str, str, int | None, str, int]) -> list[dict[str, object]]:
    """All rows of one program: its status, then one row per candidate."""
    name, source, seed, compiler, budget = arguments
    target = read_target(compiler)
    base: dict[str, object] = {"program": name, "loop": None, "operator": None, "candidate": None, "class": None}
    base["admitted"] = None

    def status(text: str) -> list[dict[str, object]]:
        return [{**base, "row": "program", "status": text}]

    signal.signal(signal.SIGALRM, _alarm)
    signal.setitimer(signal.ITIMER_REAL, budget, 1.0)
    try:
        unit, certification = adapter.check(adapter.load_text(source, f"{name}.c"), target, level="memory")
        if not certification.accepted:
            return status("not certified")
        if not unit.loop_sites:
            return status("no loop")
        stripped, written = strip_invariants(source)
        by_line = dict(written)
        inferred = {(item.function, item.line): item.invariant for item in unit.inferred}
        baseline = []
        for site in unit.loop_sites:
            parts = [text for text in (by_line.get(site.line), inferred.get((site.function, site.line))) if text]
            baseline.append(" && ".join(f"({part})" for part in parts) if parts else "1 == 1")
        if not adapter.admit(stripped, f"{name}.c", tuple(baseline), target, level="memory").accepted:
            return status("baseline not admitted")
        generated = generate.program(seed) if seed is not None else None
        inputs = generate.cases(generated, INPUTS) if generated is not None else []
        if generated is not None and refuted_any(stripped, name, tuple(baseline), inputs, compiler):
            return status("baseline violated")
        rows = status("used" if generated is not None else "used without a falsity check")
        scalars = ["n", "k", "x"] if generated is not None else []
        rng = Random(f"pfc2-eval-inject:{name}")
        for loop, original in enumerate(baseline):
            for operator, text in candidates(original, scalars, rng):
                proposal = tuple(text if index == loop else item for index, item in enumerate(baseline))
                row = {
                    **base,
                    "row": "candidate",
                    "status": None,
                    "loop": loop,
                    "operator": operator,
                    "candidate": text,
                }
                try:
                    kind = "not-refuted"
                    if generated is not None and refuted(
                        stripped, f"{name}.c", proposal, loop, inputs, compiler, "entry"
                    ):
                        kind = "false"
                    admitted = adapter.admit(stripped, f"{name}.c", proposal, target, level="memory").accepted
                    row.update({"class": kind, "admitted": admitted})
                except FrontendError:
                    row.update({"class": "unparseable", "admitted": False})
                rows.append(row)
        return rows
    except _OutOfTime:
        return status("not judged within the time budget")
    except ctypes.ArgumentError as error:
        # The timer can fire while ctypes converts an argument of a solver call; ctypes then reports the
        # timer's exception as its own, by name (amendments 25 and 27). Anything else is a real error.
        if _OutOfTime.__name__ not in str(error):
            raise
        return status("not judged within the time budget")
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


def refuted_any(text: str, name: str, invariants: tuple[str, ...], inputs: list[Inputs], compiler: str) -> bool:
    target = read_target(compiler)
    unit = adapter.load_text(text, f"{name}.c", invariants=invariants)
    for case in inputs:
        observed = interpret.run(adapter.released(unit), case, target=target, function="entry", fuel=FUEL)
        if any(v.startswith("INVARIANT") for v in observed.annotation_violations):
            return True
    return False


def _rows(records: tuple[evidence.Record, ...]) -> Iterable[Mapping[str, object]]:
    return [record.data for record in records]


def run(
    *,
    output: Path,
    compiler: str,
    seed: int,
    programs: int,
    workers: int = 1,
    budget: int = JUDGING_SECONDS,
    dry_run: bool = False,
    progress: Callable[[str], None] = campaign.progress,
) -> bool:
    """Generated programs from `seed` upward until `programs` of them have been used (certified, with loops)."""
    if dry_run:
        progress(f"inject: would damage the invariants of {programs} certified programs from seed {seed} into {output}")
        return True
    settings = {
        "programs_wanted": programs,
        "operators": list(OPERATORS),
        "max_candidates_per_loop": MAX_CANDIDATES,
        "inputs": INPUTS,
        "generator": generate.GENERATOR,
        "judging_seconds": budget,
        "workers": workers,
    }
    started = campaign.start(EXPERIMENT, output, compiler=compiler, seed=seed, settings=settings, schema=SCHEMA)
    counts: Counter[tuple[str, bool]] = Counter()
    statuses: Counter[str] = Counter()
    by_operator: Counter[tuple[str, str, bool]] = Counter()
    unsound: list[str] = []
    used, number = 0, seed
    with ProcessPoolExecutor(max_workers=workers) as pool:
        while used < programs and number < seed + 10 * programs:
            batch = [
                (f"g{n}", generate.program(n).text, n, compiler, budget) for n in range(number, number + 2 * workers)
            ]
            number += 2 * workers
            for rows in pool.map(one_program, batch):
                if used >= programs:
                    break  # Programs beyond the registered count are not recorded.
                statuses[str(rows[0]["status"])] += 1
                used += rows[0]["status"] == "used"
                for index, row in enumerate(rows):
                    started.evidence.record(str(row["program"]), "rows", f"r{index}", row)
                    if row["row"] == "candidate":
                        counts[(str(row["class"]), bool(row["admitted"]))] += 1
                        by_operator[(str(row["operator"]), str(row["class"]), bool(row["admitted"]))] += 1
                        if row["class"] == "false" and row["admitted"]:
                            unsound.append(f"{row['program']} loop {row['loop']}: {row['candidate']}")
            progress(f"inject: {used}/{programs} programs used; false admitted {len(unsound)}")
    false_total = counts[("false", True)] + counts[("false", False)]
    passed = not unsound and false_total > 0
    summary = {
        "passed": passed,
        "programs": dict(sorted(statuses.items())),
        "false_candidates": false_total,
        "false_admitted": counts[("false", True)],
        "not_refuted_admitted": counts[("not-refuted", True)],
        "not_refuted_refused": counts[("not-refuted", False)],
        "unparseable": counts[("unparseable", False)],
        "unsound": unsound,
        "by_operator": {f"{o}/{c}/{'admitted' if a else 'refused'}": v for (o, c, a), v in sorted(by_operator.items())},
    }
    lines = [
        "# E3: false invariants",
        "",
        "| Candidate | Admitted | Refused |",
        "| --- | ---: | ---: |",
        f"| false (a run violates it) | {counts[('false', True)]} | {counts[('false', False)]} |",
        f"| not refuted by any run | {counts[('not-refuted', True)]} | {counts[('not-refuted', False)]} |",
        "",
        "| Program status | Programs |",
        "| --- | ---: |",
        *[f"| {name} | {count} |" for name, count in sorted(statuses.items())],
        "",
    ]
    campaign.finish(started, summary, "\n".join(lines), _rows)
    progress(f"inject: {'passed' if passed else 'FAILED'}; false {false_total}, admitted {counts[('false', True)]}")
    return passed
