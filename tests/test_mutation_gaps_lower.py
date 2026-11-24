"""Lowering facts the proofs depend on: literal values, complete returns, fresh names, argument and result types.

Each expectation is written by hand from C11 (literal and escape values, conversion to _Bool) or from the documented
subset rules; none is computed with the lowering under test. Programs go through the public path: the frontend,
then the strict gate with real Z3.
"""

import pytest

from pfc2 import frontend, gate
from pfc2.core.diagnostics import FrontendError
from pfc2.core.target import Target

TARGET = Target("test LP64 layout (no clang queried)", "x86_64-pc-linux-gnu", 32, 64)
HEADER = '#include "pfc.h"\n'


def certify(text: str) -> gate.Certification:
    """Memory level: only the stated assertions, contracts and memory checks decide, not accumulator overflow."""
    return gate.certify(frontend.load_text(HEADER + text, "t.c").program, TARGET, level="memory")


def refusal(text: str) -> str:
    with pytest.raises(FrontendError) as error:
        frontend.load_text(HEADER + text, "t.c")
    return error.value.diagnostic.rule


def assert_holds(text: str) -> None:
    result = certify(text)
    assert result.accepted and result.c is not None, result.reason


def assert_fails(text: str) -> None:
    result = certify(text)
    assert not result.accepted and result.c is None
    assert any(blocker.status == "failed" for blocker in result.blockers)


# --- octal and hexadecimal literals ---------------------------------------------------------------------------


@pytest.mark.integration
@pytest.mark.parametrize(
    ("spelling", "value"),
    [("010", 8), ("017", 15), ("0777", 511), ("0x1F", 31), ("0x5", 5), ("0X10", 16), ("0x7fff", 32767), ("010L", 8)],
)
def test_an_octal_or_hexadecimal_literal_has_its_c_value(spelling: str, value: int) -> None:
    assert_holds(f"long f(void) {{ long x = {spelling}; assert(x == {value}); return x; }}\n")


@pytest.mark.integration
@pytest.mark.parametrize(("spelling", "wrong"), [("010", 7), ("010", 9), ("010", 10), ("0x1F", 15), ("0x5", 0)])
def test_an_octal_or_hexadecimal_literal_has_no_other_value(spelling: str, wrong: int) -> None:
    assert_fails(f"long f(void) {{ long x = {spelling}; assert(x == {wrong}); return x; }}\n")


@pytest.mark.integration
@pytest.mark.parametrize(("length", "index"), [(8, "010"), (16, "0x1F"), (31, "0x1F"), (5, "0x5")])
def test_an_index_spelled_in_another_base_past_the_end_keeps_the_program_refused(length: int, index: str) -> None:
    """a[010] is a[8]: one past the end of eight elements, whatever a misread literal would suggest."""
    result = certify(f"long f(long n, long a[n]) requires(n == {length}) {{ return a[{index}]; }}\n")
    assert not result.accepted and result.c is None
    assert [(blocker.kind, blocker.status) for blocker in result.blockers] == [("bounds", "failed")]


@pytest.mark.integration
@pytest.mark.parametrize(("length", "index"), [(9, "010"), (32, "0x1F"), (6, "0x5")])
def test_an_index_spelled_in_another_base_inside_the_array_is_proved(length: int, index: str) -> None:
    assert_holds(f"long f(long n, long a[n]) requires(n == {length}) {{ return a[{index}]; }}\n")


@pytest.mark.integration
def test_a_divisor_written_in_octal_that_is_zero_in_c_is_not_proved_nonzero() -> None:
    """010 - 8 is 0 in C; reading 010 as nine would make the divisor one."""
    result = certify("long f(long x) { long d = 010 - 8; return x / d; }\n")
    assert not result.accepted and result.c is None


# --- character constants and string initial values ------------------------------------------------------------

ESCAPES = [
    ("\\n", 10),
    ("\\t", 9),
    ("\\r", 13),
    ("\\0", 0),
    ("\\\\", 92),
    ("\\'", 39),
    ('\\"', 34),
    ("\\a", 7),
    ("\\b", 8),
    ("\\f", 12),
    ("\\v", 11),
]


