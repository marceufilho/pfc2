"""Mutation gaps of clauses.py: only `main` is renamed to the entry; other functions keep their own names."""

import pytest

from pfc2 import frontend
from pfc2.check import check
from pfc2.core.emit import GUARD_LINE
from pfc2.core.target import Target
from pfc2.gate import Certification, Level

TARGET = Target("test LP64 layout (no clang queried)", "x86_64-pc-linux-gnu", 32, 64)
HEADERS = '#include "pfc.h"\n#include <stdbool.h>\n\n'


def judge(text: str, level: Level = "full") -> Certification:
    """Lines of `text` are numbered from 4 in the diagnostics: three header lines come first."""
    return check(frontend.load_text(HEADERS + text, "gap.c"), TARGET, level=level)[1]


@pytest.mark.integration
@pytest.mark.parametrize("level", ["full", "memory"])
def test_main_is_verified_when_an_external_function_is_declared_after_it(level: Level) -> None:
    """The declaration after main belongs to `ext`: main keeps its body and its read of a[5] (line 7) is refused."""
    result = judge(
        """int main(void)
{
    long a[2] = {0};
    return a[5];
}

long ext(long x);
""",
        level,
    )
    assert not result.accepted and result.c is None
    assert [(b.kind, b.function, b.location.line, b.status) for b in result.blockers] == [
        ("bounds", "pfc2_main", 7, "failed")
    ]


@pytest.mark.integration
def test_function_declared_before_main_and_defined_after_it_is_one_function() -> None:
    """The prototype and the definition around main are both `helper`; its contract is checked at its entry."""
    result = judge("""long helper(long x)
    requires(x > 0);

int main(void)
{
    return 0;
}

long helper(long x)
    requires(x > 0)
{
    return x;
}
""")
    assert result.accepted and result.c is not None
    assert "long pfc2_main(void)\n{" in result.c and "long helper(long x)\n{" in result.c
    assert "_Bool pfc_entry_1 = (x > (long)0);" in result.c
    assert not GUARD_LINE.search(result.c)
    assert result.c.rstrip().endswith("int main(void) { return (int)pfc2_main(); }")
