"""Proof bundles: the function and the law are written by hand, the proof arrives as data."""

import json
from pathlib import Path

import pytest

from pfc2 import bundle, frontend, proof, prove, surface
from pfc2.check import check
from pfc2.cli import main
from pfc2.core.diagnostics import FrontendError
from pfc2.core.target import Target

FIXTURES = Path(__file__).parent / "fixtures"
TARGET = Target("test LP64 layout (no clang queried)", "x86_64-pc-linux-gnu", 32, 64)
GOOD = '{"invariants": ["s == 2 * i"]}'


def test_program_without_a_proof_is_refused_and_reports_its_loops():
    unit = frontend.load(FIXTURES / "needs_proof.c")
    assert unit.loops == 1 and unit.invariants == ()
    assert not check(unit, TARGET)[1].accepted


def test_bundle_supplies_the_invariant_and_the_law_is_certified():
    unit = frontend.load(FIXTURES / "needs_proof.c", invariants=bundle.parse(GOOD, 1))
    unit, result = check(unit, TARGET)
    assert result.accepted and unit.invariants == ("s == 2 * i",)
    record = proof.build(unit, result)
    assert record["bundle"] == {"invariants": ["s == 2 * i"]}
    assert {
        "function": "twice",
        "kind": "invariant",
        "binder": "loop 1",
        "predicate": "s == 2 * i",
        "line": 10,
    } in (record["proof"])
    assert proof.replay(json.loads(json.dumps(record))) == []


def test_replay_notices_a_changed_bundle():
    unit = frontend.load(FIXTURES / "needs_proof.c", invariants=bundle.parse(GOOD, 1))
    record = json.loads(json.dumps(proof.build(*check(unit, TARGET))))
    record["bundle"]["invariants"] = ["0 <= s"]
    assert "accepted" in proof.replay(record)
    record["bundle"]["invariants"] = ["system(0)"]
    assert proof.replay(record) == ["format"]


@pytest.mark.parametrize(
    "reply",
    [
        "not json",
        "[]",
        '{"invariants": []}',
        '{"invariants": ["1", "1"]}',
        '{"invariants": ["f(i)"]}',
        '{"invariants": ["i; }"]}',
        '{"invariants": ["i /* x */"]}',
        '{"invariants": [1]}',
        '{"invariants": ["0 <= i"], "extra": 1}',
        '{"invariants": ["' + "i" * 20000 + '"]}',
    ],
)
def test_bundle_is_parsed_as_data_and_malformed_replies_are_rejected(reply):
    with pytest.raises(ValueError):
        bundle.parse(reply, 1)


def test_bundle_cannot_replace_a_handwritten_invariant_or_change_the_code():
    with pytest.raises(FrontendError) as error:
        frontend.load(FIXTURES / "count.c", invariants=("0 <= i",) * 2)
    assert error.value.diagnostic.rule == "proof-shape"
    text = (
        '# 1 "x.c"\nlong f(long n)\n{\n    while (n > 0) {\n        __spec_invariant(n >= 0);\n'
        "        n = n - 1;\n    }\n    return n;\n}\n"
    )
    with pytest.raises(FrontendError) as error:
        surface.extract(text, "x.c", invariants=("n >= 0",))
    assert error.value.diagnostic.rule == "proof-shape"


def test_prover_loop_retries_with_checker_feedback_and_stops_at_the_first_proof():
    replies = iter(['{"invariants": ["0 <= s"]}', "garbage", GOOD, '{"invariants": ["never asked"]}'])
    prompts: list[str] = []

    def ask(prompt: str, attempt: int) -> str:
        prompts.append(prompt)
        return next(replies)

    outcome = prove.prove(FIXTURES / "needs_proof.c", TARGET, ask=ask)
    assert outcome.certification is not None and outcome.certification.accepted
    assert outcome.unit is not None and outcome.unit.invariants == ("s == 2 * i",)
    assert [a.accepted for a in outcome.attempts] == [False, False, True]
    assert "law twice_is_double" in prompts[0] and "while (i < n)" in prompts[0]
    assert "1 loop" in prompts[0]
    assert '{"invariants": ["0 <= s"]}' in prompts[1] and "cannot prove" in prompts[1]
    assert outcome.attempts[1].problem is not None


def test_prover_loop_is_bounded_and_a_failed_proof_certifies_nothing():
    calls = []

    def ask(prompt: str, attempt: int) -> str:
        calls.append(attempt)
        return '{"invariants": ["1"]}'

    outcome = prove.prove(FIXTURES / "needs_proof.c", TARGET, ask=ask)
    assert calls == [1, 2, 3, 4, 5] and outcome.certification is None and outcome.unit is None


def test_transport_failure_consumes_an_attempt():
    def ask(prompt: str, attempt: int) -> str:
        if attempt == 1:
            raise OSError("network down")
        return GOOD

    outcome = prove.prove(FIXTURES / "needs_proof.c", TARGET, ask=ask)
    assert [a.accepted for a in outcome.attempts] == [False, True]


def test_cli_build_with_a_proof_file_and_reuse_of_an_earlier_one(capsys, tmp_path):
    hint = tmp_path / "hint.json"
    hint.write_text(GOOD, encoding="utf-8")
    source = str(FIXTURES / "needs_proof.c")
    assert main(["check", source]) == 1
    assert "--proof" in capsys.readouterr().out
    output = tmp_path / "out"
    assert main(["build", source, "--proof", str(hint), "--output", str(output)]) == 0
    capsys.readouterr()
    record = output / "needs_proof.proof.json"
    assert json.loads(record.read_text(encoding="utf-8"))["bundle"] == {"invariants": ["s == 2 * i"]}
    # The proof file written by build is itself accepted as the proof of the next build.
    assert main(["check", source, "--proof", str(record)]) == 0
    assert "proof twice: loop 1 invariant s == 2 * i" in capsys.readouterr().out
    bad = tmp_path / "bad.json"
    bad.write_text('{"invariants": ["f(i)"]}', encoding="utf-8")
    assert main(["check", source, "--proof", str(bad)]) == 1
    assert "proof" in capsys.readouterr().err


def test_cli_live_proving_is_opt_in_and_needs_a_key(capsys, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    assert main(["check", str(FIXTURES / "needs_proof.c"), "--prove"]) == 1
    assert "OPENAI_API_KEY" in capsys.readouterr().err
