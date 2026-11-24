"""Surface pass: `where(...)` is extracted, blanked in place and turned into marker statements."""

import pytest

from pfc2 import surface
from pfc2.core.diagnostics import FrontendError

SOURCE = """# 1 "demo.c"
long count(long n where(0 <= n)) where(RESULT == n)
{
    long i where(0 <= i && i <= n) = 0;
    return i;
}
"""


def test_where_is_extracted_with_binder_kind_and_position():
    result = surface.extract(SOURCE, "demo.c")
    assert [(w.kind, w.function, w.binder, w.predicate) for w in result.wheres] == [
        ("parameter", "count", "n", "0 <= n"),
        ("result", "count", "count", "RESULT == n"),
        ("local", "count", "i", "0 <= i && i <= n"),
    ]
    first = result.wheres[0]
    assert (first.location.file, first.location.line, first.location.column) == ("demo.c", 1, 19)
    assert result.wheres[2].location.line == 3


def test_text_keeps_every_line_and_gains_marker_statements():
    result = surface.extract(SOURCE, "demo.c")
    lines = result.text.splitlines()
    assert len(lines) == len(SOURCE.splitlines())
    assert "where" not in result.text
    assert lines[1].startswith("long count(long n ")
    assert lines[2] == "{ __spec_requires((0 <= n)); __spec_ensures((RESULT == n));"
    assert lines[3].endswith("= 0; __spec_assert((0 <= i && i <= n));")
    # The declaration itself does not move: the initializer keeps its column.
    assert lines[3].index("= 0;") == SOURCE.splitlines()[3].index("= 0;")


def test_source_without_where_is_unchanged():
    text = '# 1 "plain.c"\nlong f(long x)\n{\n    return x;\n}\n'
    result = surface.extract(text, "plain.c")
    assert result.text == text and result.wheres == ()


def test_where_inside_a_string_is_not_a_refinement():
    text = '# 1 "s.c"\nlong f(long x)\n{\n    char *s = "where(x)";\n    return x;\n}\n'
    assert surface.extract(text, "s.c").wheres == ()


def test_line_markers_set_file_and_line():
    text = (
        '# 1 "main.c"\n# 1 "other.h" 1\nlong g(long x);\n# 7 "main.c" 2\n'
        "long f(long x where(x > 0))\n{\n return x;\n}\n"
    )
    (where,) = surface.extract(text, "main.c").wheres
    assert (where.location.file, where.location.line) == ("main.c", 7)


@pytest.mark.parametrize(
    ("body", "rule"),
    [
        ("long f(long x where x > 0)\n{\n return x;\n}\n", "where-syntax"),
        ("long f(long x where())\n{\n return x;\n}\n", "where-syntax"),
        ("long f(long x where(x > 0)\n{\n return x;\n}\n", "where-syntax"),
        ("long f(long where(1))\n{\n return 0;\n}\n", "where-position"),
        ("long f(long a[] where(1), long a_len)\n{\n return 0;\n}\n", "where-position"),
        ("long f(long x)\n{\n for (long i where(i >= 0) = 0; i < x; i = i + 1) { }\n return x;\n}\n", "where-position"),
        ("long f(long x)\n{\n long y = (x) where(y > 0);\n return y;\n}\n", "where-position"),
        ("long g where(g > 0);\n", "where-position"),
    ],
)
def test_malformed_where_is_rejected_with_a_rule(body, rule):
    with pytest.raises(FrontendError) as error:
        surface.extract('# 1 "bad.c"\n' + body, "bad.c")
    assert error.value.diagnostic.rule == rule
    assert error.value.diagnostic.location.file == "bad.c"


def test_prototype_where_must_match_the_definition():
    good = '# 1 "p.c"\nlong f(long x where(x > 0));\nlong f(long x where(x  >  0))\n{\n return x;\n}\n'
    assert [w.predicate for w in surface.extract(good, "p.c").wheres] == ["x > 0"]
    bad = '# 1 "p.c"\nlong f(long x where(x > 1));\nlong f(long x where(x > 0))\n{\n return x;\n}\n'
    with pytest.raises(FrontendError) as error:
        surface.extract(bad, "p.c")
    assert error.value.diagnostic.rule == "where-mismatch"
    orphan = '# 1 "p.c"\nlong f(long x where(x > 1));\n'
    with pytest.raises(FrontendError) as error:
        surface.extract(orphan, "p.c")
    assert error.value.diagnostic.rule == "where-mismatch"


LAW = """# 1 "law.c"
long count(long n)
{
    return n;
}

law count_is_identity(long n where(0 <= n))
{
    long r = count(n);
    __spec_assert((r == n));
}
"""


def test_law_becomes_a_checked_function_and_keeps_its_source():
    result = surface.extract(LAW, "law.c")
    (law,) = result.laws
    assert law.name == "count_is_identity" and law.location.line == 6
    assert law.text.startswith("law count_is_identity(long n where(0 <= n)) {") and law.text.endswith("}")
    lines = result.text.splitlines()
    assert len(lines) == len(LAW.splitlines())
    assert lines[6].startswith("long count_is_identity(long n ")
    assert lines[7] == "{ __spec_requires((0 <= n));"
    assert lines[10] == " return 0; }"
    assert [(w.kind, w.function) for w in result.wheres] == [("parameter", "count_is_identity")]


@pytest.mark.parametrize(
    "body",
    [
        "law f(long x);\n",
        "long f(long x)\n{\n long law = x;\n return law;\n}\n",
        "law long(long x)\n{\n}\n",
        "law f(long x)\n",
    ],
)
def test_law_is_a_reserved_word_with_one_form(body):
    with pytest.raises(FrontendError) as error:
        surface.extract('# 1 "bad.c"\n' + body, "bad.c")
    assert error.value.diagnostic.rule == "law-syntax"
