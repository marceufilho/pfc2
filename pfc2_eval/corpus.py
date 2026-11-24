"""Tests versus proofs on ported modules: upstream tests against a port, and mutants of the port against both.

A unit is a directory with `port.c` (PFC2 source: the upstream solution ported, with its contract) and
`glue.c` (host C that offers the upstream interface on top of the port). The upstream exercise supplies the
header, the test file and the Unity test framework, used unmodified except that the `TEST_IGNORE()` lines,
which the exercise tells the learner to delete, are deleted.

Measured here:

- do the upstream tests pass against the port compiled as plain C, and against the certified C;
- for each mutant of the port's code (never of its contract): do the upstream tests fail, and does PFC2
  refuse the mutant with a failed obligation. A refusal that is only a timeout or an unknown is recorded as
  inconclusive, not as detection. A mutant that does not compile is discarded and counted.

The mutants change one token on one line of code: a relational operator, an arithmetic operator, or an integer
constant by one; or they delete one assignment statement. Lines that carry a clause (`requires`, `ensures`,
`invariant`, `decreases`, `assert`, `where`) are left alone, so the loop conditions written on such lines are not
mutated: the count of mutants is a lower bound of what the operators could produce.
"""

import json
import math
import multiprocessing
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from collections.abc import Callable, Iterable, Mapping
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from multiprocessing.connection import Connection
from pathlib import Path
from random import Random

from pfc2.core.config import C_FLAGS
from pfc2.core.diagnostics import FrontendError
from pfc2.core.target import Target, read_target
from pfc2.gate import Level
from pfc2_eval import adapter, build, campaign, evidence, heldout, stats

EXPERIMENT = "corpus"
CLAUSE = re.compile(r"\b(requires|ensures|invariant|decreases|assert|where|law)\b")
RELATIONAL = {"<=": ["<", "=="], "<": ["<=", "!="], ">=": [">", "=="], ">": [">=", "!="], "==": ["!="], "!=": ["=="]}
ARITHMETIC = {"+": ["-"], "-": ["+"], "*": ["+"], "/": ["*"], "%": ["/"]}
TOKEN = re.compile(r"'(?:[^'\\]|\\.)'|<=|>=|==|!=|&&|\|\||\+\+|--|[-+*/%]=|[<>+\-*/%]|\b\d+\b")
# An assignment statement: not a declaration, not a return.
DELETABLE = re.compile(
    r"(?!long\b|_Bool\b|const\b|char\b|int\b|return\b)[A-Za-z_][\w\[\] +\-*/%]*?\s*(=(?!=)|[-+*/%]=|\+\+|--).*;"
)
SUMMARY = re.compile(r"(\d+) Tests (\d+) Failures (\d+) Ignored")
PROOF = ("certified", "refused-failed", "refused-inconclusive", "rejected", "not-judged")
TESTS = ("pass", "fail", "crash")
SUBSUMPTION = ("subsumed", "not-subsumed", "inexpressible", "error", "not-judged")
BUDGET_SECONDS = 600.0
COMMENT = re.compile(r"/\*.*?\*/", re.DOTALL)
LAW = re.compile(r"(?m)^law\b")
REGISTERED_RULES = frozenset(f"P{number}" for number in range(1, 9))
REVIEW_SEED = 20261118
SCHEMA = evidence.Schema(
    (
        evidence.Column("row", "string", allowed=("unit", "mutant", "assertion")),
        evidence.Column("unit", "string"),
        evidence.Column("level", "string", nullable=True),
        evidence.Column("upstream_tests", "integer", nullable=True),
        evidence.Column("tests_on_port", "string", nullable=True, allowed=TESTS),
        evidence.Column("tests_on_certified", "string", nullable=True, allowed=TESTS),
        evidence.Column("code_lines", "integer", nullable=True),
        evidence.Column("clause_lines", "integer", nullable=True),
        evidence.Column("mutant", "string", nullable=True),
        evidence.Column("operator", "string", nullable=True),
        evidence.Column("line", "integer", nullable=True),
        evidence.Column("tests", "string", nullable=True, allowed=TESTS),
        evidence.Column("proof", "string", nullable=True, allowed=PROOF),
        evidence.Column("case", "string", nullable=True),
        evidence.Column("subsumption", "string", nullable=True, allowed=SUBSUMPTION),
    )
)


