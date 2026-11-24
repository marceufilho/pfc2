"""Command line: one command to check, one to build C plus a separate proof file, one to replay."""

import json
import subprocess
from pathlib import Path

import pytest

from pfc2.cli import main

FIXTURES = Path(__file__).parent / "fixtures"


def run(capsys, *arguments: str) -> tuple[int, str, str]:
    code = main(list(arguments))
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def test_help_names_every_command(capsys):
    with pytest.raises(SystemExit) as stop:
        main(["--help"])
    assert stop.value.code == 0
    text = capsys.readouterr().out
    assert all(name in text for name in ("check", "build", "replay", "elaborate"))


def test_check_reports_success_and_writes_nothing(capsys, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    code, out, _ = run(capsys, "check", str(FIXTURES / "count.c"))
    assert code == 0
    assert "certified (full)" in out and "n where 0 <= n" in out and "6 of 6" in out
    assert list(tmp_path.iterdir()) == []


def test_check_explains_a_refusal_with_location_and_counterexample(capsys):
    code, out, _ = run(capsys, "check", str(FIXTURES / "wrong.c"))
    assert code == 1
    assert "not certified" in out and "wrong.c:5" in out and "n = 0" in out


def test_check_suggests_memory_level_when_only_overflow_blocks(capsys):
    code, out, _ = run(capsys, "check", str(FIXTURES / "sum.c"))
    assert code == 1 and "--level memory" in out and "sum.c:9" in out
    code, out, _ = run(capsys, "check", str(FIXTURES / "sum.c"), "--level", "memory")
    assert code == 0 and "certified (memory)" in out and "1 overflow trap kept" in out


def test_build_writes_c_and_a_separate_proof_file_that_replays(capsys, tmp_path):
    output = tmp_path / "out"
    code, out, _ = run(capsys, "build", str(FIXTURES / "fill.c"), "--output", str(output))
    assert code == 0
    assert sorted(p.name for p in output.iterdir()) == ["fill.c", "fill.proof.json"]
    data = json.loads((output / "fill.proof.json").read_text(encoding="utf-8"))
    assert data["c"] == (output / "fill.c").read_text(encoding="utf-8")
    compiled = subprocess.run(
        ["clang-19", "-std=c11", "-O2", "-Wall", "-Wextra", "-Werror", "-c", str(output / "fill.c")]
        + ["-o", str(tmp_path / "fill.o")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert compiled.returncode == 0, compiled.stderr
    code, out, _ = run(capsys, "replay", str(output / "fill.proof.json"))
    assert code == 0 and "reproduced" in out


def test_build_refuses_to_replace_existing_output_without_force(capsys, tmp_path):
    output = tmp_path / "out"
    assert run(capsys, "build", str(FIXTURES / "count.c"), "--output", str(output))[0] == 0
    code, _, err = run(capsys, "build", str(FIXTURES / "count.c"), "--output", str(output))
    assert code == 1 and "--force" in err
    assert run(capsys, "build", str(FIXTURES / "count.c"), "--output", str(output), "--force")[0] == 0


def test_refused_build_writes_no_file(capsys, tmp_path):
    output = tmp_path / "out"
    code, _, _ = run(capsys, "build", str(FIXTURES / "wrong.c"), "--output", str(output))
    assert code == 1 and not output.exists()


def test_dry_run_build_writes_no_file(capsys, tmp_path):
    output = tmp_path / "out"
    code, out, _ = run(capsys, "build", str(FIXTURES / "count.c"), "--output", str(output), "--dry-run")
    assert code == 0 and not output.exists() and "would write" in out


def test_replay_detects_an_edited_proof_file(capsys, tmp_path):
    output = tmp_path / "out"
    run(capsys, "build", str(FIXTURES / "count.c"), "--output", str(output))
    path = output / "count.proof.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["obligations"][0]["status"] = "failed"
    path.write_text(json.dumps(data), encoding="utf-8")
    code, out, _ = run(capsys, "replay", str(path))
    assert code == 1 and "obligations" in out


def test_json_output_and_frontend_errors(capsys, tmp_path):
    code, out, _ = run(capsys, "check", str(FIXTURES / "count.c"), "--json")
    assert code == 0 and json.loads(out)["accepted"] is True
    code, out, err = run(capsys, "check", str(tmp_path / "missing.c"))
    assert code == 1 and out == "" and "source-read" in err
    bad = tmp_path / "bad.c"
    bad.write_text('#include "pfc.h"\nlong f(long x where x)\n{\n    return x;\n}\n', encoding="utf-8")
    code, _, err = run(capsys, "check", str(bad))
    assert code == 1 and "where-syntax" in err and "bad.c:2" in err


def test_usage_error_exits_two(capsys):
    with pytest.raises(SystemExit) as stop:
        main(["build"])
    assert stop.value.code == 2


def test_elaborate_prints_the_contracts_the_checker_sees(capsys):
    code, out, _ = run(capsys, "elaborate", str(FIXTURES / "count.c"))
    assert code == 0
    assert "REQUIRES((0 <= n));" in out and "INVARIANT(((0 <= i) && (i <= n)));" in out and "where" not in out
