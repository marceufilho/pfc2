"""Behaviour of the verification-condition generator that the mutation campaign found unobserved (real Z3).

Every expectation is derived by hand from the C meaning of the program: what a value is at run time, which state
reaches a statement, and which formula would be false there. Nothing is computed with the generator under test.
"""

from pathlib import Path

import pytest

from pfc2 import frontend
from pfc2.check import check
from pfc2.core.emit import GUARD_LINE
from pfc2.core.target import Target
from pfc2.gate import Certification

TARGET = Target("static LP64 layout (test)", "x86_64-pc-linux-gnu", 32, 64)
LONG_MIN = -(2**63)
pytestmark = pytest.mark.integration


def _check(tmp_path: Path, body: str) -> Certification:
    source = tmp_path / "t.c"
    source.write_text('#include "pfc.h"\n#include <stdbool.h>\n' + body, encoding="utf-8")
    return check(frontend.load(source), TARGET)[1]


def _failed(certification: Certification) -> list[tuple[str, str]]:
    """Kind and function of every obligation the solver refuted, in report order."""
    assert not certification.accepted and certification.c is None
    return [(b.kind, b.function) for b in certification.blockers if b.status == "failed"]


def _model(certification: Certification, kind: str) -> dict[str, int]:
    blocker = next(b for b in certification.blockers if b.kind == kind and b.status == "failed")
    assert blocker.counterexample is not None
    return {v.name: v.value for v in blocker.counterexample.scalars}


def _certified(certification: Certification) -> str:
    assert certification.accepted and certification.blockers == () and certification.c is not None
    return certification.c


# --- 0/1 values of `!x`, comparisons and conversions to bool ----------------------------------------------------------

NOT_VALUE = "long f(long x)\n{requires}    ensures({claim})\n{{\n    long y = !x;\n    return y;\n}}\n"
COMPARISON = "long f(long a, long b)\n{requires}    ensures({claim})\n{{\n    long y = a < b;\n    return y;\n}}\n"
CONVERSION = "bool f(long x)\n{requires}    ensures({claim})\n{{\n    bool b = x;\n    return b;\n}}\n"


@pytest.mark.parametrize(
    ("template", "requires", "claim"),
    [
        (NOT_VALUE, "", "result == 0"),  # !0 is 1.
        (NOT_VALUE, "", "result != 1"),  # !0 is 1.
        (NOT_VALUE, "", "result != 0"),  # !7 is 0.
        (NOT_VALUE, "    requires(x == 7)\n", "result != 0"),
        (NOT_VALUE, "    requires(x == 0)\n", "result != 1"),
        (COMPARISON, "", "result != 1"),  # 1 < 2 is 1.
        (COMPARISON, "", "result != 0"),  # 2 < 1 is 0.
        (COMPARISON, "    requires(a < b)\n", "result != 1"),
        (COMPARISON, "    requires(a >= b)\n", "result != 0"),
        (CONVERSION, "", "result == 0"),  # (bool)5 is 1.
        (CONVERSION, "    requires(x == 0)\n", "result == 1"),
        (CONVERSION, "    requires(x == 0)\n", "result != 0"),
        (CONVERSION, "    requires(x == 5)\n", "result != 1"),
        (CONVERSION, "    requires(x == 1)\n", "result == 0"),
        (CONVERSION, "    requires(x == -1)\n", "result == 0"),
    ],
)
def test_a_false_claim_about_a_logical_value_is_refused(
    tmp_path: Path, template: str, requires: str, claim: str
) -> None:
    certification = _check(tmp_path, template.format(requires=requires, claim=claim))
    assert _failed(certification) == [("postcondition", "f")]


