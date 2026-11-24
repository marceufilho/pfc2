"""E7: an independent verifier beside PFC2.

Each case is a PFC2 program and a hand-written ACSL transcription of it (`corpus/independent-verifier`).
Frama-C/WP proves the transcription in the digest-pinned image, offline; PFC2 judges its own source in a
fresh process. The two tools share no code. They are compared per function and class of property
(bounds, division, overflow, conversion, postcondition, assertion, call precondition, invariant on
entry, invariant preserved), because sites cannot be paired mechanically between two differently laid
out files. A cell in which PFC2 proves everything and WP leaves a goal open is inconclusive, never a
counterexample; a cell in which WP proves everything and PFC2 does not is a disagreement to classify.
Nothing WP says gives PFC2 any authority, and the harness never pulls the image.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from collections.abc import Callable, Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

from pfc2_eval import adapter, campaign, evidence

EXPERIMENT = "verifier"
CLASSES = (
    "bounds",
    "division",
    "overflow",
    "conversion",
    "postcondition",
    "assert",
    "call-precondition",
    "entry",
    "preservation",
)
OUTCOMES = ("agree-proved", "agree-open", "wp-open", "disagreement", "pfc2-only", "wp-only")
PROCESS_SECONDS = 900
SCHEMA = evidence.Schema(
    (
        evidence.Column("row", "string", allowed=("cell", "support", "control", "case")),
        evidence.Column("case", "string"),
        evidence.Column("corpus", "string", nullable=True),
        evidence.Column("function", "string", nullable=True),
        evidence.Column("class", "string", nullable=True),
        evidence.Column("pfc2_total", "integer", nullable=True),
        evidence.Column("pfc2_proved", "integer", nullable=True),
        evidence.Column("wp_total", "integer", nullable=True),
        evidence.Column("wp_valid", "integer", nullable=True),
        evidence.Column("wp_smoke", "integer", nullable=True),
        evidence.Column("outcome", "string", nullable=True, allowed=OUTCOMES),
        evidence.Column("status", "string", nullable=True),
        evidence.Column("detected", "boolean", nullable=True),
    )
)
_VERDICTS = frozenset({"none", "valid", "failed", "unknown", "stepout", "timeout"})

Goal = Mapping[str, object]
Prover = Callable[[Path, Sequence[str], str], tuple[int, object]]


def parse_goals(payload: object) -> list[dict[str, object]]:
    """The goals of a WP JSON report; a malformed or empty report is an error, never an empty success."""
    if not isinstance(payload, list) or not payload:
        raise ValueError("missing or empty WP goal list")
    goals: list[dict[str, object]] = []
    seen: set[str] = set()
    for item in payload:
        if not isinstance(item, dict):
            raise ValueError("a WP goal must be an object")
        name, verdict, smoke = item.get("goal"), item.get("verdict"), item.get("smoke")
        if not isinstance(name, str) or not name or name in seen:
            raise ValueError("a WP goal has no name or repeats one")
        if verdict not in _VERDICTS or type(smoke) is not bool:
            raise ValueError(f"WP goal {name} has no usable verdict")
        seen.add(name)
        goal: dict[str, object] = {"goal": name, "verdict": verdict, "smoke": smoke}
        for key in ("function", "property"):
            if isinstance(item.get(key), str):
                goal[key] = item[key]
        goals.append(goal)
    return goals


def split(goal: Goal, functions: Sequence[str]) -> tuple[str, str] | None:
    """(function, rest) of a goal. Its name is `typed_<function>_<rest>`, the longest function name winning;
    WP shortens a long function name there, and then its `function` and `property` fields say the same."""
    name = str(goal["goal"])
    if name.startswith("typed_"):
        body = name[len("typed_") :]
        for function in sorted(functions, key=len, reverse=True):
            if body.startswith(function + "_"):
                return function, body[len(function) + 1 :]
    owner_name, described = goal.get("function"), goal.get("property")
    if isinstance(owner_name, str) and owner_name in functions and isinstance(described, str):
        if described.startswith(owner_name + "_"):
            return owner_name, described[len(owner_name) + 1 :]
    return None


def goal_class(rest: str) -> str:
    """The class of a WP goal from the part of its name after the function; `support` is WP's own."""
    if rest.startswith(("assert_rte_mem_access", "assert_rte_index_bound", "assert_bounds_")):
        return "bounds"
    if rest.startswith(("assert_rte_division_by_zero", "assert_division_")):
        return "division"
    if rest.startswith("assert_rte_signed_overflow"):
        return "overflow"
    if rest.startswith("assert_rte_signed_downcast"):
        return "conversion"
    if rest.startswith("assert_rte_"):
        return "support"
    if rest.startswith(("assert", "loop_variant")):
        return "assert"
    if rest.startswith("ensures"):
        return "postcondition"
    if re.match(r"call_.+_requires", rest):
        return "call-precondition"
    if rest.startswith("loop_invariant") and "established" in rest:
        return "entry"
    if rest.startswith("loop_invariant") and "preserved" in rest:
        return "preservation"
    return "support"


