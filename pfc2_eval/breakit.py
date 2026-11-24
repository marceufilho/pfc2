"""E2: a precondition that a proof relies on must be missed when it is gone.

Each top-level conjunct of each `requires` of a certified program is removed, alone, and the program is judged
again. What should happen is decided without the solver, by a search in a small domain with the interpreter:

    witness  some input that the full contract rejects is accepted by the weakened one and then reaches a
             failing bounds or division check, a conversion out of range, a call whose callee refuses it, or
             an `assert`, `ensures` or invariant that is false. The certificate must be lost (sensitivity).
    overflow some such input only reaches an arithmetic overflow. At `memory` overflow is trapped, not
             proved, so the certificate may stay; the line where it overflowed must then keep a trap in the
             new C, or the certificate be lost. Counted apart.
    none     no such input in the domain. Verdict, decisions and code (without the entry checks, which restate
             the `requires`) must be unchanged (specificity). "None in the domain" is not "none".
    undecided  no such input, and on some input the interpreter could not follow the program (a declared
             function without a model, the step budget, an annotation it cannot evaluate). Not scored.

The function that carries the clause is run directly, so a helper's precondition is judged on the helper's own
inputs and not only on what its caller happens to pass.
"""

import ctypes
import re
import signal
from collections import Counter
from collections.abc import Callable, Iterable, Mapping
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from random import Random

from pfc2.core import ir
from pfc2.core.diagnostics import FrontendError
from pfc2.core.target import Target, read_target
from pfc2.gate import Certification
from pfc2_eval import adapter, campaign, evidence, generate, interpret
from pfc2_eval.inject import conjuncts
from pfc2_eval.interpret import Inputs

EXPERIMENT = "breakit"
EXPECTED = ("witness", "overflow", "none", "undecided")
STRATA = ("generated", "examples")
DRAWS = 5000  # At most this many inputs are drawn for one removal...
USABLE = 300  # ...and the search stops after this many that only the removed conjunct had kept out.
FUEL = 200_000
JUDGING_SECONDS = 600
LONG_MAX = 2**63 - 1
SCALARS = (-LONG_MAX - 1, -51, -50, -49, -9, *range(-3, 11), 49, 50, 51, LONG_MAX)
LENGTHS = tuple(range(-1, 10))
ELEMENTS = (-2, -1, 0, 1, 2, 9)
MAX_BUFFER = 12
SAFETY = frozenset({"OutOfBounds", "DivisionByZero", "ConversionOutOfRange"})
SCHEMA = evidence.Schema(
    (
        evidence.Column("row", "string", allowed=("program", "removal")),
        evidence.Column("program", "string"),
        evidence.Column("stratum", "string", allowed=STRATA),
        evidence.Column("status", "string", nullable=True),
        evidence.Column("function", "string", nullable=True),
        evidence.Column("line", "integer", nullable=True),
        evidence.Column("conjunct", "string", nullable=True),
        evidence.Column("expected", "string", nullable=True, allowed=EXPECTED),
        evidence.Column("witness", "string", nullable=True),
        evidence.Column("certified", "boolean", nullable=True),
        evidence.Column("decisions_same", "boolean", nullable=True),
        evidence.Column("code_same", "boolean", nullable=True),
        evidence.Column("overflow_trap_kept", "boolean", nullable=True),
        evidence.Column("as_expected", "boolean", nullable=True),
    )
)
_CLAUSE = re.compile(r"\brequires\s*\(")
_ENTRY_CHECK = re.compile(r"^\s*(?://\s*entry check|_Bool pfc_entry_\d+ =|if \(!pfc_entry_\d+\))")
_HASH = re.compile(r":[0-9a-f]{64}")
_POSITION = re.compile(r"\.c:\d+:\d+")


class _OutOfTime(BaseException):
    pass


def _alarm(signum: int, frame: object) -> None:
    raise _OutOfTime


@dataclass(frozen=True)
class Removal:
    line: int
    conjunct: str
    text: str  # The whole source with this conjunct gone; no line moves.


def removals(text: str) -> list[Removal]:
    """One weakened source per top-level conjunct of each `requires(...)`, in source order."""
    found: list[Removal] = []
    index = 0
    while True:
        match = _CLAUSE.search(text, index)
        if match is None:
            return found
        depth, end = 0, match.end() - 1
        while end < len(text):
            depth += (text[end] == "(") - (text[end] == ")")
            if depth == 0:
                break
            end += 1
        parts = conjuncts(text[match.end() : end])
        line = text.count("\n", 0, match.start()) + 1
        for position, part in enumerate(parts):
            rest = parts[:position] + parts[position + 1 :]
            clause = f"requires({' && '.join(rest)})" if rest else ""
            found.append(Removal(line, part, text[: match.start()] + clause + text[end + 1 :]))
        index = end + 1


