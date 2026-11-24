"""Mutation gaps of core/vc.py: a bool is exactly 0 or 1, as an assumption and as a promise (real Z3)."""

import pytest

from pfc2 import frontend
from pfc2.check import check
from pfc2.core.target import Target
from pfc2.gate import Certification, Level

TARGET = Target("test LP64 layout (no clang queried)", "x86_64-pc-linux-gnu", 32, 64)
HEADERS = '#include "pfc.h"\n#include <stdbool.h>\n\n'


def judge(text: str, level: Level = "full") -> Certification:
    """Lines of `text` are numbered from 4 in the diagnostics: three header lines come first."""
    return check(frontend.load_text(HEADERS + text, "gap.c"), TARGET, level=level)[1]


@pytest.mark.integration
@pytest.mark.parametrize("level", ["full", "memory"])
def test_out_of_bounds_read_under_a_false_bool_parameter_is_refused_with_that_bool_as_zero(level: Level) -> None:
    """A bool parameter may be false: the path under `!b` is live and its read of a[5] in a 2-element array fails."""
    result = judge(
        """long pick(long n, long a[n], bool b)
    requires(n == 2)
{
    if (!b) {
        return a[5];
    }
    return a[0];
}
""",
        level,
    )
    assert not result.accepted and result.c is None
    assert [(b.kind, b.function, b.location.line, b.status) for b in result.blockers] == [
        ("bounds", "pick", 8, "failed")
    ]
    counterexample = result.blockers[0].counterexample
    assert counterexample is not None
    assert {(v.name, v.value) for v in counterexample.scalars} >= {("n", 2), ("b", 0)}


@pytest.mark.integration
def test_bool_parameter_is_a_proved_index_into_a_two_element_array() -> None:
    """A bool is never below 0 or above 1, so a[b] is inside an array of exactly two elements."""
    result = judge("""long at(long n, long a[n], bool b)
    requires(n == 2)
{
    long x = b;
    return a[x];
}
""")
    assert result.accepted and result.blockers == () and result.c is not None
    assert [d.removed for d in result.emission.decisions] == [True]


@pytest.mark.integration
@pytest.mark.parametrize("promise", ["result == 2", "result + 1 == 0", "result > 1", "result < 0"])
def test_declared_bool_function_promising_a_value_no_bool_has_is_refused(promise: str) -> None:
    """The contract of an external function is trusted, so one that no _Bool result can satisfy must be refused."""
    result = judge(f"""bool odd(long x)
    ensures({promise});

long use(long x)
{{
    long k = odd(x);
    return k;
}}
""")
    assert not result.accepted and result.c is None
    assert result.reason == "the contract of odd cannot be satisfied: it is contradictory"


@pytest.mark.integration
@pytest.mark.parametrize("promise", ["result == 0", "result == 1"])
def test_declared_bool_function_promising_zero_or_one_is_accepted(promise: str) -> None:
    result = judge(f"""bool odd(long x)
    ensures({promise});

long use(long x)
{{
    long k = odd(x);
    return k;
}}
""")
    assert result.accepted and result.c is not None
