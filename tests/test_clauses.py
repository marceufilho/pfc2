"""Clean clause spelling: requires/ensures after the declarator, invariant on the loop, result, assert."""

from pathlib import Path

import pytest

from pfc2 import frontend
from pfc2.clauses import rewrite
from pfc2.core.diagnostics import FrontendError
from pfc2.core.parse import SpecKind
from pfc2.core.target import Target
from pfc2.gate import certify

FIXTURES = Path(__file__).parent / "fixtures"
TARGET = Target("static LP64 layout (test)", "x86_64-pc-linux-gnu", 32, 64)
COUNT = """long count(long n)
    requires(0 <= n)
    ensures(result == n)
{
    long i = 0;
    while (i < n) invariant(0 <= i) invariant(i <= n) {
        i = i + 1;
    }
    assert(i == n);
    return i;
}
"""


def test_clauses_become_markers_inside_the_body_without_moving_any_line() -> None:
    clauses = rewrite(COUNT, "count.c")
    lines = clauses.text.splitlines()
    assert len(lines) == len(COUNT.splitlines())
    assert lines[1].strip() == "" and lines[2].strip() == ""
    assert lines[3] == "{ __spec_requires((0 <= n)); __spec_ensures((RESULT == n));"
    assert lines[5] == "    while (i < n)" + " " * 36 + " { __spec_invariant(((0 <= i) && (i <= n)));"
    assert lines[8] == "    __spec_assert(i == n);"
    assert [(c.kind, c.function, c.location.line, c.location.column) for c in clauses.clauses] == [
        ("requires", "count", 2, 5),
        ("ensures", "count", 3, 5),
        ("invariant", "count", 6, 19),
        ("invariant", "count", 6, 37),
    ]


def test_words_inside_strings_other_identifiers_and_expressions_are_left_alone() -> None:
    text = "long f(long requires_more) { long result = 1; long x = result; return x; }\n"
    assert rewrite(text, "f.c").text == text


@pytest.mark.parametrize(
    ("text", "rule"),
    [
        ("long f(long n) requires(0 <= n);\nlong f(long n) requires(1 <= n) { return n; }\n", "clause-mismatch"),
        ("long f(long n) requires 0 <= n { return n; }\n", "clause-syntax"),
        ("long f(long n) requires() { return n; }\n", "clause-syntax"),
        ("long f(long n) { while (n > 0) invariant(n >= 0) n = n - 1; return n; }\n", "clause-position"),
        ("long f(long n) { long x = n; invariant(x >= 0); return x; }\n", "clause-position"),
        ("long f(long n) requires(0 <= n)\nlong g(long n) { return n; }\n", "clause-position"),
    ],
)
def test_malformed_clauses_are_refused_with_their_rule(text: str, rule: str) -> None:
    with pytest.raises(FrontendError) as error:
        rewrite(text, "bad.c")
    assert error.value.diagnostic.rule == rule


def test_declaration_with_the_same_clauses_as_its_definition_is_accepted() -> None:
    text = "long f(long n) requires(0 <= n);\nlong f(long n) requires(0 <= n) { return n; }\n"
    assert rewrite(text, "f.c").text.count("__spec_requires") == 1


@pytest.mark.integration
def test_clean_program_and_its_law_certify_at_the_full_level() -> None:
    unit = frontend.load(FIXTURES / "clean_count.c")
    certification = certify(unit.program, TARGET, code=unit.code)
    assert certification.accepted, certification.reason
    assert certification.c is not None and "count_is_never_negative" not in certification.c


@pytest.mark.integration
def test_a_false_invariant_is_reported_at_the_clause_not_at_the_brace() -> None:
    unit = frontend.load(FIXTURES / "clean_wrong.c")
    certification = certify(unit.program, TARGET, code=unit.code)
    assert not certification.accepted and certification.c is None
    blockers = [b for b in certification.blockers if b.kind == "entry"]
    assert [(b.location.line, b.location.column) for b in blockers] == [(9, 19)]
    assert [(c.kind, c.location.line, c.location.column) for c in unit.program.functions[0].contracts] == [
        (SpecKind.REQUIRES, 4, 5),
        (SpecKind.ENSURES, 5, 5),
    ]


def test_separated_names_two_arrays_and_takes_their_lengths_from_their_types() -> None:
    from pfc2.core import ir
    from pfc2.core.lower import lower
    from pfc2.core.parse import parse_preprocessed

    header = (
        "void __spec_requires(_Bool condition);\n"
        "_Bool __spec_separated(const void *left, long left_len, const void *right, long right_len);\n"
    )
    clean = (
        "long copy(long n, long dst[n], const long src[], long src_len) requires(separated(dst, src)) { return n; }\n"
    )
    program = lower(parse_preprocessed(rewrite(header + clean, "copy.c").text, "copy.c"))
    assert ir.render_expression(program.functions[0].contracts[0].condition) == "SEPARATED(dst, n, src, src_len)"
    with pytest.raises(FrontendError) as error:
        lower(parse_preprocessed(rewrite(header + clean.replace("(dst, src)", "(dst, n)"), "copy.c").text, "copy.c"))
    assert error.value.diagnostic.rule == "subset-separated"