@dataclass(frozen=True)
class Mutant:
    identifier: str
    operator: str
    line: int
    text: str


def mutants(source: str) -> list[Mutant]:
    """Every single-token mutant of the code lines of a port, and every deletion of an assignment statement."""
    lines = source.split("\n")
    found: list[Mutant] = []
    depth = 0
    for number, line in enumerate(lines, 1):
        inside = depth > 0
        depth += line.count("{") - line.count("}")
        if not inside or CLAUSE.search(line) or line.lstrip().startswith(("/*", "*", "//", "#")):
            continue

        def variant(text: str, operator: str, at: int = number) -> None:
            changed = [*lines[: at - 1], text, *lines[at:]]
            found.append(Mutant(f"m{len(found):03d}", operator, at, "\n".join(changed)))

        for match in TOKEN.finditer(line):
            token = match.group()
            before, after = line[: match.start()], line[match.end() :]
            if token in RELATIONAL:
                for other in RELATIONAL[token]:
                    variant(before + other + after, "relational")
            elif token in ARITHMETIC:
                unary = not re.search(r"[\w)\]]\s*$", before)
                if not unary:
                    for other in ARITHMETIC[token]:
                        variant(before + other + after, "arithmetic")
            elif token.isdigit():
                for number_ in (int(token) + 1, int(token) - 1):
                    if number_ >= 0:
                        variant(before + str(number_) + after, "constant")
        statement = line.strip()
        if DELETABLE.fullmatch(statement):
            variant(line[: len(line) - len(line.lstrip())] + ";", "deletion")
    return found


def declarations(source: str) -> str:
    """The contracts alone: every function body replaced by `;`, every law and comment removed."""
    text = COMMENT.sub("", source)
    kept: list[str] = []
    start = 0
    position = 0
    while position < len(text):
        if text[position] != "{":
            position += 1
            continue
        end = position + 1
        depth = 1
        while depth:
            if text[end] == "'":  # A character constant may hold a brace.
                end = text.index("'", end + 2) + 1
                continue
            depth += {"{": 1, "}": -1}.get(text[end], 0)
            end += 1
        head = text[start:position]
        written_law = LAW.search(head)
        kept.append(head[: written_law.start()] if written_law else head.rstrip() + ";\n")
        start = position = end
    kept.append(text[start:])
    return "".join(kept)


def law(declared: str, functions: Mapping[str, Mapping[str, str]], case: Mapping[str, object]) -> str:
    """One upstream assertion as a law over fixed inputs: assume the inputs, call, assert what the test expects."""
    function = functions[str(case["function"])]
    inputs = case["inputs"]
    assert isinstance(inputs, Mapping)
    facts: list[str] = []
    for name, value in inputs.items():
        if isinstance(value, str):
            facts += [f"{name}[{index}] == {ord(character)}" for index, character in enumerate(value)]
        elif isinstance(value, list):
            facts += [f"{name}[{index}] == {element}" for index, element in enumerate(value)]
        else:
            facts.append(f"{name} == {value}")
    known = " && ".join(facts) or "1 == 1"
    # An array the function writes is a local of the law when it must not overlap the inputs.
    locals_ = str(case.get("locals", function.get("locals", "")))
    call = str(case.get("call", function["call"]))
    return (
        f"{declared.rstrip()}\n\nlaw case_{case['name']}({function['parameters']})\n{{\n"
        + (f"    {locals_}\n\n" if locals_ else "")
        + f"    if ({known}) {{\n        {function['result']} found = {call};\n\n"
        f"        assert({case['expected']});\n    }}\n}}\n"
    )


