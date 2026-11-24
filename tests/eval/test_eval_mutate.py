"""E4: which mutants exist, how one is applied and judged, and how the score is computed."""

import os
import sys
import time
from pathlib import Path

import pytest

from pfc2_eval import mutate

SOURCE = '''def f(a, b):
    """Text that is never deleted."""
    total = a + b
    if a < b and b != 0:
        total = total - 1
    return total > 3
'''


def test_the_sites_of_a_small_function_are_the_ones_derived_by_hand() -> None:
    found = {(site.operator, site.line, site.original, site.replacement) for site in mutate.sites(SOURCE)}
    assert found == {
        ("arithmetic", 3, "a + b", "a - b"),
        ("statement-deletion", 3, "total = a + b", "pass"),
        ("relational", 4, "a < b", "a <= b"),
        ("relational", 4, "b != 0", "b == 0"),
        ("boolean", 4, "a < b and b != 0", "a < b or b != 0"),
        ("boolean", 4, "a < b and b != 0", "not (a < b and b != 0)"),
        ("constant", 4, "0", "1"),
        ("constant", 4, "0", "-1"),
        ("arithmetic", 5, "total - 1", "total + 1"),
        ("constant", 5, "1", "2"),
        ("constant", 5, "1", "0"),
        ("relational", 6, "total > 3", "total >= 3"),
        ("constant", 6, "3", "4"),
        ("constant", 6, "3", "2"),
        ("return-replacement", 6, "return total > 3", "return None"),
        ("return-replacement", 6, "return total > 3", "return not (total > 3)"),
    }


def test_a_mutant_changes_exactly_its_segment_and_always_parses() -> None:
    site = next(site for site in mutate.sites(SOURCE) if site.replacement == "a <= b")
    assert mutate.apply(SOURCE, site) == SOURCE.replace("a < b", "a <= b")
    with pytest.raises(ValueError):
        mutate.apply(SOURCE.replace("a < b", "b > a"), site)
    texts = [mutate.apply(SOURCE, site) for site in mutate.sites(SOURCE)]
    assert len(set(texts)) == len(texts)


def test_the_population_covers_every_registered_file_and_names_mutants_in_order() -> None:
    mutants = mutate.population()
    assert {mutant.target for mutant in mutants} == set(mutate.TARGETS)
    assert mutants[0].identifier == "vc-0001" and len({mutant.identifier for mutant in mutants}) == len(mutants)
    assert all((mutate.ROOT / mutant.target).read_text(encoding="utf-8") != mutant.text for mutant in mutants[:50])


def test_test_files_are_ordered_quickest_first() -> None:
    order = mutate.test_order({"tests/test_cli.py": 0.5, "tests/test_freeze.py": 99.0})
    assert order[-1] == "tests/test_freeze.py" and order.index("tests/test_cli.py") > order.index("tests/test_gate.py")
    assert "tests/eval/test_eval_mutate.py" in order


def tree(root: Path) -> mutate.Mutant:
    (root / "pkg").mkdir(parents=True)
    (root / "pkg" / "__init__.py").write_text("", encoding="utf-8")
    (root / "pkg" / "m.py").write_text("def f(a, b):\n    return a + b\n", encoding="utf-8")
    site = next(site for site in mutate.sites("def f(a, b):\n    return a + b\n") if site.operator == "arithmetic")
    return mutate.Mutant("m-0001", "pkg/m.py", site, "def f(a, b):\n    return a - b\n")


