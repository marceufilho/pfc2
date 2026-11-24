"""E10: probe programs, candidate families, Houdini filtering, the model loop and the summary."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pfc2.core.target import read_target
from pfc2_eval import adapter, evidence, heldout, sources

FILL = """#include "pfc.h"

long fill(long n, long a[n])
{
    long i = 0;
    for (i = 0; i < n; i++)
    {
        a[i] = 0;
    }
    return 1;
}
"""
UP = """#include "pfc.h"

long up(long n)
{
    long i = 0;
    long k = 0;
    while (i < n) {
        i++;
        k++;
    }
    assert(k == i);
    return 0;
}
"""


@pytest.fixture(scope="module")
def target():  # type: ignore[no-untyped-def]
    return read_target("clang-19")


def test_loops_are_found_in_source_order_and_comments_do_not_count() -> None:
    text = (
        "/* for (;;) { } */\nlong f(long n) {\n  for (long i = 0; i < n; i++) {\n    while (i < 3) { i++; }\n  }\n}\n"
    )
    found = sources.loops(text)
    assert [item.keyword for item in found] == ["for", "while"]
    assert text[found[0].open : found[0].close + 1] == "(long i = 0; i < n; i++)"
    assert found[0].body_close > found[1].body_close


@pytest.mark.parametrize(
    "text",
    [
        "long f(long n) { do { n--; } while (n > 0); return n; }",
        "long f(long n) { while (n > 0) { n--; continue; } return n; }",
        "long f(long n) { while (n > 0) n--; return n; }",
        "long f(long n) { while (n > 0) invariant(n >= 0) { n--; } return n; }",
    ],
)
def test_a_loop_that_cannot_be_probed_is_refused(text: str) -> None:
    with pytest.raises(ValueError):
        sources.loops(text)


def test_a_probe_asserts_each_candidate_before_the_loop_and_after_the_update(target) -> None:  # type: ignore[no-untyped-def]
    probe, lines = sources.build_probe(FILL, [["0 <= i", "i <= 3"]], [(0, 0), (0, 1)])
    assert f"long {sources.PROBE} = 0;" in probe
    assert "while (i < n) invariant((0 <= i) && (i <= 3)) {" in probe
    assert sorted(lines.values()) == [(0, 0), (0, 0), (0, 1), (0, 1)]
    body = probe[probe.index("while (i < n)") :]
    assert body.index("i++;") < body.index("assert(")
    unit = adapter.load_text(probe, "fill.c")
    results = adapter.check(unit, target, level="memory", inference=False)[1].proof.results
    by_candidate: dict[tuple[int, int], list[str]] = {}
    for item in results:
        if item.obligation.kind == "assert" and item.obligation.location.line in lines:
            by_candidate.setdefault(lines[item.obligation.location.line], []).append(item.status)
    assert by_candidate[(0, 0)] == ["proved", "proved"]
    assert sorted(by_candidate[(0, 1)]) == ["failed", "proved"]


def test_the_b1_family_bounds_each_scalar_by_the_others_and_by_the_constants() -> None:
    function = adapter.load_text(FILL, "fill.c").program.functions[0]
    (family,) = sources.family_b1(function, FILL)
    assert sources.constants(FILL) == (0, 1)
    assert set(family) == {
        "n <= i",
        "i <= n",
        "n <= 0",
        "0 <= n",
        "n <= 1",
        "1 <= n",
        "i <= 0",
        "0 <= i",
        "i <= 1",
        "1 <= i",
    }


def test_houdini_keeps_the_inductive_bounds_and_the_result_is_admitted(target) -> None:  # type: ignore[no-untyped-def]
    function = adapter.load_text(FILL, "fill.c").program.functions[0]
    filtered = sources.houdini(FILL, "fill.c", sources.family_b1(function, FILL), target, sources.ROUNDS)
    assert filtered.status == "fixpoint" and filtered.candidates == 10
    assert "(0 <= i)" in filtered.invariants[0] and "(i <= 0)" not in filtered.invariants[0]
    assert adapter.admit(FILL, "fill.c", filtered.invariants, target, level="memory").accepted
    assert not adapter.admit(FILL, "fill.c", (sources.TRUE,), target, level="memory").accepted


def test_one_round_is_not_always_enough(target) -> None:  # type: ignore[no-untyped-def]
    function = adapter.load_text(FILL, "fill.c").program.functions[0]
    filtered = sources.houdini(FILL, "fill.c", sources.family_b1(function, FILL), target, 1)
    assert filtered.status == "round-limit" and filtered.rounds == 1


def test_observed_candidates_follow_the_grammar() -> None:
    states = [{"i": value, "k": value, "n": 7, "j": 2 * value + 1} for value in range(25)]
    found = sources.observed_candidates(states)
    assert "n == 7" in found and "i == k" in found and "0 <= i" in found and "i <= k" in found
    assert "j == 2 * i + 1" in found
    assert "i <= 24" not in found  # An observed extreme beyond the small constants is an artefact of the inputs.
    assert sources.observed_candidates(states[:5]) == []


def test_b2_observes_loop_heads_and_proves_the_assertion_b1_also_proves(target) -> None:  # type: ignore[no-untyped-def]
    unit = adapter.load_text(UP, "up.c")
    function = unit.program.functions[0]
    families, accepted = sources.family_b2(unit, function, target, "0:up")
    assert accepted == sources.INPUTS and "i == k" in families[0]
    filtered = sources.houdini(UP, "up.c", families, target, sources.ROUNDS)
    assert adapter.admit(UP, "up.c", filtered.invariants, target, level="memory").accepted


def test_the_model_loop_feeds_the_refusal_back_only_with_feedback(target) -> None:  # type: ignore[no-untyped-def]
    prompts: list[str] = []
    replies = iter(['{"invariants": ["i <= 0"]}', "not json", '{"invariants": ["0 <= i && i <= n"]}'])

    def ask(prompt: str) -> str:
        prompts.append(prompt)
        return next(replies)

    success, used, transcript = sources.model_run(FILL, "fill.c", target, ask, feedback=True)
    assert (success, used) == (True, 3)
    assert "The checker refused" in prompts[1] and "could not be used" in prompts[2]
    assert transcript[0]["accepted"] is False and "problem" in transcript[1] and transcript[2]["accepted"] is True

    prompts.clear()
    success, used, transcript = sources.model_run(
        FILL, "fill.c", target, lambda p: (prompts.append(p), "{}")[1], feedback=False
    )
    assert (success, used) == (False, sources.ATTEMPTS)
    assert len(set(prompts)) == 1 and prompts[0] == sources.instruction(FILL, 1)


def _rows(l1: list[int]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index in range(10):
        base = {"program": f"p{index}", "family": "f", "rounds_budget": None, "run": None, "attempts": None}
        rows.append({**base, "condition": "N", "success": False})
        rows.append({**base, "condition": "I", "success": index < 4})
        for budget in (sources.ROUNDS, sources.ROUNDS_SENSITIVITY):
            rows.append({**base, "condition": "B1", "rounds_budget": budget, "success": index < 4})
            rows.append({**base, "condition": "B2", "rounds_budget": budget, "success": index < 5})
        for run in range(1, 3):
            rows.append({**base, "condition": "L1", "run": run, "success": index < l1[run - 1], "attempts": 1})
            rows.append({**base, "condition": "L2", "run": run, "success": index < 6, "attempts": 2})
    return rows


def test_the_summary_computes_the_registered_contrasts_by_program() -> None:
    summary = sources.summarise(_rows([10, 8]))
    assert summary["conditions"]["I"]["successes"] == 4 and summary["conditions"]["L1"]["trials"] == 20  # type: ignore[index]
    contrasts = summary["registered_contrasts"]
    assert contrasts["I - N"]["difference"] == 0.4 and contrasts["I - N"]["supported"] is True  # type: ignore[index]
    assert contrasts["L1 - I"]["difference"] == 0.5 and contrasts["L1 - I"]["supported"] is True  # type: ignore[index]
    assert contrasts["L1 - B2"]["difference"] == 0.4  # type: ignore[index]
    assert summary["no_power_for_model_contrasts"] is False
    assert summary["exploratory"]["certified under exactly one condition"]["L1"] == ["p6", "p7", "p8", "p9"]  # type: ignore[index]


def test_a_difference_below_the_threshold_is_not_supported() -> None:
    summary = sources.summarise(_rows([5, 5]))
    assert summary["registered_contrasts"]["L1 - I"]["difference"] == 0.1  # type: ignore[index]
    assert summary["registered_contrasts"]["L1 - I"]["supported"] is False  # type: ignore[index]


def test_a_small_campaign_without_the_model_seals(tmp_path: Path) -> None:
    directory = tmp_path / "set"
    directory.mkdir()
    (directory / "fill.c").write_text(FILL, encoding="utf-8")
    tasks = [{"task": "fill", "family": "toy", "sha256": "x"}, {"task": "gone", "family": "toy", "excluded": "goto"}]
    (directory / "PROVENANCE.json").write_text(json.dumps({"tasks": tasks}), encoding="utf-8")
    heldout.seal(directory, rule="test", candidate=None)
    output = tmp_path / "out"
    assert sources.run(
        directory=directory, output=output, compiler="clang-19", seed=0, live=False, progress=lambda t: None
    )
    loaded = evidence.load(output)
    summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    assert summary["programs"] == 1 and summary["model_ran"] is False
    assert summary["conditions"]["N"]["successes"] == 0 and summary["conditions"]["I"]["successes"] == 1
    assert summary["conditions"]["B1"]["successes"] == 1
    assert len(loaded.observations) == 6
    (directory / "fill.c").write_text(FILL + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="differs from its seal"):
        sources.run(directory=directory, output=tmp_path / "again", compiler="clang-19", seed=0, live=False)
