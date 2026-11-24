"""Behaviour of the solver adapter that the mutation campaign found unobserved: externals and narrow targets."""

import pytest

from pfc2 import frontend
from pfc2.check import check
from pfc2.core.diagnostics import FrontendError
from pfc2.core.target import Target
from pfc2.gate import Certification

TARGET = Target("static LP64 layout (test)", "x86_64-pc-linux-gnu", 32, 64)
ILP32 = Target("static ILP32 layout (test)", "i386-unknown-linux-gnu", 32, 32)
pytestmark = pytest.mark.integration

USE_ABOVE = """
long use(long n, const long a[n])
    requires(n >= 1)
{
    long r = above(n, a);
    return 0;
}
"""
USE_SETTER = """
long use(long n, long a[n])
    requires(REQUIRES)
{
    long r = setter(n, a);
    return r;
}
"""
THROUGH_CONST_ARRAY = """long setter(long n, long a[n], long m, const char b[m])
    requires(n >= 2 && m >= 1 && 0 <= b[0] && b[0] < n)
    ensures(result == 0 && a[b[0]] == 1);

long use(long n, long a[n], long m, const char b[m])
    requires(n >= 2 && m >= 1 && 0 <= b[0] && b[0] < n)
{
    long r = setter(n, a, m, b);
    return r;
}
"""


def _check(body: str, target: Target = TARGET) -> Certification:
    return check(frontend.load_text('#include "pfc.h"\n' + body, "t.c"), target)[1]


def _externals(certification: Certification) -> list[tuple[str, str, str]]:
    return [(e.query.function, e.consistent, e.total) for e in certification.proof.external_results]


def test_a_result_above_an_array_cell_is_not_total_because_the_cell_may_hold_the_largest_long() -> None:
    """No long is greater than a[0] == LONG_MAX: memory before the call ranges over the whole type, ends included."""
    contract = "long above(long n, const long a[n])\n    requires(n >= 1)\n    ensures(result > a[0]);\n"
    certification = _check(contract + USE_ABOVE)
    assert not certification.accepted and certification.c is None
    assert "contract of above" in certification.reason
    assert [(name, consistent) for name, consistent, _ in _externals(certification)] == [("above", "sat")]
    assert _externals(certification)[0][2] != "total"


def test_a_result_at_least_an_array_cell_is_total_and_the_caller_is_certified() -> None:
    contract = "long above(long n, const long a[n])\n    requires(n >= 1)\n    ensures(result >= a[0]);\n"
    certification = _check(contract + USE_ABOVE)
    assert certification.accepted and certification.c is not None
    assert _externals(certification) == [("above", "sat", "total")]


def test_a_written_cell_selected_through_an_unwritten_array_is_modelled_and_found_total() -> None:
    """a[b[0]] with b const: the address reads memory the function cannot write, so one cell of a is chosen."""
    certification = _check(THROUGH_CONST_ARRAY)
    assert certification.accepted and certification.c is not None
    assert _externals(certification) == [("setter", "sat", "total")]


@pytest.mark.parametrize(
    ("requires", "ensures"),
    [
        ("n >= 2", "result == 0 && 0 <= a[0] && a[0] < n && a[a[0]] == 1"),
        ("n >= 2 && a[1] == 1", "result == 0 && a[0] == 1 && a[a[0]] == 1"),
    ],
)
def test_a_written_cell_selected_through_the_written_array_itself_is_reported_unknown(
    requires: str, ensures: str
) -> None:
    """a[a[0]]: the written cell picks another written cell, which the totality query does not model."""
    contract = f"long setter(long n, long a[n])\n    requires({requires})\n    ensures({ensures});\n"
    certification = _check(contract + USE_SETTER.replace("REQUIRES", requires))
    assert not certification.accepted and certification.c is None
    assert _externals(certification) == [("setter", "sat", "unknown")]


def _literal_program(literal: str) -> str:
    return f"long f(long x)\n    requires(0 <= x && x < 10)\n{{\n    long y = {literal};\n    return y - y + x;\n}}\n"


@pytest.mark.parametrize("literal", ["2147483648", "2147483649", "2147483648L", "4294967295", "8589934591"])
def test_a_decimal_literal_above_the_largest_32_bit_long_is_refused_on_a_target_with_a_32_bit_long(
    literal: str,
) -> None:
    """2**31 - 1 == 2147483647 is the largest 32-bit long; C types anything above as long long there.

    Reached through the Python API with an explicit layout: no installed clang here reports a 32-bit long.
    """
    with pytest.raises(FrontendError) as refusal:
        _check(_literal_program(literal), ILP32)
    assert refusal.value.diagnostic.rule == "target-literal"
    assert refusal.value.diagnostic.location.line == 5


def test_the_largest_32_bit_long_is_accepted_with_a_suffix_on_a_target_with_a_32_bit_long() -> None:
    certification = _check(_literal_program("2147483647L"), ILP32)
    assert certification.accepted and certification.c is not None


def test_the_same_literal_above_32_bits_is_accepted_on_the_64_bit_long_layout() -> None:
    certification = _check(_literal_program("2147483648"), TARGET)
    assert certification.accepted and certification.c is not None
