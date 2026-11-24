"""Mutation gaps of core/authorization.py: a proof report is admitted only when every identity in it is exact.

`gate.certify` always hands `authorize` the report that `smt.check` has just computed for the same program, target
and timeout, so no source file can reach these rejections. Each test therefore calls `authorize` directly with a
real report in which exactly one field of one entry was tampered with; the rule under test is that proofs match the
exact obligation, query and settings, whoever built the report.
"""

from dataclasses import replace

import pytest

from pfc2 import frontend
from pfc2.core import ir, smt, vc
from pfc2.core.authorization import Authorization, authorize
from pfc2.core.target import Target

TARGET = Target("test LP64 layout (no clang queried)", "x86_64-pc-linux-gnu", 32, 64)
# Every obligation is provable: the declared types bound the index and the counter, and nothing accumulates.
FILL = """#include "pfc.h"

long fill(long n, long a[n], long value)
{
    long i where(0 <= i && i <= n) = 0;

    while (i < n) {
        a[i] = value;
        i = i + 1;
    }
    return 0;
}
"""
Fresh = tuple[ir.Program, vc.VCReport, smt.CheckReport]


@pytest.fixture(scope="module")
def fresh() -> Fresh:
    program = frontend.load_text(FILL, "fill.c").program
    return program, vc.generate(program), smt.check(program, TARGET, timeout_ms=10_000)


def decide(fresh: Fresh, proof: smt.CheckReport) -> Authorization:
    program, conditions, _ = fresh
    return authorize(program, conditions, TARGET, proof)


def swap(items: tuple, index: int, item: object) -> tuple:  # type: ignore[type-arg]
    return (*items[:index], item, *items[index + 1 :])


@pytest.mark.integration
def test_untampered_report_is_admitted_with_every_obligation(fresh: Fresh) -> None:
    """The baseline of every case below: one entry query, several proved obligations, all admitted."""
    _, conditions, proof = fresh
    assert len(proof.entry_results) == 1 and len(proof.results) >= 3
    assert all(r.status == "proved" for r in proof.results)
    decision = decide(fresh, proof)
    assert decision.allowed and set(decision.proved) == {o.id for o in conditions.obligations}


@pytest.mark.integration
def test_entry_result_with_another_query_id_is_rejected(fresh: Fresh) -> None:
    """Only the query id is altered (the id of other settings); the query itself is the expected one."""
    proof = fresh[2]
    stale = replace(proof.entry_results[0], query_id="0" * 64)
    decision = decide(fresh, replace(proof, entry_results=(stale,)))
    assert (decision.allowed, decision.reason, decision.proved) == (False, "entry consistency identity mismatch", ())


@pytest.mark.integration
def test_entry_result_answering_another_query_under_the_expected_id_is_rejected(fresh: Fresh) -> None:
    """Only the query is altered (no hypotheses, so trivially consistent); its id is the expected one."""
    proof = fresh[2]
    entry = proof.entry_results[0]
    assert entry.query.hypotheses != ()
    other = replace(entry, query=replace(entry.query, hypotheses=()))
    decision = decide(fresh, replace(proof, entry_results=(other,)))
    assert (decision.allowed, decision.reason, decision.proved) == (False, "entry consistency identity mismatch", ())


@pytest.mark.integration
def test_duplicated_result_is_rejected(fresh: Fresh) -> None:
    proof = fresh[2]
    decision = decide(fresh, replace(proof, results=(*proof.results, proof.results[-1])))
    assert (decision.allowed, decision.reason, decision.proved) == (
        False,
        "missing, duplicate or extra proof results",
        (),
    )


@pytest.mark.integration
@pytest.mark.parametrize("dropped", [0, -1])
def test_missing_result_is_rejected_as_an_incomplete_report_and_admits_nothing(fresh: Fresh, dropped: int) -> None:
    """Not merely 'one obligation unproved': the other results of an incomplete report are not admitted either."""
    proof = fresh[2]
    results = tuple(r for r in proof.results if r is not proof.results[dropped])
    assert len(results) == len(proof.results) - 1
    decision = decide(fresh, replace(proof, results=results))
    assert (decision.allowed, decision.reason, decision.proved) == (
        False,
        "missing, duplicate or extra proof results",
        (),
    )


@pytest.mark.integration
def test_extra_result_for_an_unknown_obligation_is_rejected(fresh: Fresh) -> None:
    proof = fresh[2]
    last = proof.results[-1]
    unknown = replace(last, obligation=replace(last.obligation, id="bounds:" + "0" * 64))
    decision = decide(fresh, replace(proof, results=(*proof.results, unknown)))
    assert (decision.allowed, decision.reason, decision.proved) == (
        False,
        "missing, duplicate or extra proof results",
        (),
    )


@pytest.mark.integration
@pytest.mark.parametrize("index", [0, -1])
def test_proved_result_with_another_query_id_is_rejected(fresh: Fresh, index: int) -> None:
    """Only the query id is altered (a proof made under other settings); the obligation is the expected one."""
    proof = fresh[2]
    position = index % len(proof.results)
    stale = replace(proof.results[position], query_id="0" * 64)
    decision = decide(fresh, replace(proof, results=swap(proof.results, position, stale)))
    assert (decision.allowed, decision.reason, decision.proved) == (False, "obligation or query identity mismatch", ())


@pytest.mark.integration
@pytest.mark.parametrize("index", [0, -1])
def test_proved_result_for_an_altered_obligation_under_the_expected_ids_is_rejected(fresh: Fresh, index: int) -> None:
    """Only the obligation's content is altered (an extra hypothesis-free copy); its id and query id are intact."""
    proof = fresh[2]
    position = index % len(proof.results)
    result = proof.results[position]
    assert result.obligation.hypotheses != ()
    altered = replace(result, obligation=replace(result.obligation, hypotheses=result.obligation.hypotheses[:-1]))
    decision = decide(fresh, replace(proof, results=swap(proof.results, position, altered)))
    assert (decision.allowed, decision.reason, decision.proved) == (False, "obligation or query identity mismatch", ())
