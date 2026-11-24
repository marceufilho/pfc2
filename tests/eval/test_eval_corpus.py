"""The mutant generator of the corpus study, by hand."""

from pfc2_eval import corpus

SOURCE = """#include "pfc.h"

long f(long n, const long a[n], long k)
    requires(0 <= k && k < n)
    ensures(result >= 0 - 1)
{
    long total = 0;

    for (long i = 0; i < n; i++) invariant(0 <= total) {
        if (a[i] <= 3 && a[i] != -2) {
            total = total + a[i] * 2;
        }
    }
    total += k;
    return total;
}
"""


def test_only_code_inside_bodies_is_mutated_and_clause_lines_never() -> None:
    found = corpus.mutants(SOURCE)
    lines = {mutant.line for mutant in found}
    assert lines == {7, 10, 11, 14}  # Not the contract (4, 5), not the loop line with its invariant (9).
    for mutant in found:
        changed = [
            (old, new) for old, new in zip(SOURCE.split("\n"), mutant.text.split("\n"), strict=True) if old != new
        ]
        assert len(changed) == 1


def test_each_operator_family_produces_what_it_should() -> None:
    found = corpus.mutants(SOURCE)
    line10 = sorted(m.text.split("\n")[9].strip() for m in found if m.line == 10 and m.operator == "relational")
    assert line10 == sorted(
        [
            "if (a[i] < 3 && a[i] != -2) {",
            "if (a[i] == 3 && a[i] != -2) {",
            "if (a[i] <= 3 && a[i] == -2) {",
        ]
    )
    constants = sorted(m.text.split("\n")[9].strip() for m in found if m.line == 10 and m.operator == "constant")
    assert "if (a[i] <= 4 && a[i] != -2) {" in constants and "if (a[i] <= 3 && a[i] != -1) {" in constants
    # The minus of `-2` is a sign, not a subtraction: it is not an arithmetic mutant.
    assert not [m for m in found if m.line == 10 and m.operator == "arithmetic"]
    arithmetic = sorted(m.text.split("\n")[10].strip() for m in found if m.line == 11 and m.operator == "arithmetic")
    assert arithmetic == ["total = total + a[i] + 2;", "total = total - a[i] * 2;"]
    deletions = [(m.line, m.text.split("\n")[m.line - 1].strip()) for m in found if m.operator == "deletion"]
    assert deletions == [(11, ";"), (14, ";")]  # Declarations and returns are not deleted.
    assert len({m.identifier for m in found}) == len(found)


SPECIFIED = """#include "pfc.h"

#define LIMIT 3

/* A struct {a, {b}} in a comment must not confuse the scan. */
long twice(long x)
    requires(0 <= x && x <= LIMIT)
    ensures(result == 2 * x)
{
    return x + x;
}

long first(long n, const int a[n])
    requires(1 <= n)
    ensures(result == a[0])
{
    for (long i = 0; i < n; i++) invariant(0 <= i) {
        if (i == 0) {
            return a[i];
        }
    }
    return 0;
}

law doubling(long x where(0 <= x && x <= LIMIT)) { assert(twice(x) == x + x); }
"""


def test_declarations_keep_contracts_and_drop_bodies_and_laws() -> None:
    text = corpus.declarations(SPECIFIED)
    assert "return" not in text and "law" not in text and "for (" not in text
    assert "#define LIMIT 3" in text and '#include "pfc.h"' in text
    assert "long twice(long x)\n    requires(0 <= x && x <= LIMIT)\n    ensures(result == 2 * x);" in text
    assert "long first(long n, const int a[n])\n    requires(1 <= n)\n    ensures(result == a[0]);" in text


def test_a_law_states_one_test_case_over_the_contract_alone() -> None:
    functions = {"first": {"result": "long", "parameters": "long n, const int a[n]", "call": "first(n, a)"}}
    case = {"name": "first_of_two", "function": "first", "inputs": {"n": 2, "a": [7, 9]}, "expected": "found == 7"}
    law = corpus.law(corpus.declarations(SPECIFIED), functions, case)
    assert "law case_first_of_two(long n, const int a[n])" in law  # Never the name of a function.
    assert "if (n == 2 && a[0] == 7 && a[1] == 9) {" in law
    assert "long found = first(n, a);" in law and "assert(found == 7);" in law
    text = {"name": "t", "function": "first", "inputs": {"n": 2, "a": "hi"}, "expected": "found == 104"}
    assert "a[0] == 104 && a[1] == 105" in corpus.law(corpus.declarations(SPECIFIED), functions, text)
    local = {**case, "locals": "long out[2] = {0, 0};", "call": "first(2, a)"}
    written = corpus.law(corpus.declarations(SPECIFIED), functions, local)
    assert "{\n    long out[2] = {0, 0};\n\n    if (" in written and "long found = first(2, a);" in written


