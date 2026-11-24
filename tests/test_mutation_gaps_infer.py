"""Mutation gaps of infer.py: inferred loop bounds are added to a written invariant, never put in its place."""

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


COUNT = """long count(long n)
    requires(0 <= n)
    ensures(result == n)
{{
    long i = 0;

    while (i < n)
        invariant({invariant})
    {{
        i++;
    }}
    return i;
}}
"""


@pytest.mark.integration
@pytest.mark.parametrize("level", ["full", "memory"])
def test_written_false_invariant_is_refused_even_when_bounds_are_inferred_for_its_loop(level: Level) -> None:
    """`invariant(0)` is a false claim of the source: it fails when the loop starts (line 11, n = 0, i = 0)."""
    result = judge(COUNT.format(invariant="0"), level)
    assert not result.accepted and result.c is None
    first = result.blockers[0]
    assert (first.kind, first.function, first.location.line, first.status) == ("entry", "count", 11, "failed")
    assert first.counterexample is not None


@pytest.mark.integration
@pytest.mark.parametrize("invariant", ["1", "0 <= i", "i <= n"])
def test_written_true_invariant_is_kept_and_the_counting_loop_is_certified(invariant: str) -> None:
    """Each of these is too weak alone for `result == n`; the inferred counter bounds supply the rest."""
    result = judge(COUNT.format(invariant=invariant))
    assert result.accepted and result.blockers == () and result.c is not None