@pytest.mark.parametrize(
    ("template", "requires", "claim"),
    [
        (NOT_VALUE, "    requires(x == 0)\n", "result == 1"),
        (NOT_VALUE, "    requires(x == 7)\n", "result == 0"),
        (NOT_VALUE, "", "result == 0 || result == 1"),
        (COMPARISON, "    requires(a < b)\n", "result == 1"),
        (COMPARISON, "    requires(a >= b)\n", "result == 0"),
        (CONVERSION, "    requires(x == 5)\n", "result == 1"),
        (CONVERSION, "    requires(x == -1)\n", "result == 1"),
        (CONVERSION, "    requires(x == 1)\n", "result == 1"),
        (CONVERSION, "    requires(x == 0)\n", "result == 0"),
    ],
)
def test_a_true_claim_about_a_logical_value_is_certified(
    tmp_path: Path, template: str, requires: str, claim: str
) -> None:
    _certified(_check(tmp_path, template.format(requires=requires, claim=claim)))


def test_the_counterexample_of_a_bool_conversion_is_the_only_input_the_law_allows(tmp_path: Path) -> None:
    certification = _check(tmp_path, CONVERSION.format(requires="    requires(x == 5)\n", claim="result != 1"))
    assert _model(certification, "postcondition")["x"] == 5


# --- separated() ------------------------------------------------------------------------------------------------------

SAME = "long f(long n, long a[n], long m, long b[m])\n"
MIXED = "long f(long n, long a[n], long m, char b[m])\n"


@pytest.mark.parametrize("header", [SAME, MIXED])
@pytest.mark.parametrize(("array", "length"), [("a", "n"), ("b", "m")])
def test_separated_does_not_promise_a_non_empty_array(tmp_path: Path, header: str, array: str, length: str) -> None:
    """Two empty arrays are separated, so element 0 need not exist and its bounds check cannot be proved away."""
    certification = _check(tmp_path, header + f"    requires(separated(a, b))\n{{\n    return {array}[0];\n}}\n")
    assert _failed(certification) == [("bounds", "f")]
    assert _model(certification, "bounds")[length] == 0


@pytest.mark.parametrize("header", [SAME, MIXED])
def test_separated_alone_is_a_satisfiable_law(tmp_path: Path, header: str) -> None:
    _certified(_check(tmp_path, header + "    requires(separated(a, b))\n{\n    return 0;\n}\n"))


@pytest.mark.parametrize(
    ("header", "requires", "negative"),
    [
        (SAME, "    requires(m == 0)\n", "n"),
        (SAME, "    requires(n == 0)\n", "m"),
        (MIXED, "", "n"),
        (MIXED, "", "m"),
    ],
)
def test_a_region_of_negative_length_is_never_separated(
    tmp_path: Path, header: str, requires: str, negative: str
) -> None:
    body = f"{{\n    {negative} = -1;\n    assert(SEPARATED(a, n, b, m));\n    return 0;\n}}\n"
    assert _failed(_check(tmp_path, header + requires + body)) == [("assert", "f")]


@pytest.mark.parametrize("regions", ["a, 0, b, m", "a, n, b, 0"])
def test_an_empty_region_is_separated_from_any_region(tmp_path: Path, regions: str) -> None:
    _certified(_check(tmp_path, SAME + f"{{\n    assert(SEPARATED({regions}));\n    return 0;\n}}\n"))


@pytest.mark.parametrize("regions", ["a, 1, b, m", "a, n, b, 1", "a, 1, b, 1"])
def test_a_one_element_region_may_overlap_another_region(tmp_path: Path, regions: str) -> None:
    """Nothing is known about the two addresses, so a and b may be the same array."""
    assert _failed(_check(tmp_path, SAME + f"{{\n    assert(SEPARATED({regions}));\n    return 0;\n}}\n")) == [
        ("assert", "f")
    ]


def test_separated_used_as_a_number_is_one_when_it_holds_for_arrays_of_one_type(tmp_path: Path) -> None:
    """With n == 0 the regions are separated, so the predicate is 1 and `!= 1` is false; `== 1` is true."""
    refused = _check(tmp_path, SAME + "{\n    assert(SEPARATED(a, n, b, m) != 1);\n    return 0;\n}\n")
    assert _failed(refused) == [("assert", "f")]
    _certified(
        _check(tmp_path, SAME + "    requires(n == 0)\n{\n    assert(SEPARATED(a, n, b, m) == 1);\n    return 0;\n}\n")
    )