def owner(unit_program: ir.Program, line: int) -> ir.Function:
    """The function whose header holds a clause on `line`: the last one that starts at or before it."""
    best = unit_program.functions[0]
    for function in unit_program.functions:
        if function.location.line <= line:
            best = function
    return best


def draw(function: ir.Function, program: ir.Program, rng: Random) -> Inputs:
    """One input of the small domain; every buffer holds exactly what its length says."""
    lengths = {p.length.name for p in function.parameters if p.length is not None}
    scalars: dict[str, int] = {}
    arrays: dict[str, list[int]] = {}
    for parameter in function.parameters:
        symbol = parameter.symbol
        if isinstance(symbol.type, ir.ArrayType):
            continue
        if symbol.type is ir.ScalarType.BOOL:
            scalars[symbol.name] = rng.choice((0, 1))
        else:
            scalars[symbol.name] = rng.choice(LENGTHS if symbol.name in lengths else SCALARS)
    for parameter in function.parameters:
        symbol = parameter.symbol
        if not isinstance(symbol.type, ir.ArrayType):
            continue
        size = scalars[parameter.length.name] if parameter.length is not None else rng.choice(LENGTHS)
        small = symbol.type.element in {ir.ScalarType.BOOL, ir.ScalarType.CHAR}
        choices = (0, 1) if symbol.type.element is ir.ScalarType.BOOL else (0, 1, 2, 9) if small else ELEMENTS
        arrays[symbol.name] = [rng.choice(choices) for _ in range(max(0, min(size, MAX_BUFFER)))]
    return Inputs(scalars, arrays, {item.symbol.name: rng.choice(ELEMENTS) for item in program.globals})


def search(
    original: ir.Program, weakened: ir.Program, function: str, target: Target, seed: str
) -> tuple[str, str, int | None]:
    """(expected, the first input that shows it, the line of an overflow) from draws of the small domain."""
    rng = Random(seed)
    entry = next(item for item in weakened.functions if item.name == function)
    refusal = f"requires of {function} is false"
    overflow = ""
    overflow_line: int | None = None
    usable = 0
    lost = False
    for _ in range(DRAWS):
        if usable == USABLE:
            break
        inputs = draw(entry, weakened, rng)
        before = interpret.run(original, inputs, target=target, function=function, fuel=FUEL)
        if not (isinstance(before, interpret.Rejection) and before.message == refusal):
            continue  # Inside the full contract, or not a state this function can be entered in.
        after = interpret.run(weakened, inputs, target=target, function=function, fuel=FUEL)
        shown = f"{dict(inputs.scalars)} {dict(inputs.arrays)} {dict(inputs.globals)}"
        if isinstance(after, interpret.Rejection) and after.message == refusal:
            continue  # Another conjunct keeps this input out.
        usable += 1
        if isinstance(after, interpret.Rejection):
            callee = after.kind == "PreconditionViolated" and after.message != refusal
            if after.kind in SAFETY or callee or after.annotation_violations:
                return "witness", f"{after.kind}: {after.message}; {shown}", None
            if after.kind == "Overflow" and not overflow:
                overflow = f"Overflow: {after.message}; {shown}"
                overflow_line = after.location.line if after.location is not None else None
            lost = lost or after.kind in {"Unsupported", "Inconclusive", "AnnotationUndefined"}
        elif after.annotation_violations:
            return "witness", f"{after.annotation_violations[0]} is false; {shown}", None
    if overflow:
        return "overflow", overflow, overflow_line
    return ("undecided", "", None) if lost else ("none", "", None)


def sites(certification: Certification) -> list[tuple[str, int, int, bool]]:
    found = [*certification.emission.decisions, *certification.emission.overflow]
    return sorted((item.kind, item.location.line, item.location.column or 0, item.removed) for item in found)


def body(c: str) -> str:
    """Certified C without the entry checks, the proof identifiers and the source positions."""
    kept = [line for line in c.splitlines() if not _ENTRY_CHECK.match(line)]
    return _POSITION.sub(".c:L:C", _HASH.sub(":#", "\n".join(kept)))


