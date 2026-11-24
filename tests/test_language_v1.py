"""Language growth before the first freeze: each feature with a certifying program and a refused neighbour.

Expectations are derived from C11 semantics by hand, never from the tool's output.
"""

import shutil
import subprocess
from pathlib import Path

import pytest

from pfc2 import frontend
from pfc2.check import check
from pfc2.core.diagnostics import FrontendError
from pfc2.core.target import Target
from pfc2.elaborate import Unit
from pfc2.gate import Certification

TARGET = Target("static LP64 layout (test)", "x86_64-pc-linux-gnu", 32, 64)
HEADER = '#include "pfc.h"\n'
INCLUDE = Path(__file__).resolve().parents[1] / "pfc2" / "include"
CLANG = shutil.which("clang-19") or shutil.which("clang")


def certify(text: str, level: str = "full") -> tuple[Unit, Certification]:
    return check(frontend.load_text(HEADER + text, "t.c"), TARGET, level=level)  # type: ignore[arg-type]


def accepted(text: str, level: str = "full") -> bool:
    return certify(text, level)[1].accepted


def blockers(text: str, level: str = "full") -> list[str]:
    certification = certify(text, level)[1]
    assert not certification.accepted
    return sorted({b.kind for b in certification.blockers if not b.status.startswith("depends")})


def refused(text: str) -> str:
    with pytest.raises(FrontendError) as error:
        certify(text)
    return error.value.diagnostic.rule


def run(text: str, driver: str, tmp_path: Path, level: str = "full") -> tuple[str, str]:
    """Output of the certified C and of the source compiled as plain C, with the same driver."""
    assert CLANG is not None
    certification = certify(text, level)[1]
    assert certification.accepted and certification.c is not None, certification.reason
    outputs = []
    for name, unit, flags in (("certified", certification.c, []), ("plain", HEADER + text, [f"-I{INCLUDE}"])):
        source = tmp_path / f"{name}.c"
        source.write_text(unit + "\n#include <stdio.h>\n" + driver, encoding="utf-8")
        binary = tmp_path / name
        subprocess.run(
            [CLANG, "-std=c11", "-O1", "-fsanitize=address,undefined", "-fno-sanitize-recover=all", *flags]
            + [str(source), "-o", str(binary)],
            check=True,
            capture_output=True,
            timeout=120,
        )
        outputs.append(subprocess.run([str(binary)], capture_output=True, text=True, timeout=60, check=True).stdout)
    return outputs[0], outputs[1]


RANGE = "    requires(1 <= a && a <= 100 && 1 <= b && b <= 100 && 1 <= c && c <= 100)\n"


def chained(expression: str, contract: str = RANGE) -> str:
    return f"long f(long a, long b, long c)\n{contract}{{\n    return {expression};\n}}\n"


# Chained operators -----------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "expression", ["a + b + c", "a / b / c", "a + b - c + a", "a * b * c * a", "a - b - c - a - b", "a + b + (c + a)"]
)
def test_operators_of_the_same_kind_in_one_expression_are_separate_checks(expression: str) -> None:
    assert accepted(chained(expression))


def test_each_operator_of_a_chain_is_still_checked_on_its_own() -> None:
    # c may be 0: only the second division is wrong, and it is the one reported.
    loose = RANGE.replace("1 <= c", "0 <= c")
    assert blockers(chained("a / b / c", loose)) == ["division"]
    # a + b fits, the sum of three may not: 3 * (2^62) exceeds a long.
    wide = "    requires(0 <= a && a <= 4611686018427387904 && a == b && b == c)\n"
    assert blockers(chained("a + b + c", wide)) == ["overflow"]
    assert accepted(chained("a + b + c", wide), "memory")


@pytest.mark.integration
def test_a_chain_computes_what_c_computes(tmp_path: Path) -> None:
    driver = 'int main(void) { printf("%ld\\n", f(7, 3, 2)); return 0; }\n'
    assert run(chained("a - b - c + a * b * c / b / c"), driver, tmp_path) == ("9\n", "9\n")  # 7-3-2 + 42/3/2