def test_separated_used_as_a_number_is_one_when_it_holds_for_arrays_of_two_types(tmp_path: Path) -> None:
    """Arrays of different types with lengths >= 0 are always separated: the predicate is 1, never anything else."""
    refused = _check(tmp_path, MIXED + "    requires(separated(a, b) != 1)\n{\n    return 0;\n}\n")
    assert not refused.accepted and refused.c is None
    assert "law of f cannot be satisfied" in refused.reason
    _certified(_check(tmp_path, MIXED + "{\n    assert(SEPARATED(a, n, b, m) == 1);\n    return 0;\n}\n"))
    assert _failed(
        _check(tmp_path, MIXED + "{\n    n = -1;\n    assert(SEPARATED(a, n, b, m) != 0);\n    return 0;\n}\n")
    ) == [("assert", "f")]
    _certified(_check(tmp_path, MIXED + "{\n    n = -1;\n    assert(SEPARATED(a, n, b, m) == 0);\n    return 0;\n}\n"))


# --- LONG_MIN / -1 in program code and in annotations -----------------------------------------------------------------


def test_remainder_by_a_non_zero_divisor_is_still_refused_for_long_min_and_minus_one(tmp_path: Path) -> None:
    """LONG_MIN % -1 is undefined in C although the mathematical remainder is 0; only the division check covers it."""
    certification = _check(tmp_path, "long f(long a, long b)\n    requires(b != 0)\n{\n    return a % b;\n}\n")
    assert _failed(certification) == [("division", "f")]
    model = _model(certification, "division")
    assert (model["a"], model["b"]) == (LONG_MIN, -1)


def test_remainder_is_certified_without_a_guard_once_minus_one_is_excluded(tmp_path: Path) -> None:
    c = _certified(_check(tmp_path, "long f(long a, long b)\n    requires(b > 0)\n{\n    return a % b;\n}\n"))
    assert not GUARD_LINE.search(c)


def test_division_at_memory_level_keeps_its_guard_for_long_min_and_minus_one(tmp_path: Path) -> None:
    source = tmp_path / "t.c"
    source.write_text('#include "pfc.h"\nlong f(long a, long b)\n    requires(b != 0)\n{\n    return a / b;\n}\n')
    certification = check(frontend.load(source), TARGET, level="memory")[1]
    assert _failed(certification)[0] == ("division", "f")


def test_division_in_a_law_is_mathematical_and_needs_only_a_non_zero_divisor(tmp_path: Path) -> None:
    body = "long f(long a, long b)\n    requires(b != 0)\n    requires(a / b >= 0)\n{\n    return 0;\n}\n"
    _certified(_check(tmp_path, body))


# --- definedness of assert, ensures and invariant ---------------------------------------------------------------------


def test_an_assert_that_divides_by_zero_is_refused(tmp_path: Path) -> None:
    certification = _check(tmp_path, "long f(long x)\n{\n    assert(x / 0 == 0);\n    return 0;\n}\n")
    assert _failed(certification) == [("division", "f")]
    assert [b.location.line for b in certification.blockers] == [5, 5]  # Two lines of includes precede the program.


def test_an_assert_that_reads_past_the_array_is_refused(tmp_path: Path) -> None:
    body = "long f(long n, const long a[n])\n{\n    assert(a[n] == a[n]);\n    return 0;\n}\n"
    assert set(_failed(_check(tmp_path, body))) == {("bounds", "f")}


def test_a_postcondition_that_divides_by_zero_is_refused(tmp_path: Path) -> None:
    certification = _check(tmp_path, "long f(long x)\n    ensures(result / 0 == 0)\n{\n    return x;\n}\n")
    assert _failed(certification) == [("division", "f")]


