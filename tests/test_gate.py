"""Strict gate: C is produced only when the requested level is completely proved (real Z3)."""

from pathlib import Path

from pfc2 import frontend, gate
from pfc2.core.emit import ENTRY_LINE, GUARD_LINE, OVERFLOW_LINE
from pfc2.core.target import Target

FIXTURES = Path(__file__).parent / "fixtures"
TARGET = Target("test LP64 layout (no clang queried)", "x86_64-pc-linux-gnu", 32, 64)


def certify(name: str, level: gate.Level = "full") -> gate.Certification:
    return gate.certify(frontend.load(FIXTURES / name).program, TARGET, level=level)


def test_fully_proved_program_is_certified_without_guards_or_traps():
    result = certify("count.c")
    assert result.accepted and result.blockers == () and result.c is not None
    assert not GUARD_LINE.search(result.c) and not OVERFLOW_LINE.search(result.c)
    # The boundary with unverified callers stays checked: 0 <= n is tested at entry.
    assert len(ENTRY_LINE.findall(result.c)) == 1
    assert "where" not in result.c and "__spec" not in result.c


def test_array_program_is_certified_and_cites_its_proofs():
    result = certify("fill.c")
    assert result.accepted and result.c is not None
    assert "// proved: obligation" in result.c
    assert not GUARD_LINE.search(result.c) and not OVERFLOW_LINE.search(result.c)


def test_sum_is_refused_at_full_for_its_accumulator_and_emits_no_c():
    result = certify("sum.c")
    assert not result.accepted and result.c is None
    assert [(b.kind, b.location.line, b.status) for b in result.blockers] == [("overflow", 9, "failed")]
    assert result.blockers[0].counterexample is not None
    assert result.memory_would_pass


def test_sum_is_certified_at_memory_and_keeps_exactly_the_unproved_trap():
    result = certify("sum.c", "memory")
    assert result.accepted and result.c is not None
    assert not GUARD_LINE.search(result.c)
    assert len(OVERFLOW_LINE.findall(result.c)) == 1
    assert [(d.kind, d.location.line) for d in result.retained_traps] == [("overflow", 9)]


def test_wrong_type_is_refused_at_its_declaration_with_a_counterexample():
    result = certify("wrong.c")
    assert not result.accepted and result.c is None and not result.memory_would_pass
    first = result.blockers[0]
    assert (first.kind, first.location.line, first.status) == ("assert", 5, "failed")
    assert first.counterexample is not None
    assert {(v.name, v.value) for v in first.counterexample.scalars} >= {("n", 0)}


def test_contradictory_law_is_refused_even_though_every_formula_is_valid():
    result = certify("contradiction.c")
    assert not result.accepted and result.c is None
    assert "cannot be satisfied" in result.reason
    assert all(r.status == "proved" for r in result.proof.results)


def test_refusal_is_the_same_at_every_call():
    first, second = certify("wrong.c"), certify("wrong.c")
    assert [(b.obligation_id, b.status) for b in first.blockers] == [
        (b.obligation_id, b.status) for b in second.blockers
    ]


def test_timeout_never_certifies():
    program = frontend.load(FIXTURES / "count.c").program

    class Stuck:
        def set(self, **options: int) -> None: ...
        def add(self, *expressions: object) -> None: ...
        def check(self) -> object:
            import z3

            return z3.unknown

        def model(self) -> object:
            raise AssertionError("no model for unknown")

        def reason_unknown(self) -> str:
            return "timeout"

    result = gate.certify(program, TARGET, solver_factory=Stuck)
    assert not result.accepted and result.c is None
    assert {b.status for b in result.blockers} <= {"timeout", "unknown"}


def certify_unit(name: str, level: gate.Level = "full") -> gate.Certification:
    unit = frontend.load(FIXTURES / name)
    return gate.certify(unit.program, TARGET, level=level, code=unit.code)


def test_law_is_proved_and_only_the_function_is_emitted():
    result = certify_unit("count_law.c")
    assert result.accepted and result.c is not None
    assert "count_reaches_n" not in result.c and "long count(long n)" in result.c
    assert not GUARD_LINE.search(result.c) and not OVERFLOW_LINE.search(result.c)
    # The hypothesis of the law is the checked boundary of the emitted function.
    assert len(ENTRY_LINE.findall(result.c)) == 1


def test_false_law_is_refused_at_the_function_it_is_about():
    result = certify_unit("false_law.c")
    assert not result.accepted and result.c is None
    assert ("assert", "count_is_one_more") in {(b.kind, b.function) for b in result.blockers}


def test_array_law_certifies_the_writes():
    result = certify_unit("fill_law.c")
    assert result.accepted and result.c is not None and "fill_writes_inside_the_array" not in result.c
