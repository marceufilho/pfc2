"""E2: which conjuncts are removed, what the small-domain search expects, and how a removal is scored."""

import json
from pathlib import Path

import pytest

from pfc2.core.target import read_target
from pfc2_eval import adapter, breakit, evidence

SOURCE = """#include "pfc.h"

long get(long n, long a[n], long k)
    requires(0 <= k && k < n)
{
    return a[k];
}

long entry(long n, long a[n], long x, long y)
    requires(1 <= n && n <= 8)
    requires(-50 <= x && x <= 50)
    requires(-50 <= y && y <= 50)
{
    long first = get(n, a, 0);
    long more = x + 1;
    return first + (more / 4);
}
"""


def test_each_top_level_conjunct_is_removed_alone_and_no_line_moves() -> None:
    found = breakit.removals(SOURCE)
    assert [(item.line, item.conjunct) for item in found] == [
        (4, "0 <= k"),
        (4, "k < n"),
        (10, "1 <= n"),
        (10, "n <= 8"),
        (11, "-50 <= x"),
        (11, "x <= 50"),
        (12, "-50 <= y"),
        (12, "y <= 50"),
    ]
    assert "    requires(k < n)\n{\n    return a[k];" in found[0].text
    assert all(item.text.count("\n") == SOURCE.count("\n") for item in found)
    lone = breakit.removals("long f(long x)\n    requires(x == 0)\n{\n    return x;\n}\n")
    assert len(lone) == 1 and lone[0].text == "long f(long x)\n    \n{\n    return x;\n}\n"


def rows() -> dict[str, dict[str, object]]:
    target = read_target("clang-19")
    baseline = adapter.check(adapter.load_text(SOURCE, "p.c"), target, level="memory")[1]
    assert baseline.accepted
    return {
        str(removal.conjunct): breakit.judge(SOURCE, baseline, removal, target, "p")
        for removal in breakit.removals(SOURCE)
    }


def test_removals_are_classified_by_the_interpreter_and_scored_against_the_new_verdict() -> None:
    judged = rows()
    # The helper is run on its own inputs: its caller always passes 0, yet both bounds are needed.
    for conjunct in ("0 <= k", "k < n"):
        row = judged[conjunct]
        assert row["function"] == "get" and row["expected"] == "witness" and "OutOfBounds" in str(row["witness"])
        assert row["certified"] is False and row["as_expected"] is True
    # Without `1 <= n` the call get(n, a, 0) is refused by the helper: a callee's precondition is a witness.
    assert judged["1 <= n"]["expected"] == "witness" and judged["1 <= n"]["certified"] is False
    # `y` is never read, and no array is as long as the bound: nothing depends on these three.
    for conjunct in ("n <= 8", "-50 <= y", "y <= 50"):
        row = judged[conjunct]
        assert row["expected"] == "none" and row["certified"] is True, row
        assert row["decisions_same"] is True and row["code_same"] is True and row["as_expected"] is True
    # x + 1 overflows only at LONG_MAX: the removed trap must come back; the lower bound protects nothing.
    upper = judged["x <= 50"]
    assert upper["expected"] == "overflow" and upper["certified"] is True
    assert upper["overflow_trap_kept"] is True and upper["as_expected"] is True
    assert judged["-50 <= x"]["expected"] == "none"


def test_a_witness_that_keeps_its_certificate_fails_sensitivity_and_a_silent_change_fails_specificity() -> None:
    def row(expected: str, good: bool) -> dict[str, object]:
        return {"row": "removal", "program": "p", "function": "f", "line": 1, "conjunct": "c"} | {
            "expected": expected,
            "as_expected": good,
        }

    good = breakit.summarise([row("witness", True), row("none", True), row("overflow", False)])
    assert good["passed"] is True and good["overflow_only"] == {"as_expected": 0, "total": 1, "rate": 0.0}
    missed = breakit.summarise([row("witness", False), row("none", True)])
    assert missed["sensitivity_passed"] is False and missed["witness_and_still_certified"] == ["p f line 1: c"]
    changed = breakit.summarise([row("witness", True), row("none", False)])
    assert changed["specificity_passed"] is False and changed["passed"] is False
    assert breakit.summarise([row("none", True)])["passed"] is False  # No witness at all shows no sensitivity.


