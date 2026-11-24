"""Everyday C in the forked core: ++, compound assignment, calls inside expressions, arrays with their length.

Each expectation is the same program written by hand in the explicit subset; the two must lower
to the same structured program.
"""

import pytest

from pfc2.core import ir
from pfc2.core.diagnostics import FrontendError
from pfc2.core.lower import lower
from pfc2.core.parse import parse_preprocessed


def _c(text: str) -> str:
    return ir.print_c(lower(parse_preprocessed(text, "t.c")))


def test_increment_and_compound_assignment_are_explicit_assignments() -> None:
    sugared = """long f(long n) {
    long s = 0;
    for (long i = 0; i < n; i++) { s += i; }
    for (long j = n; j > 0; --j) { s -= 1; }
    s *= 2; s /= 3; s++; s--; ++s;
    return s;
}
"""
    explicit = """long f(long n) {
    long s = 0;
    for (long i = 0; i < n; i = i + 1) { s = s + i; }
    for (long j = n; j > 0; j = j - 1) { s = s - 1; }
    s = s * 2; s = s / 3; s = s + 1; s = s - 1; s = s + 1;
    return s;
}
"""
    assert _c(sugared) == _c(explicit)


def test_array_element_updates_keep_their_index() -> None:
    sugared = "long f(long a[], long a_len, long i) { a[i] += 2; a[i]++; return a[i]; }\n"
    explicit = "long f(long a[], long a_len, long i) { a[i] = a[i] + 2; a[i] = a[i] + 1; return a[i]; }\n"
    assert _c(sugared) == _c(explicit)


def test_calls_inside_expressions_are_evaluated_first_left_to_right() -> None:
    sugared = """long g(long x) { return x; }
_Bool p(long x) { return x > 0; }
long f(long n, long a[], long a_len) {
    long y = g(n) + g(1);
    g(n);
    if (p(y)) { y = 2; }
    a[0] = g(y);
    y = g(y);
    if (y > 0) return g(g(y)) + 1;
    return g(y);
}
"""
    explicit = """long g(long x) { return x; }
_Bool p(long x) { return x > 0; }
long f(long n, long a[], long a_len) {
    long tmp1 = g(n);
    long tmp2 = g(1);
    long y = tmp1 + tmp2;
    long tmp3 = g(n);
    _Bool tmp4 = p(y);
    if (tmp4) { y = 2; }
    long tmp5 = g(y);
    a[0] = tmp5;
    y = g(y);
    if (y > 0) { long tmp6 = g(y); long tmp7 = g(tmp6); return tmp7 + 1; }
    return g(y);
}
"""
    assert _c(sugared).replace("pfc2_t", "tmp") == _c(explicit)


@pytest.mark.parametrize(
    "body",
    [
        "while (g(n) > 0) { n = n - 1; } return n;",
        "for (long i = 0; i < g(n); i++) { n = n - 1; } return n;",
        "for (long i = 0; i < n; i = g(i)) { n = n - 1; } return n;",
        "if (n > 0 && g(n) > 0) { return 1; } return n;",
        "if (n > 0 || g(n) > 0) { return 1; } return n;",
    ],
)
def test_a_call_whose_evaluation_depends_on_control_flow_is_refused_not_reordered(body: str) -> None:
    with pytest.raises(FrontendError) as error:
        _c(f"long g(long x) {{ return x; }}\nlong f(long n) {{ {body} }}\n")
    assert error.value.diagnostic.rule == "subset-call-order"


def test_names_reserved_for_temporaries_are_refused() -> None:
    with pytest.raises(FrontendError) as error:
        _c("long f(long pfc2_t1) { return pfc2_t1; }\n")
    assert error.value.diagnostic.rule == "ir-name"


def test_an_array_parameter_carries_its_length() -> None:
    program = lower(parse_preprocessed("long f(long n, const long a[n], long b[], long b_len) { return n; }\n", "t.c"))
    n, a, b, b_len = program.functions[0].parameters
    assert a.length is n.symbol and b.length is b_len.symbol and n.length is None
    assert "long f(long n, const long a[], long b[], long b_len)" in ir.print_c(program).splitlines()


@pytest.mark.parametrize(
    "parameters", ["const long a[m]", "_Bool n, const long a[n]", "long n, const long a[n + 1]", "const long a[4]"]
)
def test_an_array_length_must_be_a_long_parameter(parameters: str) -> None:
    with pytest.raises(FrontendError) as error:
        _c(f"long f({parameters}) {{ return 0; }}\n")
    assert error.value.diagnostic.rule == "ir-array-length"


def test_ordinary_literals_are_typed_as_c_types_them_on_the_checked_target() -> None:
    from pfc2.core import smt
    from pfc2.core.target import Target

    text = "long f(void) { long a = 1000000; long b = 3000000000; long c = 9223372036854775807L; return a + b + c; }\n"
    program = lower(parse_preprocessed(text, "t.c"))
    a, b, c = (statement.initializer for statement in program.functions[0].body.statements[:3])
    assert isinstance(a, ir.Convert) and a.operand.type is ir.ScalarType.INT
    assert b.type is ir.ScalarType.LONG and c.type is ir.ScalarType.LONG
    smt.check(program, Target("LP64", "x86_64-pc-linux-gnu", 32, 64))
    # Where int is not 32 bits, C would give these literals another type: refuse rather than guess.
    for layout in (Target("int16", "test", 16, 64), Target("ILP64", "test", 64, 64), Target("ILP32", "test", 32, 32)):
        with pytest.raises(FrontendError) as error:
            smt.check(program, layout)
        assert error.value.diagnostic.rule == "target-literal"
    with pytest.raises(FrontendError) as error:
        _c("long f(void) { return 9223372036854775808; }\n")
    assert error.value.diagnostic.rule == "ir-literal-range"


def test_arithmetic_under_a_short_circuit_is_matched_to_its_proof_and_loses_its_trap(tmp_path) -> None:  # type: ignore[no-untyped-def]
    from pfc2 import frontend
    from pfc2.check import check
    from pfc2.core.target import Target

    source = tmp_path / "t.c"
    source.write_text(
        '#include "pfc.h"\nlong f(long x)\n    requires(0 <= x && x < 8)\n{\n'
        "    if (x > 0 && x + 1 < 8 || x - 1 > 3) {\n        return 1;\n    }\n    return 0;\n}\n",
        encoding="utf-8",
    )
    unit, certification = check(frontend.load(source), Target("t", "x86_64-pc-linux-gnu", 32, 64))
    # Hand-derived: x is in [0, 8), so neither x + 1 nor x - 1 can leave the range of long.
    assert [(d.location.column, d.removed) for d in certification.emission.overflow] == [(18, True), (31, True)]
    assert certification.accepted and certification.c is not None and "__builtin_trap" in certification.c
    assert "_overflow(" not in certification.c