def owner(spans: Sequence[tuple[str, int]], line: int) -> str:
    """The function whose text holds `line`: the last one that starts at or before it."""
    best = spans[0][0]
    for name, start in spans:
        if start <= line:
            best = name
    return best


def outcome(pfc2_total: int, pfc2_proved: int, wp_total: int, wp_valid: int) -> str:
    if not wp_total:
        return "pfc2-only"
    if not pfc2_total:
        return "wp-only"
    ours, theirs = pfc2_proved == pfc2_total, wp_valid == wp_total
    if ours and theirs:
        return "agree-proved"
    if ours:
        return "wp-open"
    return "disagreement" if theirs else "agree-open"


def cells(
    case: str,
    corpus: str,
    spans: Sequence[tuple[str, int]],
    obligations: Iterable[Mapping[str, object]],
    goals: Iterable[Goal],
) -> list[dict[str, object]]:
    """One row per (function, class) either tool has something in, and one support row per case."""
    functions = [name for name, _ in spans]
    counts: dict[tuple[str, str], list[int]] = {}
    for item in obligations:
        kind = str(item["kind"])
        if kind not in CLASSES:
            raise ValueError(f"{case}: PFC2 reports a kind of obligation this comparison does not know: {kind}")
        entry = counts.setdefault((owner(spans, int(str(item["line"]))), kind), [0, 0, 0, 0])
        entry[0] += 1
        entry[1] += item["status"] == "proved"
    support = [0, 0]
    smoke = 0
    for goal in goals:
        if goal["smoke"]:
            smoke += 1
            continue
        parts = split(goal, functions)
        if parts is None:
            raise ValueError(f"{case}: WP goal {goal['goal']} belongs to no function of the PFC2 source")
        kind = goal_class(parts[1])
        valid = goal["verdict"] == "valid"
        if kind == "support":
            support[0] += 1
            support[1] += valid
            continue
        entry = counts.setdefault((parts[0], kind), [0, 0, 0, 0])
        entry[2] += 1
        entry[3] += valid
    rows: list[dict[str, object]] = []
    for (function, kind), (total, proved, wp_total, wp_valid) in sorted(counts.items()):
        rows.append(
            {
                "row": "cell",
                "case": case,
                "corpus": corpus,
                "function": function,
                "class": kind,
                "pfc2_total": total,
                "pfc2_proved": proved,
                "wp_total": wp_total,
                "wp_valid": wp_valid,
                "outcome": outcome(total, proved, wp_total, wp_valid),
            }
        )
    rows.append(
        {
            "row": "support",
            "case": case,
            "corpus": corpus,
            "wp_total": support[0],
            "wp_valid": support[1],
            "wp_smoke": smoke,
        }
    )
    return rows


def control_detected(control: Mapping[str, object], code: int, goals: Iterable[Goal]) -> bool:
    """A negative control is detected when WP runs and leaves the expected goal unproved (or finds the
    contradictory precondition by its smoke test)."""
    if code != 0:
        return False
    if control.get("expected_inconsistent"):
        return any(g["smoke"] and "requires" in str(g["goal"]) and g["verdict"] == "valid" for g in goals)
    pattern = str(control["expected_unproved"])
    return any(not g["smoke"] and pattern in str(g["goal"]) and g["verdict"] != "valid" for g in goals)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def configuration(directory: Path, root: Path) -> dict[str, Any]:
    """`cases.json`, with every file it names checked against its recorded SHA-256."""
    data = json.loads((directory / "cases.json").read_text(encoding="utf-8"))
    if not re.fullmatch(r"framac/frama-c@sha256:[0-9a-f]{64}", str(data.get("image", ""))):
        raise ValueError("the verifier image must be pinned by digest")
    names: set[str] = set()
    for case in [*data["cases"], *data["controls"]]:
        if case["name"] in names:
            raise ValueError(f"case named twice: {case['name']}")
        names.add(case["name"])
        if digest(directory / case["acsl"]) != case["acsl_sha256"]:
            raise ValueError(f"{case['name']}: the ACSL file is not the recorded one")
        if "source" in case and digest(root / case["source"]) != case["source_sha256"]:
            raise ValueError(f"{case['name']}: the PFC2 source is not the recorded one")
    return dict(data)