# Remainder -------------------------------------------------------------------------------------------------
# C11 6.5.5: a / b truncates toward zero and (a / b) * b + a % b == a, so a % b has the sign of a (or is 0).
# Both are undefined when b == 0 and when the quotient is not representable (LONG_MIN / -1).
REMAINDER = (
    "long rem(long a, long b)\n    requires(b != 0 && b != -1)\n    ensures(a == (a / b) * b + result)\n"
    "    ensures((a >= 0 && result >= 0) || (a < 0 && result <= 0))\n"
    "    ensures((b > 0 && result < b && -b < result) || (b < 0 && result < -b && b < result))\n"
    "{\n    return a % b;\n}\n"
)


def test_remainder_is_c_remainder_truncating_toward_zero() -> None:
    assert accepted(REMAINDER)
    # b may be 0: the operation is undefined, and no result lies strictly between -0 and 0 either.
    assert blockers(REMAINDER.replace("b != 0 && b != -1", "b != -1")) == ["division", "postcondition"]
    assert blockers(REMAINDER.replace("b != 0 && b != -1", "b != 0")) == ["division"]  # LONG_MIN % -1.
    floored = REMAINDER.replace("(a >= 0 && result >= 0) || (a < 0 && result <= 0)", "result >= 0 || b < 0")
    assert blockers(floored) == ["postcondition"]  # -7 % 2 is -1 in C, not 1.


@pytest.mark.integration
def test_remainder_runs_as_in_plain_c(tmp_path: Path) -> None:
    driver = (
        'int main(void) { printf("%ld %ld %ld %ld\\n", rem(7, 2), rem(-7, 2), rem(7, -2), rem(-7, -2)); return 0; }\n'
    )
    assert run(REMAINDER, driver, tmp_path) == ("1 -1 1 -1\n", "1 -1 1 -1\n")


def test_a_remainder_by_a_positive_number_keeps_an_index_inside_its_array() -> None:
    ring = (
        "long next(long n, long head)\n    requires(1 <= n && 0 <= head && head < n)\n"
        "    ensures(0 <= result && result < n)\n{\n    return (head + 1) % n;\n}\n"
        "long peek(long n, const long a[n], long k)\n    requires(1 <= n && 0 <= k)\n{\n    return a[k % n];\n}\n"
    )
    assert accepted(ring)
    assert blockers(ring.replace("requires(1 <= n && 0 <= k)", "requires(1 <= n)")) == ["bounds"]  # k < 0.


def test_remainder_assignment_and_euclid_with_a_proved_measure() -> None:
    gcd = (
        "long gcd(long a, long b)\n    requires(0 <= a && 0 <= b)\n    ensures(0 <= result)\n{\n"
        "    while (b != 0) invariant(0 <= a && 0 <= b) decreases(b) {\n"
        "        long t = b;\n        a %= b;\n        b = a;\n        a = t;\n    }\n    return a;\n}\n"
    )
    unit, certification = certify(gcd)
    assert certification.accepted and len(unit.measures) == 1
    # Without the invariant nothing says b stays non-negative, so the measure is not proved.
    assert not accepted(gcd.replace(" invariant(0 <= a && 0 <= b)", ""))


def test_a_remainder_in_requires_is_checked_at_entry() -> None:
    even = "long half(long n)\n    requires(n % 2 == 0)\n    ensures(result + result == n)\n{\n    return n / 2;\n}\n"
    certification = certify(even)[1]
    assert certification.accepted and certification.c is not None
    assert "((n % 2) == 0)" in certification.c.replace("(long)", "")


