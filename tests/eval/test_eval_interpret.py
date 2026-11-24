"""The reference interpreter against results derived by hand from C11."""

from typing import Any

import pytest

from pfc2 import frontend
from pfc2.core.target import Target
from pfc2_eval import interpret
from pfc2_eval.interpret import Inputs, Observation, Rejection

TARGET = Target("static LP64 layout (test)", "x86_64-pc-linux-gnu", 32, 64)
LONG_MAX, LONG_MIN = 2**63 - 1, -(2**63)
HEADER = '#include "pfc.h"\n'


def run(text: str, function: str | None = None, **inputs: Any) -> Observation | Rejection:
    unit = frontend.load_text(HEADER + text, "t.c")
    scalars = {k: v for k, v in inputs.items() if isinstance(v, int)}
    arrays = {k: v for k, v in inputs.items() if isinstance(v, list)}
    given = inputs.get("globals_", {})
    program = unit.code or unit.program
    return interpret.run(program, Inputs(scalars, arrays, given), target=TARGET, function=function)


def result(text: str, function: str | None = None, **inputs: Any) -> int:
    observed = run(text, function, **inputs)
    assert isinstance(observed, Observation), observed
    return observed.result


def rejected(text: str, function: str | None = None, **inputs: Any) -> str:
    observed = run(text, function, **inputs)
    assert isinstance(observed, Rejection), observed
    return observed.kind


BINARY = "long f(long a, long b)\n{\n    return a OP b;\n}\n"


@pytest.mark.parametrize(
    ("operator", "a", "b", "expected"),
    [
        ("/", 7, 2, 3),
        ("/", -7, 2, -3),  # Truncation toward zero, not floor.
        ("/", 7, -2, -3),
        ("%", 7, 2, 1),
        ("%", -7, 2, -1),  # The remainder has the sign of the dividend.
        ("%", 7, -2, 1),
        ("%", -7, -2, -1),
        ("+", LONG_MAX - 1, 1, LONG_MAX),
        ("*", -1, LONG_MAX, -LONG_MAX),
        ("<", 1, 2, 1),
        ("==", 3, 4, 0),
    ],
)
def test_arithmetic_is_c_arithmetic(operator: str, a: int, b: int, expected: int) -> None:
    assert result(BINARY.replace("OP", operator), a=a, b=b) == expected


@pytest.mark.parametrize(
    ("operator", "a", "b", "kind"),
    [
        ("+", LONG_MAX, 1, "Overflow"),
        ("-", LONG_MIN, 1, "Overflow"),
        ("*", LONG_MAX, 2, "Overflow"),
        ("/", 1, 0, "DivisionByZero"),
        ("%", 1, 0, "DivisionByZero"),
        ("/", LONG_MIN, -1, "Overflow"),
        ("%", LONG_MIN, -1, "Overflow"),  # Undefined although the mathematical remainder is 0 (C11 6.5.5p6).
    ],
)
def test_undefined_arithmetic_is_rejected_not_computed(operator: str, a: int, b: int, kind: str) -> None:
    assert rejected(BINARY.replace("OP", operator), a=a, b=b) == kind


def test_short_circuit_skips_the_operand_that_would_be_undefined() -> None:
    text = "long f(long a, long b)\n{\n    if (b != 0 && a / b > 1) {\n        return 1;\n    }\n    return 0;\n}\n"
    assert result(text, a=9, b=0) == 0 and result(text, a=9, b=2) == 1
    assert rejected(text.replace("b != 0 &&", "b == 0 &&"), a=9, b=0) == "DivisionByZero"


SUM = (
    "long sum(long n, const long a[n])\n{\n    long s = 0;\n    for (long i = 0; i < n; i++) {\n"
    "        s += a[i];\n    }\n    return s;\n}\n"
)