def test_a_mutant_is_run_in_the_copy_stopped_by_the_first_failing_layer_and_the_file_restored(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    mutant = tree(tmp_path)
    check = "import pkg.m, sys; sys.exit(0 if pkg.m.f(2, 1) == {} else 1)"
    monkeypatch.setattr(
        mutate,
        "layers",
        lambda copy, order, python: [
            ("tests", [python, "-c", check.format("pkg.m.f(2, 1)")], 60),  # Notices nothing.
            ("e1", [python, "-c", check.format(3)], 60),  # Notices the mutant.
        ],
    )
    row = mutate.judge(tmp_path, mutant, (), sys.executable)
    assert row["outcome"] == "killed by e1" and row["operator"] == "arithmetic" and row["line"] == 2
    assert (tmp_path / "pkg" / "m.py").read_text(encoding="utf-8") == "def f(a, b):\n    return a + b\n"
    monkeypatch.setattr(mutate, "layers", lambda copy, order, python: [("tests", [python, "-c", "pass"], 60)])
    assert mutate.judge(tmp_path, mutant, (), sys.executable)["outcome"] == "survived"
    slow = [("tests", [sys.executable, "-c", "import time; time.sleep(30)"], 1)]
    monkeypatch.setattr(mutate, "layers", lambda copy, order, python: slow)
    assert mutate.judge(tmp_path, mutant, (), sys.executable)["outcome"] == "timeout in tests"


def gone(pid: int) -> bool:
    for _ in range(50):
        try:
            state = Path(f"/proc/{pid}/stat").read_text(encoding="utf-8").rsplit(")", 1)[1].split()[0]
        except OSError:
            return True
        if state == "Z":
            return True
        time.sleep(0.1)
    return False


def test_a_layer_that_outgrows_the_memory_limit_is_stopped_and_named(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    mutant = tree(tmp_path)
    monkeypatch.setattr(mutate, "MEMORY_BYTES", 150 * 1024 * 1024)
    greedy = "import time; kept = b'x' * (400 * 1024 * 1024); time.sleep(60)"
    monkeypatch.setattr(mutate, "layers", lambda copy, order, python: [("tests", [python, "-c", greedy], 60)])
    started = time.monotonic()
    row = mutate.judge(tmp_path, mutant, (), sys.executable)
    assert row["outcome"] == "memory limit in tests"
    assert time.monotonic() - started < 30
    assert isinstance(row["peak_rss_mb"], int) and row["peak_rss_mb"] > 150
    modest = [("tests", [sys.executable, "-c", "kept = b'x' * (20 * 1024 * 1024)"], 60)]
    monkeypatch.setattr(mutate, "layers", lambda copy, order, python: modest)
    row = mutate.judge(tmp_path, mutant, (), sys.executable)
    assert row["outcome"] == "survived" and isinstance(row["peak_rss_mb"], int)


def test_the_memory_of_a_layer_is_the_sum_over_the_processes_it_started(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    mutant = tree(tmp_path)
    monkeypatch.setattr(mutate, "MEMORY_BYTES", 250 * 1024 * 1024)
    child = "import time; kept = b'x' * (150 * 1024 * 1024); time.sleep(60)"
    parent = f"import subprocess, sys; [subprocess.Popen([sys.executable, '-c', {child!r}]) for _ in range(3)]; "
    parent += "import time; time.sleep(60)"
    monkeypatch.setattr(mutate, "layers", lambda copy, order, python: [("e1", [python, "-c", parent], 60)])
    assert mutate.judge(tmp_path, mutant, (), sys.executable)["outcome"] == "memory limit in e1"


def test_a_layer_that_runs_out_of_time_takes_the_processes_it_started_with_it(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    mutant = tree(tmp_path)
    note = tmp_path / "child.pid"
    parent = "import subprocess, sys, time, pathlib; "
    parent += "child = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(120)']); "
    parent += f"pathlib.Path({str(note)!r}).write_text(str(child.pid)); time.sleep(120)"
    monkeypatch.setattr(mutate, "layers", lambda copy, order, python: [("tests", [python, "-c", parent], 2)])
    assert mutate.judge(tmp_path, mutant, (), sys.executable)["outcome"] == "timeout in tests"
    assert gone(int(note.read_text(encoding="utf-8")))
    assert os.getpid() > 0  # The harness itself is not in the stopped session.


def test_a_failing_layer_still_reports_what_stopped_it(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    mutant = tree(tmp_path)
    failing = "import sys; print('FAILED tests/test_x.py::test_y - boom'); sys.exit(1)"
    monkeypatch.setattr(mutate, "layers", lambda copy, order, python: [("tests", [python, "-c", failing], 60)])
    row = mutate.judge(tmp_path, mutant, (), sys.executable)
    assert row["outcome"] == "killed by tests" and row["stopped_by"] == "FAILED tests/test_x.py::test_y - boom"


def test_a_mutant_stopped_by_the_memory_limit_counts_as_killed_and_is_shown_apart() -> None:
    def row(name: str, outcome: str) -> dict[str, object]:
        return {"mutant": name, "target": "pfc2/gate.py", "operator": "relational", "outcome": outcome}

    rows = [
        row("a", "killed by tests"),
        row("b", "memory limit in tests"),
        row("c", "memory limit in e1"),
        row("d", "timeout in e1"),
        row("e", "survived"),
    ]
    summary = mutate.summarise(rows)
    assert summary["killed"] == 4 and summary["score"] == 0.8
    assert summary["stopped_by_a_limit"] == 3
    assert summary["score_without_limits"] == 0.5  # One killed by an assertion of the two that met no limit.
    assert summary["outcomes"]["memory limit in tests"] == 1  # type: ignore[index]
    assert "memory limit in e1" in mutate.table(summary)


def test_the_score_counts_timeouts_as_killed_and_leaves_out_classified_equivalents() -> None:
    def row(name: str, outcome: str) -> dict[str, object]:
        return {"mutant": name, "target": "pfc2/gate.py", "operator": "relational", "outcome": outcome}

    rows = [row("a", "killed by tests"), row("b", "killed by e1"), row("c", "timeout in tests"), row("d", "survived")]
    summary = mutate.summarise(rows)
    assert summary["killed"] == 3 and summary["score"] == 0.75 and summary["passed"] is False
    assert summary["survivors"] == ["d"]
    assert mutate.summarise(rows, equivalent=["d"])["score"] == 1.0
    assert mutate.summarise(rows, equivalent=["a"])["score"] == 0.75  # Only a survivor can be set aside.


def test_the_real_layers_leave_out_the_byte_comparisons_and_run_e1_on_fifty_programs(tmp_path: Path) -> None:
    (tests, command, _), (e1, differential, _) = mutate.layers(tmp_path, ("tests/test_gate.py",), "python")
    assert tests == "tests" and "-x" in command and "tests/test_gate.py" in command
    assert command.count("--deselect") == 4 and "tests/test_site_data.py" in command
    assert e1 == "e1" and differential[differential.index("--programs") + 1] == "50"
