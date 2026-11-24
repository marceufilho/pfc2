"""Lexical behaviour of PFC2's own preprocessor that the mutation campaign found unobserved.

Every expected text is written by hand: a comment becomes as many spaces as it had characters, a literal is
left alone, a directive becomes an empty line. The functions are called directly because the difference is
in the text handed to the parser; a wrong text here makes the checker read a program the C compiler does not.
"""

import pytest

from pfc2.preprocess import preprocess, strip_comments

SEVEN = " " * 7  # The width of a comment such as `/* c */` or `// tail`.

# Order matters for a mutated scanner that never leaves `/**/`: the cases before the last fail first.
BLOCK_COMMENTS = [
    pytest.param("/* c /*/ x = 1; /* d */", " " * 8 + " x = 1; " + SEVEN, id="slash-before-terminator"),
    pytest.param("/*/ x = 1; /*/", " " * 14, id="slash-star-slash-does-not-close"),
    pytest.param("a/* c */-b", "a" + SEVEN + "-b", id="character-after-comment-kept"),
    pytest.param("a /* e */", "a " + SEVEN, id="comment-ends-the-text"),
    pytest.param("x = 3 /* c */* 1; x = 1; /* d */;", "x = 3 " + SEVEN + "* 1; x = 1; " + SEVEN + ";", id="star-after"),
    pytest.param('f(/* c */"/*"); x = 1; g("*/");', "f(" + SEVEN + '"/*"); x = 1; g("*/");', id="string-after"),
    pytest.param("/**/ x = 1; /* c */", " " * 4 + " x = 1; " + SEVEN, id="empty-comment"),
]

LITERALS = [
    pytest.param('"" /* c */ y', '"" ' + SEVEN + " y", id="empty-string"),
    pytest.param('p("\\"/*"); x = 1; q("*/");', 'p("\\"/*"); x = 1; q("*/");', id="escaped-quote"),
    pytest.param('p("a\\n"); // tail', 'p("a\\n"); ' + SEVEN, id="escape-before-closing-quote"),
    pytest.param('p("a"); // t', 'p("a"); ' + " " * 4, id="one-character-string"),
    pytest.param("c = '\\''; // t", "c = '\\''; " + " " * 4, id="escaped-apostrophe"),
]


@pytest.mark.parametrize(("text", "expected"), BLOCK_COMMENTS)
def test_block_comment_is_blanked_exactly_from_its_opening_to_its_terminator(text: str, expected: str) -> None:
    assert strip_comments(text, "t.c") == expected


@pytest.mark.parametrize(("text", "expected"), LITERALS)
def test_literal_ends_at_its_unescaped_quote_and_only_real_comments_are_blanked(text: str, expected: str) -> None:
    assert strip_comments(text, "t.c") == expected


def test_scan_starts_at_the_first_character_even_when_the_text_ends_with_a_quote() -> None:
    """No final newline and a quote as last character: the comment on line 1 must still be blanked."""
    assert strip_comments('// first\nlong x; // "', "t.c") == " " * 8 + "\nlong x; " + " " * 4


@pytest.mark.parametrize("name", ["N1", "SIZE_", "_limit", "_k_", "MAX_2"])
def test_macro_is_expanded_whatever_the_shape_of_its_name(name: str) -> None:
    assert preprocess(f"#define {name} 10\nlong a = {name};\n", "t.c", {}) == "\nlong a = 10;\n"


def test_inner_else_flips_only_the_inner_conditional() -> None:
    source = "#ifdef PFC_CHECK\n#ifdef PFC_CHECK\nlong a;\n#else\nlong b;\n#endif\nlong c;\n#endif\nlong d;\n"
    assert preprocess(source, "t.c", {}) == "\n\nlong a;\n\n\n\nlong c;\n\nlong d;\n"


def test_inner_else_of_an_undefined_name_is_read_when_the_outer_branch_is_read() -> None:
    source = "#ifdef PFC_CHECK\n#ifdef NOPE\nlong a;\n#else\nlong b;\n#endif\n#endif\n"
    assert preprocess(source, "t.c", {}) == "\n\n\n\nlong b;\n\n\n"


def test_last_line_without_final_newline_is_kept() -> None:
    assert preprocess("long a;\nlong b;", "t.c", {}) == "long a;\nlong b;\n"
