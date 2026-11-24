"""Elaboration: refinements become ordinary contracts of the frozen IR (expectations derived by hand)."""

from collections import Counter
from pathlib import Path

import pytest

from pfc2 import elaborate, frontend
from pfc2.core import ir, vc
from pfc2.core.diagnostics import FrontendError
from pfc2.core.ir import render_expression as _render
from pfc2.core.parse import SpecKind
from pfc2.core.target import Target
from pfc2.gate import certify

FIXTURES = Path(__file__).parent / "fixtures"

TARGET = Target("static LP64 layout (test)", "x86_64-pc-linux-gnu", 32, 64)


def render(expression: ir.Expr) -> str:
    """The harness renderer parenthesizes fully; these flat predicates read better without."""
    return _render(expression).replace("(", "").replace(")", "")


def load(name: str) -> elaborate.Unit:
    return frontend.load(FIXTURES / name)


def test_count_becomes_requires_ensures_asserts_and_a_loop_invariant():
    unit = load("count.c")
    (function,) = unit.program.functions
    assert [(c.kind, render(c.condition)) for c in function.contracts] == [
        (SpecKind.REQUIRES, "0 <= n"),
        (SpecKind.ENSURES, "RESULT == n"),
    ]
    local, initial, loop, final = function.body.statements
    assert isinstance(local, ir.Local) and local.symbol.name == "i"
    assert isinstance(initial, ir.Contract) and initial.kind is SpecKind.ASSERT
    assert render(initial.condition) == "0 <= i && i <= n"
    assert isinstance(loop, ir.While) and loop.invariant is not None
    assert loop.invariant.kind is SpecKind.INVARIANT and render(loop.invariant.condition) == "0 <= i && i <= n"
    assign, after = loop.body.statements
    assert isinstance(assign, ir.Assign)
    assert isinstance(after, ir.Contract) and after.kind is SpecKind.ASSERT
    assert render(after.condition) == "0 <= i && i <= n"
    # The re-check is reported at the assignment that may break the type.
    assert after.location == assign.location and after.location.line == 8
    assert isinstance(final, ir.Return)


def test_count_obligations_are_the_hand_derived_set():
    # Type at the declaration, type after the assignment, loop initiation, loop preservation,
    # the postcondition, and one reported overflow for i + 1.
    report = vc.generate(load("count.c").program)
    assert Counter((o.kind, o.category) for o in report.obligations) == Counter(
        {
            ("assert", "required"): 2,
            ("entry", "required"): 1,
            ("preservation", "required"): 1,
            ("postcondition", "required"): 1,
            ("overflow", "reported"): 1,
        }
    )
    assert len({o.id for o in report.obligations}) == len(report.obligations)


def test_assignment_to_an_unrelated_variable_is_not_rechecked():
    unit = load("sum.c")
    loop = next(s for s in unit.program.functions[0].body.statements if isinstance(s, ir.While))
    kinds = [type(s).__name__ for s in loop.body.statements]
    assert kinds == ["Assign", "Assign", "Contract"]  # only `i = i + 1` touches the type of i


def test_existing_invariant_is_kept_and_strengthened(tmp_path):
    source = tmp_path / "both.c"
    source.write_text(
        '#include "pfc.h"\n'
        "long f(long n where(0 <= n))\n"
        "{\n"
        "    long s = 0;\n"
        "    long i where(0 <= i && i <= n) = 0;\n"
        "    while (i < n) {\n"
        "        INVARIANT(s == 0);\n"
        "        i = i + 1;\n"
        "    }\n"
        "    return s;\n"
        "}\n",
        encoding="utf-8",
    )
    loop = next(s for s in frontend.load(source).program.functions[0].body.statements if isinstance(s, ir.While))
    assert loop.invariant is not None
    assert render(loop.invariant.condition) == "0 <= i && i <= n && s == 0"


def test_parameter_type_is_maintained_when_the_parameter_is_assigned(tmp_path):
    source = tmp_path / "param.c"
    source.write_text(
        '#include "pfc.h"\n' "long f(long n where(0 <= n))\n" "{\n" "    n = n - 1;\n" "    return n;\n" "}\n",
        encoding="utf-8",
    )
    assign, check, _ = frontend.load(source).program.functions[0].body.statements
    assert isinstance(check, ir.Contract) and render(check.condition) == "0 <= n"


def test_legacy_contract_file_is_accepted_unchanged():
    unit = load("legacy.c")
    assert unit.wheres == ()
    assert [c.kind for c in unit.program.functions[0].contracts] == [SpecKind.ENSURES]


def test_predicate_must_mention_its_binder(tmp_path):
    source = tmp_path / "binder.c"
    source.write_text('#include "pfc.h"\nlong f(long n where(0 <= 1), long m)\n{\n    return m;\n}\n', encoding="utf-8")
    with pytest.raises(FrontendError) as error:
        frontend.load(source)
    assert error.value.diagnostic.rule == "where-binder"
    assert error.value.diagnostic.location.line == 2


def test_source_still_compiles_as_plain_c(tmp_path):
    import subprocess

    root = Path(__file__).resolve().parents[1]
    for name in ("count.c", "fill.c", "sum.c"):
        result = subprocess.run(
            ["clang-19", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-Wno-unused-parameter"]
            + ["-I", str(root / "pfc2" / "include")]
            + ["-c", str(FIXTURES / name), "-o", str(tmp_path / (name + ".o"))],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr


def test_a_law_is_verified_as_a_function_and_left_out_of_the_released_program():
    unit = load("count_law.c")
    count, law = unit.program.functions
    assert [(c.kind, render(c.condition)) for c in count.contracts] == [
        (SpecKind.REQUIRES, "0 <= n"),
        (SpecKind.ENSURES, "RESULT == n"),
    ]
    assert [law.name for law in unit.laws] == ["count_reaches_n"]
    assert [type(s).__name__ for s in law.body.statements] == ["Local", "Contract", "Return"]
    assert unit.code is not None and [f.name for f in unit.code.functions] == ["count"]


def test_a_law_never_gives_a_function_a_contract(tmp_path):
    source = tmp_path / "bare.c"
    source.write_text(
        '#include "pfc.h"\n'
        "long same(long x)\n{\n    return x;\n}\n"
        "law small(long x where(x == 1))\n{\n    long r = same(x);\n    assert(r == 1);\n}\n",
        encoding="utf-8",
    )
    unit = frontend.load(source)
    assert unit.program.functions[0].contracts == ()
    # Without a postcondition on `same`, the law about its result cannot be proved.
    certification = certify(unit.program, TARGET, code=unit.code)
    assert not certification.accepted and [b.kind for b in certification.blockers] == ["assert"]


def test_calling_a_law_is_rejected(tmp_path):
    source = tmp_path / "call.c"
    source.write_text(
        '#include "pfc.h"\n'
        "law nothing(long x)\n{\n    assert(x == x);\n}\n"
        "long f(long x)\n{\n    long y = nothing(x);\n    return y;\n}\n",
        encoding="utf-8",
    )
    with pytest.raises(FrontendError) as error:
        frontend.load(source)
    assert error.value.diagnostic.rule == "law-call"
