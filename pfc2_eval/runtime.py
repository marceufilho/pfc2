"""E11: run time of the plain, checked and certified builds (descriptive).

Each array program of `examples` and `thesis-derived` is built three ways with the same flags: the source as
an ordinary compiler reads it (plain), the C with every runtime check in place (checked) and the C PFC2
releases at level `memory` (certified). A host driver appended to the translation unit allocates the arrays,
fills them before every repetition outside the timed region, calls the function through a volatile pointer
and prints a checksum of everything it returned and wrote together with the nanoseconds spent in the calls.
The three builds must print the same checksum; a run that differs is a failure, never a timing.

Three warm-ups per build, then three blocks of ten runs with the builds interleaved. Reported: the median
per build and the ratios paired by (block, run) with a seeded bootstrap. The result is labelled `controlled`
only when the frequency governor is `performance` and an instruction counter is available; otherwise
`exploratory`. No performance claim is made either way.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import time
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from random import Random
from statistics import median

from pfc2.core.target import read_target
from pfc2_eval import adapter, build, campaign, evidence, heldout

EXPERIMENT = "runtime"
VARIANTS = ("plain", "checked", "certified")
ELEMENTS = 1 << 24
WARMUPS = 3
BLOCKS = 3
RUNS = 10
BOOTSTRAP = 2000
RUN_SECONDS = 300
POSIX = "#define _POSIX_C_SOURCE 200809L\n"  # For clock_gettime under -std=c11; before any include.
SCHEMA = evidence.Schema(
    (
        evidence.Column("row", "string", allowed=("program", "run")),
        evidence.Column("program", "string"),
        evidence.Column("corpus", "string"),
        evidence.Column("status", "string", nullable=True),
        evidence.Column("variant", "string", nullable=True, allowed=VARIANTS),
        evidence.Column("block", "integer", nullable=True),
        evidence.Column("run", "integer", nullable=True),
        evidence.Column("nanoseconds", "integer", nullable=True),
        evidence.Column("checksum", "string", nullable=True),
        evidence.Column("at", "number", nullable=True),
    )
)


@dataclass(frozen=True)
class Array:
    name: str
    element: str  # long or char
    length: str  # A C expression over bench_n.
    fill: str  # A C expression over the index i.
    written: bool = False


@dataclass(frozen=True)
class Bench:
    name: str
    corpus: str
    source: str
    function: str
    arrays: tuple[Array, ...]
    call: str  # A C expression; F is the function, bench_n the element count, k the inner index.
    elements: int = ELEMENTS
    inner: int = 1
    repetitions: int = 4


def _a(name: str = "a", fill: str = "i % 7", *, written: bool = False, length: str = "bench_n") -> Array:
    return Array(name, "long", length, fill, written)


def _thesis(stratum: str, name: str, arrays: tuple[Array, ...], call: str, **more: int) -> Bench:
    return Bench(
        f"thesis-{name}", "thesis-derived", f"corpus/thesis-derived/{stratum}/{name}.c", name, arrays, call, **more
    )


def _example(directory: str, file: str, function: str, arrays: tuple[Array, ...], call: str, **more: int) -> Bench:
    return Bench(f"example-{function}", "examples", f"examples/{directory}/{file}.c", function, arrays, call, **more)


SIDE = 4096  # 4096 * 4096 = 2^24 matrix elements.
PROGRAMS: tuple[Bench, ...] = (
    _thesis("kernels", "sum", (_a(),), "F(a, bench_n, bench_n)"),
    _thesis("kernels", "dot", (_a(), _a("b", "i % 5")), "F(a, bench_n, b, bench_n, bench_n)"),
    _thesis("kernels", "saxpy", (_a(), _a("b", "i % 5", written=True)), "F(3, a, bench_n, b, bench_n, bench_n)"),
    _thesis("kernels", "prefix_sum", (_a(written=True),), "F(a, bench_n, bench_n)"),
    _thesis(
        "kernels",
        "matvec",
        (_a("m"), _a("x", length=str(SIDE)), _a("y", "0", written=True, length=str(SIDE))),
        f"F(m, bench_n, x, {SIDE}, y, {SIDE}, {SIDE}, {SIDE})",
    ),
    _thesis("kernels", "binary_search", (_a(fill="i"),), "F(a, bench_n, bench_n, (k * 7919) % bench_n)", inner=1 << 20),
    _thesis("acsl", "accumulate", (_a(),), "F(a, bench_n, bench_n, 0)"),
    _thesis("acsl", "copy", (_a(), _a("b", "0", written=True)), "F(a, bench_n, b, bench_n, bench_n)"),
    _thesis("acsl", "count", (_a(),), "F(a, bench_n, bench_n, 3)"),
    _thesis("acsl", "fill", (_a(written=True),), "F(a, bench_n, bench_n, 5)"),
    _thesis("acsl", "find", (_a(),), "F(a, bench_n, bench_n, -1)"),
    _thesis("acsl", "replace", (_a(written=True),), "F(a, bench_n, bench_n, 3, 4)"),
    _thesis("acsl", "reverse", (_a(written=True),), "F(a, bench_n, bench_n)"),
    _thesis(
        "acsl",
        "swap_ranges",
        (_a(written=True), _a("b", "i % 5", written=True)),
        "F(a, bench_n, b, bench_n, bench_n)",
    ),
    _example("02_fill", "fill", "fill", (_a(written=True),), "F(bench_n, a, 5)"),
    _example("03_sum", "sum", "sum", (_a(),), "F(bench_n, a)"),
    _example(
        "05_binary_search",
        "binary_search",
        "binary_search",
        (_a(fill="i"),),
        "F(bench_n, a, (k * 7919) % bench_n)",
        inner=1 << 20,
    ),
    _example("06_copy", "copy", "copy", (_a("dst", "0", written=True), _a("src")), "F(bench_n, dst, src)"),
    _example("11_flag", "flag", "play", (_a("moves", "i % 4"),), "F(bench_n, moves)"),
    _example(
        "12_rest_api",
        "api",
        "handle",
        (_a("used", "i % 2", written=True), _a("vals", "i % 7", written=True)),
        "F(bench_n, used, vals, k % 3, (k * 7919) % bench_n, k % 100)",
        inner=1 << 20,
    ),
    _example(
        "14_tree",
        "tree",
        "path_max",
        (_a("tree"),),
        "F(bench_n, tree, (k * 7919) % bench_n)",
        elements=1_000_000,
        inner=1 << 20,
    ),
    _example(
        "15_matrix",
        "matrix",
        "multiply",
        (_a(), _a("b", "i % 5"), _a("c", "0", written=True)),
        "F(bench_n, a, b, c)",
        elements=9,
        inner=1 << 20,
    ),
    _example("17_text", "text", "count_char", (Array("s", "char", "bench_n", "97 + i % 26"),), "F(bench_n, s, 'e')"),
    _example("17_text", "text", "index_of", (Array("s", "char", "bench_n", "97 + i % 26"),), "F(bench_n, s, 'A')"),
    _example(
        "17_text", "text", "to_upper", (Array("s", "char", "bench_n", "97 + i % 26", written=True),), "F(bench_n, s)"
    ),
)


def driver(bench: Bench) -> str:
    """Host C appended to a build: fill, time the calls, fold results and written arrays into a checksum."""
    lines = [
        "",
        "#include <stdio.h>",
        "#include <stdlib.h>",
        "#include <time.h>",
        "",
        "int main(void)",
        "{",
        f"    const long bench_n = {bench.elements};",
        f"    __typeof__({bench.function}) *volatile F = {bench.function};",
        "    unsigned long bench_sum = 0;",
        "    long long bench_ns = 0;",
    ]
    for array in bench.arrays:
        lines.append(f"    {array.element} *{array.name} = malloc(sizeof *{array.name} * (size_t)({array.length}));")
        lines.append(f"    if ({array.name} == NULL) {{ return 3; }}")
    lines.append(f"    for (long bench_rep = 0; bench_rep < {bench.repetitions}; bench_rep++) {{")
    for array in bench.arrays:
        lines.append(
            f"        for (long i = 0; i < ({array.length}); i++) "
            f"{{ {array.name}[i] = ({array.element})({array.fill}); }}"
        )
    lines += [
        "        struct timespec bench_t0, bench_t1;",
        "        clock_gettime(CLOCK_MONOTONIC, &bench_t0);",
        f"        for (long k = 0; k < {bench.inner}; k++) "
        f"{{ bench_sum = bench_sum * 31u + (unsigned long)({bench.call}); }}",
        "        clock_gettime(CLOCK_MONOTONIC, &bench_t1);",
        "        bench_ns += (bench_t1.tv_sec - bench_t0.tv_sec) * 1000000000LL;",
        "        bench_ns += bench_t1.tv_nsec - bench_t0.tv_nsec;",
    ]
    for array in bench.arrays:
        if array.written:
            lines.append(
                f"        for (long i = 0; i < ({array.length}); i++) "
                f"{{ bench_sum = bench_sum * 31u + (unsigned long){array.name}[i]; }}"
            )
    lines += ["    }", '    printf("%lu %lld\\n", bench_sum, bench_ns);', "    return 0;", "}", ""]
    return "\n".join(lines)


def builds(bench: Bench, root: Path, compiler: str, scratch: Path) -> dict[str, Path] | str:
    """The three binaries, or the reason there are none."""
    source = root / bench.source
    target = read_target(compiler)
    unit = adapter.load(source)
    _, certification = adapter.check(adapter.load(source), target, level="memory")
    if certification.c is None:
        return f"not certified at memory: {certification.reason}"
    texts = {"plain": adapter.plain_c(unit), "checked": adapter.checked_c(unit, target), "certified": certification.c}
    binaries = {}
    for variant, text in texts.items():
        binaries[variant] = scratch / f"{bench.name}-{variant}"
        try:
            build.compile_c(
                POSIX + text + driver(bench),
                binaries[variant],
                clang=compiler,
                plain=variant == "plain",
                sanitize=False,
            )
        except build.BuildError as error:
            return f"{variant} does not build: {str(error)[:300]}"
    return binaries


def one_run(binary: Path, cpu: int | None) -> tuple[int, str] | None:
    """(nanoseconds in the calls, checksum) of one process, or None when it did not finish cleanly."""
    command = [str(binary)] if cpu is None else ["taskset", "-c", str(cpu), str(binary)]
    try:
        done = subprocess.run(command, capture_output=True, text=True, timeout=RUN_SECONDS, check=False)
    except (OSError, subprocess.SubprocessError):
        return None
    parts = done.stdout.split()
    if done.returncode != 0 or len(parts) != 2 or not parts[1].isdigit():
        return None
    return int(parts[1]), parts[0]


def measure(
    bench: Bench, binaries: Mapping[str, Path], cpu: int | None, blocks: int, runs: int
) -> list[dict[str, object]]:
    """Warm-ups, then `blocks` blocks of `runs` rounds; in each round every build runs once, in a rotating order."""
    rows: list[dict[str, object]] = []
    for _ in range(WARMUPS):
        for variant in VARIANTS:
            one_run(binaries[variant], cpu)
    for block in range(blocks):
        for run in range(runs):
            shift = (block * runs + run) % len(VARIANTS)
            for variant in VARIANTS[shift:] + VARIANTS[:shift]:
                outcome = one_run(binaries[variant], cpu)
                rows.append(
                    {
                        "row": "run",
                        "program": bench.name,
                        "corpus": bench.corpus,
                        "variant": variant,
                        "block": block,
                        "run": run,
                        "nanoseconds": outcome[0] if outcome else None,
                        "checksum": outcome[1] if outcome else None,
                        "at": round(time.time(), 3),
                    }
                )
    return rows


def ratio(rows: Sequence[Mapping[str, object]], top: str, bottom: str, seed: int) -> dict[str, object] | None:
    """Median of the ratios paired by (block, run), with a percentile bootstrap over the pairs."""
    times: dict[tuple[object, object], dict[str, int]] = {}
    for row in rows:
        if row["nanoseconds"] is not None:
            times.setdefault((row["block"], row["run"]), {})[str(row["variant"])] = int(str(row["nanoseconds"]))
    pairs = [
        entry[top] / entry[bottom] for entry in times.values() if top in entry and bottom in entry and entry[bottom]
    ]
    if not pairs:
        return None
    rng = Random(seed)
    samples = sorted(median(rng.choices(pairs, k=len(pairs))) for _ in range(BOOTSTRAP))
    low, high = samples[int(0.025 * BOOTSTRAP)], samples[int(0.975 * BOOTSTRAP) - 1]
    return {"median": round(median(pairs), 4), "interval": [round(low, 4), round(high, 4)], "pairs": len(pairs)}


def summarise(rows: Sequence[Mapping[str, object]], label: str, seed: int) -> dict[str, object]:
    programs: dict[str, dict[str, object]] = {}
    failures: list[str] = []
    for head in [row for row in rows if row["row"] == "program"]:
        name = str(head["program"])
        mine = [row for row in rows if row["row"] == "run" and row["program"] == name]
        entry: dict[str, object] = {"corpus": head["corpus"], "status": head["status"]}
        if head["status"] == "measured":
            sums = {row["checksum"] for row in mine}
            if None in sums or len(sums) != 1:
                failures.append(name)
                entry["status"] = "builds disagree or a run failed"
            else:
                medians = {
                    variant: int(median(int(str(row["nanoseconds"])) for row in mine if row["variant"] == variant))
                    for variant in VARIANTS
                }
                entry["median_ns"] = medians
                entry["checked_over_plain"] = ratio(mine, "checked", "plain", seed)
                entry["certified_over_plain"] = ratio(mine, "certified", "plain", seed)
                entry["certified_over_checked"] = ratio(mine, "certified", "checked", seed)
        programs[name] = entry
    measured = [name for name, entry in programs.items() if entry["status"] == "measured"]
    return {
        "label": label,
        "programs": len(programs),
        "measured": len(measured),
        "not_measured": {name: entry["status"] for name, entry in programs.items() if entry["status"] != "measured"},
        "failures": failures,
        "by_program": programs,
        "passed": bool(measured) and not failures,  # Descriptive: passing means every measured run agreed.
    }


def table(summary: Mapping[str, object]) -> str:
    lines = [
        "# E11: run time (descriptive)",
        "",
        f"Label: **{summary['label']}**. Programs measured: {summary['measured']} of {summary['programs']}.",
        "",
        "| Program | plain ms | checked ms | certified ms | checked/plain | certified/plain | certified/checked |",
        "| --- | ---: | ---: | ---: | --- | --- | --- |",
    ]
    by_program = summary["by_program"]
    assert isinstance(by_program, Mapping)

    def shown(item: object) -> str:
        return f"{item['median']} {item['interval']}" if isinstance(item, Mapping) else "-"

    for name, entry in by_program.items():
        if "median_ns" not in entry:
            lines.append(f"| {name} | - | - | - | - | - | {entry['status']} |")
            continue
        ms = [f"{entry['median_ns'][variant] / 1e6:.2f}" for variant in VARIANTS]
        lines.append(
            f"| {name} | {ms[0]} | {ms[1]} | {ms[2]} | {shown(entry['checked_over_plain'])} | "
            f"{shown(entry['certified_over_plain'])} | {shown(entry['certified_over_checked'])} |"
        )
    return "\n".join(lines) + "\n"


def conditions() -> dict[str, object]:
    """What decides the label, and what a reader needs to judge the noise."""
    governor_file = Path("/sys/devices/system/cpu/cpu0/cpufreq/scaling_governor")
    governor = governor_file.read_text(encoding="utf-8").strip() if governor_file.is_file() else "unknown"
    counter = shutil.which("perf")
    return {
        "governor": governor,
        "instruction_counter": counter,
        "load_average": [round(value, 2) for value in os.getloadavg()],
        "processors": os.cpu_count(),
    }


def _rows(records: tuple[evidence.Record, ...]) -> Iterable[Mapping[str, object]]:
    names = [column.name for column in SCHEMA.columns]
    return [{name: record.data.get(name) for name in names} for record in records]


def run(
    *,
    output: Path,
    compiler: str,
    seed: int,
    cpu: int | None = None,
    programs: Sequence[Bench] = PROGRAMS,
    blocks: int = BLOCKS,
    runs: int = RUNS,
    root: Path = campaign.ROOT,
    dry_run: bool = False,
    progress: Callable[[str], None] = campaign.progress,
) -> bool:
    heldout.require_intact([root / "corpus" / "thesis-derived"])
    if dry_run:
        progress(f"runtime: would build and time {len(programs)} programs into {output}")
        return True
    before = conditions()
    label = "controlled" if before["governor"] == "performance" and before["instruction_counter"] else "exploratory"
    settings = {
        "elements": ELEMENTS,
        "warmups": WARMUPS,
        "blocks": blocks,
        "runs": runs,
        "level": "memory",
        "cpu": cpu,
        "label": label,
        "conditions_at_start": before,
        "programs": [bench.name for bench in programs],
    }
    started = campaign.start(EXPERIMENT, output, compiler=compiler, seed=seed, settings=settings, schema=SCHEMA)
    kept: list[dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="pfc2-runtime-") as scratch:
        for bench in programs:
            made = builds(bench, root, compiler, Path(scratch))
            status = made if isinstance(made, str) else "measured"
            rows: list[dict[str, object]] = [
                {"row": "program", "program": bench.name, "corpus": bench.corpus, "status": status}
            ]
            if not isinstance(made, str):
                rows += measure(bench, made, cpu, blocks, runs)
            for index, row in enumerate(rows):
                started.evidence.record(bench.name, "rows", f"r{index}", row)
            kept += rows
            progress(f"runtime: {bench.name}: {status}")
    started.evidence.record("machine", "conditions", "end", conditions())
    full = [{column.name: row.get(column.name) for column in SCHEMA.columns} for row in kept]
    summary = summarise(full, label, seed)
    campaign.finish(
        started, summary, table(summary), lambda records: _rows(tuple(r for r in records if r.shard == "rows"))
    )
    progress(f"runtime: {label}; measured {summary['measured']} of {summary['programs']}")
    return bool(summary["passed"])
