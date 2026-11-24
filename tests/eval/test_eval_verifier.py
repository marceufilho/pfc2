"""E7: pairing WP goals with PFC2 obligations, and a small sealed campaign with a scripted prover."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from pathlib import Path

import pytest

from pfc2_eval import evidence, verifier

ROOT = Path(__file__).resolve().parents[2]
CASES = ROOT / "corpus" / "independent-verifier"


def goal(name: str, verdict: str = "valid", smoke: bool = False) -> dict[str, object]:
    return {"goal": name, "verdict": verdict, "smoke": smoke}


def test_a_goal_belongs_to_the_longest_function_name_that_fits() -> None:
    functions = ["count", "count_char", "at"]
    assert verifier.split(goal("typed_count_char_ensures"), functions) == ("count_char", "ensures")
    assert verifier.split(goal("typed_count_loop_invariant_preserved"), functions) == (
        "count",
        "loop_invariant_preserved",
    )
    assert verifier.split(goal("typed_other_ensures"), functions) is None
    assert verifier.split(goal("count_ensures"), functions) is None


def test_a_shortened_goal_name_is_read_from_the_function_and_property_fields() -> None:
    long_name = "the_determinant_of_a_product_is_the_product_of_the_determinants"
    shortened = {
        **goal("typed_the_determinant_of_a_product_is_the_product_of_the_4"),
        "function": long_name,
        "property": long_name + "_assert_rte_signed_overflow",
    }
    assert verifier.split(shortened, ["det2", long_name]) == (long_name, "assert_rte_signed_overflow")
    assert verifier.split({**shortened, "function": "elsewhere"}, ["det2", long_name]) is None
    kept = verifier.parse_goals([{**shortened, "passed": True}])
    assert kept[0]["function"] == long_name and kept[0]["property"].endswith("signed_overflow")  # type: ignore[union-attr]


@pytest.mark.parametrize(
    ("rest", "expected"),
    [
        ("assert_rte_mem_access_3", "bounds"),
        ("assert_rte_index_bound", "bounds"),
        ("assert_bounds_a", "bounds"),
        ("assert_rte_division_by_zero", "division"),
        ("assert_division_mid", "division"),
        ("assert_rte_signed_overflow_2", "overflow"),
        ("assert_rte_signed_downcast", "conversion"),
        ("assert_rte_shift", "support"),
        ("assert", "assert"),
        ("assert_2", "assert"),
        ("loop_variant_decrease", "assert"),
        ("ensures_2", "postcondition"),
        ("call_step_x_requires", "call-precondition"),
        ("loop_invariant_2_established", "entry"),
        ("loop_invariant_preserved", "preservation"),
        ("loop_assigns_part2", "support"),
        ("assigns_normal_part1", "support"),
        ("terminates", "support"),
        ("exits", "support"),
    ],
)
def test_the_class_of_a_goal_is_read_from_its_name(rest: str, expected: str) -> None:
    assert verifier.goal_class(rest) == expected


def test_the_four_outcomes_and_the_one_sided_cells() -> None:
    assert verifier.outcome(2, 2, 3, 3) == "agree-proved"
    assert verifier.outcome(2, 2, 3, 2) == "wp-open"
    assert verifier.outcome(2, 1, 3, 3) == "disagreement"
    assert verifier.outcome(2, 1, 3, 2) == "agree-open"
    assert verifier.outcome(2, 2, 0, 0) == "pfc2-only"
    assert verifier.outcome(0, 0, 1, 0) == "wp-only"


def test_cells_count_each_side_per_function_and_class() -> None:
    spans = [("f", 3), ("g", 20)]
    obligations = [
        {"kind": "bounds", "line": 5, "status": "proved"},
        {"kind": "bounds", "line": 6, "status": "proved"},
        {"kind": "overflow", "line": 6, "status": "failed"},
        {"kind": "assert", "line": 22, "status": "proved"},
    ]
    goals = [
        goal("typed_f_assert_rte_mem_access"),
        goal("typed_f_assert_rte_signed_overflow", "timeout"),
        goal("typed_f_loop_assigns"),
        goal("typed_g_assert", "unknown"),
        goal("typed_g_ensures"),
        goal("typed_g_requires_smoke", "unknown", smoke=True),
    ]
    rows = verifier.cells("c", "examples", spans, obligations, goals)
    found = {(r["function"], r["class"]): r for r in rows if r["row"] == "cell"}
    assert found[("f", "bounds")]["outcome"] == "agree-proved"
    assert (found[("f", "bounds")]["pfc2_total"], found[("f", "bounds")]["wp_total"]) == (2, 1)
    assert found[("f", "overflow")]["outcome"] == "agree-open"
    assert found[("g", "assert")]["outcome"] == "wp-open"
    assert found[("g", "postcondition")]["outcome"] == "wp-only"
    support = rows[-1]
    assert (support["row"], support["wp_total"], support["wp_valid"], support["wp_smoke"]) == ("support", 1, 1, 1)


def test_a_goal_of_an_unknown_function_or_an_unknown_kind_is_an_error() -> None:
    with pytest.raises(ValueError, match="no function"):
        verifier.cells("c", "x", [("f", 1)], [], [goal("typed_h_ensures")])
    with pytest.raises(ValueError, match="does not know"):
        verifier.cells("c", "x", [("f", 1)], [{"kind": "novel", "line": 1, "status": "proved"}], [])


def test_a_malformed_report_is_never_an_empty_success() -> None:
    for payload in (None, [], [{"goal": "a", "verdict": "valid"}], [goal("a"), goal("a")], [goal("a", "fine")]):
        with pytest.raises(ValueError):
            verifier.parse_goals(payload)
    assert verifier.parse_goals([{**goal("a"), "passed": True}]) == [goal("a")]


def test_a_control_is_detected_only_by_the_expected_open_goal() -> None:
    control = {"expected_unproved": "assert_bounds_a", "expected_inconsistent": False}
    assert verifier.control_detected(control, 0, [goal("typed_f_assert_bounds_a", "timeout")])
    assert not verifier.control_detected(control, 0, [goal("typed_f_assert_bounds_a")])
    assert not verifier.control_detected(control, 1, [goal("typed_f_assert_bounds_a", "timeout")])
    vacuous = {"expected_unproved": None, "expected_inconsistent": True}
    assert verifier.control_detected(vacuous, 0, [goal("typed_f_requires_smoke", "valid", smoke=True)])
    assert not verifier.control_detected(vacuous, 0, [goal("typed_f_requires_smoke", "unknown", smoke=True)])


def test_the_committed_cases_name_the_files_that_are_there() -> None:
    data = verifier.configuration(CASES, ROOT)
    assert len(data["cases"]) == 29 and len(data["controls"]) == 6  # type: ignore[arg-type]
    listed = {case["acsl"] for case in [*data["cases"], *data["controls"]]}  # type: ignore[misc]
    present = {str(path.relative_to(CASES)) for path in CASES.rglob("*.c")}
    assert listed == present


def test_a_changed_file_is_refused(tmp_path: Path) -> None:
    source = tmp_path / "p.c"
    source.write_text('#include "pfc.h"\nlong f(long n) { return n; }\n', encoding="utf-8")
    cases = tmp_path / "cases"
    cases.mkdir()
    (cases / "p.c").write_text("long f(long n) { return n; }\n", encoding="utf-8")
    entry = {
        "name": "p",
        "corpus": "examples",
        "source": "p.c",
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "acsl": "p.c",
        "acsl_sha256": "0" * 64,
    }
    image = "framac/frama-c@sha256:" + "a" * 64
    (cases / "cases.json").write_text(json.dumps({"image": image, "options": [], "cases": [entry], "controls": []}))
    with pytest.raises(ValueError, match="ACSL file"):
        verifier.configuration(cases, tmp_path)


def _campaign(tmp_path: Path, goals: Sequence[dict[str, object]], control_goals: Sequence[dict[str, object]]) -> Path:
    source = ROOT / "examples" / "01_count" / "count.c"
    cases = tmp_path / "cases"
    cases.mkdir()
    for name in ("count.c", "control.c"):
        (cases / name).write_text("/* stands for an ACSL file */\n", encoding="utf-8")
    sha = hashlib.sha256((cases / "count.c").read_bytes()).hexdigest()
    data = {
        "image": "framac/frama-c@sha256:" + "a" * 64,
        "options": ["-wp"],
        "cases": [
            {
                "name": "count",
                "corpus": "examples",
                "source": str(source.relative_to(ROOT)),
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "acsl": "count.c",
                "acsl_sha256": sha,
            }
        ],
        "controls": [
            {
                "name": "control",
                "acsl": "control.c",
                "acsl_sha256": sha,
                "expected_unproved": "assert_bounds_a",
                "expected_inconsistent": False,
            }
        ],
    }
    (cases / "cases.json").write_text(json.dumps(data), encoding="utf-8")

    def prover(path: Path, options: Sequence[str], label: str) -> tuple[int, object]:
        return 0, list(control_goals if label == "control" else goals)

    output = tmp_path / "out"
    verifier.run(cases=cases, output=output, compiler="clang-19", prover=prover, progress=lambda text: None)
    return output


COUNT_GOALS = [
    goal("typed_count_ensures"),
    goal("typed_count_loop_invariant_established"),
    goal("typed_count_loop_invariant_preserved"),
    goal("typed_count_assert_rte_signed_overflow"),
    goal("typed_count_loop_assigns"),
    goal("typed_counting_to_n_gives_n_assert"),
    goal("typed_counting_to_n_gives_n_call_count_requires"),
]


def test_a_small_campaign_seals_and_agrees(tmp_path: Path) -> None:
    output = _campaign(tmp_path, COUNT_GOALS, [goal("typed_f_assert_bounds_a", "timeout")])
    loaded = evidence.load(output)
    summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    assert summary["passed"] is True
    assert summary["cases_compared"] == 1 and summary["controls_detected"] == 1
    assert summary["outcomes"]["disagreement"] == 0 and summary["outcomes"]["agree-proved"] >= 5
    assert any(row["row"] == "control" for row in loaded.observations)


def test_an_open_wp_goal_is_inconclusive_and_a_missed_control_fails(tmp_path: Path) -> None:
    goals = [goal("typed_count_ensures", "timeout"), *COUNT_GOALS[1:]]
    output = _campaign(tmp_path, goals, [goal("typed_f_assert_bounds_a")])
    summary = json.loads((output / "summary.json").read_text(encoding="utf-8"))
    assert summary["outcomes"]["wp-open"] == 1 and summary["outcomes"]["disagreement"] == 0
    assert summary["controls_missed"] == ["control"] and summary["passed"] is False
