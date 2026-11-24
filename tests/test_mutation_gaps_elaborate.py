"""Behaviour of elaboration that the mutation campaign found unobserved: shared local arrays, ghosts, endless for."""

import pytest

from pfc2 import frontend
from pfc2.check import check
from pfc2.core.emit import GUARD_LINE
from pfc2.core.target import Target
from pfc2.elaborate import Unit
from pfc2.gate import Certification

TARGET = Target("static LP64 layout (test)", "x86_64-pc-linux-gnu", 32, 64)
HEADER = '#include "pfc.h"\n'

CLOBBERED_LOCAL_ARRAY = """long clobber(long n, long a[n])
    requires(1 <= n)
    ensures(result == 0)
{
    a[0] = 0;
    return 0;
}

long f(void)
{
    long a[2] = {5, 5};
    long x where(x <= a[0]) = 3;
    long r = 0;
    r = clobber(2, a);
    return x + r;
}
"""

UNTOUCHED_LOCAL_ARRAY = CLOBBERED_LOCAL_ARRAY.replace("    r = clobber(2, a);\n", "")

# The outer measure is the constant 5: it never decreases. The inner loop always leaves through break.
CONSTANT_OUTER_MEASURE = """long spin(long n)
    requires(0 <= n && n <= 100)
{
    long i = 0;
    while (i < n) invariant(0 <= i && i <= n) decreases(5) {
        long j = 0;
        while (j < 10) invariant(j == 0) decreases(100 - j) {
            if (j >= 0) {
                break;
            }
            j++;
        }
    }
    return i;
}
"""

# n == 4 and i == 0, so a[i + 7] is outside the array on the only path through the body.
ENDLESS_FOR_OUT_OF_BOUNDS = """long scan(long n, long a[n])
    requires(n == 4)
{
    long s = 0;
    long i = 0;
    for (;;) invariant(i == 0) decreases(10 - i) {
        s = a[i + 7];
        break;
    }
    return s;
}
"""

ELSE_BRANCH = """long f(long n, long c)
    requires(0 <= n && n <= 100)
{
    long i = 0;
    long k = 0;
    while (i < n) invariant(0 <= i && i <= n && 0 <= k) decreases(n - i) {
        if (c > 0) {
            k = 1;
        } else {
            INNER
        }
        i++;
    }
    return i;
}
"""
UNMEASURED_IN_ELSE = ELSE_BRANCH.replace("INNER", "while (k < 5) invariant(0 <= k) { k = k; }")
MEASURED_IN_ELSE = ELSE_BRANCH.replace("INNER", "while (k < 5) invariant(0 <= k) decreases(5 - k) { k++; }")


def _load(body: str) -> Unit:
    return frontend.load_text(HEADER + body, "t.c")


def _check(body: str, level: str = "full") -> tuple[Unit, Certification]:
    return check(_load(body), TARGET, level=level)  # type: ignore[arg-type]


@pytest.mark.integration
def test_a_type_that_reads_a_local_array_is_checked_again_after_a_call_that_may_write_the_array() -> None:
    """clobber sets a[0] to 0, so `x <= a[0]` with x == 3 no longer holds after the call (program line 15)."""
    _, certification = _check(CLOBBERED_LOCAL_ARRAY)
    assert not certification.accepted and certification.c is None
    assert ("assert", 15, "failed") in [(b.kind, b.location.line, b.status) for b in certification.blockers]


@pytest.mark.integration
def test_the_same_type_over_a_local_array_is_certified_when_nothing_writes_the_array() -> None:
    _, certification = _check(UNTOUCHED_LOCAL_ARRAY)
    assert certification.accepted and certification.c is not None


@pytest.mark.integration
def test_an_outer_measure_that_never_decreases_is_refused_even_when_the_inner_measured_loop_breaks() -> None:
    """Each measured loop has its own ghost: the outer goal compares 5 with 5, never with the inner measure."""
    _, certification = _check(CONSTANT_OUTER_MEASURE)
    assert not certification.accepted and certification.c is None
    failed = [(b.kind, b.location.line, b.goal) for b in certification.blockers if b.status == "failed"]
    assert failed == [("assert", 6, "(5 < 5)")]


@pytest.mark.integration
@pytest.mark.parametrize("level", ["full", "memory"])
def test_the_body_of_a_measured_endless_for_is_reachable_so_its_out_of_bounds_read_is_refused(level: str) -> None:
    """`for (;;)` runs its body: nothing in it may be proved under a false loop condition."""
    _, certification = _check(ENDLESS_FOR_OUT_OF_BOUNDS, level)
    assert not certification.accepted and certification.c is None
    assert ("bounds", 8, "failed") in [(b.kind, b.location.line, b.status) for b in certification.blockers]
    assert GUARD_LINE.search(certification.emission.c)  # The guard on a[i + 7] stays in the (unreleased) emission.


def test_a_loop_whose_else_branch_holds_an_unmeasured_loop_is_not_recorded_as_proved_to_terminate() -> None:
    """The inner `while (k < 5) { k = k; }` may run forever, so the outer measure establishes nothing."""
    assert _load(UNMEASURED_IN_ELSE).measures == ()


def test_measured_loops_inside_an_else_branch_are_recorded_together_with_the_loop_around_them() -> None:
    measures = _load(MEASURED_IN_ELSE).measures
    assert sorted((m.function, m.location.line, m.predicate) for m in measures) == [
        ("f", 7, "n - i"),
        ("f", 11, "5 - k"),
    ]
