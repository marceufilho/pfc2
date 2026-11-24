"""The pure entry point used by the playground: same verdicts as the command line, refusals as data."""

import ast
import json
from pathlib import Path

import pytest

from pfc2 import frontend, proof, web
from pfc2.check import check

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
COUNT = (EXAMPLES / "01_count" / "count.c").read_text(encoding="utf-8")


def test_a_program_is_checked_and_the_result_is_plain_json() -> None:
    result = web.analyze(COUNT, name="count.c")
    assert result["ok"] and result["accepted"] and result["level"] == "full"
    assert result["report"].startswith("count.c: certified (full)\n")
    assert "long count(long n)" in result["c"] and "INVARIANT" in result["elaborated"]
    assert result["record"]["inferred"] == [{"function": "count", "line": 11, "invariant": "((0 <= i) && (i <= n))"}]
    assert result["provenance"]["engine"] == web.ENGINE and result["provenance"]["target"]["long_bits"] == 64
    json.dumps(result)


def test_a_refused_program_reports_its_blockers_and_releases_no_c() -> None:
    result = web.analyze((EXAMPLES / "wrong" / "off_by_one.c").read_text(encoding="utf-8"), name="off_by_one.c")
    assert result["ok"] and not result["accepted"] and result["c"] is None
    first = result["blockers"][0]
    assert (first["kind"], first["line"], first["status"]) == ("bounds", 7, "failed")
    assert first["meaning"] == "this index may be outside the array" and "n = 0" in first["example"]
    memory = web.analyze((EXAMPLES / "03_sum" / "sum.c").read_text(encoding="utf-8"), name="sum.c", level="memory")
    assert memory["accepted"] and len(memory["record"]["retained_traps"]) == 1


@pytest.mark.parametrize(
    ("arguments", "rule"),
    [
        ({"source": "long f(void) { return 0 }\n"}, "parse-syntax"),
        ({"source": '#include "other.h"\n'}, "preprocess-include"),
        ({"source": "x" * (web.MAX_SOURCE_BYTES + 1)}, "engine-size"),
        ({"source": COUNT, "level": "none"}, "engine-usage"),
        ({"source": COUNT, "timeout_ms": 0}, "engine-usage"),
        ({"source": COUNT, "timeout_ms": True}, "engine-usage"),
        ({"source": COUNT, "name": "../x.c"}, "engine-usage"),
        ({"source": 3}, "engine-usage"),
    ],
)
def test_bad_input_is_a_diagnostic_not_an_exception(arguments: dict[str, object], rule: str) -> None:
    result = web.analyze(**arguments)  # type: ignore[arg-type]
    assert not result["ok"] and result["diagnostic"]["rule"] == rule


@pytest.mark.integration
@pytest.mark.parametrize("path", sorted(EXAMPLES.rglob("*.c")), ids=lambda p: str(p.relative_to(EXAMPLES)))
def test_the_web_entry_point_agrees_with_the_checked_path_on_every_example(path: Path) -> None:
    for level in ("full", "memory"):
        unit, certification = check(frontend.load(path), web.STATIC_TARGET, level=level)  # type: ignore[arg-type]
        expected = json.loads(json.dumps(proof.build(unit, certification)))
        result = web.analyze(path.read_text(encoding="utf-8"), name=path.name, level=level, timeout_ms=10_000)
        actual = json.loads(json.dumps(result["record"]))
        assert {k: v for k, v in actual.items() if k != "solver"} == {
            k: v for k, v in expected.items() if k != "solver"
        }


def test_the_browser_path_imports_no_process_network_or_frozen_module() -> None:
    reachable = ["web.py", "frontend.py", "preprocess.py", "check.py", "report.py", "release.py", "infer.py"]
    reachable += ["proof.py", "gate.py", "elaborate.py", "clauses.py", "surface.py", "text.py", "bundle.py"]
    for name in reachable:
        tree = ast.parse((ROOT / "pfc2" / name).read_text(encoding="utf-8"))
        names = {a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names}
        names |= {n.module or "" for n in ast.walk(tree) if isinstance(n, ast.ImportFrom)}
        banned = (
            "subprocess",
            "socket",
            "urllib",
            "http",
            "openai",
            "pfc.",
            "pfc_eval",
            "pfc_web",
            "pfc2.cli",
            "pfc2.prove",
        )
        assert not [n for n in names if n == "pfc" or n.startswith(banned)], name
