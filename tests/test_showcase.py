"""The showcase programs get the verdicts written by hand in showcase/showcase.json, and the site data says so."""

import importlib.util
import json
from pathlib import Path

import pytest

from pfc2 import web

ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "showcase" / "showcase.json").read_text(encoding="utf-8"))
MODEL_INVARIANT = (
    "n == 4 && 0 <= i && i <= n && 0 <= right && right <= i && ((right == i) == ((i < 1 || keys[0] == 3) && "
    "(i < 2 || keys[1] == 1) && (i < 3 || keys[2] == 4) && (i < 4 || keys[3] == 1)))"
)


def _site_data():
    spec = importlib.util.spec_from_file_location("site_data", ROOT / "tools" / "site_data.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _analyze(case: dict) -> dict:
    path = ROOT / "showcase" / case["path"]
    return web.analyze(path.read_text(encoding="utf-8"), name=path.name, level=case.get("level", "full"))


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["path"])
def test_each_program_gets_the_verdict_written_by_hand(case: dict) -> None:
    outcome = _analyze(case)
    assert outcome["ok"]
    if "refused" in case:
        first = next(b for b in outcome["blockers"] if b["kind"] == case["refused"]["kind"])
        assert not outcome["accepted"] and outcome["c"] is None
        assert first["line"] == case["refused"]["line"] and first["status"] == "failed" and first["example"]
        return
    summary = web.summary(outcome)
    assert outcome["accepted"] and all(status == "proved" for _, status in summary["obligations"])
    assert sum(removed for _, _, removed in summary["guards"]) == case["guards"] == len(summary["guards"])
    assert len(outcome["record"]["law"]) == case.get("laws", 0)


def test_the_wrong_midpoint_is_refused_with_the_two_numbers_that_overflow() -> None:
    blocker = _analyze(CASES[0])["blockers"][0]
    assert blocker["goal"] == "((LONG_MIN <= (lo + hi)) && ((lo + hi) <= LONG_MAX))"
    values = dict(part.split(" = ") for part in blocker["example"].split(", "))
    assert 0 <= int(values["lo"]) <= int(values["hi"]) and int(values["lo"]) + int(values["hi"]) > 2**63 - 1


def test_the_committed_lock_carries_the_invariant_the_recorded_model_run_had_admitted() -> None:
    record = json.loads((ROOT / "showcase/lock/model-proof.json").read_text(encoding="utf-8"))
    assert record["accepted"] and record["level"] == "full" and MODEL_INVARIANT in json.dumps(record)
    committed = " ".join((ROOT / "showcase/lock/lock.c").read_text(encoding="utf-8").split())
    assert f"invariant({MODEL_INVARIANT})" in committed
    without = (ROOT / "showcase/lock/lock_without_invariant.c").read_text(encoding="utf-8")
    assert "invariant(" not in without


def test_the_copy_paste_lock_is_refused_with_a_fourth_key_that_should_not_open_it() -> None:
    blocker = next(b for b in _analyze(CASES[4])["blockers"] if b["kind"] == "postcondition")
    values = dict(part.split(" = ") for part in blocker["example"].split(", "))
    assert [values[f"keys[{i}]"] for i in range(3)] == ["3", "1", "4"] and values["keys[3]"] != "1"


def test_site_data_runs_every_digit_combination_through_the_compiled_lock() -> None:
    site = _site_data()
    data = site.showcase(ROOT)
    by_path = {entry["path"]: entry for entry in data["programs"]}
    assert list(by_path) == [case["path"] for case in CASES]
    for case in CASES:
        entry = by_path[case["path"]]
        assert entry["accepted"] == ("refused" not in case) and entry["source"].startswith('#include "pfc.h"')
        if "openers" in case:
            assert entry["openers"] == case["openers"] and entry["tried"] == 10_000
            assert entry["certified_c"] == entry["accepted"]
    assert by_path["midpoint/midpoint_wrong.c"]["refusal"][0]["meaning"] == "this arithmetic may overflow"
    assert site.build(ROOT)["public/data/showcase.json"] == site._json(data)  # Two builds give the same text.
    assert by_path["lock/lock.c"]["proved"] == by_path["lock/lock.c"]["obligations"] == 55