# break and continue ----------------------------------------------------------------------------------------
FIND = (
    "long find(long n, const long a[n], long key)\n"
    "    ensures(result == -1 || (0 <= result && result < n && a[result] == key))\n{\n    long found = -1;\n"
    "    for (long i = 0; i < n; i++) invariant(found == -1) {\n"
    "        if (a[i] == key) {\n            found = i;\n            break;\n        }\n    }\n    return found;\n}\n"
)
POSITIVES = (
    "long positives(long n, const long a[n])\n    ensures(0 <= result && result <= n)\n{\n    long c = 0;\n"
    "    for (long i = 0; i < n; i++) invariant(0 <= c && c <= i) {\n"
    "        if (a[i] <= 0) {\n            continue;\n        }\n        c++;\n    }\n    return c;\n}\n"
)
# The update of a `for` runs after `continue` (C11 6.8.6.2): s == i survives only because i++ still happens.
STEPS = (
    "long steps(long n)\n    requires(0 <= n && n <= 1000)\n    ensures(result == n)\n{\n    long s = 0;\n"
    "    for (long i = 0; i < n; i++) invariant(s == i) {\n        s++;\n"
    "        if (s > 5) {\n            continue;\n        }\n        s = s + 0;\n    }\n    return s;\n}\n"
)


def test_break_leaves_the_loop_with_what_was_true_at_the_break() -> None:
    assert accepted(FIND)
    # The state at the break is what the code after the loop sees: a wrong index stored there is noticed.
    assert blockers(FIND.replace("found = i;", "found = i + 1;")) == ["postcondition"]
    forever = (
        "long f(void)\n    ensures(result == 10)\n{\n    long i = 0;\n    while (1) invariant(0 <= i && i <= 10) {\n"
    )
    forever += "        if (i == 10) {\n            break;\n        }\n        i++;\n    }\n    return i;\n}\n"
    assert accepted(forever)
    assert blockers(forever.replace("result == 10", "result == 9")) == ["postcondition"]


def test_continue_goes_to_the_update_of_a_for_and_must_keep_the_invariant() -> None:
    assert accepted(POSITIVES)
    assert accepted(STEPS)
    skipped = STEPS.replace("        s++;\n", "").replace("        s = s + 0;\n", "        s++;\n")
    assert blockers(skipped) == ["preservation"]  # On the continue path s stays while i grows.


def test_break_and_continue_belong_to_the_innermost_loop() -> None:
    nested = (
        "long f(long n)\n    requires(0 <= n && n <= 10)\n    ensures(result == n)\n{\n    long c = 0;\n"
        "    for (long i = 0; i < n; i++) invariant(c == i) {\n        for (long j = 0; j < 3; j++) {\n"
        "            break;\n        }\n        c++;\n    }\n    return c;\n}\n"
    )
    assert accepted(nested)
    assert blockers(nested.replace("result == n", "result == 0")) == ["postcondition"]
    assert refused("long f(long n)\n{\n    break;\n    return n;\n}\n") == "subset-break"
    assert (
        refused("long f(long n)\n{\n    if (n > 0) {\n        continue;\n    }\n    return n;\n}\n") == "subset-break"
    )


def test_a_measure_is_not_claimed_for_a_loop_that_continue_can_restart_without_progress() -> None:
    spin = (
        "long f(long n, const long a[n])\n{\n    long i = 0;\n    while (i < n) DECREASES {\n"
        "        if (a[i] == 0) {\n            continue;\n        }\n        i++;\n    }\n    return i;\n}\n"
    )
    assert accepted(spin.replace(" DECREASES", ""))  # What it computes if it ends; it may not end.
    assert refused(spin.replace("DECREASES", "decreases(n - i)")) == "decreases-continue"


@pytest.mark.integration
def test_break_and_continue_run_as_in_plain_c(tmp_path: Path) -> None:
    driver = (
        "int main(void) {\n    long a[6] = {3, -1, 0, 7, -2, 9};\n"
        '    printf("%ld %ld %ld %ld\\n", find(6, a, 7), find(6, a, 8), positives(6, a), steps(9));\n    return 0;\n}\n'
    )
    assert run(FIND + POSITIVES + STEPS, driver, tmp_path) == ("3 -1 3 9\n", "3 -1 3 9\n")


