"""Proof help: counter bounds proposed from the loop shape and kept only if proved; `decreases` for termination."""

from pathlib import Path

import pytest

from pfc2 import frontend, infer
from pfc2.core import ir
from pfc2.core.target import Target
from pfc2.elaborate import Unit
from pfc2.gate import Certification, certify

TARGET = Target("static LP64 layout (test)", "x86_64-pc-linux-gnu", 32, 64)
pytestmark = pytest.mark.integration


def _unit(tmp_path: Path, body: str) -> Unit:
    source = tmp_path / "t.c"
    source.write_text('#include "pfc.h"\n' + body, encoding="utf-8")
    return infer.apply(frontend.load(source), TARGET)


def _certify(unit: Unit, level: str = "full") -> Certification:
    return certify(unit.program, TARGET, level=level, code=unit.code)  # type: ignore[arg-type]


def test_an_up_counter_gets_both_bounds_and_the_program_certifies_without_a_written_invariant(tmp_path: Path) -> None:
    unit = _unit(
        tmp_path,
        "long count(long n)\n    requires(0 <= n)\n    ensures(result == n)\n{\n    long i = 0;\n"
        "    while (i < n) {\n        i++;\n    }\n    return i;\n}\n",
    )
    assert [(i.function, i.line, i.invariant) for i in unit.inferred] == [("count", 7, "((0 <= i) && (i <= n))")]
    assert _certify(unit).accepted


def test_a_bound_that_does_not_hold_is_dropped_and_the_other_is_kept(tmp_path: Path) -> None:
    unit = _unit(
        tmp_path,
        "long count(long n)\n    ensures(result >= 0)\n{\n    long i = 0;\n"
        "    while (i < n) {\n        i++;\n    }\n    return i;\n}\n",
    )
    assert [(i.line, i.invariant) for i in unit.inferred] == [(6, "(0 <= i)")]
    assert _certify(unit).accepted


def test_a_down_counter_and_a_for_loop_over_an_array(tmp_path: Path) -> None:
    unit = _unit(
        tmp_path,
        "long down(long n)\n    requires(0 <= n)\n    ensures(result == 0)\n{\n    long i = n;\n"
        "    while (i > 0) {\n        i--;\n    }\n    return i;\n}\n"
        "long sum(long n, const long a[n])\n{\n    long s = 0;\n"
        "    for (long i = 0; i < n; i++) {\n        s += a[i];\n    }\n    return s;\n}\n",
    )
    assert [(i.function, i.invariant) for i in unit.inferred] == [
        ("down", "((i <= n) && (0 <= i))"),
        ("sum", "((0 <= i) && (i <= n))"),
    ]
    assert not _certify(unit).accepted  # The accumulator may overflow.
    memory = _certify(unit, "memory")
    assert memory.accepted and len(memory.retained_traps) == 1


def test_a_written_invariant_is_kept_and_a_loop_without_a_counter_gets_nothing(tmp_path: Path) -> None:
    unit = _unit(
        tmp_path,
        "long f(long n)\n    requires(0 <= n)\n    ensures(result == n)\n{\n    long i = 0;\n    long j = 0;\n"
        "    while (i < n) invariant(i == j) {\n        i++;\n        j++;\n    }\n"
        "    while (j != i) {\n        j = i;\n    }\n    return j;\n}\n",
    )
    assert [(i.line, i.invariant) for i in unit.inferred] == [(8, "((0 <= i) && (i <= n))")]
    assert _certify(unit).accepted


def test_decreases_proves_termination_and_leaves_no_trace_in_the_emitted_c(tmp_path: Path) -> None:
    unit = _unit(
        tmp_path,
        "long count(long n)\n    requires(0 <= n)\n    ensures(result == n)\n{\n    long i = 0;\n"
        "    while (i < n) decreases(n - i) {\n        i++;\n    }\n    long j = 0;\n"
        "    for (long k = 0; k < n; k++) decreases(n - k) {\n        j = k;\n    }\n    return i;\n}\n",
    )
    assert [(m.function, m.location.line, m.predicate) for m in unit.measures] == [
        ("count", 7, "n - i"),
        ("count", 11, "n - k"),
    ]
    certification = _certify(unit)
    assert certification.accepted and certification.c is not None and "pfc2_d" not in certification.c


@pytest.mark.parametrize(
    "loop",
    [
        "while (i < n) decreases(i) {\n        i++;\n    }",  # Grows.
        "while (i < n) decreases(n - i) {\n        i = i;\n    }",  # Does not move.
        "while (i != n) decreases(n - i) {\n        i = i + 2;\n    }",  # Can pass n and become negative.
    ],
)
def test_a_measure_that_does_not_decrease_or_can_go_negative_is_refused(tmp_path: Path, loop: str) -> None:
    unit = _unit(
        tmp_path,
        f"long count(long n)\n    requires(0 <= n)\n{{\n    long i = 0;\n    {loop}\n    return i;\n}}\n",
    )
    certification = _certify(unit)
    assert not certification.accepted and certification.c is None
    assert any(b.kind == "assert" and b.location.line == 6 for b in certification.blockers)


def test_an_array_of_n_elements_implies_a_non_negative_n_checked_at_calls_and_at_entry(tmp_path: Path) -> None:
    unit = _unit(
        tmp_path,
        "long fill(long n, long a[n], long value)\n    ensures(result == n)\n{\n"
        "    for (long i = 0; i < n; i++) {\n        a[i] = value;\n"
        "    }\n    return n;\n}\n"
        "law fill_returns_its_count(long n, long a[n], long v)\n{\n    assert(fill(n, a, v) == n);\n}\n"
        "long legacy(long a[], long a_len)\n{\n    return 0;\n}\n",
    )
    fill, law, legacy = unit.program.functions
    assert [ir.render_expression(c.condition) for c in fill.contracts] == ["(RESULT == n)", "(0 <= n)"]
    assert [ir.render_expression(c.condition) for c in law.contracts] == ["(0 <= n)"]
    assert legacy.contracts == ()  # The older spelling states its capacity itself.
    certification = _certify(unit)
    assert certification.accepted and certification.c is not None
    assert "_Bool pfc_entry_1 = ((long)0 <= n);\n    if (!pfc_entry_1) __builtin_trap();" in certification.c
    assert [(i.function, i.invariant) for i in unit.inferred] == [("fill", "((0 <= i) && (i <= n))")]
