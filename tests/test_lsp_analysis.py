"""What the editor shows: diagnostics, hovers and symbols computed from source text.

Positions are counted by hand in the example files (1-based line and column, as the checker reports them).
"""

from pathlib import Path

from pfc2.lsp.analysis import analyze, hover_at

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def _read(name: str) -> str:
    return (EXAMPLES / name).read_text(encoding="utf-8")


def _marks(analysis, severity):  # type: ignore[no-untyped-def]
    return [(d.line, d.column, d.code) for d in analysis.diagnostics if d.severity == severity]


def test_an_unproved_obligation_is_an_error_at_its_operation_with_the_counterexample() -> None:
    analysis = analyze(_read("wrong/off_by_one.c"), "off_by_one.c")
    assert analysis.applicable and analysis.accepted is False
    assert _marks(analysis, "error") == [(7, 9, "bounds"), (6, 30, "overflow")]
    bounds = analysis.diagnostics[0]
    assert "this index may be outside the array" in bounds.message
    assert "((0 <= i) && (i < n))" in bounds.message and "n = 0" in bounds.message
    assert (bounds.end_column - bounds.column) == 1  # The identifier `a`.


def test_a_certified_file_has_no_errors_only_hints() -> None:
    analysis = analyze(_read("01_count/count.c"), "count.c")
    assert analysis.accepted is True and _marks(analysis, "error") == [] and _marks(analysis, "warning") == []
    assert _marks(analysis, "hint") == [(11, 5, "inferred"), (11, 5, "termination")]
    assert "((0 <= i) && (i <= n))" in analysis.diagnostics[0].message


def test_a_kept_overflow_trap_is_a_warning_at_the_memory_level_and_an_error_at_full() -> None:
    source = _read("03_sum/sum.c")
    memory = analyze(source, "sum.c", level="memory")
    assert memory.accepted is True and _marks(memory, "warning") == [(10, 9, "overflow-trap")]
    full = analyze(source, "sum.c", level="full")
    assert full.accepted is False and _marks(full, "error") == [(10, 9, "overflow")]


def test_a_source_error_is_one_diagnostic_with_its_rule() -> None:
    analysis = analyze('#include "pfc.h"\nlong f(void) { return 0 }\n', "bad.c")
    assert analysis.accepted is None and [(d.line, d.code, d.severity) for d in analysis.diagnostics] == [
        (2, "parse-syntax", "error")
    ]
    refused = analyze(_read("wrong/contradictory_extern.c"), "x.c")
    assert [(d.line, d.code) for d in refused.diagnostics if d.severity == "error"] == [(6, "contract")]
    assert "the contract of sensor cannot be satisfied" in refused.diagnostics[0].message


def test_a_file_that_does_not_include_pfc_h_is_left_alone() -> None:
    analysis = analyze("int main(void) { return 0; }\n", "plain.c")
    assert not analysis.applicable and analysis.diagnostics == () and analysis.symbols == ()


def test_hover_explains_a_function_a_loop_and_a_removed_check() -> None:
    analysis = analyze(_read("02_fill/fill.c"), "fill.c")
    function = hover_at(analysis, 5, 6)  # `fill` in `long fill(long n, long a[n], long value)`
    assert function is not None and "**fill**" in function.text and "requires `(0 <= n)`" in function.text
    assert "obligations proved: 4 of 4" in function.text
    loop = hover_at(analysis, 7, 5)  # `for`
    assert loop is not None and "((0 <= i) && (i <= n))" in loop.text and "termination is not claimed" in loop.text
    access = hover_at(analysis, 8, 9)  # `a[i] = value`
    assert access is not None and "bounds check removed" in access.text
    assert hover_at(analysis, 2, 1) is None
    measured = analyze(_read("07_countdown/countdown.c"), "countdown.c")
    stops = hover_at(measured, 11, 5)
    assert stops is not None and "terminates" in stops.text and "`left`" in stops.text


def test_symbols_list_functions_laws_and_globals() -> None:
    counter = analyze(_read("08_counter/counter.c"), "counter.c")
    assert [(s.name, s.kind, s.line) for s in counter.symbols] == [
        ("hits", "global", 5),
        ("limit", "global", 6),
        ("hit", "function", 8),
        ("twice", "function", 19),
    ]
    count = analyze(_read("01_count/count.c"), "count.c")
    assert [(s.name, s.kind) for s in count.symbols] == [("count", "function"), ("counting_to_n_gives_n", "law")]
