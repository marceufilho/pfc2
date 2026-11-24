"""Defects found by the engine audit of 2026-11-18, each as a permanent test, with a guard for its class.

Every program here once got a wrong answer from PFC2. Expectations are derived from the C semantics of the
program, not from the tool.
"""

import re
from pathlib import Path

import pytest

from pfc2 import frontend
from pfc2.check import check
from pfc2.core.diagnostics import FrontendError
from pfc2.core.target import Target
from pfc2.elaborate import Unit
from pfc2.gate import Certification
from pfc2.preprocess import preprocess

TARGET = Target("static LP64 layout (test)", "x86_64-pc-linux-gnu", 32, 64)
EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
HEADER = '#include "pfc.h"\n'


def _check(text: str, level: str = "full") -> tuple[Unit, Certification]:
    return check(frontend.load_text(HEADER + text, "t.c"), TARGET, level=level)  # type: ignore[arg-type]


def _refused(text: str) -> str:
    with pytest.raises(FrontendError) as error:
        _check(text)
    return error.value.diagnostic.rule


# F1 ------------------------------------------------------------------------------------------------------------
def test_a_source_name_cannot_collide_with_a_name_the_emitter_generates() -> None:
    shadowed = (
        "long pfc_tmp_1 = 0;\nlong get(long n, long a[n])\n    requires(n == 1 && pfc_tmp_1 == 0)\n"
        "{\n    long y = n + 5;\n    return a[pfc_tmp_1];\n}\n"
    )
    assert _refused(shadowed) == "ir-name"
    assert _refused("long pfc_entry_1 = 0;\nlong f(void)\n{\n    return pfc_entry_1;\n}\n") == "ir-name"
    assert _refused("long f(long pfc_x)\n{\n    return pfc_x;\n}\n") == "ir-name"


@pytest.mark.integration
@pytest.mark.parametrize("path", sorted(EXAMPLES.rglob("*.c")), ids=lambda p: p.name)
def test_no_declaration_in_the_emitted_c_reuses_a_name_of_the_source(path: Path) -> None:
    unit, certification = check(frontend.load(path), TARGET, level="memory")
    if certification.c is None:
        return
    source = {g.symbol.name for g in unit.program.globals}
    for function in unit.program.functions:
        source |= {p.symbol.name for p in function.parameters}
    declared = re.findall(r"^\s+(?:long|int|_Bool) (pfc_\w+)", certification.c, flags=re.MULTILINE)
    assert declared and not source & set(declared)
    assert len(declared) == len(set(declared)) or len(unit.program.functions) > 1


# F2 ------------------------------------------------------------------------------------------------------------
TICK = (
    "long k = 0;\nlong tick(void)\n    requires(0 <= k && k < 1000)\n    ensures(result == 1 && k >= 1)\n"
    "{\n    k = k + 1;\n    return 1;\n}\n"
)


def test_an_assert_cannot_run_code_only_a_law_may_call_inside_assert() -> None:
    # Compiled as plain C the assert is never evaluated, so k would stay 0 and the postcondition would be false.
    hidden = (
        "long f(long x)\n    requires(k == 0)\n    ensures(k >= 1)\n{\n    assert(tick() == 1);\n    return x;\n}\n"
    )
    assert _refused(TICK + hidden) == "assert-call"
    law = "law ticking_returns_one(long x where(x == 0))\n{\n    assert(tick() == 1 || k < 0 || k >= 1000);\n}\n"
    unit, certification = _check(TICK + law.replace(" || k < 0 || k >= 1000", ""))
    assert not certification.accepted  # The law does not state k's range, so the call's precondition fails...
    assert [b.kind for b in certification.blockers if not b.status.startswith("depends")] == ["call-precondition"]
    assert certification.c is None  # ...but a call inside a law's assert is accepted as source.


# F3 ------------------------------------------------------------------------------------------------------------
STUCK = "long f(long n) requires(1 <= n) { while (0 < n) decreases(n) { n = n + 0; } return n; }\n"


def test_a_measure_is_attached_whatever_the_layout_and_a_loop_that_never_ends_is_not_called_terminating() -> None:
    unit, certification = _check(STUCK)
    assert len(unit.measures) == 1 and not certification.accepted
    assert "assert" in [b.kind for b in certification.blockers]
    spread = (
        STUCK.replace(" requires", "\n    requires")
        .replace(" { while", "\n{\n    while")
        .replace(" return", "\n    return")
    )
    assert not _check(spread)[1].accepted