def test_subsumption_is_decided_by_the_contract_not_by_the_body() -> None:
    from pfc2.core.target import read_target

    target = read_target("clang-19")
    functions = {
        "first": {"result": "long", "parameters": "long n, const int a[n]", "call": "first(n, a)"},
        "twice": {"result": "long", "parameters": "long x", "call": "twice(x)"},
    }
    said = {"name": "said", "function": "first", "inputs": {"n": 2, "a": [7, 9]}, "expected": "found == 7"}
    wrong = {"name": "wrong", "function": "first", "inputs": {"n": 2, "a": [7, 9]}, "expected": "found == 9"}
    outside = {"name": "outside", "function": "twice", "inputs": {"x": 4}, "expected": "found == 8"}
    skipped = {"name": "skipped", "inexpressible": "compares text built by the host"}
    assert corpus.subsumption(SPECIFIED, functions, said, target) == "subsumed"
    assert corpus.subsumption(SPECIFIED, functions, wrong, target) == "not-subsumed"
    assert corpus.subsumption(SPECIFIED, functions, outside, target) == "not-subsumed"  # 4 breaks the requires.
    assert corpus.subsumption(SPECIFIED, functions, skipped, target) == "inexpressible"


def test_same_code_ignores_clauses_and_notices_a_changed_token(tmp_path) -> None:  # type: ignore[no-untyped-def]
    bare = SPECIFIED.replace("    requires(0 <= x && x <= LIMIT)\n    ensures(result == 2 * x)\n", "")
    bare = bare.replace(" invariant(0 <= i)", "").replace("    requires(1 <= n)\n    ensures(result == a[0])\n", "")
    assert corpus.same_code(bare, SPECIFIED, "clang-19", tmp_path / "a")
    assert not corpus.same_code(bare, SPECIFIED.replace("return x + x;", "return x * 2;"), "clang-19", tmp_path / "b")


def test_selection_must_list_every_candidate_in_order_and_match_the_units(tmp_path) -> None:  # type: ignore[no-untyped-def]
    import json

    import pytest

    upstream = tmp_path / "practice"
    for slug in ("alpha", "beta", "gamma"):
        (upstream / slug).mkdir(parents=True)
    rows = [
        {"slug": "alpha", "status": "pilot"},
        {"slug": "beta", "status": "ported", "rules": ["P1", "P9"], "fixes": 0},
        {"slug": "gamma", "status": "excluded", "exclusion": "X1", "reason": "double"},
    ]
    path = tmp_path / "SELECTION.json"
    path.write_text(json.dumps({"units": rows}), encoding="utf-8")
    chosen = corpus.selection(path, upstream, ["beta"])
    assert chosen["candidates"] == 2 and chosen["ported"] == 1 and chosen["pilot"] == 1
    assert chosen["ported_registered_rules"] == 0 and chosen["ported_without_p14"] == 1
    assert chosen["excluded"] == {"X1": 1}
    with pytest.raises(ValueError, match="units"):
        corpus.selection(path, upstream, ["beta", "gamma"])
    path.write_text(json.dumps({"units": rows[:2]}), encoding="utf-8")
    with pytest.raises(ValueError, match="candidate"):
        corpus.selection(path, upstream, ["beta"])


def test_the_review_sample_is_seeded_and_a_fifth_rounded_up() -> None:
    names = [f"u{index:02d}" for index in range(21)]
    drawn = corpus.sample(names, seed=20261118, rate=0.2)
    assert len(drawn) == 5 and drawn == sorted(drawn) and set(drawn) <= set(names)
    assert drawn == corpus.sample(list(reversed(names)), seed=20261118, rate=0.2)
    assert drawn != corpus.sample(names, seed=1, rate=0.2)


def _row(**values: object) -> dict[str, object]:
    return {**{column.name: None for column in corpus.SCHEMA.columns}, **values}


