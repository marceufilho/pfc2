"""The semantics PFC2 added to the core, each as a program that must certify and a neighbour that must not.

Verdicts are derived by reading the programs. A pair differs in one line, named in the case.
"""

from pathlib import Path

import pytest

from pfc2 import frontend
from pfc2.check import check
from pfc2.core.target import Target
from pfc2.elaborate import Unit
from pfc2.gate import Certification

TARGET = Target("static LP64 layout (test)", "x86_64-pc-linux-gnu", 32, 64)
pytestmark = pytest.mark.integration

GLOBAL_LOOP = """long total = 0;
long add_all(long n)
    requires(0 <= n && n <= 100)
    requires(total == 0)
    ensures(total == n)
{
    for (long i = 0; i < n; i++) INVARIANT {
        total++;
    }
    return total;
}
"""
TWO_LEVELS = """long hits = 0;
long other = 7;
long inc(void)
    requires(hits < 1000)
{
    hits++;
    return hits;
}
long mid(void)
    requires(hits < 1000)
{
    return inc();
}
long top(void)
    requires(hits < 1000)
{
    long before = WATCHED;
    mid();
    assert(WATCHED == before);
    return 0;
}
"""
EXTERNAL_ARRAY = """long touch(long n, QUALIFIER long a[n]);
long use(long n, long a[n])
    requires(n > 0)
{
    a[0] = 1;
    touch(n, a);
    assert(a[0] == 1);
    return 0;
}
"""
NESTED = """long grid(long n)
    requires(0 <= n && n <= 100)
{
    long c = 0;
    for (long i = 0; i < n; i++) decreases(n - i) {
        for (long j = 0; j < n; j++) decreases(MEASURE) {
            c = j;
        }
    }
    return c;
}
"""
EARLY_RETURN = """long find(long n, const long a[n], long key)
    ensures(-1 <= result && result < n)
{
    long i = 0;
    while (i < n) decreases(MEASURE) {
        if (a[i] == key) {
            return i;
        }
        i++;
    }
    return -1;
}
"""
MIXED = """long twice(long n)
    requires(0 <= n && n <= 1000)
    ensures(result == 2 * n)
{
    long s = 0;
    long i where(0 <= i) = 0;
    while (i < n) INVARIANT {
        s += 2;
        i++;
    }
    return s;
}
"""
NESTED_INFERENCE = """long last(long n, const long a[n])
{
    long s = 0;
    for (long i = 0; i < n; i++) {
        for (long j = 0; j BOUND; j++) {
            s = a[j];
        }
    }
    return s;
}
"""
CALL_ORDER = """long g = 0;
long bump(void)
    ensures(g == 5)
    ensures(result == 1)
{
    g = 5;
    return 1;
}
long f(void)
{
    g = 0;
    long r = bump() + g;
    assert(r == EXPECTED);
    return r;
}
"""
BOOL_GLOBAL = """_Bool on = 0;
long toggle(void)
    ensures(ENSURED)
{
    if (on) {
        on = 0;
        return 0;
    }
    on = 1;
    return 1;
}
"""
CONSTANT = """#define LIMIT 100
long clamp(long n)
    requires(0 <= n && n <= LIMIT)
    ensures(result <= CEILING)
{
    return n;
}
"""
CASES = [
    ("a loop that writes a global needs an invariant about it", GLOBAL_LOOP, "INVARIANT", "invariant(total == i)", ""),
    ("a caller keeps a global its callees never write, two levels down", TWO_LEVELS, "WATCHED", "other", "hits"),
    ("a declared function may write a non-const array it is given", EXTERNAL_ARRAY, "QUALIFIER", "const", ""),
    ("both loops of a nest terminate", NESTED, "MEASURE", "n - j", "j"),
    ("a loop with an early return terminates", EARLY_RETURN, "MEASURE", "n - i", "i"),
    ("inferred bounds join a written invariant and a typed counter", MIXED, "INVARIANT", "invariant(s == 2 * i)", ""),
    ("both loops of a nest get their bounds", NESTED_INFERENCE, "BOUND", "< n", "<= n"),
    ("a call is evaluated before the global it writes is read", CALL_ORDER, "EXPECTED", "6", "1"),
    ("a _Bool global", BOOL_GLOBAL, "ENSURED", "result == 0 || result == 1", "result == 1"),
    ("a #define constant in a contract", CONSTANT, "CEILING", "LIMIT", "50"),
]


def _check(tmp_path: Path, body: str) -> tuple[Unit, Certification]:
    source = tmp_path / "t.c"
    source.write_text('#include "pfc.h"\n' + body, encoding="utf-8")
    return check(frontend.load(source), TARGET)


@pytest.mark.parametrize(("claim", "template", "hole", "good", "bad"), CASES, ids=[case[0] for case in CASES])
def test_the_program_certifies_and_its_neighbour_is_refused(
    tmp_path: Path, claim: str, template: str, hole: str, good: str, bad: str
) -> None:
    assert template.count(hole) >= 1
    accepted = _check(tmp_path, template.replace(hole, good))[1]
    assert accepted.accepted and accepted.c is not None, accepted.reason
    refused = _check(tmp_path, template.replace(hole, bad))[1]
    assert not refused.accepted and refused.c is None


def test_details_the_pairs_do_not_show(tmp_path: Path) -> None:
    nested, _ = _check(tmp_path, NESTED.replace("MEASURE", "n - j"))
    assert [m.predicate for m in nested.measures] == ["n - i", "n - j"] and nested.loops == 2
    inferred, _ = _check(tmp_path, NESTED_INFERENCE.replace("BOUND", "< n"))
    assert [i.invariant for i in inferred.inferred] == ["((0 <= i) && (i <= n))", "((0 <= j) && (j <= n))"]
    mixed, _ = _check(tmp_path, MIXED.replace("INVARIANT", "invariant(s == 2 * i)"))
    assert [i.invariant for i in mixed.inferred] == ["((0 <= i) && (i <= n))"]
    unit, certification = _check(tmp_path, CALL_ORDER.replace("EXPECTED", "6"))
    assert certification.c is not None
    call, read = certification.c.index("= bump();"), certification.c.index("+ g)")
    assert call < read  # The emitted C fixes the order the proof used.
