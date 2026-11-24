"""Proof file: a separate, self-contained record that is recomputed, never trusted."""

import copy
import json
from pathlib import Path

from pfc2 import frontend, gate, proof
from pfc2.check import check
from pfc2.core.target import Target

FIXTURES = Path(__file__).parent / "fixtures"
TARGET = Target("test LP64 layout (no clang queried)", "x86_64-pc-linux-gnu", 32, 64)


def record(name: str, level: gate.Level = "full") -> dict[str, object]:
    return proof.build(*check(frontend.load(FIXTURES / name), TARGET, level=level))


def test_proof_file_states_the_law_the_proof_and_every_obligation():
    data = record("count.c")
    assert data["format"] == proof.FORMAT and data["level"] == "full"
    assert data["law"] == [
        {"function": "count", "kind": "precondition", "binder": "n", "predicate": "0 <= n", "line": 3},
        {"function": "count", "kind": "postcondition", "binder": "count", "predicate": "RESULT == n", "line": 3},
    ]
    assert data["proof"] == [
        {"function": "count", "kind": "type", "binder": "i", "predicate": "0 <= i && i <= n", "line": 5}
    ]
    obligations = data["obligations"]
    assert isinstance(obligations, list) and len(obligations) == 6
    assert {o["status"] for o in obligations} == {"proved"}
    assert all(o["id"].startswith(o["kind"] + ":") and len(o["query_id"]) == 64 and o["goal"] for o in obligations)
    assert data["boundary"] == {"checked": ["(0 <= n)"], "unchecked": []}
    assert data["retained_traps"] == []
    json.dumps(data)  # plain JSON data


def test_proof_file_has_no_wall_clock_fields():
    assert "elapsed" not in json.dumps(record("count.c"))
    assert record("count.c") == record("count.c")


def test_replay_recomputes_the_same_record_without_the_source_file():
    data = json.loads(json.dumps(record("fill.c")))
    assert proof.replay(data) == []


def test_replay_reports_an_edited_status_c_text_or_law():
    original = json.loads(json.dumps(record("count.c")))
    edited = copy.deepcopy(original)
    edited["obligations"][0]["status"] = "failed"
    assert proof.replay(edited) == ["obligations"]
    edited = copy.deepcopy(original)
    edited["c"] = edited["c"].replace("return i;", "return 0;")
    assert edited["c"] != original["c"] and proof.replay(edited) == ["c"]
    edited = copy.deepcopy(original)
    edited["preprocessed"] = edited["preprocessed"].replace("0 <= i && i <= n", "0 <= i")
    assert "proof" in proof.replay(edited)


def test_replay_refuses_a_record_whose_program_no_longer_certifies():
    data = json.loads(json.dumps(record("count.c")))
    data["preprocessed"] = data["preprocessed"].replace("i <= n) = 0", "i < n) = 0")
    assert "accepted" in proof.replay(data)


def test_replay_rejects_malformed_records():
    assert proof.replay({"format": "something-else"}) == ["format"]
    assert proof.replay([]) == ["format"]
    data = json.loads(json.dumps(record("count.c")))
    data["solver"]["z3"] = "0.0.0"
    assert proof.replay(data) == ["solver"]


def test_memory_level_lists_the_trap_it_keeps():
    data = record("sum.c", "memory")
    assert data["level"] == "memory"
    (trap,) = data["retained_traps"]
    assert trap["kind"] == "overflow" and trap["line"] == 9