def docker_prover(image: str) -> Prover:
    """Run WP on one file in a fresh offline container; returns (exit code, parsed JSON or None)."""

    def prove(source: Path, options: Sequence[str], label: str) -> tuple[int, object]:
        with tempfile.TemporaryDirectory(prefix="pfc2-verifier-") as scratch:
            os.chmod(scratch, 0o777)
            command = [
                "docker",
                "run",
                "--rm",
                "--pull=never",
                "--network=none",
                "--name",
                f"pfc2-verifier-{label}-{os.getpid()}",
                "--cap-drop=ALL",
                "--security-opt=no-new-privileges",
                "--cpus=2",
                "--memory=2g",
                "--user",
                f"{os.getuid()}:{os.getgid()}",
                "--mount",
                f"type=bind,src={source.parent.resolve()},dst=/input,readonly",
                "--mount",
                f"type=bind,src={scratch},dst=/output",
                image,
                "frama-c",
                f"/input/{source.name}",
                *options,
                "-wp-report-json",
                "/output/wp.json",
            ]
            try:
                done = subprocess.run(command, capture_output=True, text=True, timeout=PROCESS_SECONDS, check=False)
                code = done.returncode
            except subprocess.TimeoutExpired:
                subprocess.run(["docker", "rm", "-f", command[6]], capture_output=True, timeout=60, check=False)
                return 124, None
            report = Path(scratch) / "wp.json"
            if not report.is_file():
                return code or 1, None
            return code, json.loads(report.read_text(encoding="utf-8"))

    return prove


def image_present(image: str) -> bool:
    done = subprocess.run(["docker", "image", "inspect", image], capture_output=True, text=True, check=False)
    return done.returncode == 0


def pfc2_obligations(source: Path, compiler: str) -> list[dict[str, object]]:
    """PFC2's own judgement of its source at level `full`, in a process of its own."""
    command = [sys.executable, "-m", "pfc2", "check", str(source), "--json", "--clang", compiler]
    done = subprocess.run(command, capture_output=True, text=True, timeout=PROCESS_SECONDS, check=False)
    report = json.loads(done.stdout)
    return [
        {"kind": item["kind"], "line": item["line"], "status": item["status"], "category": item["category"]}
        for item in report["obligations"]
    ]


def summarise(rows: Sequence[Mapping[str, object]]) -> dict[str, object]:
    compared = [r for r in rows if r["row"] == "cell" and r["outcome"] not in ("pfc2-only", "wp-only")]
    by_outcome = {name: sum(r["outcome"] == name for r in rows if r["row"] == "cell") for name in OUTCOMES}
    by_corpus: dict[str, dict[str, int]] = {}
    by_class: dict[str, dict[str, int]] = {}
    for row in rows:
        if row["row"] != "cell":
            continue
        for table, key in ((by_corpus, str(row["corpus"])), (by_class, str(row["class"]))):
            entry = table.setdefault(key, {name: 0 for name in OUTCOMES})
            entry[str(row["outcome"])] += 1
    cases = [r for r in rows if r["row"] == "case"]
    controls = [r for r in rows if r["row"] == "control"]
    errors = [str(r["case"]) for r in cases if r["status"] != "compared"]
    missed = [str(r["case"]) for r in controls if not r["detected"]]
    disagreements = [
        f"{r['case']}:{r['function']}:{r['class']}"
        for r in rows
        if r["row"] == "cell" and r["outcome"] == "disagreement"
    ]
    return {
        "cases": len(cases),
        "cases_compared": len(cases) - len(errors),
        "cases_in_error": errors,
        "cells": sum(r["row"] == "cell" for r in rows),
        "cells_compared": len(compared),
        "outcomes": by_outcome,
        "by_corpus": dict(sorted(by_corpus.items())),
        "by_class": dict(sorted(by_class.items())),
        "disagreements": disagreements,
        "wp_goals": sum(int(str(r["wp_total"])) for r in rows if r["row"] in ("cell", "support")),
        "wp_goals_valid": sum(int(str(r["wp_valid"])) for r in rows if r["row"] in ("cell", "support")),
        "pfc2_obligations": sum(int(str(r["pfc2_total"])) for r in rows if r["row"] == "cell"),
        "controls": len(controls),
        "controls_detected": len(controls) - len(missed),
        "controls_missed": missed,
        "criterion": "0 disagreements, every case compared, every control detected",
        "passed": not disagreements and not errors and not missed and bool(cases),
    }


