"""E4: would the tests and E1 notice a wrong rule in the engine?

Every mutant of the registered files under the registered operators is applied, one at a time, to a private
copy of the tree, and two layers are run until one fails:

    tests  the whole test suite, quickest files first, stopping at the first failure
    e1     the differential experiment on the first 50 programs of its registered seed

A mutant that neither stops is a survivor. Four tests are left out of the first layer because they compare
bytes, not behaviour, and would stop every mutant: the three that ask whether the tree is the frozen candidate
and the one that compares the committed site bundle, which embeds the engine's files. That nothing else does
is checked before a campaign by a change that alters no behaviour (a comment), which must survive.

The repository is never written: a worker copies it once to a temporary directory, writes one mutated file,
runs the layers there with the copy first on the import path, and restores the file.
"""

import ast
import atexit
import difflib
import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from collections import Counter
from collections.abc import Callable, Iterable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from pfc2_eval import campaign, evidence, stats

EXPERIMENT = "mutate"
ROOT = Path(__file__).resolve().parents[1]
TARGETS = (
    "pfc2/core/vc.py",
    "pfc2/core/wp.py",
    "pfc2/core/smt.py",
    "pfc2/core/authorization.py",
    "pfc2/core/emit.py",
    "pfc2/core/desugar.py",
    "pfc2/core/lower.py",
    "pfc2/gate.py",
    "pfc2/infer.py",
    "pfc2/elaborate.py",
    "pfc2/clauses.py",
    "pfc2/preprocess.py",
)
OPERATORS = ("relational", "arithmetic", "boolean", "constant", "statement-deletion", "return-replacement")
OUTCOMES = (
    "killed by tests",
    "killed by e1",
    "timeout in tests",
    "timeout in e1",
    "memory limit in tests",
    "memory limit in e1",
    "survived",
)
LIMITS = ("timeout in tests", "timeout in e1", "memory limit in tests", "memory limit in e1")
TARGET_SCORE = 0.90
TESTS_SECONDS = 2400
E1_SECONDS = 3600
MEMORY_BYTES = 4 * 1024**3  # Resident memory of one layer and everything it starts (amendment 25).
POLL_SECONDS = 0.5
E1_PROGRAMS = 50
E1_SEED = 100000
COPIED = ("pfc2", "pfc2_eval", "tests", "examples", "tools", "validation")
COPIED_FILES = ("Makefile", "pyproject.toml", "uv.lock", "README.md", ".python-version")
LINKED = ("corpus",)  # Read by some tests, never written by them.
BYTE_COMPARISONS = (
    "tests/test_freeze.py::test_the_committed_inventories_describe_this_tree",
    "tests/eval/test_eval_harness.py::test_the_tree_is_the_frozen_candidate_and_a_changed_file_is_noticed",
    "tests/eval/test_eval_harness.py::test_commands_report_usage_planned_steps_and_dry_runs",
    "tests/test_site_data.py",
)
SCHEMA = evidence.Schema(
    (
        evidence.Column("mutant", "string"),
        evidence.Column("target", "string"),
        evidence.Column("operator", "string", allowed=OPERATORS),
        evidence.Column("line", "integer"),
        evidence.Column("original", "string"),
        evidence.Column("replacement", "string"),
        evidence.Column("outcome", "string", allowed=OUTCOMES),
        evidence.Column("stopped_by", "string", nullable=True),
        evidence.Column("seconds", "number"),
        evidence.Column("peak_rss_mb", "integer", nullable=True),
    )
)
_RELATIONAL: dict[type[ast.cmpop], type[ast.cmpop]] = {
    ast.Lt: ast.LtE,
    ast.LtE: ast.Lt,
    ast.Gt: ast.GtE,
    ast.GtE: ast.Gt,
    ast.Eq: ast.NotEq,
    ast.NotEq: ast.Eq,
    ast.In: ast.NotIn,
    ast.NotIn: ast.In,
    ast.Is: ast.IsNot,
    ast.IsNot: ast.Is,
}
_ARITHMETIC: dict[type[ast.operator], type[ast.operator]] = {
    ast.Add: ast.Sub,
    ast.Sub: ast.Add,
    ast.Mult: ast.FloorDiv,
    ast.FloorDiv: ast.Mult,
    ast.Mod: ast.FloorDiv,
}
_DELETABLE = (ast.Assign, ast.AugAssign, ast.AnnAssign, ast.Expr, ast.Raise)