# Local arrays ----------------------------------------------------------------------------------------------
# C11 6.7.9p21: elements without an initializer in a braced list are zero. 6.2.4: a new automatic object does
# not overlap any object that already exists.
BUFFER = (
    "long twice(long x)\n    requires(0 <= x && x <= 100)\n    ensures(result == x + x)\n{\n"
    "    long buf[4] = {0};\n    buf[0] = x;\n    buf[3] = x;\n    return buf[0] + buf[3];\n}\n"
)
DAYS = (
    "long days(long month)\n    requires(1 <= month && month <= 12)\n    ensures(28 <= result && result <= 31)\n{\n"
    "    const long table[12] = {31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};\n    return table[month - 1];\n}\n"
)


def test_a_local_array_has_its_declared_length_and_initial_contents() -> None:
    assert accepted(BUFFER)
    assert blockers(BUFFER.replace("buf[3] = x;", "buf[4] = x;").replace("buf[0] + buf[3]", "buf[0] + buf[0]")) == [
        "bounds"
    ]
    zero = "long z(void)\n    ensures(result == 0)\n{\n    long buf[4] = {7};\n    return buf[3];\n}\n"
    assert accepted(zero)  # Elements after the listed ones are zero.
    assert blockers(zero.replace("buf[3]", "buf[0]")) == ["postcondition"]  # The listed one is 7.
    assert accepted(DAYS)
    assert blockers(DAYS.replace("28 <= result", "29 <= result")) == ["postcondition"]  # February.
    # December would read past the table, and nothing is known about what is there.
    assert blockers(DAYS.replace("table[month - 1]", "table[month]")) == ["bounds", "postcondition"]


def test_a_local_array_is_a_new_object_separate_from_every_other_array() -> None:
    kept = (
        "long g(long n, long a[n])\n    requires(1 <= n)\n    ensures(result == 7 && a[0] == 7)\n{\n"
        "    long t[2] = {0};\n    long u[2] = {0};\n    a[0] = 7;\n    t[0] = 1;\n    u[0] = 2;\n    t[1] = a[0];\n"
        "    return t[1] + u[0] - t[0] - 1;\n}\n"
    )
    assert accepted(kept)
    assert blockers(kept.replace("result == 7 &&", "result == 8 &&")) == ["postcondition"]


def test_a_local_array_can_be_passed_and_a_callee_buffer_does_not_disturb_the_caller() -> None:
    callee = (
        "long put(long n, long a[n])\n    requires(n == 2)\n    ensures(a[0] == 5 && result == 0)\n{\n"
        "    a[0] = 5;\n    return 0;\n}\n"
    )
    caller = "long use(void)\n    ensures(result == 5)\n{\n    long t[2] = {0};\n    put(2, t);\n    return t[0];\n}\n"
    assert accepted(callee + caller)
    longer = callee.replace("requires(n == 2)", "requires(n == 3)") + caller.replace("put(2, t)", "put(3, t)")
    assert blockers(longer) == ["call-precondition"]  # t has two elements, not three.
    scratch = (
        "long scratch(long x)\n    requires(0 <= x && x <= 9)\n    ensures(result == x)\n{\n"
        "    long s[1] = {0};\n    s[0] = x;\n    return s[0];\n}\n"
        "long h(long n, long a[n])\n    requires(1 <= n)\n    ensures(result == 3)\n{\n"
        "    a[0] = 3;\n    long y = scratch(1);\n    return a[0] + y - 1;\n}\n"
    )
    assert accepted(scratch)


@pytest.mark.parametrize(
    ("declaration", "rule"),
    [
        ("long b[n] = {0};", "subset-local-array"),  # The length is a literal, not a variable.
        ("long b[4];", "subset-local-array"),  # Without an initializer the contents would be indeterminate.
        ("long b[0] = {0};", "subset-local-array"),
        ("long b[2] = {1, 2, 3};", "subset-local-array"),
        ("long b[2] = {n};", "subset-local-array"),  # Initial values are literals.
        ("long b[100000000] = {0};", "subset-local-array"),
    ],
)
def test_local_array_declarations_outside_the_supported_form_are_refused(declaration: str, rule: str) -> None:
    assert refused(f"long f(long n)\n{{\n    {declaration}\n    return n;\n}}\n") == rule