def test_the_body_comparison_ignores_entry_checks_identifiers_and_positions() -> None:
    c = (
        "    // entry check 1: REQUIRES p.c:4:5 conjunct 1\n    _Bool pfc_entry_1 = ((long)0 <= k);\n"
        "    if (!pfc_entry_1) __builtin_trap();\n    // proved: obligation bounds:" + "a" * 64 + "\n    return a[k];\n"
    )
    assert breakit.body(c) == "    // proved: obligation bounds:#\n    return a[k];"


def test_a_removal_the_interpreter_cannot_follow_is_not_scored() -> None:
    source = (
        '#include "pfc.h"\n\nlong outside(long x)\n    requires(0 <= x)\n    ensures(result == x);\n\n'
        "long entry(long x)\n    requires(0 <= x && x <= 9)\n{\n    long y = outside(x);\n    return y;\n}\n"
    )
    rows = breakit.one_program(("p", source, "clang-19", 600, "examples"))
    assert rows[0]["status"] == "used" and rows[0]["stratum"] == "examples"
    removed = {str(row["conjunct"]): row for row in rows[1:] if row["function"] == "entry"}
    assert removed["x <= 9"]["expected"] == "undecided" and removed["x <= 9"]["as_expected"] is None
    summary = breakit.by_stratum(rows)
    assert summary["sensitivity"]["total"] == 0  # type: ignore[index]
    assert summary["examples"]["removals_the_interpreter_could_not_decide"] >= 1  # type: ignore[index]


def test_a_small_campaign_with_an_example_in_a_subdirectory_is_sealed(tmp_path: Path) -> None:
    examples = tmp_path / "examples" / "01_get"
    examples.mkdir(parents=True)
    (examples / "get.c").write_text(SOURCE, encoding="utf-8")
    (tmp_path / "examples" / "wrong").mkdir()
    (tmp_path / "examples" / "wrong" / "bad.c").write_text("long f(", encoding="utf-8")
    output = tmp_path / "breakit"
    breakit.run(
        output=output,
        compiler="clang-19",
        seed=300,
        programs=1,
        directories=[tmp_path / "examples"],
        progress=lambda _: None,
    )
    assert evidence.status(output).complete
    rows = evidence.load(output).observations
    assert {row["stratum"] for row in rows} == {"generated", "examples"}
    assert sum(row["row"] == "removal" and row["stratum"] == "examples" for row in rows) == 8
    summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    assert summary["examples"]["sensitivity"] == {"as_expected": 3, "total": 3, "rate": 1.0}


@pytest.mark.parametrize(
    ("message", "swallowed"), [("argument 1: _OutOfTime: ", True), ("argument 1: TypeError: x", False)]
)
def test_a_timer_that_fires_inside_a_solver_binding_call_is_still_out_of_time(
    monkeypatch: pytest.MonkeyPatch, message: str, swallowed: bool
) -> None:
    """ctypes reports the timer's exception as its own ArgumentError, by name (amendments 25 and 27)."""
    import ctypes

    def wrapped(*arguments: object, **options: object) -> object:
        raise ctypes.ArgumentError(message)

    monkeypatch.setattr(breakit.adapter, "check", wrapped)
    if not swallowed:
        with pytest.raises(ctypes.ArgumentError):
            breakit.one_program(("p", "long f(void)\n{\n    return 0;\n}\n", "clang-19", 600, "examples"))
        return
    rows = breakit.one_program(("p", "long f(void)\n{\n    return 0;\n}\n", "clang-19", 600, "examples"))
    assert rows[0]["status"] == "not judged within the time budget"
