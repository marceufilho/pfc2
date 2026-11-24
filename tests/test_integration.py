"""Every example: the verdict written by hand in examples.json, replay, and (real clang) the same behaviour
from the certified C and from the plain C build of the same source."""

import json
import subprocess
from pathlib import Path

import pytest

from pfc2 import frontend, proof
from pfc2.check import check
from pfc2.core.config import C_FLAGS
from pfc2.core.emit import GUARD_LINE, OVERFLOW_LINE
from pfc2.core.target import read_target

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples"
RUNTIME = ROOT / "pfc2" / "runtime" / "pfc_rt.c"
INCLUDE = ["-I", str(ROOT / "pfc2" / "include")]
CASES = json.loads((EXAMPLES / "examples.json").read_text(encoding="utf-8"))
pytestmark = pytest.mark.integration


def test_every_example_file_has_an_expectation() -> None:
    listed = {case["path"] for case in CASES}
    assert listed == {str(path.relative_to(EXAMPLES)) for path in EXAMPLES.rglob("*.c")}
    assert len(listed) == len(CASES)


def _compile(sources: list[Path], output: Path, *extra: str) -> None:
    command = ["clang-19", *C_FLAGS, *extra, *map(str, sources), "-o", str(output)]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("case", [c for c in CASES if "refused" in c], ids=lambda c: c["path"])
def test_a_wrong_example_is_refused_where_its_comment_says_and_releases_no_c(case: dict[str, object]) -> None:
    unit, certification = check(frontend.load(EXAMPLES / str(case["path"])), read_target("clang-19"))
    assert not certification.accepted and certification.c is None
    primary = [(b.kind, b.location.line) for b in certification.blockers if not b.status.startswith("depends")]
    expected = case["refused"]
    assert isinstance(expected, dict)
    if "reason" in expected:  # Refused before any obligation is judged.
        assert str(expected["reason"]) in certification.reason
    else:
        assert (expected["kind"], expected["line"]) in primary
    assert not check(unit, read_target("clang-19"), level="memory")[1].accepted


@pytest.mark.parametrize("case", [c for c in CASES if "refused" not in c], ids=lambda c: c["path"])
def test_a_good_example_certifies_replays_and_runs_like_plain_c(case: dict[str, str | int], tmp_path: Path) -> None:
    source = EXAMPLES / str(case["path"])
    target = read_target("clang-19")
    unit, certification = check(frontend.load(source), target, level=case["level"])  # type: ignore[arg-type]
    assert certification.accepted and certification.c is not None, certification.reason
    full = check(frontend.load(source), target)[1]
    assert full.accepted == (case["level"] == "full")
    assert len(certification.emission.decisions) == case.get("guards", 0)
    assert len(certification.retained_traps) == case.get("kept_traps", 0)
    assert len(unit.laws) == case.get("laws", 0)
    assert len(unit.inferred) == case.get("inferred", 0)
    assert len(unit.measures) == case.get("terminating", 0)
    assert not GUARD_LINE.search(certification.c)
    assert len(OVERFLOW_LINE.findall(certification.c)) == case.get("kept_traps", 0)
    record = json.loads(json.dumps(proof.build(unit, certification)))
    assert proof.replay(record) == []
    certified = tmp_path / source.name
    certified.write_text(certification.c, encoding="utf-8")
    if "expected" not in case:  # A library: both forms compile without a warning.
        _compile([certified], tmp_path / "certified.o", "-c")
        _compile([source], tmp_path / "plain.o", "-c", *INCLUDE)
        return
    _compile([certified, RUNTIME], tmp_path / "certified")
    _compile([source, RUNTIME], tmp_path / "plain", *INCLUDE)
    answers = (EXAMPLES / str(case["stdin"])).read_text(encoding="utf-8")
    expected = (EXAMPLES / str(case["expected"])).read_text(encoding="utf-8")
    for name in ("certified", "plain"):
        run = subprocess.run([str(tmp_path / name)], input=answers, capture_output=True, text=True, check=False)
        assert (run.stdout, run.returncode) == (expected, 0), name
