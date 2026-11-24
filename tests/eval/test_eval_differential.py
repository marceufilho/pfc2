"""The judging rules of E1/E8 on hand-made outcomes, and one small real run on development seeds."""

import json
from pathlib import Path

import pytest

from pfc2 import frontend
from pfc2.core.target import Target
from pfc2_eval import differential, evidence
from pfc2_eval.build import Outcome
from pfc2_eval.interpret import Inputs, Observation, Rejection

TARGET = Target("static LP64 layout (test)", "x86_64-pc-linux-gnu", 32, 64)
FINE = Observation(5, {"a": (1, 2)}, {"g": 3}, "", 10, ())
SAME = Outcome("ok", 5, ((1, 2),), (3,))
TRAP = Outcome("trap", detail=4)


def judge(
    reference: Observation | Rejection,
    certified: Outcome,
    checked: Outcome,
    plain: Outcome | None,
    violation: str | None = None,
) -> str:
    return differential.judge(
        reference, {"certified": certified, "checked": checked, "plain": plain}, ["a"], ["g"], violation
    )[0]


def rejection(kind: str) -> Rejection:
    return Rejection(kind, "message", None)  # type: ignore[arg-type]


def test_an_accepted_input_requires_the_same_complete_observation_from_every_build() -> None:
    assert judge(FINE, SAME, SAME, SAME) == "agree"
    assert judge(FINE, Outcome("ok", 6, ((1, 2),), (3,)), SAME, SAME) == "differ"
    assert judge(FINE, SAME, Outcome("ok", 5, ((1, 9),), (3,)), SAME) == "differ"  # One array element.
    assert judge(FINE, SAME, SAME, Outcome("ok", 5, ((1, 2),), (4,))) == "differ"  # One global.
    assert judge(FINE, TRAP, SAME, SAME) == "differ"  # A trap on a valid input is a difference, not noise.
    assert judge(FINE, Outcome("missing"), SAME, SAME) == "failed"


def test_a_rejected_input_requires_a_trap_where_the_design_says_so() -> None:
    assert judge(rejection("Overflow"), TRAP, TRAP, None) == "trapped-as-required"
    assert judge(rejection("Overflow"), SAME, TRAP, None) == "missing-trap"  # The certified C ran on.
    assert judge(rejection("Overflow"), TRAP, Outcome("exit", detail=1), None) == "missing-trap"
    # Inside the entry contract, a certified program must not reach these at all.
    for kind in ("OutOfBounds", "DivisionByZero", "ConversionOutOfRange"):
        assert judge(rejection(kind), TRAP, TRAP, None) == "certified-unsafe"
    assert judge(rejection("PreconditionViolated"), TRAP, TRAP, None) == "certified-unsafe"  # A callee's contract.
    assert judge(rejection("PreconditionViolated"), TRAP, SAME, None, "rendered") == "trapped-as-required"
    assert judge(rejection("PreconditionViolated"), SAME, SAME, None, "rendered") == "missing-trap"
    assert judge(rejection("PreconditionViolated"), SAME, SAME, None, "skipped") == "unscored"
    assert judge(rejection("Inconclusive"), SAME, SAME, None) == "unscored"


def test_the_entry_contract_is_read_conjunct_by_conjunct() -> None:
    text = (
        '#include "pfc.h"\nlong f(long n, long a[n], long k)\n    requires(0 <= k && k < n)\n'
        "    requires(a[0] > 0)\n{\n    return a[k];\n}\n"
    )
    program = frontend.load_text(text, "t.c").program
    function = program.functions[0]
    parts = differential.conjuncts(function)
    assert len(parts) == 4  # 0 <= k, k < n, a[0] > 0, and the 0 <= n that `long a[n]` adds.
    rendered = [True, True, False, True]  # A conjunct about array contents has no entry check.

    def violation(k: int, first: int) -> str | None:
        case = Inputs({"n": 2, "k": k}, {"a": [first, 0]})
        return differential.entry_violation(program, function, case, rendered, TARGET)

    assert violation(1, 5) is None
    assert violation(2, 5) == "rendered"
    assert violation(1, 0) == "skipped"
    assert violation(2, 0) == "rendered"  # A rendered check is false, so the trap is required all the same.


@pytest.mark.integration
def test_a_small_run_on_development_seeds_is_sealed_and_counts_what_it_did(tmp_path: Path) -> None:
    output = tmp_path / "differential"
    differential.run(
        output=output, compiler="clang-19", seed=0, programs=8, cases=12, workers=4, progress=lambda _: None
    )
    assert evidence.status(output).complete
    summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    rows = evidence.load(output).observations
    programs = [row for row in rows if row["row"] == "program"]
    assert len(programs) == 8 and summary["certified_memory"] == sum(row["certified_memory"] for row in programs)
    cases = [row for row in rows if row["row"] == "case" and row["level"] == "memory"]
    assert len(cases) == 12 * summary["certified_memory"]
    assert summary["e9_replayed"] == summary["certified_memory"]


@pytest.mark.integration
def test_a_program_that_cannot_be_judged_in_time_is_recorded_as_not_judged() -> None:
    (row,) = differential.one_program((339, 5, "clang-19", 1))  # Development seed 339 needs minutes.
    assert row["certified_memory"] is False and row["refusal"] == "not judged within the time budget"


def test_a_timer_that_fires_inside_a_solver_binding_call_is_still_out_of_time(monkeypatch: pytest.MonkeyPatch) -> None:
    """ctypes wraps an exception raised while it converts an argument; observed once in a full run (amendment 25)."""
    import ctypes

    def wrapped(*arguments: object, **options: object) -> object:
        raise ctypes.ArgumentError("argument 1: _OutOfTime: ")

    monkeypatch.setattr(differential.adapter, "check", wrapped)
    (row,) = differential.one_program((0, 5, "clang-19", 600))
    assert row["certified_memory"] is False and row["refusal"] == "not judged within the time budget"

    def other(*arguments: object, **options: object) -> object:
        raise ctypes.ArgumentError("argument 1: TypeError: wrong type")

    monkeypatch.setattr(differential.adapter, "check", other)
    with pytest.raises(ctypes.ArgumentError):
        differential.one_program((0, 5, "clang-19", 600))
