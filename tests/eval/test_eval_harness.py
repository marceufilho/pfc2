"""Independence of the harness, the candidate check, sealing of held-out sets and the command line."""

import ast
import json
from pathlib import Path

import pytest

from pfc2_eval import campaign, cli, evidence, heldout, selfcheck

ROOT = Path(__file__).resolve().parents[2]


def _imports(path: Path) -> set[str]:
    found = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
        if isinstance(node, ast.Import):
            found |= {alias.name for alias in node.names}
        elif isinstance(node, ast.ImportFrom) and node.module:
            found |= {node.module} | {f"{node.module}.{alias.name}" for alias in node.names}
    return found


def test_the_package_never_imports_the_harness() -> None:
    for path in (ROOT / "pfc2").rglob("*.py"):
        assert not any(name.split(".")[0] == "pfc2_eval" for name in _imports(path)), path


def test_the_interpreter_shares_only_the_ir_and_the_target_with_the_compiler() -> None:
    forbidden = {"vc", "wp", "smt", "emit", "authorization", "infer", "gate", "check", "elaborate", "desugar"}
    for module in ("interpret.py", "hosts.py"):
        names = _imports(ROOT / "pfc2_eval" / module)
        assert not any(set(name.split(".")) & forbidden for name in names if name.startswith("pfc2.")), module
    used = {name for name in _imports(ROOT / "pfc2_eval" / "interpret.py") if name.startswith("pfc2.")}
    assert used == {
        "pfc2.core",
        "pfc2.core.ir",
        "pfc2.core.diagnostics",
        "pfc2.core.diagnostics.SourceLocation",
        "pfc2.core.parse",
        "pfc2.core.parse.SpecKind",
        "pfc2.core.target",
        "pfc2.core.target.Target",
        "pfc2.core.target.limits",
    }


def test_the_generator_does_not_consult_the_compiler() -> None:
    assert not any(name.startswith("pfc2.") for name in _imports(ROOT / "pfc2_eval" / "generate.py"))


def test_the_tree_is_the_frozen_candidate_and_a_changed_file_is_noticed(tmp_path: Path) -> None:
    frozen = campaign.candidate()
    assert frozen.name == "pfc2-v3" and frozen.intact and frozen.protected.checked >= 40
    copy = tmp_path / "copy"
    (copy / "pfc2").mkdir(parents=True)
    (copy / "validation" / "freeze").mkdir(parents=True)
    (copy / "pfc2" / "a.py").write_text("x = 1\n", encoding="utf-8")
    digest = "ca5c4a1a1c1d3c6e3d2b9a0b0a0c7a5b8f4f2d5e6a7b8c9d0e1f2a3b4c5d6e7f"
    (copy / "validation" / "freeze" / "protected.sha256").write_text(f"{digest}  pfc2/a.py\n", encoding="utf-8")
    (copy / "validation" / "freeze" / "baseline.sha256").write_text("", encoding="utf-8")
    (copy / "validation" / "freeze" / "CANDIDATE.json").write_text('{"candidate": "x"}', encoding="utf-8")
    assert not campaign.candidate(copy).intact  # The digest does not match the file.
    (copy / "pfc2" / "new.py").write_text("", encoding="utf-8")
    assert campaign.candidate(copy).unlisted == ("pfc2/new.py",)
    assert campaign.candidate(tmp_path / "nowhere").name is None


def test_a_sealed_set_notices_a_change_an_addition_and_a_removal(tmp_path: Path) -> None:
    (tmp_path / "a.c").write_text("long f(void);\n", encoding="utf-8")
    (tmp_path / "b.c").write_text("long g(void);\n", encoding="utf-8")
    assert not heldout.verify(tmp_path).sealed
    with pytest.raises(ValueError):
        heldout.seal(tmp_path, rule=" ", candidate=None)
    assert heldout.seal(tmp_path, rule="every file, in order", candidate="pfc2-v1") == 3  # Two sources and the record.
    assert heldout.verify(tmp_path).intact
    with pytest.raises(FileExistsError):
        heldout.seal(tmp_path, rule="again", candidate=None)
    (tmp_path / "a.c").write_text("long f(long x);\n", encoding="utf-8")
    (tmp_path / "c.c").write_text("", encoding="utf-8")
    (tmp_path / "b.c").unlink()
    assert heldout.verify(tmp_path).problems == ("changed: a.c", "missing: b.c", "added: c.c")
    with pytest.raises(ValueError):
        heldout.require_intact([tmp_path])


def test_commands_report_usage_planned_steps_and_dry_runs(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as usage:
        cli.main(["selfcheck"])
    assert usage.value.code == 2
    assert cli.main(["oracle"]) == 1 and "not implemented" in capsys.readouterr().err
    target = tmp_path / "out"
    assert cli.main(["selfcheck", "--output", str(target), "--dry-run"]) == 0 and not target.exists()
    assert cli.main(["generate", "--seed", "3"]) == 0
    assert capsys.readouterr().out.startswith('#include "pfc.h"')
    assert cli.main(["candidate"]) == 0 and json.loads(capsys.readouterr().out)["candidate"] == "pfc2-v3"


@pytest.mark.integration
def test_a_small_selfcheck_is_sealed_complete_and_refuses_to_overwrite(tmp_path: Path) -> None:
    output = tmp_path / "selfcheck"
    assert selfcheck.run(output=output, compiler="clang-19", seed=0, programs=6, cases=10, progress=lambda _: None)
    assert evidence.status(output).complete
    loaded = evidence.load(output)
    assert len(loaded.observations) == 60 and loaded.configuration["settings"]["candidate"] == "pfc2-v3"
    summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    assert summary["passed"] and summary["outcomes"]["mismatch"] == 0
    assert summary["compared"] + summary["outcomes"]["rejected"] == 60
    assert cli.main(["selfcheck", "--output", str(output), "--programs", "1", "--cases", "1"]) == 1
    (output / "tables.md").write_text("edited\n", encoding="utf-8")
    assert not evidence.status(output).complete  # A sealed directory that was touched is no longer evidence.