@pytest.mark.integration
@pytest.mark.parametrize(("escape", "code"), ESCAPES)
def test_a_simple_escape_in_a_character_constant_has_its_c_code(escape: str, code: int) -> None:
    assert_holds(f"long f(void) {{ long x = '{escape}'; assert(x == {code}); return x; }}\n")


@pytest.mark.integration
@pytest.mark.parametrize(("escape", "code"), ESCAPES)
def test_a_simple_escape_in_a_string_initial_value_has_its_c_code(escape: str, code: int) -> None:
    assert_holds(f'long f(void) {{ char w[4] = "{escape}"; assert(w[0] == {code} && w[1] == 0); return w[0]; }}\n')


@pytest.mark.integration
@pytest.mark.parametrize(
    ("escape", "wrong"),
    [("\\r", 12), ("\\r", 14), ('\\"', 33), ('\\"', 35), ("\\a", 6), ("\\a", 8), ("\\b", 7), ("\\b", 9)]
    + [("\\f", 11), ("\\f", 13), ("\\v", 10), ("\\v", 12)],
)
def test_a_simple_escape_has_no_neighbouring_code(escape: str, wrong: int) -> None:
    assert_fails(f"long f(void) {{ long x = '{escape}'; assert(x == {wrong}); return x; }}\n")


@pytest.mark.parametrize("text", ["ab\\01", "\\01x", "\\01", "a\\07b", "\\012", "x\\00", "ab\\09cd"])
def test_an_octal_escape_in_a_string_is_refused_rather_than_read_as_nul_and_a_digit(text: str) -> None:
    assert refusal(f'long f(void) {{ char w[8] = "{text}"; return w[0]; }}\n') == "subset-literal"


@pytest.mark.parametrize("constant", ["'\\q'", "'\\x41'", "'\\01'", "'ab'", "'\\nx'", "'\u0080'", "'é'"])
def test_a_character_constant_outside_the_simple_set_is_refused(constant: str) -> None:
    assert refusal(f"long f(void) {{ long x = {constant}; return x; }}\n") == "subset-literal"


@pytest.mark.parametrize("text", ["\u0080", "a\u0080", "\\q"])
def test_a_string_with_a_character_outside_the_simple_set_is_refused(text: str) -> None:
    assert refusal(f'long f(void) {{ char w[4] = "{text}"; return w[0]; }}\n') == "subset-literal"


@pytest.mark.integration
@pytest.mark.parametrize(
    ("text", "codes"),
    [
        ("a\\nbc", [97, 10, 98, 99, 0]),
        ("\\n5", [10, 53, 0]),
        ("0\\n1", [48, 10, 49, 0]),
        ("\\0a", [0, 97, 0]),
        ("1\\t2\\\\3", [49, 9, 50, 92, 51, 0]),
        ("\x7f", [127, 0]),
        ("", [0, 0]),
    ],
)
def test_a_string_initial_value_stores_each_character_then_zeros(text: str, codes: list[int]) -> None:
    claims = " && ".join(f"w[{index}] == {code}" for index, code in enumerate(codes))
    assert_holds(f'long f(void) {{ char w[8] = "{text}"; assert({claims}); return w[0]; }}\n')


@pytest.mark.integration
@pytest.mark.parametrize(
    ("text", "false_claim"),
    [("", "w[0] == -1"), ("", "w[0] == 1"), ("a\\nbc", "w[2] == 99"), ("a\\nbc", "w[3] == 0")],
)
def test_a_false_claim_about_a_string_initial_value_is_refused(text: str, false_claim: str) -> None:
    assert_fails(f'long f(void) {{ char w[8] = "{text}"; assert({false_claim}); return w[0]; }}\n')


# --- local-array initial values -------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("element", "value"),
    [("_Bool", "-1"), ("_Bool", "2"), ("char", "-1"), ("char", "128"), ("int", "-2147483649"), ("int", "2147483648")],
)
def test_an_initial_value_the_element_type_cannot_hold_unchanged_is_refused(element: str, value: str) -> None:
    text = f"long f(void) {{ {element} a[2] = {{{value}}}; long r = a[0]; return r; }}\n"
    assert refusal(text) == "subset-local-array"


