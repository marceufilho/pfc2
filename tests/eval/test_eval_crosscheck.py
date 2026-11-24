"""E6: the comparison rule, the SMT-LIB export, and a real run when cvc5 is installed."""

import os
from pathlib import Path

import pytest
import z3

from pfc2_eval import crosscheck

CVC5 = Path(os.environ.get("PFC2_EVAL_CVC5", Path.home() / ".local/opt/cvc5-1.4.2/cvc5"))
needs_cvc5 = pytest.mark.skipif(not CVC5.is_file(), reason="cvc5 is not installed; set PFC2_EVAL_CVC5")


def test_only_two_clear_and_opposite_answers_are_a_disagreement() -> None:
    assert crosscheck.agreement("unsat", "unsat") == "agree" and crosscheck.agreement("sat", "sat") == "agree"
    assert crosscheck.agreement("unsat", "sat") == "disagree" and crosscheck.agreement("sat", "unsat") == "disagree"
    for unclear in ("unknown", "timeout", "error"):
        assert crosscheck.agreement("unsat", unclear) == "inconclusive"
        assert crosscheck.agreement(unclear, "sat") == "inconclusive"


@needs_cvc5
def test_cvc5_answers_exported_formulas_as_arithmetic_says() -> None:
    x = z3.Int("x")
    assert crosscheck.ask(CVC5, crosscheck.smtlib([x > 0, x < 0]), 5000) == "unsat"
    assert crosscheck.ask(CVC5, crosscheck.smtlib([x > 0, x < 2]), 5000) == "sat"
    assert crosscheck.ask(CVC5, "(this is not smt-lib", 5000) == "error"
    assert crosscheck.ask(Path("/nonexistent/cvc5"), "(check-sat)", 5000) == "error"


@needs_cvc5
@pytest.mark.integration
def test_both_solvers_judge_the_obligations_of_a_wrong_and_a_right_program() -> None:
    wrong = '#include "pfc.h"\nlong f(long n, long a[n])\n{\n    return a[n];\n}\n'  # Always out of bounds.
    rows = crosscheck.one_program(("wrong", wrong, "clang-19", str(CVC5), 5000))
    bounds = [row for row in rows if row["kind"] == "bounds"]
    assert [(row["z3"], row["cvc5"], row["agreement"]) for row in bounds] == [("sat", "sat", "agree")]
    assert [row["agreement"] for row in rows if row["kind"] == "entry-consistency"] == ["agree"]
    right = wrong.replace("return a[n];", "return n;")
    assert all(
        row["agreement"] == "agree" for row in crosscheck.one_program(("right", right, "clang-19", str(CVC5), 5000))
    )