@pytest.mark.integration
@pytest.mark.parametrize("path", sorted(EXAMPLES.rglob("*.c")), ids=lambda p: p.name)
def test_joining_a_program_onto_fewer_lines_changes_no_verdict(path: Path) -> None:
    """Metamorphic guard: clause attachment must not depend on where line breaks fall."""
    text = path.read_text(encoding="utf-8")
    joined = re.sub(r"\)\n(\s*)(requires|ensures)\(", r") \2(", text)  # Signature clauses onto the declarator's line.
    joined = re.sub(r"\)\n\{", ") {", joined)  # The opening brace of a function body too.
    assert joined != text or "requires(" not in text
    results = []
    for source in (text, joined):
        unit, certification = check(frontend.load_text(source, path.name), TARGET, level="memory")
        blockers = sorted({b.kind for b in certification.blockers if not b.status.startswith("depends")})
        results.append((certification.accepted, len(unit.measures), len(unit.inferred), blockers))
    assert results[0] == results[1]


# F4 ------------------------------------------------------------------------------------------------------------
def test_a_call_in_the_index_of_a_compound_assignment_runs_once() -> None:
    counted = (
        "long cnt = 0;\nlong next(long e)\n    requires(cnt == e && 0 <= e && e < 100)\n"
        "    ensures(cnt == e + 1 && result == 0)\n{\n    cnt = cnt + 1;\n    return 0;\n}\n"
        "long bump(long n, long a[n])\n    requires(n == 1 && cnt == 0)\n    requires(-5 <= a[0] && a[0] <= 5)\n"
        "    ensures(cnt == CALLS)\n{\n    a[next(cnt)] += 1;\n    return 0;\n}\n"
    )
    once = _check(counted.replace("CALLS", "1"))[1]
    assert once.accepted and once.c is not None and once.c.count("= next(") == 1
    assert not _check(counted.replace("CALLS", "2"))[1].accepted
    stepped = _check(counted.replace("CALLS", "1").replace("a[next(cnt)] += 1;", "a[next(cnt)]++;"))[1]
    assert stepped.accepted and stepped.c is not None and stepped.c.count("= next(") == 1


# F5 ------------------------------------------------------------------------------------------------------------
def test_macros_are_not_replaced_inside_numbers_and_are_rescanned_as_cpp_does() -> None:
    assert (
        preprocess("#define L 7\n#define xFF 1\nlong a = 10L + 0xFF;\n", "t.c", {}).splitlines()[-1]
        == "long a = 10L + 0xFF;"
    )
    assert preprocess("#define A B\n#define B 1\nlong a = A;\n", "t.c", {}).splitlines()[-1] == "long a = 1;"
    assert (
        preprocess("#define A A\nlong A = 1;\n", "t.c", {}).splitlines()[-1] == "long A = 1;"
    )  # No endless expansion.
    for keyword in ("long", "return", "requires", "result", "while"):
        with pytest.raises(FrontendError) as error:
            preprocess(f"#define {keyword} 1\n", "t.c", {})
        assert error.value.diagnostic.rule == "preprocess-unsupported"


# F6 ------------------------------------------------------------------------------------------------------------
def test_an_external_contract_that_some_array_contents_make_impossible_is_refused() -> None:
    first = "long first(long n, const long a[n])\n    requires(1 <= n)\n    ensures(result == a[0] && a[0] > 0);\n"
    use = (
        "long g(long n, long a[n])\n    requires(1 <= n)\n{\n    a[0] = 0 - 5;\n    long r = first(n, a);\n"
        "    return a[r + 100];\n}\n"
    )
    unit, certification = _check(first + use, "memory")
    assert not certification.accepted and "contract of first" in certification.reason
    (result,) = certification.proof.external_results
    assert result.total == "partial"  # Any array whose first element is not positive has no valid result.
    honest = first.replace(" && a[0] > 0", "")
    reads = _check(honest + "long g(long n, const long a[n])\n    requires(1 <= n)\n{\n    return first(n, a);\n}\n")[1]
    assert reads.accepted and reads.proof.external_results[0].total == "total"


# Smaller items -------------------------------------------------------------------------------------------------
def test_a_parameter_cannot_be_called_result_and_an_array_length_is_declared_before_its_array() -> None:
    assert _refused("long f(long result)\n    ensures(result == 0)\n{\n    return 0;\n}\n") == "ir-name"
    assert _refused("long f(long a[n], long n)\n{\n    return n;\n}\n") == "ir-array-length"


def test_a_typed_local_that_mentions_a_global_is_checked_again_after_a_call_that_writes_it() -> None:
    text = (
        "long g = 0;\nlong raise(void)\n    requires(g < 100)\n{\n    g = g + 50;\n    return 0;\n}\n"
        "long f(void)\n    requires(g == 0)\n{\n    long x where(x >= g) = 10;\n    raise();\n    return x;\n}\n"
    )
    certification = _check(text)[1]
    assert not certification.accepted and "assert" in [b.kind for b in certification.blockers]