@pytest.mark.integration
@pytest.mark.parametrize(
    ("element", "value"),
    [("_Bool", "0"), ("_Bool", "1"), ("char", "0"), ("char", "127"), ("int", "-2147483648"), ("int", "2147483647")],
)
def test_an_initial_value_at_the_edge_of_the_element_type_is_stored_unchanged(element: str, value: str) -> None:
    assert_holds(f"long f(void) {{ {element} a[2] = {{{value}}}; long r = a[0]; assert(r == {value}); return r; }}\n")


# --- every path returns ---------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "body",
    [
        "if (x > 0) { return 1; }",
        "long y = x;",
        "long y = 0; y = x;",
        "if (x > 0) { return 1; } else { long y = x; }",
        "if (x > 0) { long y = x; } else { return 1; }",
        "{ long y = x; }",
        "",
    ],
)
def test_a_function_with_a_path_that_falls_off_the_end_is_refused(body: str) -> None:
    assert refusal(f"long f(long x) ensures(result == 1) {{ {body} }}\n") == "ir-return"


@pytest.mark.integration
@pytest.mark.parametrize(
    "body",
    [
        "if (x > 0) { return 1; } else { return 2; }",
        "if (x > 0) { return 1; } return 2;",
        "{ return 1; }",
        "if (x > 0) { return 1; } else { if (x < 0) { return 2; } else { return 1; } }",
    ],
)
def test_a_function_whose_every_path_ends_in_a_return_is_certified(body: str) -> None:
    assert_holds(f"long f(long x) ensures(result == 1 || result == 2) {{ {body} }}\n")


# --- fresh names ----------------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "function",
    [
        "long f(long x, long x) { return x; }",
        "long f(long x) { long y = 1; long y = 2; return y; }",
        "long f(long x) { long x = 1; return x; }",
        "long f(long x) { long r = 0; if (x > 0) { long x = x + 1; r = x; } return r; }",
        "long f(long x) { long r = 0; while (r < 1) { long x = 3; r = x; } return r; }",
    ],
)
def test_a_name_already_bound_cannot_be_declared_again(function: str) -> None:
    """Shadowing is refused: in C `long x = x + 1;` reads the new, uninitialized x."""
    assert refusal(function + "\n") == "ir-name"


# --- result and argument types --------------------------------------------------------------------------------


@pytest.mark.integration
def test_a_bool_function_returns_zero_or_one_and_is_released_as_bool() -> None:
    result = certify("_Bool f(long x) ensures(result == 1) { return 5; }\n")
    assert result.accepted and result.c is not None, result.reason
    assert "_Bool f(long x)" in result.c and "long f(long x)" not in result.c


@pytest.mark.integration
def test_a_bool_function_cannot_promise_the_unconverted_value_it_returns() -> None:
    assert_fails("_Bool f(long x) ensures(result == 5) { return 5; }\n")


@pytest.mark.integration
def test_a_caller_sees_a_bool_result_as_zero_or_one() -> None:
    callee = "_Bool f(long x) { return x; }\n"
    assert_holds(callee + "long g(long x) { long y = f(x); assert(y == 0 || y == 1); return y; }\n")


WRITER = "long set(long n, long a[n]) requires(n >= 1) { a[0] = 1000000; return 0; }\n"


@pytest.mark.parametrize(
    ("parameters", "argument"),
    [
        ("long n, char s[n]", "s"),
        ("long n, int s[n]", "s"),
        ("long n, _Bool s[n]", "s"),
        ("long n, const long s[n]", "s"),
        ("long n, long s[n]", "n"),
        ("long n, long s[n]", "0"),
        ("long n, long s[n]", "s[0]"),
    ],
)
def test_an_array_argument_must_be_an_array_of_the_same_element_type_and_writable_if_written(
    parameters: str, argument: str
) -> None:
    caller = f"long f({parameters}) requires(n >= 1) {{ long r = set(n, {argument}); return r; }}\n"
    assert refusal(WRITER + caller) == "subset-call-type"


@pytest.mark.integration
def test_a_matching_writable_array_argument_is_accepted() -> None:
    assert_holds(WRITER + "long f(long n, long s[n]) requires(n >= 1) { long r = set(n, s); return r; }\n")