def test_a_postcondition_that_reads_past_the_array_is_refused(tmp_path: Path) -> None:
    body = "long f(long n, const long a[n])\n    ensures(a[result] == a[result])\n{\n    return n;\n}\n"
    assert set(_failed(_check(tmp_path, body))) == {("bounds", "f")}


def test_an_invariant_undefined_on_entry_is_refused_even_if_every_iteration_repairs_it(tmp_path: Path) -> None:
    """d is 0 the first time the invariant is evaluated and 1 at the end of every iteration."""
    body = (
        "long f(long n)\n    requires(0 <= n)\n{\n    long d = 0;\n    long i = 0;\n"
        "    while (i < n) invariant(0 <= i && (i / d) * 0 == 0) {\n"
        "        d = 1;\n        i++;\n    }\n    return 0;\n}\n"
    )
    assert _failed(_check(tmp_path, body)) == [("division", "f")]


def test_an_invariant_defined_on_entry_and_after_every_iteration_is_admitted(tmp_path: Path) -> None:
    body = (
        "long f(long n)\n    requires(0 <= n)\n{\n    long d = 1;\n    long i = 0;\n"
        "    while (i < n) invariant(0 <= i && i <= n && d == 1 && (i / d) * 0 == 0) {\n"
        "        i++;\n    }\n    return 0;\n}\n"
    )
    _certified(_check(tmp_path, body))


def test_an_invariant_that_reads_past_the_array_after_the_last_iteration_is_refused(tmp_path: Path) -> None:
    """On entry i == 0 < n, so a[i] exists; after the last iteration i == n and a[i] does not."""
    body = (
        "long f(long n, const long a[n])\n    requires(0 < n)\n{\n    long i = 0;\n"
        "    while (i < n) invariant(0 <= i && i <= n && a[i] == a[i]) {\n        i++;\n    }\n    return 0;\n}\n"
    )
    certification = _check(tmp_path, body)
    assert set(_failed(certification)) == {("bounds", "f")}
    model = _model(certification, "bounds")
    assert model["i"] + 1 == model["n"]


# --- memory and parameters across calls and loops ---------------------------------------------------------------------

SET5 = "long set5(long n, long a[n])\n    requires(n > 0)\n    ensures(a[0] == 5)\n{\n    a[0] = 5;\n    return 0;\n}\n"


def test_a_callee_postcondition_describes_the_memory_after_the_call(tmp_path: Path) -> None:
    caller = (
        "long g(long n, long a[n])\n    requires(n > 0)\n    ensures(result == 5)\n"
        "{\n    a[0] = 1;\n    long r = set5(n, a);\n    return a[0];\n}\n"
    )
    _certified(_check(tmp_path, SET5 + caller))


def test_a_callee_postcondition_does_not_contradict_what_the_caller_wrote_before_the_call(tmp_path: Path) -> None:
    """If a[0] == 5 were assumed of the memory holding a[0] == 1, everything after the call would be proved."""
    caller = (
        "long g(long n, long a[n])\n    requires(n > 0)\n"
        "{\n    a[0] = 1;\n    long r = set5(n, a);\n    return a[n + 7];\n}\n"
    )
    assert _failed(_check(tmp_path, SET5 + caller)) == [("overflow", "g"), ("bounds", "g")]


def test_the_old_content_is_not_known_after_a_call_that_overwrites_it(tmp_path: Path) -> None:
    caller = (
        "long g(long n, long a[n])\n    requires(n > 0)\n    ensures(result == 1)\n"
        "{\n    a[0] = 1;\n    long r = set5(n, a);\n    return a[0];\n}\n"
    )
    assert _failed(_check(tmp_path, SET5 + caller)) == [("postcondition", "g")]


INCREMENT = (
    "long f(long x)\n    requires(-100 < x && x < 100)\n    ensures(result == x)\n{\n    x = x + 1;\n    return x;\n}\n"
)