def test_a_const_local_array_cannot_be_written() -> None:
    assert refused(DAYS.replace("    return table", "    table[0] = 1;\n    return table")) == "ir-const"


@pytest.mark.integration
def test_local_arrays_run_as_in_plain_c(tmp_path: Path) -> None:
    driver = 'int main(void) { printf("%ld %ld %ld\\n", twice(21), days(2), days(12)); return 0; }\n'
    assert run(BUFFER + DAYS, driver, tmp_path) == ("42 28 31\n", "42 28 31\n")


# char and int elements -------------------------------------------------------------------------------------
# On the test target `char` is signed and 8 bits wide, `int` is 32 bits. C11 6.3.1.1: a char or int element
# read in an expression is promoted to int, which changes no value. 6.3.1.3p3: storing a value the element
# type cannot represent is implementation-defined, so PFC2 requires a proof that it fits.
COUNT = (
    "long count(long n, const char s[n], long c)\n    ensures(0 <= result && result <= n)\n{\n    long k = 0;\n"
    "    for (long i = 0; i < n; i++) invariant(0 <= k && k <= i) {\n"
    "        if (s[i] == c) {\n            k++;\n        }\n    }\n    return k;\n}\n"
)
DIGIT = (
    "long digit(long n, const char s[n], long i)\n    requires(0 <= i && i < n && '0' <= s[i] && s[i] <= '9')\n"
    "    ensures(0 <= result && result <= 9)\n{\n    return s[i] - '0';\n}\n"
)
UPPER = (
    "long upper(long n, char s[n])\n    requires(1 <= n && 'a' <= s[0] && s[0] <= 'z')\n"
    "    ensures('A' <= s[0] && s[0] <= 'Z')\n{\n    s[0] = s[0] - 32;\n    return 0;\n}\n"
)
PUT = (
    "long put(long n, TYPE s[n], long v)\n    requires(1 <= n RANGE)\n"
    "    ensures(s[0] == v)\n{\n    s[0] = v;\n    return 0;\n}\n"
)


def test_char_elements_are_read_as_small_integers() -> None:
    assert accepted(COUNT)
    assert accepted(DIGIT)
    assert blockers(DIGIT.replace("result <= 9", "result <= 8")) == ["postcondition"]  # '9' - '0' is 9.
    read = "long first(long n, const char s[n])\n    requires(1 <= n)\n    ensures(RANGE)\n{\n    return s[0];\n}\n"
    assert accepted(read.replace("RANGE", "-128 <= result && result <= 127"))
    assert blockers(read.replace("RANGE", "0 <= result")) == ["postcondition"]  # A signed char may be negative.
    assert accepted(UPPER)


@pytest.mark.parametrize(
    ("type_", "fits", "too_wide"),
    [
        ("char", "-128 <= v && v <= 127", "0 <= v && v <= 255"),
        ("int", "-2147483648 <= v && v <= 2147483647", "0 <= v && v <= 2147483648"),
    ],
)
def test_a_value_stored_in_a_narrower_element_must_be_proved_to_fit(type_: str, fits: str, too_wide: str) -> None:
    put = PUT.replace("TYPE", type_)
    assert accepted(put.replace("RANGE", f"&& {fits}"))
    assert blockers(put.replace("RANGE", f"&& {too_wide}")) == ["conversion"]
    assert blockers(put.replace("RANGE", "")) == ["conversion"]
    assert blockers(put.replace("RANGE", ""), "memory") == ["conversion"]  # Not an overflow trap: always required.


def test_int_elements_follow_int_arithmetic() -> None:
    wide = (
        "long sum(long n, const int a[n])\n    requires(n == 2)\n{\n"
        "    long x = a[0];\n    long y = a[1];\n    return x + y;\n}\n"
    )
    assert accepted(wide)  # Two 32-bit values always fit a 64-bit sum.
    narrow = "long sum(long n, const int a[n])\n    requires(n == 2)\n{\n    return a[0] + a[1];\n}\n"
    assert blockers(narrow) == ["overflow"]  # int + int is computed as int.
    assert accepted(narrow, "memory")