def test_arrays_have_the_capacity_they_were_declared_with() -> None:
    assert result(SUM, n=3, a=[1, 2, 3]) == 6
    assert result(SUM, n=2, a=[1, 2, 3]) == 3  # The function is told 2 elements.
    assert rejected(SUM, n=4, a=[1, 2, 3]) == "InvalidInput"  # The buffer is shorter than declared.
    assert rejected(SUM.replace("i < n", "i <= n"), n=3, a=[1, 2, 3]) == "OutOfBounds"
    assert rejected(SUM, n=2, a=[LONG_MAX, 1]) == "Overflow"
    late = SUM.replace("    long s = 0;\n", "    long s = 0;\n    n = n + 1;\n")
    assert rejected(late, n=2, a=[1, 2, 3]) == "OutOfBounds"  # Capacity is the value at entry, not the new n.


def test_writes_are_visible_in_the_observation_and_one_buffer_under_two_names_is_one_buffer() -> None:
    text = (
        "long f(long n, long a[n], long m, long b[m])\n    requires(n == 1 && m == 1)\n{\n"
        "    a[0] = 5;\n    b[0] = b[0] + 1;\n    return a[0];\n}\n"
    )
    apart = run(text, n=1, a=[0], m=1, b=[9])
    assert isinstance(apart, Observation) and (apart.result, apart.arrays) == (5, {"a": (5,), "b": (10,)})
    shared = [0]
    unit = frontend.load_text(HEADER + text, "t.c")
    same = interpret.run(unit.program, Inputs({"n": 1, "m": 1}, {"a": shared, "b": shared}), target=TARGET)
    assert isinstance(same, Observation) and same.result == 6 and shared == [0]  # The caller's list is not touched.
    separated = text.replace("requires(n == 1 && m == 1)", "requires(n == 1 && m == 1 && separated(a, b))")
    unit = frontend.load_text(HEADER + separated, "t.c")
    refused = interpret.run(unit.program, Inputs({"n": 1, "m": 1}, {"a": shared, "b": shared}), target=TARGET)
    assert isinstance(refused, Rejection) and refused.kind == "PreconditionViolated"


def test_a_negative_length_is_for_the_contract_to_refuse() -> None:
    assert rejected(SUM, n=-1, a=[]) == "PreconditionViolated"  # `long a[n]` requires 0 <= n.
    legacy = "long f(long a[], long a_len)\n{\n    return a_len;\n}\n"
    assert result(legacy, a_len=-1, a=[]) == -1  # The older spelling states nothing; nothing is accessed.
    assert rejected(legacy.replace("return a_len;", "return a[0];"), a_len=-1, a=[]) == "OutOfBounds"


def test_break_continue_and_the_update_of_a_for() -> None:
    text = (
        "long f(long n)\n{\n    long s = 0;\n    for (long i = 0; i < n; i++) {\n"
        "        if (i == 2) {\n            continue;\n        }\n"
        "        if (i == 5) {\n            break;\n        }\n"
        "        s += i;\n    }\n    return s;\n}\n"
    )
    assert result(text, n=10) == 0 + 1 + 3 + 4  # 2 is skipped (and i still advances); 5 ends the loop.
    assert result(text, n=2) == 1


def test_local_arrays_start_from_their_initial_values_each_time() -> None:
    text = (
        "long f(long n)\n{\n    long total = 0;\n    for (long i = 0; i < n; i++) {\n"
        "        long t[3] = {7};\n        total += t[0] + t[1] + t[2];\n        t[1] = 100;\n    }\n"
        "    return total;\n}\n"
    )
    assert result(text, n=3) == 21  # 7 + 0 + 0 each time: the write of the previous round is gone.
    assert rejected("long f(long i)\n{\n    long t[2] = {1, 2};\n    return t[i];\n}\n", i=2) == "OutOfBounds"