@pytest.mark.parametrize("claim", ["result == 3", "result <= 3", "result != 4"])
def test_a_postcondition_over_a_reassigned_parameter_says_nothing_about_the_argument(
    tmp_path: Path, claim: str
) -> None:
    """f(3) returns 4: `result == x` holds for the final x, which the caller cannot see."""
    caller = f"long g(void)\n    ensures({claim})\n{{\n    long r = f(3);\n    return r;\n}}\n"
    assert _failed(_check(tmp_path, INCREMENT + caller)) == [("postcondition", "g")]


def test_a_postcondition_over_an_unassigned_parameter_is_about_the_argument(tmp_path: Path) -> None:
    callee = "long f(long x)\n    ensures(result == x)\n{\n    return x;\n}\n"
    caller = "long g(void)\n    ensures(result == 3)\n{\n    long r = f(3);\n    return r;\n}\n"
    _certified(_check(tmp_path, callee + caller))


def test_array_contents_written_by_a_loop_are_unknown_after_it(tmp_path: Path) -> None:
    """The loop zeroes a[0] on its first iteration (n > 0), so the function returns 0, not 1."""
    body = (
        "long f(long n, long a[n])\n    requires(n > 0)\n    ensures(result == 1)\n{\n    a[0] = 1;\n"
        "    for (long i = 0; i < n; i++) {\n        a[i] = 0;\n    }\n    return a[0];\n}\n"
    )
    assert _failed(_check(tmp_path, body)) == [("postcondition", "f")]


def test_array_contents_written_by_a_function_called_in_a_loop_are_unknown_after_it(tmp_path: Path) -> None:
    body = (
        "long zero(long n, long a[n])\n    requires(n > 0)\n{\n    a[0] = 0;\n    return 0;\n}\n"
        "long f(long n, long a[n])\n    requires(n > 0)\n    ensures(result == 1)\n{\n    a[0] = 1;\n"
        "    for (long i = 0; i < 3; i++) {\n        long r = zero(n, a);\n    }\n    return a[0];\n}\n"
    )
    assert _failed(_check(tmp_path, body)) == [("postcondition", "f")]


def test_array_contents_are_kept_across_a_loop_that_writes_no_array(tmp_path: Path) -> None:
    body = (
        "long f(long n, long a[n])\n    requires(n > 0)\n    ensures(result == 1)\n{\n    a[0] = 1;\n"
        "    for (long i = 0; i < 3; i++) {\n    }\n    return a[0];\n}\n"
    )
    _certified(_check(tmp_path, body))


# --- external contracts over bool arrays ------------------------------------------------------------------------------

USE = "long f(long n, {const}bool a[n])\n    requires(n > 0)\n{{\n    long r = h(n, a);\n    return r;\n}}\n"


@pytest.mark.parametrize(
    ("const", "ensures"),
    [
        ("", "a[0] + 1 == 0"),  # No bool is -1.
        ("", "a[0] == 2"),  # No bool is 2.
        ("const ", "result == 5 && a[0] == 0"),  # The caller may pass a[0] == true.
        ("const ", "result == 5 && a[0] == 1"),  # The caller may pass a[0] == false.
    ],
)
def test_an_external_contract_no_bool_array_can_meet_is_refused(tmp_path: Path, const: str, ensures: str) -> None:
    declaration = f"long h(long n, {const}bool a[n])\n    requires(n > 0)\n    ensures({ensures});\n"
    certification = _check(tmp_path, declaration + USE.format(const=const))
    assert not certification.accepted and certification.c is None
    assert "contract of h" in certification.reason
    assert [(e.query.function, e.total) for e in certification.proof.external_results] == [("h", "partial")]


@pytest.mark.parametrize("ensures", ["a[0] == 1", "a[0] == 0", "a[0] + a[0] == 2"])
def test_an_external_contract_a_bool_array_can_meet_is_accepted(tmp_path: Path, ensures: str) -> None:
    declaration = f"long h(long n, bool a[n])\n    requires(n > 0)\n    ensures({ensures});\n"
    certification = _check(tmp_path, declaration + USE.format(const=""))
    _certified(certification)
    assert [(e.query.function, e.total) for e in certification.proof.external_results] == [("h", "total")]
