"""Released C keeps the proved control flow, pins char signedness and never evaluates undefined entry checks."""

import re
import subprocess
from pathlib import Path

import pytest

from pfc2 import frontend, gate
from pfc2.core.config import C_FLAGS
from pfc2.core.target import Target, read_target

pytestmark = pytest.mark.integration

TARGET = Target("test LP64 layout (no clang queried)", "x86_64-pc-linux-gnu", 32, 64)
CHAR_ASSERT = '_Static_assert((char)-1 < 0, "pfc target char signedness mismatch");'
JUMP = re.compile(r"^\s*(continue;|goto pfc_next_\d+;|pfc_next_\d+:;)$", re.MULTILINE)
DRIVER = """
#include <stdio.h>
#include <stdlib.h>
long f(long n);
int main(int argc, char **argv) {
    (void)argc;
    printf("%ld\\n", f(atol(argv[1])));
    return 0;
}
"""

# Outer `while` (plain continue) around an inner `for` whose continue must still run `j++`.
WHILE_AROUND_FOR = """#include "pfc.h"

long f(long n)
    requires(0 <= n && n <= 10)
{
    long i = 0;
    long c = 0;
    while (i < n) invariant(0 <= i && i <= n && 0 <= c && c <= 100 * i) {
        i = i + 1;
        for (long j = 0; j < 5; j++) invariant(0 <= j && j <= 5) {
            if (j == 2) {
                continue;
            }
        }
        if (i == 3) {
            continue;
        }
        c = c + 1;
    }
    return c;
}
"""

# Outer `for` whose continue comes after an inner `while` with its own plain continue.
FOR_AROUND_WHILE = """#include "pfc.h"

long f(long n)
    requires(0 <= n && n <= 10)
{
    long c = 0;
    for (long i = 0; i < n; i++) invariant(0 <= i && i <= n && 0 <= c && c <= 100 * i) {
        long k = 0;
        while (k < 3) invariant(0 <= k && k <= 3) {
            k = k + 1;
            if (k == 2) {
                continue;
            }
        }
        if (i == 3) {
            continue;
        }
        c = c + 1;
    }
    return c;
}
"""

CHAR_PARAMETER = """#include "pfc.h"

long f(long n, const char s[n])
    requires(1 <= n)
{
    long x = s[0];
    return x;
}
"""

LOCAL_CHAR_ARRAY = """#include "pfc.h"

long f(long n)
{
    char s[4] = {0};
    s[0] = 'a';
    long x = s[0];
    return x;
}
"""


def certify(tmp_path: Path, source: str, target: Target = TARGET) -> gate.Certification:
    path = tmp_path / "unit.c"
    path.write_text(source, encoding="utf-8")
    unit = frontend.load(path)
    return gate.certify(unit.program, target, level="full", code=unit.code)


def entry_checks(tmp_path: Path, contract: str) -> dict[str, bool]:
    """Conjunct text -> whether the released C evaluates it at entry, for `long f(long x, long r, long y)`."""
    source = f'#include "pfc.h"\n\nlong f(long x, long r, long y)\n    {contract}\n{{\n    return x;\n}}\n'
    result = certify(tmp_path, source)
    assert result.accepted and result.c is not None
    for check in result.emission.requires_checks:
        assert (check.rendered is not None) == (check.reason is None)
        if check.rendered is not None:
            assert check.rendered in result.c
    return {check.text: check.rendered is not None for check in result.emission.requires_checks}


