"""Mutation gaps of gate.py: the released program's own verdict decides, and any kept check refuses (real Z3)."""

import pytest

from pfc2 import frontend, gate
from pfc2.check import check
from pfc2.core.emit import GUARD_LINE
from pfc2.core.target import Target
from pfc2.gate import Certification, Level

TARGET = Target("test LP64 layout (no clang queried)", "x86_64-pc-linux-gnu", 32, 64)
HEADERS = '#include "pfc.h"\n#include <stdbool.h>\n\n'

# The VC generator has no obligation for statements after a return, so the emitter keeps the bounds and the
# division guard of `a[5] / k`; nothing is unproved, and only the kept-check rule can refuse the file.
AFTER_RETURN = """long pick(long n, long a[n], long k)
    ensures(result == 1)
{
    return 1;
    return a[5] / k;
}
"""
TRIVIAL_LAW = """
law pick_ignores_k(long k)
{
    assert(k == k);
}
"""
PROVED = """long one(long x)
    ensures(result == 1)
{
    return 1;
}

law one_is_one(long x)
{
    assert(one(x) == 1);
}
"""
# Bounds are proved from the declared types; only `s + a[i]` may overflow.
OVERFLOWING = """long sum(const long a[], long a_len, long n where(0 <= n && n <= a_len))
{
    long s = 0;
    long i where(0 <= i && i <= n) = 0;

    while (i < n) {
        s = s + a[i];
        i = i + 1;
    }
    return s;
}
"""


def load(text: str) -> frontend.Unit:
    return frontend.load_text(HEADERS + text, "gap.c")


def judge(text: str, level: Level = "full") -> Certification:
    return check(load(text), TARGET, level=level)[1]


@pytest.mark.integration
@pytest.mark.parametrize("level", ["full", "memory"])
def test_guard_kept_without_an_unproved_obligation_refuses_the_file(level: Level) -> None:
    """Kept guards alone refuse: there is no retained trap here, and at memory traps are never counted."""
    result = judge(AFTER_RETURN, level)
    assert not result.accepted and result.c is None
    assert result.blockers == ()
    assert result.reason == "the emitter kept a runtime check that the proof does not cover"
    # The emission the gate looked at really holds both guards and no overflow site at all.
    assert len(GUARD_LINE.findall(result.emission.c)) == 2
    assert [d.removed for d in result.emission.decisions] == [False, False]
    assert result.emission.overflow == ()
    assert not result.memory_would_pass


@pytest.mark.integration
@pytest.mark.parametrize("level", ["full", "memory"])
def test_guard_kept_in_the_released_function_refuses_a_file_whose_law_is_proved(level: Level) -> None:
    """With a law the program judged first is not the released one; the released one's refusal must win."""
    result = judge(AFTER_RETURN + TRIVIAL_LAW, level)
    assert not result.accepted and result.c is None
    assert result.reason == "the emitter kept a runtime check that the proof does not cover"
    assert all(r.status == "proved" for r in result.proof.results)


@pytest.mark.integration
def test_unproved_obligation_of_the_released_program_overrides_an_accepted_program_with_laws() -> None:
    """Direct call of certify with unrelated `program` and `code`: no source was found whose released functions
    have an unproved obligation while the same file with its laws proves everything, so the two arguments are
    built from two files. The contract under test: the blockers of `code` refuse, whatever `program` proves."""
    proved, overflowing = load(PROVED), load(OVERFLOWING)
    assert proved.code is not None and gate.certify(proved.program, TARGET, code=proved.code).accepted
    result = gate.certify(proved.program, TARGET, level="full", code=overflowing.program)
    assert not result.accepted and result.c is None
    assert result.reason == "1 obligation(s) not proved"
    # With the three header lines, line 10 of the file is `s = s + a[i];`.
    assert [(b.kind, b.function, b.location.line, b.status) for b in result.blockers] == [
        ("overflow", "sum", 10, "failed")
    ]
    assert result.retained_traps == ()


@pytest.mark.integration
def test_released_program_accepted_at_memory_keeps_the_verdict_of_the_program_with_laws() -> None:
    """The other side of the same rule: an accepted released program changes nothing and lists its kept trap."""
    proved, overflowing = load(PROVED), load(OVERFLOWING)
    result = gate.certify(proved.program, TARGET, level="memory", code=overflowing.program)
    assert result.accepted and result.c is not None and result.blockers == ()
    assert [(d.kind, d.location.line) for d in result.retained_traps] == [("overflow", 10)]