def subsumption(
    source: str,
    functions: Mapping[str, Mapping[str, str]],
    case: Mapping[str, object],
    target: Target,
    *,
    defined: bool = False,
    level: Level = "full",
) -> str:
    """Does the contract alone imply this upstream assertion? No body is present, so no body can help.

    `subsumed` means every function that keeps the contract passes the test. An assertion that cannot be
    restated as a law is `inexpressible`; a law the front end refuses is `error`. Neither counts as subsumed.

    With `defined` the law is written beside the definitions instead of beside bare declarations. A law is
    still proved through the contracts of what it calls, never through a body; what changes is that PFC2 does
    not have to show the contract of a body-less function possible for every input, a check it can leave
    undecided for reasons that have nothing to do with the test. The file then holds the unit itself, so it is
    judged at `level`, the level the unit certifies at; beside declarations the level is always `full`.
    """
    if "inexpressible" in case:
        return "inexpressible"
    try:
        text = law(source if defined else declarations(source), functions, case)
        chosen: Level = level if defined else "full"
        _, certification = adapter.check(adapter.load_text(text, "law.c"), target, level=chosen)
    except FrontendError:
        return "error"
    return "subsumed" if certification.accepted else "not-subsumed"


def same_code(port: str, specified: str, compiler: str, scratch: Path) -> bool:
    """Is the specified unit the sealed port plus clauses only? Both are preprocessed with the clauses erased."""
    scratch.mkdir(parents=True, exist_ok=True)
    seen = []
    for name, text in (("port.c", port), ("specified.c", specified)):
        (scratch / name).write_text(text, encoding="utf-8")
        command = [compiler, "-std=c11", "-E", "-P", "-I", str(build.INCLUDE), str(scratch / name)]
        ran = subprocess.run(command, capture_output=True, text=True, check=False, timeout=60)
        if ran.returncode != 0:
            return False
        seen.append(" ".join(ran.stdout.split()))
    return seen[0] == seen[1]


def selection(path: Path, upstream: Path, units: Iterable[str]) -> dict[str, object]:
    """The selection record checked against the upstream directory and the units present; counts for S1."""
    rows = json.loads(path.read_text(encoding="utf-8"))["units"]
    slugs = [str(row["slug"]) for row in rows]
    if slugs != sorted(entry.name for entry in upstream.iterdir() if entry.is_dir()):
        raise ValueError(f"{path} does not list every candidate of {upstream} in order")
    ported = [row for row in rows if row["status"] == "ported"]
    if sorted(str(row["slug"]) for row in ported) != sorted(units):
        raise ValueError(f"the units present are not the units {path} records as ported")
    excluded = Counter(str(row["exclusion"]) for row in rows if row["status"] == "excluded")
    return {
        "candidates": sum(row["status"] != "pilot" for row in rows),
        "pilot": sum(row["status"] == "pilot" for row in rows),
        "ported": len(ported),
        "ported_registered_rules": sum(set(row["rules"]) <= REGISTERED_RULES for row in ported),
        "ported_without_p14": sum("P14" not in row["rules"] for row in ported),
        "fixes": sum(int(row.get("fixes", 0)) for row in ported),
        "excluded": dict(sorted(excluded.items())),
    }


def sample(names: Iterable[str], *, seed: int = REVIEW_SEED, rate: float = 0.2) -> list[str]:
    """The units the author reviews: a seeded draw of `rate` of them, rounded up."""
    ordered = sorted(names)
    return sorted(Random(seed).sample(ordered, math.ceil(rate * len(ordered))))


