"""E5: the four rewritings, what is compared, and that a difference is noticed."""

import pytest

from pfc2.core.target import read_target
from pfc2_eval import adapter, generate, robustness

SOURCE = """#include "pfc.h"

long g0 = 3;

long entry(long n, long a[n], long k, long x)
    requires(1 <= n && n <= 8)
    requires(0 <= k && k < n)
    requires(-50 <= x && x <= 50)
{
    long t1 = (x + 2);
    long t2 = a[k];
    if ((t1 * 3) != (x + g0)) {
        a[k] = t2;
    }
    return t1;
}
"""


def test_renaming_gives_every_introduced_name_the_suffix_and_leaves_the_language_alone() -> None:
    variant = robustness.rename(SOURCE)
    assert variant is not None and '#include "pfc.h"' in variant.text
    assert "long entry_zq(long n_zq, long a_zq[n_zq], long k_zq, long x_zq)" in variant.text
    assert "requires(-50 <= x_zq && x_zq <= 50)" in variant.text and "return t1_zq;" in variant.text
    assert robustness.rename('#include "pfc.h"\n#define N 8\nlong f(long x) { return N; }\n') is None


def test_reordering_swaps_two_independent_declarations_and_maps_their_lines() -> None:
    variant = robustness.reorder(SOURCE)
    assert variant is not None and variant.lines == {10: 11, 11: 10}
    assert variant.text.index("long t2 = a[k];") < variant.text.index("long t1 = (x + 2);")
    dependent = SOURCE.replace("long t2 = a[k];", "long t2 = t1;")
    assert robustness.reorder(dependent) is None
    assert robustness.reorder(SOURCE.replace("long t2 = a[k];", "long t2 = entry(n, a, k, x);")) is None


def test_the_operand_swap_changes_one_operator_outside_the_clauses() -> None:
    variant = robustness.swap(SOURCE)
    assert variant is not None and "long t1 = (2 + x);" in variant.text
    assert "requires(1 <= n && n <= 8)" in variant.text  # A clause is never rewritten.
    nested = SOURCE.replace("long t1 = (x + 2);", "long t1 = x;")
    swapped = robustness.swap(nested)
    assert swapped is not None and "if ((x + g0) != (t1 * 3)) {" in swapped.text  # The outermost one first.
    assert robustness.swap(SOURCE.replace("(x + 2)", "(x - 2)").replace("(t1 * 3) != (x + g0)", "t1 < x")) is None
    header = '#include "pfc.h"\nlong f(long n, long a[n]) requires(2 <= n) {\n'
    indexed = robustness.swap(header + "    return (a[0] + a[1]);\n}\n")
    assert indexed is not None and "return (a[1] + a[0]);" in indexed.text


def test_the_layout_joins_clauses_and_brace_to_the_signature_and_maps_the_lines_below() -> None:
    variant = robustness.layout(SOURCE)
    assert variant is not None
    assert (
        "long entry(long n, long a[n], long k, long x) requires(1 <= n && n <= 8) requires(0 <= k && k < n) "
        "requires(-50 <= x && x <= 50) {\n    long t1 = (x + 2);"
    ) in variant.text
    assert variant.lines[10] == 6 and variant.lines[16] == 12 and 5 not in variant.lines
    assert robustness.layout(variant.text) is None


def test_every_rewriting_of_a_certified_program_is_judged_the_same() -> None:
    target = read_target("clang-19")
    baseline = adapter.check(adapter.load_text(SOURCE, "p.c"), target, level="memory")[1]
    assert baseline.accepted
    cases = [
        robustness.Inputs({"n": 2, "k": 1, "x": 4}, {"a": [5, 6]}),
        robustness.Inputs({"n": 2, "k": 1, "x": -1}, {"a": [5, 6]}),
    ]
    for kind in robustness.VARIANTS:
        row = robustness.compare(SOURCE, baseline, kind, cases, target)
        assert row["outcome"] == "same" and row["behaviour_same"] is True, row
        assert row["code_same"] is (True if kind in {"rename", "layout"} else None)
        assert row["sites"] == 5, row  # By hand: a[k] read, a[k] written; x + 2, t1 * 3, x + g0.


def test_a_variant_judged_differently_is_reported_as_differing(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    target = read_target("clang-19")
    baseline = adapter.check(adapter.load_text(SOURCE, "p.c"), target, level="memory")[1]
    weaker = SOURCE.replace("    requires(0 <= k && k < n)\n", "")
    monkeypatch.setitem(robustness.REWRITINGS, "swap", lambda text: robustness.Variant(weaker, {}))
    row = robustness.compare(SOURCE, baseline, "swap", [], target)
    assert row["outcome"] == "differs" and row["verdict_same"] is False


def test_a_rewriting_that_changes_the_result_is_caught_by_the_interpreter(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    target = read_target("clang-19")
    baseline = adapter.check(adapter.load_text(SOURCE, "p.c"), target, level="memory")[1]
    other = SOURCE.replace("return t1;", "return x;")
    monkeypatch.setitem(robustness.REWRITINGS, "swap", lambda text: robustness.Variant(other, {}))
    cases = [robustness.Inputs({"n": 2, "k": 1, "x": 4}, {"a": [5, 6]})]
    row = robustness.compare(SOURCE, baseline, "swap", cases, target)
    assert row["behaviour_same"] is False
    summary = robustness.summarise([{**row, "program": "p"}])
    assert summary["rewriting_changed_behaviour"] == ["p swap"] and summary["passed"] is False


def test_the_summary_needs_every_rewriting_to_have_applied_and_none_to_differ() -> None:
    def row(kind: str, outcome: str) -> dict[str, object]:
        return {"row": "variant", "program": "p", "variant": kind, "outcome": outcome, "behaviour_same": True}

    same = [row(kind, "same") for kind in robustness.VARIANTS]
    assert robustness.summarise(same)["passed"] is True
    assert robustness.summarise([*same[:3], row("layout", "not applicable")])["passed"] is False
    assert robustness.summarise([*same, row("rename", "differs")])["differing"] == ["p rename"]


def test_generated_programs_from_development_seeds_are_rewritten_without_a_difference() -> None:
    for seed in range(300, 303):
        rows = robustness.one_program((f"g{seed}", generate.program(seed).text, seed, "clang-19", 600))
        assert all(row["outcome"] in {"same", "not applicable"} for row in rows[1:]), rows
        assert all(row["behaviour_same"] is not False for row in rows[1:]), rows


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

    monkeypatch.setattr(robustness.adapter, "check", wrapped)
    if not swallowed:
        with pytest.raises(ctypes.ArgumentError):
            robustness.one_program(("p", "long f(void)\n{\n    return 0;\n}\n", None, "clang-19", 600))
        return
    rows = robustness.one_program(("p", "long f(void)\n{\n    return 0;\n}\n", None, "clang-19", 600))
    assert rows[0]["status"] == "not judged within the time budget"