def table(summary: Mapping[str, object]) -> str:
    def block(title: str, data: Mapping[str, Mapping[str, int]]) -> list[str]:
        lines = [f"## {title}", "", "| | " + " | ".join(OUTCOMES) + " |", "| --- |" + " ---: |" * len(OUTCOMES)]
        lines += [
            f"| {key} | " + " | ".join(str(entry[name]) for name in OUTCOMES) + " |" for key, entry in data.items()
        ]
        return [*lines, ""]

    outcomes = summary["outcomes"]
    assert isinstance(outcomes, Mapping)
    by_corpus, by_class = summary["by_corpus"], summary["by_class"]
    assert isinstance(by_corpus, Mapping) and isinstance(by_class, Mapping)
    lines = [
        "# E7: PFC2 beside Frama-C/WP",
        "",
        f"Cases compared: {summary['cases_compared']} of {summary['cases']}. "
        f"Cells (function, class): {summary['cells']}, of which {summary['cells_compared']} hold something from both.",
        f"WP goals: {summary['wp_goals_valid']} valid of {summary['wp_goals']}. "
        f"PFC2 obligations: {summary['pfc2_obligations']}.",
        f"Negative controls detected: {summary['controls_detected']} of {summary['controls']}.",
        f"Disagreements: {len(summary['disagreements'])}.",  # type: ignore[arg-type]
        "",
        *block("By corpus", by_corpus),
        *block("By class", by_class),
    ]
    return "\n".join(lines) + "\n"


def _rows(records: tuple[evidence.Record, ...]) -> Iterable[Mapping[str, object]]:
    names = [column.name for column in SCHEMA.columns]
    return [{name: record.data.get(name) for name in names} for record in records if record.shard == "rows"]


def run(
    *,
    cases: Path,
    output: Path,
    compiler: str,
    root: Path = campaign.ROOT,
    prover: Prover | None = None,
    dry_run: bool = False,
    progress: Callable[[str], None] = campaign.progress,
) -> bool:
    data = configuration(cases, root)
    positives, controls = list(data["cases"]), list(data["controls"])
    if dry_run:
        progress(f"verifier: would compare {len(positives)} cases and run {len(controls)} controls into {output}")
        return True
    image = str(data["image"])
    if prover is None:
        if not image_present(image):
            raise evidence.CommandFailed(f"the pinned image is not present and is never pulled here: {image}")
        prover = docker_prover(image)
    options = [str(option) for option in data["options"]]
    settings = {"image": image, "options": options, "cases": len(positives), "controls": len(controls), "level": "full"}
    started = campaign.start(EXPERIMENT, output, compiler=compiler, seed=0, settings=settings, schema=SCHEMA)
    kept: list[dict[str, object]] = []

    def keep(unit: str, rows: Sequence[dict[str, object]]) -> None:
        for index, row in enumerate(rows):
            started.evidence.record(unit, "rows", f"r{index}", row)
        kept.extend(rows)

    for case in positives:
        name, corpus = str(case["name"]), str(case["corpus"])
        code, payload = prover(cases / case["acsl"], options, name)
        try:
            goals = parse_goals(payload)
            obligations = pfc2_obligations(root / case["source"], compiler)
            unit = adapter.load(root / case["source"])
            spans = [(function.name, function.location.line) for function in unit.program.functions]
            started.evidence.record(name, "wp", "goals", {"exit_code": code, "goals": goals})
            started.evidence.record(name, "pfc2", "obligations", {"obligations": obligations})
            rows = cells(name, corpus, spans, obligations, goals)
            status = "compared"
        except (ValueError, KeyError, TypeError, json.JSONDecodeError, subprocess.TimeoutExpired) as error:
            rows, status = [], f"error: {error}"
        keep(name, [*rows, {"row": "case", "case": name, "corpus": corpus, "status": status}])
        progress(f"verifier: {name}: {status}")
    for control in controls:
        name = str(control["name"])
        code, payload = prover(cases / control["acsl"], options, name)
        try:
            goals = parse_goals(payload)
            started.evidence.record(name, "wp", "goals", {"exit_code": code, "goals": goals})
            detected = control_detected(control, code, goals)
        except ValueError:
            detected = False
        keep(name, [{"row": "control", "case": name, "detected": detected}])
        progress(f"verifier: control {name}: {'detected' if detected else 'MISSED'}")
    summary = summarise(kept)
    campaign.finish(started, summary, table(summary), _rows)
    progress(f"verifier: {'passed' if summary['passed'] else 'FAILED'}; {summary['outcomes']}")
    return bool(summary["passed"])