def test_narrow_elements_promote_on_read_and_must_fit_on_write() -> None:
    text = "long f(long n, char s[n], long v)\n    requires(n == 1)\n{\n    s[0] = v;\n    return s[0] + 1;\n}\n"
    assert result(text, n=1, s=[0], v=127) == 128  # Read back as an int, so 127 + 1 does not overflow.
    assert rejected(text, n=1, s=[0], v=128) == "ConversionOutOfRange"
    assert rejected(text, n=1, s=[300], v=0) == "InvalidInput"
    ints = "long f(long n, const int a[n])\n    requires(n == 2)\n{\n    return a[0] + a[1];\n}\n"
    assert rejected(ints, n=2, a=[2**31 - 1, 1]) == "Overflow"  # int + int is int arithmetic.
    assert result(ints, n=2, a=[2**31 - 1, -1]) == 2**31 - 2


COUNTER = (
    "long hits = 3;\nlong bump(long by)\n    requires(0 <= by)\n    ensures(result == hits)\n{\n"
    "    hits = hits + by;\n    return hits;\n}\n"
    "long twice(long by)\n    requires(0 <= by)\n{\n    long first = bump(by);\n    return first + bump(by);\n}\n"
)


def test_globals_calls_and_contracts() -> None:
    observed = run(COUNTER, "twice", by=2)
    assert isinstance(observed, Observation)
    assert (observed.result, observed.globals) == ((3 + 2) + (3 + 4), {"hits": 7})
    started = run(COUNTER, "twice", by=1, globals_={"hits": 10})
    assert isinstance(started, Observation) and started.result == 11 + 12
    assert rejected(COUNTER, "twice", by=-1) == "PreconditionViolated"
    wrong = COUNTER.replace("ensures(result == hits)", "ensures(result == hits + 1)")
    claimed = run(wrong, "twice", by=2)
    assert isinstance(claimed, Observation) and claimed.annotation_violations == (
        "ENSURES at 5:5",
    )  # Line 1 is the header.


def test_a_false_invariant_is_reported_once_and_the_run_goes_on() -> None:
    text = (
        "long f(long n)\n{\n    long i = 0;\n    while (i < n) invariant(i < 2) {\n"
        "        i++;\n    }\n    return i;\n}\n"
    )
    observed = run(text, n=5)
    assert isinstance(observed, Observation) and observed.result == 5
    assert observed.annotation_violations == ("INVARIANT at 5:19",)
    held = run(text, n=1)
    assert isinstance(held, Observation) and held.annotation_violations == ()


def test_the_step_budget_ends_a_loop_that_does_not() -> None:
    unit = frontend.load_text(HEADER + "long f(void)\n{\n    for (;;) {\n    }\n    return 0;\n}\n", "t.c")
    observed = interpret.run(unit.program, Inputs(), target=TARGET, fuel=1000)
    assert isinstance(observed, Rejection) and observed.kind == "Inconclusive"


def test_a_declared_function_needs_a_host_model() -> None:
    text = "long sensor(long x)\n    ensures(0 <= result);\nlong f(long x)\n{\n    return sensor(x);\n}\n"
    assert rejected(text, "f", x=1) == "Unsupported"

    class Sensor(interpret.Host):
        def call(self, name: str, arguments: Any) -> int | None:
            return -4 if name == "sensor" else None

    unit = frontend.load_text(HEADER + text, "t.c")
    observed = interpret.run(unit.program, Inputs({"x": 1}), target=TARGET, function="f", host=Sensor())
    assert isinstance(observed, Observation) and observed.result == -4
    assert observed.annotation_violations == ("ENSURES at 3:5",)  # The model broke the declared contract.


def test_evaluate_condition_reads_a_requires_conjunct_mathematically() -> None:
    unit = frontend.load_text(HEADER + "long f(long a, long b)\n    requires(a + b > 0)\n{\n    return 0;\n}\n", "t.c")
    condition = unit.program.functions[0].contracts[0].condition
    big = Inputs({"a": LONG_MAX, "b": LONG_MAX})
    assert interpret.evaluate_condition(unit.program, big, condition, target=TARGET) is True  # No overflow here.
    assert interpret.evaluate_condition(unit.program, Inputs({"a": -1, "b": 0}), condition, target=TARGET) is False
