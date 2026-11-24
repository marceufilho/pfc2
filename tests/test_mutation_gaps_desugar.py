"""Mutation gaps of core/desugar.py: an unbraced sub-statement that needs one temporary keeps its statement."""

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


UNBRACED = """long id(long x)
    ensures(result == x)
{{
    return x;
}}

long h(long n, long a[n], long i)
    requires({requires})
{{
    if (i >= 0) a[i] = id(i) + 0;
    return 0;
}}
"""


@pytest.mark.integration
@pytest.mark.parametrize("level", ["full", "memory"])
def test_unbraced_write_with_a_lifted_call_is_still_checked_and_refused_when_its_index_is_unbounded(
    level: Level,
) -> None:
    """Lifting `id(i)` makes two statements out of the unbraced one; the write a[i] (line 13) must stay judged."""
    result = judge(UNBRACED.format(requires="0 <= i"), level)
    assert not result.accepted and result.c is None
    assert [(b.kind, b.function, b.location.line, b.status) for b in result.blockers] == [("bounds", "h", 13, "failed")]


@pytest.mark.integration
def test_unbraced_write_with_a_lifted_call_is_released_inside_its_branch() -> None:
    result = judge(UNBRACED.format(requires="0 <= i && i < n"))
    assert result.accepted and result.c is not None
    body = result.c[result.c.index("long h(long n, long a[], long i)\n{") :]
    branch = body[body.index("if (") : body.index("return")]
    assert "id(i)" in branch and "a[i] = " in branch
    assert [(d.kind, d.removed) for d in result.emission.decisions] == [("bounds", True)]