def test_summary_counts_levels_assertions_and_the_two_by_two_table() -> None:
    rows = [
        _row(
            row="unit", unit="a", level="full", proof="certified", tests_on_port="pass", code_lines=10, clause_lines=2
        ),
        _row(row="assertion", unit="a", case="one", subsumption="subsumed"),
        _row(row="assertion", unit="a", case="two", subsumption="not-subsumed"),
        _row(row="assertion", unit="a", case="three", subsumption="inexpressible"),
        _row(row="mutant", unit="a", operator="relational", tests="fail", proof="refused-failed"),
        _row(row="mutant", unit="a", operator="relational", tests="fail", proof="certified"),
        _row(row="mutant", unit="a", operator="constant", tests="pass", proof="refused-failed"),
        _row(row="mutant", unit="a", operator="constant", tests="pass", proof="not-judged"),
        _row(row="unit", unit="b", level=None, proof="not-judged", tests_on_port="pass", code_lines=5, clause_lines=1),
    ]
    summary = corpus.summarise(rows)
    assert summary["s2_levels"] == {"full": 1, "not-judged": 1}
    assert summary["s2_code_lines"] == 15 and summary["s2_clause_lines"] == 3
    assert summary["s3_assertions"] == {"inexpressible": 1, "not-subsumed": 1, "subsumed": 1}
    # A timeout is not detection: the fourth mutant is in `neither` and is also counted as inconclusive.
    assert summary["s4_mutants"] == {"both": 1, "neither": 1, "proof": 1, "proof-inconclusive": 1, "tests": 1}
    assert summary["s4_by_operator"] == {"constant": {"neither": 1, "proof": 1}, "relational": {"both": 1, "tests": 1}}
    subsumed = summary["h4a_subsumed_proportion"]
    assert isinstance(subsumed, dict) and abs(subsumed["estimate"] - 1 / 3) < 1e-9 and subsumed["observations"] == 3
    difference = summary["h4b_refused_minus_killed"]
    assert isinstance(difference, dict) and difference["estimate"] == 0.0  # (0 + -1 + 1 + 0) / 4
    text = corpus.tables(rows)
    assert "| a | full | None | pass | None | 10 | 2 |" in text and "| b | not-judged |" in text
    assert "| a | 3 | 1 | 1 | 1 | 0 |" in text
    assert "| a | 4 | 1 | 1 | 1 | 1 | 1 | 0 |" in text


def _slow(sender) -> None:  # type: ignore[no-untyped-def]
    import time

    time.sleep(30)
    sender.send("late")


def _quick(value, sender) -> None:  # type: ignore[no-untyped-def]
    sender.send(value * 2)


def test_a_verdict_that_does_not_answer_in_time_is_none_and_its_process_is_gone() -> None:
    assert corpus.within(_quick, (21,), 20) == 42
    assert corpus.within(_slow, (), 0.5) is None


def test_a_law_beside_the_definitions_is_still_proved_from_the_contract_only() -> None:
    from pfc2.core.target import read_target

    target = read_target("clang-19")
    functions = {"first": {"result": "long", "parameters": "long n, const int a[n]", "call": "first(n, a)"}}
    said = {"name": "said", "function": "first", "inputs": {"n": 2, "a": [7, 9]}, "expected": "found == 7"}
    unsaid = {"name": "unsaid", "function": "first", "inputs": {"n": 2, "a": [7, 9]}, "expected": "found != 8"}
    beyond = {"name": "beyond", "function": "first", "inputs": {"n": 2, "a": [7, 9]}, "expected": "found == 9"}
    source = """#include "pfc.h"

long first(long n, const int a[n])
    requires(1 <= n)
    ensures(result == a[0])
{
    return a[0];
}
"""
    assert corpus.subsumption(source, functions, said, target, defined=True) == "subsumed"
    assert corpus.subsumption(source, functions, unsaid, target, defined=True) == "subsumed"  # 7 != 8 follows.
    assert corpus.subsumption(source, functions, beyond, target, defined=True) == "not-subsumed"
    weak = source.replace("    ensures(result == a[0])\n", "")
    assert corpus.subsumption(weak, functions, said, target, defined=True) == "not-subsumed"  # The body is not read.


def test_a_law_beside_definitions_is_judged_at_the_level_the_unit_certifies_at() -> None:
    from pfc2.core.target import read_target

    target = read_target("clang-19")
    # `x + 1` can overflow, so the unit certifies at `memory` only; its contract still implies the test.
    source = """#include "pfc.h"

long next(long x)
    ensures(result == x + 1)
{
    return x + 1;
}
"""
    functions = {"next": {"result": "long", "parameters": "long x", "call": "next(x)"}}
    case = {"name": "after_two", "function": "next", "inputs": {"x": 2}, "expected": "found == 3"}
    assert corpus.subsumption(source, functions, case, target, defined=True) == "not-subsumed"
    assert corpus.subsumption(source, functions, case, target, defined=True, level="memory") == "subsumed"