def test_character_constants_and_string_initializers() -> None:
    word = 'long f(void)\n    ensures(result == EXPECTED)\n{\n    const char w[6] = "hello";\n    return w[INDEX];\n}\n'
    assert accepted(word.replace("EXPECTED", "'o'").replace("INDEX", "4"))
    assert accepted(word.replace("EXPECTED", "0").replace("INDEX", "5"))  # The terminating zero.
    assert blockers(word.replace("EXPECTED", "'l'").replace("INDEX", "1")) == ["postcondition"]  # It is 'e'.
    escapes = (
        "long f(void)\n    ensures(result == 10 + 9 + 0 + 92 + 39)\n"
        "{\n    return '\\n' + '\\t' + '\\0' + '\\\\' + '\\'';\n}\n"
    )
    assert accepted(escapes)
    assert accepted("long f(void)\n    ensures(result == 97)\n{\n    return 'a';\n}\n")


@pytest.mark.parametrize(
    ("body", "rule"),
    [
        ("int x = 0;\n    return x;", "ir-type"),  # Variables are long or _Bool; only elements may be narrower.
        ("char c = 'a';\n    return c;", "ir-type"),
        ("return 'ab';", "subset-literal"),
        ('char w[3] = "hello";\n    return w[0];', "subset-local-array"),
        ("char w[2] = {200};\n    return w[0];", "subset-local-array"),  # 200 is not a char on every target.
        ("_Bool b[2] = {5};\n    return b[0];", "subset-local-array"),
    ],
)
def test_narrow_types_outside_the_supported_forms_are_refused(body: str, rule: str) -> None:
    assert refused(f"long f(void)\n{{\n    {body}\n}}\n") == rule


def test_unsigned_elements_are_refused() -> None:
    assert refused("long f(long n, const unsigned char s[n])\n{\n    return n;\n}\n") == "subset-type"


def test_on_a_target_with_unsigned_char_a_char_is_never_negative() -> None:
    read = (
        "long first(long n, const char s[n])\n    requires(1 <= n)\n"
        "    ensures(0 <= result && result <= 255)\n{\n    return s[0];\n}\n"
    )
    unsigned = Target("static AArch64 layout (test)", "aarch64-unknown-linux-gnu", 32, 64, char_signed=False)
    assert check(frontend.load_text(HEADER + read, "t.c"), unsigned)[1].accepted
    assert not check(frontend.load_text(HEADER + read, "t.c"), TARGET)[1].accepted


@pytest.mark.integration
def test_char_and_int_elements_run_as_in_plain_c(tmp_path: Path) -> None:
    driver = (
        'int main(void) {\n    char s[6] = "a1b1c";\n    int v[2] = {2147483647, 1};\n'
        "    printf(\"%ld %ld \", count(5, s, '1'), digit(5, s, 1));\n    upper(5, s);\n"
        '    printf("%c %ld\\n", s[0], sum(2, v));\n    return 0;\n}\n'
    )
    wide = (
        "long sum(long n, const int a[n])\n    requires(n == 2)\n{\n"
        "    long x = a[0];\n    long y = a[1];\n    return x + y;\n}\n"
    )
    assert run(COUNT + DIGIT + UPPER + wide, driver, tmp_path) == ("2 1 A 2147483648\n", "2 1 A 2147483648\n")


def test_a_string_assigned_to_an_array_element_is_still_a_text_handle() -> None:
    # Only `char name[N] = "..."` makes a string an array's contents; elsewhere a string is an opaque text value.
    text = (
        '#include "pfc_rt.h"\nlong f(long n, long names[n])\n    requires(1 <= n)\n{\n'
        '    names[0] = "first";\n    return 0;\n}\n'
    )
    unit, certification = certify(text)
    assert certification.accepted and len(unit.strings) == 1