@dataclass(frozen=True)
class Site:
    operator: str
    line: int
    column: int
    end_line: int
    end_column: int
    original: str
    replacement: str


@dataclass(frozen=True)
class Mutant:
    identifier: str
    target: str
    site: Site
    text: str  # The whole mutated file.


def _site(source: str, node: ast.expr | ast.stmt, operator: str, replacement: str) -> list[Site]:
    original = ast.get_source_segment(source, node)
    if original is None or original == replacement or node.end_lineno is None or node.end_col_offset is None:
        return []
    return [Site(operator, node.lineno, node.col_offset, node.end_lineno, node.end_col_offset, original, replacement)]


def _of(source: str, node: ast.AST) -> list[Site]:
    if isinstance(node, ast.Compare) and len(node.ops) == 1 and type(node.ops[0]) in _RELATIONAL:
        flipped = ast.Compare(node.left, [_RELATIONAL[type(node.ops[0])]()], node.comparators)
        return _site(source, node, "relational", ast.unparse(flipped))
    if isinstance(node, ast.BinOp) and type(node.op) in _ARITHMETIC:
        return _site(
            source, node, "arithmetic", ast.unparse(ast.BinOp(node.left, _ARITHMETIC[type(node.op)](), node.right))
        )
    if isinstance(node, ast.BoolOp):
        other = ast.Or() if isinstance(node.op, ast.And) else ast.And()
        return _site(source, node, "boolean", ast.unparse(ast.BoolOp(other, node.values)))
    if isinstance(node, (ast.If, ast.While)):
        return _site(source, node.test, "boolean", f"not ({ast.get_source_segment(source, node.test)})")
    if isinstance(node, ast.Constant) and type(node.value) is int:
        return [site for shift in (1, -1) for site in _site(source, node, "constant", str(node.value + shift))]
    if isinstance(node, ast.Return) and node.value is not None:
        value = node.value
        if isinstance(value, ast.Constant) and value.value is None:
            return []
        found = _site(source, node, "return-replacement", "return None")
        if isinstance(value, (ast.Compare, ast.BoolOp)) or (
            isinstance(value, ast.Constant) and type(value.value) is bool
        ):
            found += _site(source, node, "return-replacement", f"return not ({ast.unparse(value)})")
        return found
    return []


def _deletions(source: str, body: Sequence[ast.stmt]) -> list[Site]:
    if len(body) < 2:
        return []
    found: list[Site] = []
    for statement in body:
        bare = isinstance(statement, ast.AnnAssign) and statement.value is None
        docstring = isinstance(statement, ast.Expr) and isinstance(statement.value, ast.Constant)
        if isinstance(statement, _DELETABLE) and not bare and not docstring:
            found += _site(source, statement, "statement-deletion", "pass")
    return found


def apply(source: str, site: Site) -> str:
    """Replace exactly the site's segment (the columns of the syntax tree count UTF-8 bytes)."""
    data = source.encode("utf-8")
    lines = data.splitlines(keepends=True)
    start = sum(len(line) for line in lines[: site.line - 1]) + site.column
    end = sum(len(line) for line in lines[: site.end_line - 1]) + site.end_column
    if data[start:end].decode("utf-8") != site.original:
        raise ValueError("site does not match the source")
    return (data[:start] + site.replacement.encode("utf-8") + data[end:]).decode("utf-8")


def sites(source: str) -> list[Site]:
    """Every site of every operator, in source order, whose mutated text parses and is distinct."""
    found: list[Site] = []

    def visit(node: ast.AST, inside: bool) -> None:
        found.extend(_of(source, node))
        inside = inside or isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        if inside:
            for name in ("body", "orelse", "finalbody"):
                statements = getattr(node, name, None)
                if isinstance(statements, list) and statements and isinstance(statements[0], ast.stmt):
                    found.extend(_deletions(source, statements))
        for child in ast.iter_child_nodes(node):
            visit(child, inside)

    visit(ast.parse(source), False)
    ordered = sorted(set(found), key=lambda s: (s.line, s.column, OPERATORS.index(s.operator), s.replacement))
    distinct: dict[str, Site] = {}
    for site in ordered:
        text = apply(source, site)
        try:
            ast.parse(text)
        except SyntaxError:
            continue
        distinct.setdefault(text, site)
    return list(distinct.values())