def _tests(text: str, plain: bool, unit: Path, exercise: Path, scratch: Path, compiler: str) -> str:
    """Outcome of the upstream tests against one version of the port: pass, fail, or crash (also: no build)."""
    slug = exercise.name.replace("-", "_")
    scratch.mkdir(parents=True, exist_ok=True)
    header = exercise / ".meta" / "example.h"
    shutil.copy(header if header.is_file() else exercise / f"{slug}.h", scratch / f"{slug}.h")
    shutil.copytree(exercise / "test-framework", scratch / "test-framework", dirs_exist_ok=True)
    upstream = (exercise / f"test_{slug}.c").read_text(encoding="utf-8")
    (scratch / "tests.c").write_text(
        "\n".join(line for line in upstream.split("\n") if "TEST_IGNORE" not in line), encoding="utf-8"
    )
    (scratch / "port.c").write_text(text, encoding="utf-8")
    flags = [*C_FLAGS, "-Wno-error", *build.SANITIZE, "-I", str(scratch)]
    command = [compiler, *flags]
    command += [*build.PLAIN, "-I", str(build.INCLUDE)] if plain else []
    command += [str(scratch / "port.c"), str(unit / "glue.c"), str(scratch / "tests.c")]
    command += [str(scratch / "test-framework" / "unity.c"), "-lm", "-o", str(scratch / "tests")]
    try:
        built = subprocess.run(command, capture_output=True, text=True, check=False, timeout=180)
        if built.returncode != 0:
            return "crash"
        ran = subprocess.run([str(scratch / "tests")], capture_output=True, text=True, check=False, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return "crash"
    summary = SUMMARY.search(ran.stdout)
    if summary is None or ran.returncode < 0:
        return "crash"
    return "pass" if int(summary.group(2)) == 0 and ran.returncode == 0 else "fail"


def _proof(text: str, level: Level, target: Target) -> tuple[str, str | None]:
    """How PFC2 judges one version of the port, and its released C when certified."""
    try:
        _, certification = adapter.check(adapter.load_text(text, "port.c"), target, level=level)
    except FrontendError:
        return "rejected", None
    if certification.accepted:
        return "certified", certification.c
    primary = [b for b in certification.blockers if not b.status.startswith("depends")]
    return ("refused-failed" if any(b.status == "failed" for b in primary) else "refused-inconclusive"), None


def compiles(text: str, compiler: str, scratch: Path) -> bool:
    scratch.mkdir(parents=True, exist_ok=True)
    (scratch / "m.c").write_text(text, encoding="utf-8")
    command = [compiler, "-std=c11", "-fsyntax-only", "-I", str(build.INCLUDE), str(scratch / "m.c")]
    return subprocess.run(command, capture_output=True, check=False, timeout=60).returncode == 0


def _judge(text: str, level: Level, compiler: str, sender: Connection) -> None:
    sender.send(_proof(text, level, read_target(compiler)))


def _subsume(
    source: str,
    functions: Mapping[str, Mapping[str, str]],
    case: Mapping[str, object],
    compiler: str,
    defined: bool,
    level: Level,
    sender: Connection,
) -> None:
    sender.send(subsumption(source, functions, case, read_target(compiler), defined=defined, level=level))


def within(function: Callable[..., None], arguments: tuple[object, ...], seconds: float) -> object | None:
    """What `function` sends back from a process of its own, or None when it has not answered in time."""
    context = multiprocessing.get_context("spawn")
    receiver, sender = context.Pipe(duplex=False)
    child = context.Process(target=function, args=(*arguments, sender))
    child.start()
    sender.close()
    try:
        answer: object | None = receiver.recv() if receiver.poll(seconds) else None
    except EOFError:
        answer = None
    if child.is_alive():
        child.kill()
    child.join()
    return answer


def judged(text: str, level: Level, compiler: str, seconds: float) -> tuple[str, str | None]:
    """`_proof` within the time budget; `not-judged` when the budget runs out."""
    answer = within(_judge, (text, level, compiler), seconds)
    if answer is None:
        return "not-judged", None
    assert isinstance(answer, tuple)
    return str(answer[0]), answer[1]


def measure(
    unit: Path,
    exercise: Path,
    compiler: str,
    scratch: Path,
    *,
    seconds: float = BUDGET_SECONDS,
    workers: int = 1,
    defined: bool = False,
) -> list[dict[str, object]]:
    """All rows of one unit: its own status, one row per upstream assertion, one row per compilable mutant.

    With `defined` only the assertions are measured, each law beside the definitions (see `subsumption`).
    """
    source = (unit / "port.c").read_text(encoding="utf-8")
    base: dict[str, object] = {column.name: None for column in SCHEMA.columns}
    base["unit"] = unit.name
    level: Level = "full"
    verdict, released = judged(source, "full", compiler, seconds)
    if verdict != "certified":
        level = "memory"
        verdict, released = judged(source, "memory", compiler, seconds)
    upstream = (exercise / f"test_{exercise.name.replace('-', '_')}.c").read_text(encoding="utf-8")
    code = [line for line in source.split("\n") if line.strip() and not line.lstrip().startswith(("/*", "*", "#"))]
    row = {
        **base,
        "row": "unit",
        "level": level if verdict == "certified" else None,
        "proof": verdict,
        "upstream_tests": upstream.count("RUN_TEST("),
        "tests_on_port": _tests(source, True, unit, exercise, scratch / "port", compiler),
        "tests_on_certified": (
            _tests(released, False, unit, exercise, scratch / "certified", compiler) if released is not None else None
        ),
        "code_lines": sum(not CLAUSE.search(line) for line in code),
        "clause_lines": sum(bool(CLAUSE.search(line)) for line in code),
    }
    rows = [row]
    if verdict != "certified" or row["tests_on_port"] != "pass":
        return rows  # Assertions and mutants are measured on units that are certified and pass their tests.
    transcribed = unit / "tests.json"
    cases = json.loads(transcribed.read_text(encoding="utf-8")) if transcribed.is_file() else {}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        if "functions" in cases:

            def implied(case: Mapping[str, object]) -> str:
                answer = within(_subsume, (source, cases["functions"], case, compiler, defined, level), seconds)
                return "not-judged" if answer is None else str(answer)

            for case, outcome in zip(cases["cases"], pool.map(implied, cases["cases"]), strict=True):
                rows.append({**base, "row": "assertion", "level": level, "case": case["name"], "subsumption": outcome})
        generated = [] if defined else mutants(source)
        kept = [mutant for mutant in generated if compiles(mutant.text, compiler, scratch / "syntax")]

        def outcome_of(mutant: Mutant) -> tuple[str, str]:
            tests = _tests(mutant.text, True, unit, exercise, scratch / mutant.identifier, compiler)
            return tests, judged(mutant.text, level, compiler, seconds)[0]

        for mutant, (tests, proof) in zip(kept, pool.map(outcome_of, kept), strict=True):
            rows.append(
                {
                    **base,
                    "row": "mutant",
                    "level": level,
                    "mutant": mutant.identifier,
                    "operator": mutant.operator,
                    "line": mutant.line,
                    "tests": tests,
                    "proof": proof,
                }
            )
    return rows


def _rows(records: tuple[evidence.Record, ...]) -> Iterable[Mapping[str, object]]:
    return [record.data for record in records]


def _proportion(clusters: Mapping[str, list[float]]) -> dict[str, object] | None:
    """A pooled mean with a cluster bootstrap over units, or None when there is nothing to pool."""
    filled = {name: values for name, values in clusters.items() if values}
    if not filled:
        return None
    drawn = stats.cluster_bootstrap(filled, stats.mean, seed=REVIEW_SEED)
    return {
        "estimate": drawn.estimate,
        "low": drawn.interval.low,
        "high": drawn.interval.high,
        "units": len(filled),
        "observations": sum(len(values) for values in filled.values()),
    }


def summarise(rows: Iterable[Mapping[str, object]]) -> dict[str, object]:
    """S2, S3 and S4 from the rows, with the registered hypotheses H4a and H4b computed as registered."""
    units = [row for row in rows if row["row"] == "unit"]
    levels = Counter(str(row["level"] or row["proof"]) for row in units)
    subsumed_by_unit: dict[str, list[float]] = {}
    outcomes: Counter[str] = Counter()
    paired: dict[str, list[float]] = {}
    cells: Counter[str] = Counter()
    by_operator: dict[str, Counter[str]] = {}
    for row in rows:
        name = str(row["unit"])
        if row["row"] == "assertion":
            outcomes[str(row["subsumption"])] += 1
            subsumed_by_unit.setdefault(name, []).append(float(row["subsumption"] == "subsumed"))
        elif row["row"] == "mutant":
            killed = row["tests"] != "pass"
            refused = row["proof"] == "refused-failed"
            cell = {(True, True): "both", (True, False): "tests", (False, True): "proof", (False, False): "neither"}[
                (killed, refused)
            ]
            cells[cell] += 1
            by_operator.setdefault(str(row["operator"]), Counter())[cell] += 1
            if row["proof"] not in ("certified", "refused-failed"):
                cells["proof-inconclusive"] += 1
            paired.setdefault(name, []).append(float(refused) - float(killed))
    return {
        "units": len(units),
        "s2_levels": dict(sorted(levels.items())),
        "s2_tests_pass_on_port": sum(row["tests_on_port"] == "pass" for row in units),
        "s2_code_lines": sum(int(str(row["code_lines"])) for row in units),
        "s2_clause_lines": sum(int(str(row["clause_lines"])) for row in units),
        "s3_assertions": dict(sorted(outcomes.items())),
        "h4a_subsumed_proportion": _proportion(subsumed_by_unit),
        "s4_mutants": dict(sorted(cells.items())),
        "s4_by_operator": {name: dict(sorted(count.items())) for name, count in sorted(by_operator.items())},
        "h4b_refused_minus_killed": _proportion(paired),
    }


def tables(rows: list[Mapping[str, object]]) -> str:
    """The Markdown tables of one campaign."""
    lines = [
        "# Tests versus proofs on ported units",
        "",
        "| Unit | Verdict | Upstream tests | On port | On certified C | Code lines | Clause lines |",
        "| --- | --- | ---: | --- | --- | ---: | ---: |",
    ]
    names = [str(row["unit"]) for row in rows if row["row"] == "unit"]
    for row in rows:
        if row["row"] == "unit":
            lines.append(
                f"| {row['unit']} | {row['level'] or row['proof']} | {row['upstream_tests']} | {row['tests_on_port']} "
                f"| {row['tests_on_certified']} | {row['code_lines']} | {row['clause_lines']} |"
            )
    lines += [
        "",
        "Upstream assertions restated as laws over the contract alone.",
        "",
        "| Unit | Assertions | Subsumed | Not subsumed | Not expressible | Not judged or error |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name in names:
        count = Counter(str(row["subsumption"]) for row in rows if row["row"] == "assertion" and row["unit"] == name)
        if count:
            lines.append(
                f"| {name} | {sum(count.values())} | {count['subsumed']} | {count['not-subsumed']} "
                f"| {count['inexpressible']} | {count['not-judged'] + count['error']} |"
            )
    lines += [
        "",
        "Mutants: tests kill / proof refuses with a failed obligation.",
        "",
        "| Unit | Mutants | Both | Tests only | Proof only | Neither | Proof inconclusive | Rejected by front end |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for name in names:
        found = [row for row in rows if row["row"] == "mutant" and row["unit"] == name]
        if not found:
            continue
        killed = [row["tests"] != "pass" for row in found]
        refused = [row["proof"] == "refused-failed" for row in found]
        lines.append(
            f"| {name} | {len(found)} | {sum(k and r for k, r in zip(killed, refused, strict=True))} "
            f"| {sum(k and not r for k, r in zip(killed, refused, strict=True))} "
            f"| {sum(r and not k for k, r in zip(killed, refused, strict=True))} "
            f"| {sum(not k and not r for k, r in zip(killed, refused, strict=True))} "
            f"| {sum(row['proof'] in ('refused-inconclusive', 'not-judged') for row in found)} "
            f"| {sum(row['proof'] == 'rejected' for row in found)} |"
        )
    lines.append("")
    return "\n".join(lines)


def run(
    *,
    output: Path,
    compiler: str,
    units: Path,
    upstream: Path,
    chosen_from: Path | None = None,
    ports: Path | None = None,
    workers: int = 1,
    seconds: float = BUDGET_SECONDS,
    defined: bool = False,
    dry_run: bool = False,
    progress: Callable[[str], None] = campaign.progress,
) -> bool:
    chosen = sorted(path for path in units.iterdir() if (path / "port.c").is_file())
    names = [path.name for path in chosen]
    heldout.require_intact([units, *([ports] if ports is not None else [])])
    selected = selection(chosen_from, upstream, names) if chosen_from is not None else None
    if dry_run:
        progress(f"corpus: would measure {len(chosen)} units from {units} into {output}")
        return True
    with tempfile.TemporaryDirectory(prefix="pfc2-corpus-") as directory:
        if ports is not None:
            for unit in chosen:
                sealed = (ports / unit.name / "port.c").read_text(encoding="utf-8")
                written = (unit / "port.c").read_text(encoding="utf-8")
                if not same_code(sealed, written, compiler, Path(directory) / "same" / unit.name):
                    raise ValueError(f"{unit.name}: the specified unit is not its sealed port plus clauses")
        settings = {
            "units": names,
            "upstream": str(upstream.name),
            "selection": selected,
            "ports_checked_against": str(ports) if ports is not None else None,
            "budget_seconds": seconds,
            "laws_beside": "definitions; assertions only (exploratory)" if defined else "declarations",
            "workers": workers,
            "review_sample": sample(names),
        }
        started = campaign.start(EXPERIMENT, output, compiler=compiler, seed=None, settings=settings, schema=SCHEMA)
        every: list[Mapping[str, object]] = []
        for unit in chosen:
            rows = measure(
                unit,
                upstream / unit.name,
                compiler,
                Path(directory) / unit.name,
                seconds=seconds,
                workers=workers,
                defined=defined,
            )
            for index, row in enumerate(rows):
                started.evidence.record(unit.name, "rows", f"r{index}", row)
            every += rows
            progress(f"corpus: {unit.name}: {rows[0]['level'] or rows[0]['proof']}, {len(rows) - 1} rows")
    summary = summarise(every)
    passed = all(row["tests_on_port"] == "pass" for row in every if row["row"] == "unit")
    campaign.finish(started, {"passed": passed, "s1_selection": selected, **summary}, tables(every), _rows)
    progress(f"corpus: {summary['s2_levels']} {summary['s4_mutants']}")
    return passed


def subsumed(declaration: str, call: str, case: Mapping[str, object], target: Target) -> bool:
    """Does the contract alone imply this test? The function is only declared, so its body cannot help.

    The test's inputs become the law's assumptions (the length, and each array element), the function is
    called, and the expected result is asserted. A proof means every function that keeps the contract passes
    the test; the test then adds nothing to the proved contract.
    """
    array = case["array"]
    assert isinstance(array, list)
    length = int(str(case["length"]))
    known = " && ".join(f"a[{index}] == {value}" for index, value in enumerate(array[:length])) or "1 == 1"
    law = (
        f'#include "pfc.h"\n{declaration}\n'
        f"law {case['name']}(long n where(n == {length}), const int a[n])\n{{\n"
        f"    if ({known}) {{\n        long found = {call.format(value=case['value'])};\n\n"
        f"        assert(found == {case['expected']});\n    }}\n}}\n"
    )
    _, certification = adapter.check(adapter.load_text(law, "law.c"), target, level="full")
    return certification.accepted
