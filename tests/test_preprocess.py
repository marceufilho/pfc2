"""PFC2 reads its sources itself: comments, its own headers, #ifdef and simple #define, with source positions."""

import subprocess
from pathlib import Path

import pytest

from pfc2 import frontend
from pfc2.core import ir
from pfc2.core.diagnostics import FrontendError
from pfc2.elaborate import elaborate_text
from pfc2.preprocess import preprocess
from pfc2.text import SourceText

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = sorted((ROOT / "examples").rglob("*.c"))
HEADERS = frontend.headers()


def test_comments_become_spaces_so_every_token_keeps_its_line_and_column() -> None:
    source = "long f(long n) /* why */ { return n; } // done\n/* a\n   b */ long g(void) { return 1; }\n"
    output = preprocess(source, "t.c", {})
    assert output == "long f(long n)           { return n; }        \n    \n        long g(void) { return 1; }\n"
    assert preprocess('long f(void) { return "/* no */" == "//"; }\n', "t.c", {}).count("/*") == 1


def test_an_include_brings_the_header_and_positions_still_point_into_the_source() -> None:
    source = '#include "pfc.h"\n\nlong f(long n)\n{\n    return n;\n}\n'
    output = preprocess(source, "t.c", HEADERS)
    assert "void __spec_requires(_Bool condition);" in output and "#define" not in output
    text = SourceText(output, "t.c")
    where = text.locate(output.index("return n"))
    assert (where.file, where.line, where.column) == ("t.c", 5, 5)
    inside = text.locate(output.index("void __spec_requires"))
    assert inside.file == "pfc.h"


def test_object_like_macros_and_conditionals() -> None:
    source = (
        "#define LIMIT 100\n#define EMPTY\n#ifdef EMPTY\nlong a = LIMIT;\n#else\nlong a = 0;\n#endif\n"
        '#ifndef EMPTY\nlong b = 1;\n#endif\nlong f(void) { print_str("LIMIT"); return LIMITS + LIMIT; }\n'
    )
    lines = preprocess(source, "t.c", {}).splitlines()
    assert lines == [
        "",
        "",
        "",
        "long a = 100;",
        "",
        "",
        "",
        "",
        "",
        "",
        'long f(void) { print_str("LIMIT"); return LIMITS + 100; }',
    ]


@pytest.mark.parametrize(
    ("source", "rule"),
    [
        ("#define F(x) x\n", "preprocess-unsupported"),
        ("#if 1\n#endif\n", "preprocess-unsupported"),
        ("#pragma once\n", "preprocess-unsupported"),
        ('#include "other.h"\n', "preprocess-include"),
        ("#include <stdio.h>\n", "preprocess-include"),
        ("long a = 1; \\\nlong b = 2;\n", "preprocess-unsupported"),
        ("long a = 1; /* never closed\n", "preprocess-comment"),
        ("#else\n", "preprocess-conditional"),
        ("#ifdef A\n", "preprocess-conditional"),
        ("#define long int\n#define long int\n", "preprocess-unsupported"),
    ],
)
def test_everything_else_is_refused_with_a_rule(source: str, rule: str) -> None:
    with pytest.raises(FrontendError) as error:
        preprocess(source, "t.c", HEADERS)
    assert error.value.diagnostic.rule == rule


def test_a_directive_in_a_skipped_branch_is_not_read() -> None:
    assert (
        preprocess("#ifdef NEVER\n#define F(x) x\n#pragma once\n#endif\nlong a = 1;\n", "t.c", {}).splitlines()[-1]
        == "long a = 1;"
    )


@pytest.mark.integration
@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: str(p.relative_to(ROOT / "examples")))
def test_the_built_in_preprocessor_reads_every_example_as_real_cpp_does(path: Path) -> None:
    """Independent oracle: GNU cpp with the same headers must yield the same program after the surface passes."""
    command = ["cpp", "-E", "-x", "c", "-std=c11", "-undef", "-nostdinc", "-DPFC_CHECK"]
    command += ["-I", str(ROOT / "pfc2" / "include"), "-"]
    text = path.read_text(encoding="utf-8")
    result = subprocess.run(
        command, input=f'#line 1 "{path.name}"\n{text}', capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr
    oracle = elaborate_text(result.stdout, path.name)
    ours = frontend.load(path)
    assert ir.print_c(ours.program) == ir.print_c(oracle.program)
    assert (ours.externals, ours.strings, ours.entry) == (oracle.externals, oracle.strings, oracle.entry)
