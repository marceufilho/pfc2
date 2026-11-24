"""The adapter and the driver: real clang, hand-derived outcomes, and the interpreter beside the binaries."""

import json
import shutil
from pathlib import Path

import pytest

from pfc2.core.target import read_target
from pfc2_eval import adapter, build, hosts, interpret
from pfc2_eval.build import Outcome
from pfc2_eval.interpret import Inputs, Observation, Rejection

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "examples"
CLANG = shutil.which("clang-19") or shutil.which("clang") or "clang"
HEADER = '#include "pfc.h"\n'
pytestmark = pytest.mark.integration

PROGRAM = (
    "long total = 0;\n"
    "long add(long n, long a[n], long k)\n    requires(0 <= k && k < n)\n{\n"
    "    a[k] = a[k] + 1;\n    total = total + a[k];\n    return total;\n}\n"
)
CASES = [
    Inputs({"n": 2, "k": 1}, {"a": [5, 6]}, {"total": 10}),  # a[1] becomes 7; total 17.
    Inputs({"n": 2, "k": 0}, {"a": [2**63 - 1, 0]}, {"total": 0}),  # a[0] + 1 overflows.
    Inputs({"n": 2, "k": 2}, {"a": [1, 2]}, {"total": 0}),  # k is outside the contract and the array.
]


def test_parse_reads_only_complete_lines() -> None:
    text = "ok 17 | 5 7 G 17\nsignal 4\nsignal 11\nexit 1\nok 3 |\ngarbage\n"
    assert build.parse(text, 7, 1) == [
        Outcome("ok", 17, ((5, 7),), (17,)),
        Outcome("trap", detail=4),
        Outcome("signal", detail=11),
        Outcome("exit", detail=1),
        Outcome("missing"),  # No globals marker: the line was cut.
        Outcome("missing"),
        Outcome("missing"),  # Fewer lines than cases.
    ]


def test_each_variant_does_what_c_says_and_the_interpreter_names_the_same_cases(tmp_path: Path) -> None:
    target = read_target(CLANG)
    unit, certification = adapter.check(adapter.load_text(HEADER + PROGRAM, "add.c"), target, level="memory")
    assert certification.accepted and certification.c is not None
    program = adapter.released(unit)
    function = program.functions[0]
    variants = {
        "certified": (certification.c, False),
        "checked": (adapter.checked_c(unit, target), False),
        "plain": (adapter.plain_c(unit), True),
    }
    observed = {}
    for name, (text, plain) in variants.items():
        build.compile_c(build.with_driver(text, program, function), tmp_path / name, clang=CLANG, plain=plain)
        observed[name] = build.run_cases(tmp_path / name, program, function, CASES)
    fine = Outcome("ok", 17, ((5, 7),), (17,))
    assert [outcomes[0] for outcomes in observed.values()] == [fine, fine, fine]
    # Overflow: both instrumented builds trap; plain C is stopped by the sanitizer instead.
    assert observed["certified"][1].kind == observed["checked"][1].kind == "trap"
    assert observed["plain"][1].kind in {"exit", "signal"}
    # Outside the contract: the entry check of the certified C and the bounds check of the checked C trap.
    assert observed["certified"][2].kind == observed["checked"][2].kind == "trap"

    reference = [interpret.run(program, case, target=target, function="add") for case in CASES]
    assert isinstance(reference[0], Observation)
    assert (reference[0].result, reference[0].arrays, reference[0].globals) == (17, {"a": (5, 7)}, {"total": 17})
    assert [r.kind for r in reference[1:] if isinstance(r, Rejection)] == ["Overflow", "PreconditionViolated"]


def test_without_inference_a_loop_needs_its_invariant_and_admit_judges_a_supplied_one() -> None:
    target = read_target(CLANG)
    fill = (
        "long fill(long n, long a[n])\n{\n    for (long i = 0; i < n; i++) {\n"
        "        a[i] = 0;\n    }\n    return 0;\n}\n"
    )
    unit = adapter.load_text(HEADER + fill, "fill.c")
    assert adapter.check(unit, target)[1].accepted
    assert not adapter.check(unit, target, inference=False)[1].accepted
    assert adapter.admit(HEADER + fill, "fill.c", ("0 <= i && i <= n",), target).accepted
    assert adapter.admit(HEADER + fill, "fill.c", ("0 <= i && i <= n + 1",), target).accepted  # Weaker, enough.
    assert not adapter.admit(HEADER + fill, "fill.c", ("i <= n",), target).accepted  # True, but i may be negative.
    assert not adapter.admit(HEADER + fill, "fill.c", ("1 <= i",), target).accepted  # False at entry.


CONSOLE = [case for case in json.loads((EXAMPLES / "examples.json").read_text()) if "stdin" in case]


@pytest.mark.parametrize("case", CONSOLE, ids=lambda c: c["path"])
def test_the_console_model_prints_what_the_example_is_recorded_to_print(case: dict[str, str]) -> None:
    unit = adapter.load(EXAMPLES / case["path"])
    host = hosts.ConsoleHost(unit.strings, (EXAMPLES / case["stdin"]).read_text(encoding="utf-8"))
    observed = interpret.run(
        adapter.released(unit), Inputs(), target=read_target(CLANG), function=interpret.ENTRY, host=host
    )
    assert isinstance(observed, Observation), observed
    assert observed.output == (EXAMPLES / case["expected"]).read_text(encoding="utf-8")
    assert observed.result == 0 and observed.annotation_violations == ()