def population(root: Path = ROOT, targets: Sequence[str] = TARGETS) -> list[Mutant]:
    """Every mutant of every target, named `<file stem>-<number>` in source order."""
    found = []
    for target in targets:
        source = (root / target).read_text(encoding="utf-8")
        stem = Path(target).stem
        found += [
            Mutant(f"{stem}-{number:04d}", target, site, apply(source, site))
            for number, site in enumerate(sites(source), start=1)
        ]
    return found


def test_order(durations: Mapping[str, float], root: Path = ROOT) -> list[str]:
    """Every test file, quickest first by a recorded timing; a file without a timing goes first."""
    files = sorted(path.relative_to(root).as_posix() for path in (root / "tests").rglob("test_*.py"))
    return sorted(files, key=lambda name: (durations.get(name, 0.0), name))


def isolated_copy(root: Path, destination: Path) -> None:
    for name in COPIED:
        shutil.copytree(root / name, destination / name, ignore=shutil.ignore_patterns("__pycache__", ".*_cache"))
    for name in COPIED_FILES:
        shutil.copy2(root / name, destination / name)
    for name in LINKED:
        (destination / name).symlink_to(root / name, target_is_directory=True)


def _environment(copy: Path) -> dict[str, str]:
    kept = {key: value for key, value in os.environ.items() if key != "OPENAI_API_KEY"}
    return {**kept, "PYTHONPATH": str(copy), "PYTHONDONTWRITEBYTECODE": "1"}


