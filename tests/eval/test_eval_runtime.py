"""E11: the benchmark driver, the paired ratios and a small sealed campaign."""

from __future__ import annotations

import json
from pathlib import Path

from pfc2_eval import evidence, runtime

ROOT = Path(__file__).resolve().parents[2]
SMALL = runtime.Bench(
    "example-fill",
    "examples",
    "examples/02_fill/fill.c",
    "fill",
    (runtime.Array("a", "long", "bench_n", "i % 7", written=True),),
    "F(bench_n, a, 5)",
    elements=1000,
    repetitions=2,
)
SUM = runtime.Bench(
    "example-sum",
    "examples",
    "examples/03_sum/sum.c",
    "sum",
    (runtime.Array("a", "long", "bench_n", "i % 7"),),
    "F(bench_n, a)",
    elements=1000,
    repetitions=2,
)


def test_every_listed_program_exists_and_names_are_unique() -> None:
    names = [bench.name for bench in runtime.PROGRAMS]
    assert len(names) == len(set(names)) == 25
    assert all((ROOT / bench.source).is_file() for bench in runtime.PROGRAMS)
    assert {bench.corpus for bench in runtime.PROGRAMS} == {"examples", "thesis-derived"}


def test_the_driver_times_only_the_calls_and_folds_written_arrays() -> None:
    text = runtime.driver(SMALL)
    fill, start, call, stop, fold = (
        text.index("a[i] = (long)(i % 7)"),
        text.index("&bench_t0"),
        text.index("F(bench_n, a, 5)"),
        text.index("&bench_t1"),
        text.index("(unsigned long)a[i]"),
    )
    assert fill < start < call < stop < fold
    assert "__typeof__(fill) *volatile F = fill;" in text
    assert "(unsigned long)a[i]" not in runtime.driver(SUM)


def test_the_ratio_is_paired_by_block_and_run() -> None:
    rows = []
    for block in range(2):
        for run in range(5):
            base = 100 + 10 * run
            rows.append({"block": block, "run": run, "variant": "plain", "nanoseconds": base})
            rows.append({"block": block, "run": run, "variant": "checked", "nanoseconds": 2 * base})
    rows.append({"block": 2, "run": 0, "variant": "checked", "nanoseconds": None})
    found = runtime.ratio(rows, "checked", "plain", seed=0)
    assert found == {"median": 2.0, "interval": [2.0, 2.0], "pairs": 10}
    assert runtime.ratio(rows, "certified", "plain", seed=0) is None


def test_builds_that_disagree_are_a_failure_not_a_timing() -> None:
    rows = [{"row": "program", "program": "p", "corpus": "examples", "status": "measured"}]
    for variant, checksum in (("plain", "1"), ("checked", "1"), ("certified", "2")):
        rows.append(
            {
                "row": "run",
                "program": "p",
                "variant": variant,
                "block": 0,
                "run": 0,
                "nanoseconds": 5,
                "checksum": checksum,
            }
        )
    summary = runtime.summarise(rows, "exploratory", 0)
    assert summary["failures"] == ["p"] and summary["passed"] is False and summary["measured"] == 0


def test_a_small_campaign_builds_runs_agrees_and_seals(tmp_path: Path) -> None:
    output = tmp_path / "out"
    passed = runtime.run(
        output=output, compiler="clang-19", seed=0, programs=(SMALL, SUM), blocks=1, runs=2, progress=lambda text: None
    )
    summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    loaded = evidence.load(output)
    assert passed and summary["measured"] == 2 and summary["label"] in ("exploratory", "controlled")
    runs = [row for row in loaded.observations if row["row"] == "run"]
    assert len(runs) == 2 * 3 * 2 and len({row["checksum"] for row in runs if row["program"] == "example-fill"}) == 1
    assert set(summary["by_program"]["example-sum"]["median_ns"]) == set(runtime.VARIANTS)
    assert json.loads((output / "configuration.json").read_text())["settings"]["conditions_at_start"]["governor"]