def judge(source: str, baseline: Certification, removal: Removal, target: Target, name: str) -> dict[str, object]:
    """One removal row (without the program's name)."""
    row: dict[str, object] = {"row": "removal", "status": None, "line": removal.line, "conjunct": removal.conjunct}
    try:
        original = adapter.load_text(source, "p.c")
        weakened_unit = adapter.load_text(removal.text, "p.c")
        function = owner(original.program, removal.line).name
        expected, witness, overflow_line = search(
            adapter.released(original),
            adapter.released(weakened_unit),
            function,
            target,
            f"pfc2-eval-breakit:{name}:{removal.line}:{removal.conjunct}",
        )
        judged = adapter.check(weakened_unit, target, level=baseline.level)[1]
    except FrontendError as error:
        return {
            **row,
            "function": None,
            "expected": None,
            "witness": f"front end: {error.diagnostic.rule}",
            "certified": None,
            "decisions_same": None,
            "code_same": None,
            "overflow_trap_kept": None,
            "as_expected": None,
        }
    before, after = sites(baseline), sites(judged)
    decisions = before == after
    code = judged.c is not None and baseline.c is not None and body(judged.c) == body(baseline.c)
    # The arithmetic that overflowed on the witness must have its trap in the weakened program's C.
    trapped = any(item[0] == "overflow" and item[1] == overflow_line and not item[3] for item in after)
    good: bool | None
    if expected == "witness":
        good = not judged.accepted
    elif expected == "overflow":
        good = not judged.accepted or trapped
    elif expected == "undecided":
        good = None
    else:
        good = judged.accepted and decisions and code
    return {
        **row,
        "function": function,
        "expected": expected,
        "witness": witness or None,
        "certified": judged.accepted,
        "decisions_same": decisions if judged.accepted else None,
        "code_same": code if judged.accepted else None,
        "overflow_trap_kept": trapped if judged.accepted and expected == "overflow" else None,
        "as_expected": good,
    }


def one_program(arguments: tuple[str, str, str, int, str]) -> list[dict[str, object]]:
    """The program's status row, then one row per removed conjunct when it is certified."""
    name, source, compiler, budget, stratum = arguments
    target = read_target(compiler)
    empty: dict[str, object] = dict.fromkeys(
        ("function", "line", "conjunct", "expected", "witness", "certified", "decisions_same", "code_same"), None
    )
    empty.update({"overflow_trap_kept": None, "as_expected": None})

    def status(text: str) -> dict[str, object]:
        return {**empty, "row": "program", "program": name, "stratum": stratum, "status": text}

    rows: list[dict[str, object]] = []
    signal.signal(signal.SIGALRM, _alarm)
    signal.setitimer(signal.ITIMER_REAL, budget, 1.0)
    try:
        baseline = adapter.check(adapter.load_text(source, "p.c"), target, level="memory")[1]
        if not baseline.accepted:
            return [status("not certified")]
        rows = [
            {**judge(source, baseline, removal, target, name), "program": name, "stratum": stratum}
            for removal in removals(source)
        ]
        return [status("used"), *rows]
    except FrontendError:
        return [status("not accepted by the front end")]
    except _OutOfTime:
        return [status("not judged within the time budget")]
    except ctypes.ArgumentError as error:
        # The timer can fire while ctypes converts an argument of a solver call; ctypes then reports the
        # timer's exception as its own, by name (amendments 25 and 27). Anything else is a real error.
        if _OutOfTime.__name__ not in str(error):
            raise
        return [status("not judged within the time budget")]
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)


def by_stratum(rows: list[dict[str, object]]) -> dict[str, object]:
    """The registered summary on the generated programs; the examples (development data) beside it."""
    generated = summarise(row for row in rows if row["stratum"] == "generated")
    return {**generated, "examples": summarise(row for row in rows if row["stratum"] == "examples")}


def summarise(rows: Iterable[Mapping[str, object]]) -> dict[str, object]:
    """Sensitivity and specificity as registered; overflow-only witnesses and unusable removals apart."""
    statuses: Counter[str] = Counter()
    counts: Counter[tuple[str, bool]] = Counter()
    unusable = 0
    undecided = 0
    missed: list[str] = []
    changed: list[str] = []
    for row in rows:
        if row["row"] == "program":
            statuses[str(row["status"])] += 1
            continue
        if row["expected"] is None:
            unusable += 1
            continue
        if row["expected"] == "undecided":
            undecided += 1
            continue
        counts[(str(row["expected"]), bool(row["as_expected"]))] += 1
        label = f"{row['program']} {row['function']} line {row['line']}: {row['conjunct']}"
        if row["expected"] == "witness" and not row["as_expected"]:
            missed.append(label)
        if row["expected"] == "none" and not row["as_expected"]:
            changed.append(label)

    def share(kind: str) -> dict[str, object]:
        good, total = counts[(kind, True)], counts[(kind, True)] + counts[(kind, False)]
        return {"as_expected": good, "total": total, "rate": good / total if total else None}

    sensitivity, specificity = share("witness"), share("none")
    return {
        "passed": sensitivity["rate"] == 1.0 and specificity["rate"] == 1.0,
        "sensitivity_passed": sensitivity["rate"] == 1.0,
        "specificity_passed": specificity["rate"] == 1.0,
        "programs": dict(sorted(statuses.items())),
        "sensitivity": sensitivity,
        "specificity": specificity,
        "overflow_only": share("overflow"),
        "removals_not_accepted_by_the_front_end": unusable,
        "removals_the_interpreter_could_not_decide": undecided,
        "witness_and_still_certified": missed,
        "no_witness_and_changed": changed[:200],
    }