def layers(copy: Path, order: Sequence[str], python: str) -> list[tuple[str, list[str], int]]:
    deselect = [part for name in BYTE_COMPARISONS for part in ("--deselect", name)]
    tests = [python, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider", *order, *deselect]
    e1 = [python, "-m", "pfc2_eval", "differential", "--output", str(copy / "e1-evidence")]
    e1 += ["--seed", str(E1_SEED), "--programs", str(E1_PROGRAMS), "--workers", "1"]
    return [("tests", tests, TESTS_SECONDS), ("e1", e1, E1_SECONDS)]


@dataclass(frozen=True)
class Finished:
    """How one layer ended: `exited` with a return code, or stopped at the `timeout` or the `memory` limit."""

    status: str
    returncode: int | None
    stdout: str
    stderr: str
    peak_bytes: int


def session_memory(session: int) -> int:
    """Resident memory, in bytes, of every process whose session is `session`, read from Linux `/proc`."""
    page = os.sysconf("SC_PAGE_SIZE")
    total = 0
    for entry in os.scandir("/proc"):
        if not entry.name.isdigit():
            continue
        try:
            fields = Path(entry.path, "stat").read_text(encoding="utf-8").rsplit(")", 1)[1].split()
            if int(fields[3]) != session:  # After the name: state, parent, process group, session.
                continue
            total += int(Path(entry.path, "statm").read_text(encoding="utf-8").split()[1]) * page
        except (OSError, ValueError, IndexError):
            continue  # The process ended while it was being read.
    return total


def _stop(session: int) -> None:
    try:
        os.killpg(session, signal.SIGKILL)
    except ProcessLookupError:
        pass


def run_limited(command: Sequence[str], cwd: Path, env: Mapping[str, str], seconds: float, memory: int) -> Finished:
    """Run a layer in a session of its own; stop the whole session at the time limit or the memory limit."""
    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        process = subprocess.Popen(command, cwd=cwd, env=dict(env), stdout=out, stderr=err, start_new_session=True)
        deadline = time.monotonic() + seconds
        status, peak = "exited", 0
        while True:
            try:
                process.wait(timeout=POLL_SECONDS)
                break
            except subprocess.TimeoutExpired:
                pass
            used = session_memory(process.pid)
            peak = max(peak, used)
            if used > memory:
                status = "memory"
            elif time.monotonic() > deadline:
                status = "timeout"
            if status != "exited":
                _stop(process.pid)
                process.wait()
                break
        _stop(process.pid)  # Whatever the layer left running goes with it.
        out.seek(0)
        err.seek(0)
        text = out.read().decode("utf-8", "replace"), err.read().decode("utf-8", "replace")
    return Finished(status, process.returncode if status == "exited" else None, text[0], text[1], peak)


def judge(copy: Path, mutant: Mutant, order: Sequence[str], python: str) -> dict[str, object]:
    """Write the mutant into the copy, run the layers until one stops it, restore the file."""
    path = copy / mutant.target
    original = path.read_text(encoding="utf-8")
    started = time.monotonic()
    outcome, stopped_by, peak = "survived", None, 0
    path.write_text(mutant.text, encoding="utf-8")
    try:
        for name, command, seconds in layers(copy, order, python):
            shutil.rmtree(copy / "e1-evidence", ignore_errors=True)
            done = run_limited(command, copy, _environment(copy), seconds, MEMORY_BYTES)
            peak = max(peak, done.peak_bytes)
            if done.status != "exited":
                outcome = f"timeout in {name}" if done.status == "timeout" else f"memory limit in {name}"
                break
            if done.returncode != 0:
                outcome = f"killed by {name}"
                failed = [line for line in done.stdout.splitlines() if line.startswith(("FAILED ", "ERROR "))]
                stopped_by = failed[0][:300] if failed else (done.stderr.strip().splitlines() or [""])[-1][:300]
                break
    finally:
        path.write_text(original, encoding="utf-8")
        shutil.rmtree(copy / "e1-evidence", ignore_errors=True)
    site = mutant.site
    return {
        "mutant": mutant.identifier,
        "target": mutant.target,
        "operator": site.operator,
        "line": site.line,
        "original": site.original[:400],
        "replacement": site.replacement[:400],
        "outcome": outcome,
        "stopped_by": stopped_by,
        "seconds": round(time.monotonic() - started, 1),
        "peak_rss_mb": peak // (1024 * 1024),
    }


_COPY: Path | None = None


def _worker(arguments: tuple[Mutant, tuple[str, ...], str, str]) -> dict[str, object]:
    global _COPY
    mutant, order, python, root = arguments
    if _COPY is None:  # One copy per worker process, made on its first mutant and removed when it ends.
        _COPY = Path(tempfile.mkdtemp(prefix="pfc2-mutate-"))
        atexit.register(shutil.rmtree, _COPY, ignore_errors=True)
        isolated_copy(Path(root), _COPY)
    return judge(_COPY, mutant, order, python)


def diff(mutant: Mutant, root: Path = ROOT) -> str:
    before = (root / mutant.target).read_text(encoding="utf-8").splitlines(keepends=True)
    after = mutant.text.splitlines(keepends=True)
    return "".join(difflib.unified_diff(before, after, mutant.target, f"{mutant.target} ({mutant.identifier})", n=2))


def summarise(rows: Iterable[Mapping[str, object]], equivalent: Sequence[str] = ()) -> dict[str, object]:
    """The score as registered: killed over the mutants not classified equivalent.

    A mutant stopped by the time limit or the memory limit counts as killed (amendments 13 and 25) and is counted
    apart; `score_without_limits` leaves those mutants out of both the numerator and the denominator.
    """
    outcomes: Counter[str] = Counter()
    by_target: dict[str, Counter[str]] = {}
    by_operator: dict[str, Counter[str]] = {}
    survivors: list[str] = []
    for row in rows:
        outcome = str(row["outcome"])
        outcomes[outcome] += 1
        by_target.setdefault(str(row["target"]), Counter())[outcome] += 1
        by_operator.setdefault(str(row["operator"]), Counter())[outcome] += 1
        if outcome == "survived":
            survivors.append(str(row["mutant"]))
    total = sum(outcomes.values())
    excluded = len(set(equivalent) & set(survivors))
    killed = total - outcomes["survived"]
    score = killed / (total - excluded) if total > excluded else None
    interval = stats.wilson(killed, total - excluded) if total > excluded else None
    limited = sum(outcomes[outcome] for outcome in LIMITS)
    unlimited = total - excluded - limited

    def table(groups: Mapping[str, Counter[str]]) -> dict[str, dict[str, int]]:
        return {name: {outcome: counts[outcome] for outcome in OUTCOMES} for name, counts in sorted(groups.items())}

    return {
        "passed": score is not None and score >= TARGET_SCORE,
        "mutants": total,
        "outcomes": {outcome: outcomes[outcome] for outcome in OUTCOMES},
        "killed": killed,
        "survivors": survivors,
        "classified_equivalent": excluded,
        "score": score,
        "score_wilson_95": None if interval is None else [interval.low, interval.high],
        "stopped_by_a_limit": limited,
        "score_without_limits": (killed - limited) / unlimited if unlimited > 0 else None,
        "by_target": table(by_target),
        "by_operator": table(by_operator),
    }


def table(summary: Mapping[str, object]) -> str:
    def rows(title: str, key: str) -> list[str]:
        groups = summary[key]
        assert isinstance(groups, dict)
        head = f"| {title} | " + " | ".join(OUTCOMES) + " |"
        lines = [head, "| --- |" + " ---: |" * len(OUTCOMES)]
        lines += [
            f"| {name} | " + " | ".join(str(counts[o]) for o in OUTCOMES) + " |" for name, counts in groups.items()
        ]
        return [*lines, ""]

    score = summary["score"]
    shown = "—" if score is None else f"{score:.3f}"
    return "\n".join(
        [
            "# E4: mutation of the engine",
            "",
            f"Mutants: {summary['mutants']}; killed: {summary['killed']}; survivors: {len(summary['survivors'])}; "  # type: ignore[arg-type]
            f"score {shown} (threshold {TARGET_SCORE}); classified equivalent: {summary['classified_equivalent']}.",
            "",
            f"Stopped by a time or memory limit (counted as killed): {summary['stopped_by_a_limit']}; "
            f"score with those mutants left out of both counts: {summary['score_without_limits']}.",
            "",
            *rows("File", "by_target"),
            *rows("Operator", "by_operator"),
        ]
    )


def _rows(records: tuple[evidence.Record, ...]) -> Iterable[Mapping[str, object]]:
    return [record.data for record in records]


def run(
    *,
    output: Path,
    compiler: str,
    durations: Path | None,
    workers: int = 1,
    limit: int | None = None,
    dry_run: bool = False,
    progress: Callable[[str], None] = campaign.progress,
) -> bool:
    """Judge the whole population (`limit` cuts it to the first N for a rehearsal, recorded as such)."""
    mutants = population()
    chosen = mutants if limit is None else mutants[:limit]
    recorded: dict[str, float] = {}
    if durations is not None:
        for line in durations.read_text(encoding="utf-8").splitlines():
            seconds, _, name = line.strip().partition(" ")
            recorded[name.strip()] = float(seconds)
    order = tuple(test_order(recorded))
    if dry_run:
        counts = Counter(mutant.target for mutant in mutants)
        progress(f"mutate: would judge {len(chosen)} of {len(mutants)} mutants into {output}; {dict(counts)}")
        return True
    settings = {
        "targets": list(TARGETS),
        "operators": list(OPERATORS),
        "population": len(mutants),
        "judged": len(chosen),
        "whole_population": limit is None,
        "test_order": list(order),
        "tests_left_out": list(BYTE_COMPARISONS),
        "tests_seconds": TESTS_SECONDS,
        "e1_programs": E1_PROGRAMS,
        "e1_seed": E1_SEED,
        "e1_seconds": E1_SECONDS,
        "memory_bytes": MEMORY_BYTES,
        "poll_seconds": POLL_SECONDS,
        "workers": workers,
    }
    started = campaign.start(EXPERIMENT, output, compiler=compiler, seed=None, settings=settings, schema=SCHEMA)
    jobs = [(mutant, order, sys.executable, str(ROOT)) for mutant in chosen]
    kept: list[dict[str, object]] = []
    by_name = {mutant.identifier: mutant for mutant in chosen}
    with ProcessPoolExecutor(max_workers=workers) as pool:
        for done, row in enumerate(pool.map(_worker, jobs), start=1):
            started.evidence.record(str(row["target"]).replace("/", "-"), "rows", str(row["mutant"]), row)
            kept.append(row)
            if row["outcome"] == "survived":
                started.evidence.write_text(f"survivors/{row['mutant']}.diff", diff(by_name[str(row["mutant"])]))
            if done % 25 == 0:
                alive = sum(item["outcome"] == "survived" for item in kept)
                progress(f"mutate: {done}/{len(chosen)}; survivors {alive}")
    summary = summarise(kept)
    campaign.finish(started, summary, table(summary), _rows)
    progress(f"mutate: score {summary['score']}; survivors {len(kept) - int(str(summary['killed']))}")
    return bool(summary["passed"])
