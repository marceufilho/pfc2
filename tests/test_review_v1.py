"""Findings of the independent review of the language growth (2026-11-18, decision 0065), kept as tests.

Expectations come from C11 and from what each program does when run, not from the tool.
"""

import pytest

from pfc2 import frontend
from pfc2.check import check
from pfc2.core.diagnostics import FrontendError
from pfc2.core.target import Target
from pfc2.elaborate import Unit
from pfc2.gate import Certification

TARGET = Target("static LP64 layout (test)", "x86_64-pc-linux-gnu", 32, 64)
HEADER = '#include "pfc.h"\n'


def certify(text: str, level: str = "full") -> tuple[Unit, Certification]:
    return check(frontend.load_text(HEADER + text, "t.c"), TARGET, level=level)  # type: ignore[arg-type]


def refused(text: str) -> str:
    with pytest.raises(FrontendError) as error:
        certify(text)
    return error.value.diagnostic.rule


# 2. Termination ------------------------------------------------------------------------------------------------
OUTER = (
    "long f(long n)\n    requires(0 <= n && n <= 100)\n{\n    long i = n;\n"
    "    while (i > 0) invariant(0 <= i) decreases(i) {\n        long k = 0;\n"
    "        while (k < 1) invariant(0 <= k && k <= 1)INNER {\n            k = k + STEP;\n        }\n"
    "        i--;\n    }\n    return i;\n}\n"
)


def test_a_loop_is_proved_to_terminate_only_if_everything_inside_it_is() -> None:
    # With STEP 0 the inner loop never ends, so the outer loop does not either, whatever its measure says.
    stuck = certify(OUTER.replace("INNER", "").replace("STEP", "0"))[0]
    assert stuck.measures == ()
    both = certify(OUTER.replace("INNER", " decreases(1 - k)").replace("STEP", "1"))
    assert both[1].accepted and len(both[0].measures) == 2
    inner_only = certify(OUTER.replace("INNER", " decreases(1 - k)").replace("STEP", "1").replace(" decreases(i)", ""))
    assert len(inner_only[0].measures) == 1


def test_a_call_to_a_function_with_an_unmeasured_loop_does_not_count_as_terminating() -> None:
    spin = "long spin(long x)\n{\n    while (x != 0) {\n        x = x + 0;\n    }\n    return x;\n}\n"
    caller = (
        "long g(long n)\n    requires(0 <= n && n <= 100)\n{\n    long i = n;\n"
        "    while (i > 0) invariant(0 <= i) decreases(i) {\n        long r = spin(i);\n        i--;\n    }\n"
        "    return i;\n}\n"
    )
    assert certify(spin + caller)[0].measures == ()
    done = "long spin(long x)\n{\n    return x;\n}\n"
    assert len(certify(done + caller)[0].measures) == 1


# 3. Trigraphs --------------------------------------------------------------------------------------------------
def test_trigraphs_are_refused_because_c11_compilers_replace_them() -> None:
    # "??/n" is the two characters `\n` to a C11 compiler: one newline, not four characters.
    text = 'long f(void)\n{\n    char w[5] = "??/n";\n    return w[0];\n}\n'
    assert refused(text) == "preprocess-unsupported"


# 4. A unary operator on the left of a chain -------------------------------------------------------------------
@pytest.mark.parametrize("expression", ["-(a - b) - c", "-(a + b) + c", "!(a + b) + c", "-(a / b) / c"])
def test_a_unary_operator_does_not_hide_an_operation_of_the_same_kind(expression: str) -> None:
    text = (
        "long f(long a, long b, long c)\n"
        "    requires(1 <= a && a <= 9 && 1 <= b && b <= 9 && 1 <= c && c <= 9)\n"
        f"{{\n    return {expression};\n}}\n"
    )
    assert certify(text)[1].accepted


# 5. and 6. Clean refusals --------------------------------------------------------------------------------------
def test_an_update_that_needs_a_temporary_is_refused_with_its_own_rule() -> None:
    text = (
        "long f(long n, long a[n])\n{\n    for (long i = 0; i < n - 1; a[i + 1]++) {\n        i++;\n    }\n"
        "    return 0;\n}\n"
    )
    assert refused(text) == "subset-for-update"


def test_a_local_array_initial_value_that_is_not_a_literal_is_refused_not_crashed_on() -> None:
    assert refused("long f(_Bool b)\n{\n    long t[1] = {-b};\n    return t[0];\n}\n") == "subset-local-array"


# 7. Types that mention an array ------------------------------------------------------------------------------
def test_a_typed_local_that_mentions_an_array_is_checked_again_after_a_call_that_may_write_it() -> None:
    text = (
        "long w(long n, long a[n])\n    requires(1 <= n)\n{\n    a[0] = 7;\n    return 0;\n}\n"
        "long f(long n, long a[n])\n    requires(1 <= n && a[0] == 1)\n{\n"
        "    long x where(x == a[0]) = a[0];\n    long r = w(n, a);\n    return x + r;\n}\n"
    )
    certification = certify(text)[1]
    assert not certification.accepted and "assert" in [b.kind for b in certification.blockers]


# 8. Size -------------------------------------------------------------------------------------------------------
def test_a_function_with_many_array_statements_is_within_the_formula_limit() -> None:
    body = "".join(f"    a[{i}] = a[{i}] + 1;\n" for i in range(24))
    text = f"long f(long n, long a[n])\n    requires(n == 24)\n{{\n{body}    return 0;\n}}\n"
    assert certify(text, "memory")[1].accepted
