"""E3: the text operations by hand, and the experiment's rule on development seeds."""

from random import Random

import pytest

from pfc2_eval import generate, inject


def test_invariant_clauses_are_removed_with_their_line_and_nothing_else_moves() -> None:
    text = (
        "long f(long n)\n{\n    while (n > 0) invariant(0 <= n && (n < 9 || n == 9)) decreases(n) {\n"
        "        n--;\n    }\n}\n"
    )
    stripped, removed = inject.strip_invariants(text)
    assert removed == [(3, "0 <= n && (n < 9 || n == 9)")]
    assert "invariant" not in stripped and "decreases(n) {" in stripped
    assert len(stripped) == len(text) and stripped.count("\n") == text.count("\n")


def test_a_predicate_is_split_only_at_its_top_level_conjunctions() -> None:
    assert inject.conjuncts("(0 <= i) && (i <= n)") == ["(0 <= i)", "(i <= n)"]
    assert inject.conjuncts("0 <= i && (a < b && c < d) && x == 1") == ["0 <= i", "(a < b && c < d)", "x == 1"]
    assert inject.conjuncts("i <= n") == ["i <= n"]


def test_the_family_of_damaged_invariants() -> None:
    found = inject.candidates("(0 <= i) && (i <= n)", ["n", "k", "x"], Random(0))
    by_operator: dict[str, list[str]] = {}
    for operator, text in found:
        by_operator.setdefault(operator, []).append(text)
    assert by_operator["literal-false"] == ["0 == 1"]
    assert "((i <= n))" in by_operator["dropped"] and "((0 <= i))" in by_operator["dropped"]
    assert "((i <= n)) && ((0 < i))" in by_operator["off-by-one"]  # 0 < i is false when the loop starts at 0.
    assert "((0 <= i)) && ((i < n))" in by_operator["off-by-one"]  # i < n is false when the loop ends.
    assert "((i <= n)) && ((0 >= i))" in by_operator["reversed"]
    assert len(found) == len(set(found)) <= inject.MAX_CANDIDATES
    assert all(text != "(0 <= i) && (i <= n)" for _, text in found)


@pytest.mark.integration
def test_on_development_programs_false_candidates_exist_and_none_is_admitted() -> None:
    rows = []
    for seed in range(0, 12):
        rows += inject.one_program((f"g{seed}", generate.program(seed).text, seed, "clang-19", 120))
    chosen = [row for row in rows if row["row"] == "candidate"]
    false = [row for row in chosen if row["class"] == "false"]
    assert len(false) >= 5, {row["status"] for row in rows if row["row"] == "program"}
    assert not [row for row in false if row["admitted"]]
    # `0 == 1` is refuted wherever a run reaches the loop. Where no run does (seed 10: the loop is under
    # `if ((8 / 7) > 6)`), it is not refuted, and admitting it there is sound: the loop never executes.
    literal = [row for row in chosen if row["operator"] == "literal-false"]
    assert sum(row["class"] == "false" for row in literal) >= 3
    assert any(row["class"] == "not-refuted" and row["admitted"] for row in chosen)  # A weaker one that suffices.


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

    monkeypatch.setattr(inject.adapter, "check", wrapped)
    if not swallowed:
        with pytest.raises(ctypes.ArgumentError):
            inject.one_program(("p", "long f(void)\n{\n    return 0;\n}\n", None, "clang-19", 600))
        return
    rows = inject.one_program(("p", "long f(void)\n{\n    return 0;\n}\n", None, "clang-19", 600))
    assert rows[0]["status"] == "not judged within the time budget"