@pytest.mark.parametrize(
    ("source", "shape", "runs"),
    [
        # Every i in 1..n except 3 is counted; the inner `for` must reach j == 5 through its update.
        (WHILE_AROUND_FOR, ["goto", "label", "continue"], {"2": "2\n", "3": "2\n", "10": "9\n"}),
        # Every i in 0..n-1 except 3 is counted; the outer continue must still run `i++`.
        (FOR_AROUND_WHILE, ["continue", "goto", "label"], {"3": "3\n", "4": "3\n", "10": "9\n"}),
    ],
    ids=["while-around-for", "for-around-while"],
)
def test_continue_in_nested_loops_targets_its_own_loop_in_the_released_c(
    tmp_path: Path, source: str, shape: list[str], runs: dict[str, str]
) -> None:
    """A `for` continue jumps to the label before its own update; a `while` continue stays a plain continue."""
    result = certify(tmp_path, source, read_target("clang-19"))
    assert result.accepted and result.c is not None
    jumps = JUMP.findall(result.c)
    kinds = ["continue" if j == "continue;" else "goto" if j.startswith("goto") else "label" for j in jumps]
    assert kinds == shape
    goto = next(j for j in jumps if j.startswith("goto"))
    label = next(j for j in jumps if j.endswith(":;"))
    assert goto == f"goto {label[:-2]};"
    (tmp_path / "f.c").write_text(result.c, encoding="utf-8")
    (tmp_path / "main.c").write_text(DRIVER, encoding="utf-8")
    binary = tmp_path / "program"
    command = ["clang-19", *C_FLAGS, str(tmp_path / "f.c"), str(tmp_path / "main.c"), "-o", str(binary)]
    built = subprocess.run(command, capture_output=True, text=True, check=False)
    assert built.returncode == 0, built.stderr
    for argument, expected in runs.items():
        done = subprocess.run([str(binary), argument], capture_output=True, text=True, check=False, timeout=10)
        assert (done.returncode, done.stdout) == (0, expected)


@pytest.mark.parametrize(
    "source",
    [
        CHAR_PARAMETER,
        LOCAL_CHAR_ARRAY,
    ],
    ids=["char-array-parameter", "local-char-array"],
)
def test_released_c_with_a_char_array_pins_the_char_signedness_of_the_proof(tmp_path: Path, source: str) -> None:
    """The ranges proved for char cells hold only where plain char has the signedness of the proof target."""
    assert TARGET.char_signed
    result = certify(tmp_path, source)
    assert result.accepted and result.c is not None
    assert result.c.count(CHAR_ASSERT) == 1


def test_released_c_without_char_arrays_has_no_char_signedness_assertion(tmp_path: Path) -> None:
    result = certify(tmp_path, '#include "pfc.h"\n\nlong f(long n)\n{\n    return n;\n}\n')
    assert result.accepted and result.c is not None
    assert "char signedness" not in result.c


@pytest.mark.parametrize(
    ("contract", "expected"),
    [
        # x == -1, y == LONG_MIN satisfies each of these mathematically; y / x is undefined in C.
        ("requires(x != 5 && x != 0 && y / x > 0)", {"(x != 5)": True, "(x != 0)": True, "((y / x) > 0)": False}),
        ("requires(x <= 5 && x != 0 && y / x > 0)", {"(x <= 5)": True, "(x != 0)": True, "((y / x) > 0)": False}),
        ("requires(5 >= x && x != 0 && y / x > 0)", {"(5 >= x)": True, "(x != 0)": True, "((y / x) > 0)": False}),
        ("requires(r != 0 && x / r > 0)", {"(r != 0)": True, "((x / r) > 0)": False}),
        ("requires(r == 2 && x / r > 0)", {"(r == 2)": True, "((x / r) > 0)": False}),
        # A literal lower bound of at least 1 on the divisor, in any of the four spellings, makes the division defined.
        ("requires(1 <= r && x / r > 0)", {"(1 <= r)": True, "((x / r) > 0)": True}),
        ("requires(0 < r && x / r > 0)", {"(0 < r)": True, "((x / r) > 0)": True}),
        ("requires(r >= 1 && x / r > 0)", {"(r >= 1)": True, "((x / r) > 0)": True}),
        ("requires(r > 0 && x / r > 0)", {"(r > 0)": True, "((x / r) > 0)": True}),
        ("requires(x / 2 <= 50)", {"((x / 2) <= 50)": True}),
    ],
)
def test_entry_check_divides_only_by_a_divisor_bounded_below_by_one(
    tmp_path: Path, contract: str, expected: dict[str, bool]
) -> None:
    assert entry_checks(tmp_path, contract) == expected


def test_entry_check_never_negates_a_variable_but_renders_a_negated_literal(tmp_path: Path) -> None:
    """-x is undefined in C for LONG_MIN, which satisfies -x > 5 mathematically; -5 is a constant."""
    found = entry_checks(tmp_path, "requires(-x > 5)\n    requires(-5 <= r)\n    requires(!(y == 7))")
    assert found == {"((-x) > 5)": False, "((-5) <= r)": True, "(!(y == 7))": True}