def table(summary: Mapping[str, object]) -> str:
    def cells(part: Mapping[str, object], key: str) -> str:
        item = part[key]
        assert isinstance(item, dict)
        rate = "—" if item["rate"] is None else f"{item['rate']:.3f}"
        return f"{item['as_expected']} | {item['total']} | {rate}"

    def block(title: str, part: Mapping[str, object]) -> list[str]:
        return [
            f"## {title}",
            "",
            "| What the small-domain search found | As expected | Removals | Rate |",
            "| --- | ---: | ---: | ---: |",
            f"| a witness: the certificate must be lost (sensitivity) | {cells(part, 'sensitivity')} |",
            f"| no witness in the domain: nothing may change (specificity) | {cells(part, 'specificity')} |",
            f"| only an overflow: a trap kept again, or the certificate lost | {cells(part, 'overflow_only')} |",
            "",
            f"Not decided by the interpreter: {part['removals_the_interpreter_could_not_decide']}; "
            f"not accepted by the front end: {part['removals_not_accepted_by_the_front_end']}.",
            "",
        ]

    examples = summary.get("examples")
    return "\n".join(
        [
            "# E2: one `requires` conjunct removed at a time",
            "",
            *block("Generated programs (the registered population)", summary),
            *(block("Examples (development data, reported apart)", examples) if isinstance(examples, dict) else []),
            f"Domain: up to {DRAWS} draws per removal, stopping at {USABLE} usable; scalars {list(SCALARS)}; "
            f"lengths {list(LENGTHS)}; "
            f"elements {list(ELEMENTS)}.",
            "",
        ]
    )


def _rows(records: tuple[evidence.Record, ...]) -> Iterable[Mapping[str, object]]:
    return [record.data for record in records]


def run(
    *,
    output: Path,
    compiler: str,
    seed: int,
    programs: int,
    directories: Iterable[Path] = (),
    workers: int = 1,
    budget: int = JUDGING_SECONDS,
    dry_run: bool = False,
    progress: Callable[[str], None] = campaign.progress,
) -> bool:
    """Generated programs from `seed` upward until `programs` are certified and weakened; then every example."""
    examples = [
        (path.relative_to(directory).as_posix(), path.read_text(encoding="utf-8"))
        for directory in directories
        for path in sorted(directory.rglob("*.c"))
        if "wrong" not in path.parts
    ]
    if dry_run:
        progress(
            f"breakit: would weaken {programs} certified programs from seed {seed} "
            f"and {len(examples)} examples into {output}"
        )
        return True
    settings = {
        "programs_wanted": programs,
        "examples": len(examples),
        "draws_per_removal": DRAWS,
        "usable_inputs_wanted": USABLE,
        "scalars": list(SCALARS),
        "lengths": list(LENGTHS),
        "elements": list(ELEMENTS),
        "max_buffer": MAX_BUFFER,
        "generator": generate.GENERATOR,
        "judging_seconds": budget,
        "level": "memory",
        "workers": workers,
    }
    started = campaign.start(EXPERIMENT, output, compiler=compiler, seed=seed, settings=settings, schema=SCHEMA)
    kept: list[dict[str, object]] = []
    used, number = 0, seed
    with ProcessPoolExecutor(max_workers=workers) as pool:
        while used < programs and number < seed + 10 * programs:
            batch = [
                (f"g{n}", generate.program(n).text, compiler, budget, "generated")
                for n in range(number, number + 2 * workers)
            ]
            number += 2 * workers
            for rows in pool.map(one_program, batch):
                if used >= programs:
                    break  # Programs beyond the registered count are not recorded.
                used += rows[0]["status"] == "used"
                for index, row in enumerate(rows):
                    started.evidence.record(str(row["program"]), "rows", f"r{index}", row)
                kept += rows
            progress(f"breakit: {used}/{programs} programs weakened")
        listed = [(name, text, compiler, budget, "examples") for name, text in examples]
        for rows in pool.map(one_program, listed):
            for index, row in enumerate(rows):  # A path is not a record name: `01_count/count.c` -> `01_count-count.c`.
                started.evidence.record(str(row["program"]).replace("/", "-"), "rows", f"r{index}", row)
            kept += rows
    summary = by_stratum(kept)
    campaign.finish(started, summary, table(summary), _rows)
    progress(
        f"breakit: sensitivity {summary['sensitivity']}, specificity {summary['specificity']}; "
        f"{'passed' if summary['passed'] else 'FAILED'}"
    )
    return bool(summary["passed"])
