"""E5: a change that cannot change the meaning must not change the verdict.

Each certified program is rewritten four ways on its text, one at a time:

    rename   every name the program introduces gets one fixed suffix
    reorder  two adjacent local declarations that do not depend on each other change places
    swap     the operands of one `+`, `*`, `==` or `!=` change places
    layout   the clauses and the `{` of every function are joined to the line of its signature

and judged again. The verdict and the decision at every site (kind, line, removed or kept) must be the same
under the line map of the rewriting; for `rename` and `layout` the certified C must also be the same once the
suffix, the proof identifiers and the source positions are taken out. A rewriting that does not apply to a
program is counted as such, never as agreement.

That a rewriting keeps the meaning is itself checked, apart from the solver: the interpreter runs the program
and its variant on the same inputs. A difference there is a defect of this module, reported on its own.
"""

import ctypes
import re
import signal
from collections import Counter
from collections.abc import Callable, Iterable, Mapping
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from pfc2.core.diagnostics import FrontendError
from pfc2.core.target import Target, read_target
from pfc2.gate import Certification
from pfc2_eval import adapter, campaign, evidence, generate, interpret
from pfc2_eval.interpret import Inputs

EXPERIMENT = "robustness"
VARIANTS = ("rename", "reorder", "swap", "layout")
OUTCOMES = ("same", "differs", "not applicable", "variant not accepted by the front end")
SUFFIX = "_zq"
CASES = 20
FUEL = 200_000
JUDGING_SECONDS = 600
SCHEMA = evidence.Schema(
    (
        evidence.Column("row", "string", allowed=("program", "variant")),
        evidence.Column("program", "string"),
        evidence.Column("status", "string", nullable=True),
        evidence.Column("variant", "string", nullable=True, allowed=VARIANTS),
        evidence.Column("outcome", "string", nullable=True, allowed=OUTCOMES),
        evidence.Column("verdict_same", "boolean", nullable=True),
        evidence.Column("decisions_same", "boolean", nullable=True),
        evidence.Column("code_same", "boolean", nullable=True),
        evidence.Column("behaviour_same", "boolean", nullable=True),
        evidence.Column("sites", "integer", nullable=True),
    )
)
RESERVED = frozenset(
    "auto break case char const continue default do double else enum extern float for goto if inline int long "
    "register restrict return short signed sizeof static struct switch typedef union unsigned void volatile while "
    "_Bool bool true false requires ensures result invariant decreases assert where separated law string".split()
)
_TOKEN = re.compile(r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|[0-9][0-9A-Za-z_.]*|[A-Za-z_][A-Za-z0-9_]*')
_LOCAL = re.compile(r"^(\s*)(?:long|int|_Bool) ([A-Za-z_]\w*) = (.+);$")
_EFFECT = re.compile(r"[A-Za-z_]\w*\s*\(|\+\+|--|[^=!<>]=[^=]")
_CLAUSE_LINE = re.compile(r"^\s*(?:requires|ensures|invariant|decreases|where)\s*\(")
_OPERAND = r"-?[A-Za-z0-9_@]+"
_SKELETON = re.compile(rf"^({_OPERAND}) (\+|\*|==|!=) ({_OPERAND})$")
_HASH = re.compile(r":[0-9a-f]{64}")
_POSITION = re.compile(r"\.c:\d+:\d+")


class _OutOfTime(BaseException):
    pass


def _alarm(signum: int, frame: object) -> None:
    raise _OutOfTime


@dataclass(frozen=True)
class Variant:
    text: str
    lines: Mapping[int, int]  # Line of the original -> line of the variant, where they differ.


def rename(text: str) -> Variant | None:
    """Every introduced name with SUFFIX; not applicable when a directive other than the PFC2 header is present."""
    out = []
    for line in text.splitlines(keepends=True):
        if line.lstrip().startswith("#"):
            if line.split() != ["#include", '"pfc.h"']:
                return None
            out.append(line)
            continue

        def renamed(match: re.Match[str]) -> str:
            word = match.group(0)
            plain = word[0].isalpha() or word[0] == "_"
            return word + SUFFIX if plain and word not in RESERVED and not word.startswith("pfc") else word

        out.append(_TOKEN.sub(renamed, line))
    return Variant("".join(out), {})


def reorder(text: str) -> Variant | None:
    """Swap the first two adjacent local declarations where neither reads the other and neither has an effect."""
    lines = text.splitlines(keepends=True)
    for index in range(len(lines) - 1):
        first, second = _LOCAL.match(lines[index].rstrip("\n")), _LOCAL.match(lines[index + 1].rstrip("\n"))
        if first is None or second is None or first.group(1) != second.group(1):
            continue
        if _EFFECT.search(first.group(3)) or _EFFECT.search(second.group(3)):
            continue
        if re.search(rf"\b{first.group(2)}\b", second.group(3)) or re.search(rf"\b{second.group(2)}\b", first.group(3)):
            continue
        lines[index], lines[index + 1] = lines[index + 1], lines[index]
        return Variant("".join(lines), {index + 1: index + 2, index + 2: index + 1})
    return None


def _closing(text: str, start: int) -> int:
    depth = 0
    for index in range(start, len(text)):
        depth += (text[index] in "([") - (text[index] in ")]")
        if depth == 0:
            return index
    return -1


def _filled(operand: str, groups: list[str]) -> str:
    """The operand with each `@` replaced by the text it stood for."""
    pending = iter(groups)
    return re.sub("@", lambda _: next(pending), operand)


def swap(text: str) -> Variant | None:
    """Exchange the operands of the first parenthesised `+`, `*`, `==` or `!=` whose operands have no effect."""
    offset = 0
    for line in text.splitlines(keepends=True):
        body = line.rstrip("\n")
        if not body.lstrip().startswith("#") and not _CLAUSE_LINE.match(body):
            for start, character in enumerate(body):
                if character != "(":
                    continue
                before = re.search(r"([A-Za-z_]\w*)\s*$", body[:start])
                if before is not None and before.group(1) not in {"if", "while", "return"}:
                    continue  # The arguments of a call or of a clause.
                end = _closing(body, start)
                if end < 0:
                    continue
                inner = body[start + 1 : end]
                if _EFFECT.search(inner) or ";" in inner or "?" in inner:
                    continue
                skeleton, groups, position = [], [], 0
                while position < len(inner):
                    if inner[position] in "([":
                        stop = _closing(inner, position)
                        if stop < 0:
                            break
                        skeleton.append("@")  # A parenthesised operand, or the index after a name.
                        groups.append(inner[position : stop + 1])
                        position = stop + 1
                    else:
                        skeleton.append(inner[position])
                        position += 1
                match = _SKELETON.match("".join(skeleton))
                if match is None:
                    continue
                cut = match.group(1).count("@")
                left, right = _filled(match.group(1), groups[:cut]), _filled(match.group(3), groups[cut:])
                swapped = f"{right} {match.group(2)} {left}"
                if swapped == inner:
                    continue
                changed = offset + start + 1
                return Variant(text[:changed] + swapped + text[changed + len(inner) :], {})
        offset += len(line)
    return None


def layout(text: str) -> Variant | None:
    """Join every clause line and every lone `{` to the line before it."""
    out: list[str] = []
    lines: dict[int, int] = {}
    joined = False
    for number, line in enumerate(text.splitlines(), start=1):
        if out and (_CLAUSE_LINE.match(line) or line.strip() == "{") and out[-1].strip():
            out[-1] = f"{out[-1].rstrip()} {line.strip()}"
            joined = True
        else:
            out.append(line)
        if len(out) != number:
            lines[number] = len(out)
    return Variant("\n".join(out) + "\n", lines) if joined else None


REWRITINGS: Mapping[str, Callable[[str], Variant | None]] = {
    "rename": rename,
    "reorder": reorder,
    "swap": swap,
    "layout": layout,
}


def sites(certification: Certification, lines: Mapping[int, int]) -> list[tuple[str, int, bool]]:
    """Every decision as (kind, line, removed), in the variant's line numbers, in a fixed order."""
    found = [*certification.emission.decisions, *certification.emission.overflow]
    return sorted((item.kind, lines.get(item.location.line, item.location.line), item.removed) for item in found)


def normalised(c: str) -> str:
    """Certified C without the renaming suffix, the proof identifiers and the source positions."""
    return _POSITION.sub(".c:L:C", _HASH.sub(":#", c.replace(SUFFIX, "")))


def _suffixed(inputs: Inputs) -> Inputs:
    return Inputs(
        {f"{name}{SUFFIX}": value for name, value in inputs.scalars.items()},
        {f"{name}{SUFFIX}": value for name, value in inputs.arrays.items()},
        {f"{name}{SUFFIX}": value for name, value in inputs.globals.items()},
    )


def _observed(text: str, name: str, inputs: Inputs, target: Target, entry: str) -> tuple[object, ...]:
    unit = adapter.load_text(text, name)
    seen = interpret.run(adapter.released(unit), inputs, target=target, function=entry, fuel=FUEL)
    if isinstance(seen, interpret.Rejection):
        return ("rejected",)
    strip = len(SUFFIX) if entry.endswith(SUFFIX) else 0

    def plain(values: Mapping[str, object]) -> list[tuple[str, object]]:
        return sorted((key[: len(key) - strip] if strip else key, value) for key, value in values.items())

    return ("returned", seen.result, plain(seen.arrays), plain(seen.globals), seen.output)


def behaviour_same(source: str, variant: str, kind: str, cases: list[Inputs], target: Target) -> bool:
    """The interpreter's complete observation of both texts on every case (a rejection equals a rejection)."""
    renamed = kind == "rename"
    for case in cases:
        before = _observed(source, "p.c", case, target, "entry")
        after = _observed(
            variant, "p.c", _suffixed(case) if renamed else case, target, f"entry{SUFFIX if renamed else ''}"
        )
        if before != after:
            return False
    return True


def compare(source: str, baseline: Certification, kind: str, cases: list[Inputs], target: Target) -> dict[str, object]:
    """One variant row (without the program's name)."""
    row: dict[str, object] = {"row": "variant", "status": None, "variant": kind, "verdict_same": None}
    row.update({"decisions_same": None, "code_same": None, "behaviour_same": None, "sites": None})
    variant = REWRITINGS[kind](source)
    if variant is None:
        return {**row, "outcome": "not applicable"}
    try:
        judged = adapter.check(adapter.load_text(variant.text, "p.c"), target, level=baseline.level)[1]
        behaviour = behaviour_same(source, variant.text, kind, cases, target)
    except FrontendError:
        return {**row, "outcome": "variant not accepted by the front end"}
    before = sites(baseline, variant.lines)
    verdict = judged.accepted == baseline.accepted and len(judged.blockers) == len(baseline.blockers)
    decisions = before == sites(judged, {})
    code: bool | None = None
    if kind in {"rename", "layout"}:
        code = judged.c is not None and baseline.c is not None and normalised(judged.c) == normalised(baseline.c)
    same = verdict and decisions and code is not False
    row.update({"verdict_same": verdict, "decisions_same": decisions, "code_same": code, "behaviour_same": behaviour})
    return {**row, "outcome": "same" if same else "differs", "sites": len(before)}


def one_program(arguments: tuple[str, str, int | None, str, int]) -> list[dict[str, object]]:
    """The program's status row, then one row per rewriting when it is certified."""
    name, source, seed, compiler, budget = arguments
    target = read_target(compiler)
    empty: dict[str, object] = {"variant": None, "outcome": None, "verdict_same": None, "decisions_same": None}
    empty.update({"code_same": None, "behaviour_same": None, "sites": None})

    def status(text: str) -> dict[str, object]:
        return {**empty, "row": "program", "program": name, "status": text}

    signal.signal(signal.SIGALRM, _alarm)
    signal.setitimer(signal.ITIMER_REAL, budget, 1.0)
    try:
        baseline = adapter.check(adapter.load_text(source, "p.c"), target, level="memory")[1]
        if not baseline.accepted:
            return [status("not certified")]
        cases = generate.cases(generate.program(seed), CASES) if seed is not None else []
        rows = [status("used")]
        rows += [{**compare(source, baseline, kind, cases, target), "program": name} for kind in VARIANTS]
        return rows
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


def summarise(rows: Iterable[Mapping[str, object]]) -> dict[str, object]:
    """Counts by rewriting; passed when nothing differs, no behaviour differs and every rewriting applied once."""
    statuses: Counter[str] = Counter()
    outcomes: Counter[tuple[str, str]] = Counter()
    differing: list[str] = []
    defects: list[str] = []
    for row in rows:
        if row["row"] == "program":
            statuses[str(row["status"])] += 1
            continue
        kind = str(row["variant"])
        outcomes[(kind, str(row["outcome"]))] += 1
        if row["outcome"] == "differs":
            differing.append(f"{row['program']} {kind}")
        if row["behaviour_same"] is False:
            defects.append(f"{row['program']} {kind}")
    applied = {kind: outcomes[(kind, "same")] + outcomes[(kind, "differs")] for kind in VARIANTS}
    return {
        "passed": not differing and not defects and all(applied.values()),
        "programs": dict(sorted(statuses.items())),
        "variants": {kind: {name: outcomes[(kind, name)] for name in OUTCOMES} for kind in VARIANTS},
        "compared": sum(applied.values()),
        "differing": differing,
        "rewriting_changed_behaviour": defects,
    }


def table(summary: Mapping[str, object]) -> str:
    variants = summary["variants"]
    assert isinstance(variants, dict)
    lines = [
        "# E5: rewritings that keep the meaning",
        "",
        "| Rewriting | Same | Differs | Not applicable | Not accepted by the front end |",
        "| --- | ---: | ---: | ---: | ---: |",
        *[f"| {kind} | " + " | ".join(str(variants[kind][name]) for name in OUTCOMES) + " |" for kind in VARIANTS],
        "",
        f"Rewritings that changed what the interpreter observes: {len(summary['rewriting_changed_behaviour'])}",  # type: ignore[arg-type]
        "",
    ]
    return "\n".join(lines)


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
    """Generated programs from `seed` upward until `programs` of them are certified and rewritten."""
    if dry_run:
        progress(f"robustness: would rewrite {programs} certified programs from seed {seed} into {output}")
        return True
    settings = {
        "programs_wanted": programs,
        "variants": list(VARIANTS),
        "suffix": SUFFIX,
        "interpreter_cases": CASES,
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
                (f"g{n}", generate.program(n).text, n, compiler, budget) for n in range(number, number + 2 * workers)
            ]
            number += 2 * workers
            for rows in pool.map(one_program, batch):
                if used >= programs:
                    break  # Programs beyond the registered count are not recorded.
                used += rows[0]["status"] == "used"
                for index, row in enumerate(rows):
                    started.evidence.record(str(row["program"]), "rows", f"r{index}", row)
                kept += rows
            progress(f"robustness: {used}/{programs} programs rewritten")
    summary = summarise(kept)
    campaign.finish(started, summary, table(summary), _rows)
    progress(f"robustness: {'passed' if summary['passed'] else 'FAILED'}; compared {summary['compared']}")
    return bool(summary["passed"])
