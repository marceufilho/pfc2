"""The site is built from the repository: the checker bundle, the examples with native results, the docs pages."""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import site_data  # noqa: E402


def test_the_bundle_is_the_checker_without_commands_services_or_the_editor_server() -> None:
    bundle = site_data.bundle(ROOT)
    files = set(bundle["files"])
    assert {"pfc2/web.py", "pfc2/core/wp.py", "pfc2/include/pfc.h", "pfc2/include/pfc_rt.h"} <= files
    assert not {"pfc2/cli.py", "pfc2/prove.py", "pfc2/llm.py", "pfc2/__main__.py"} & files
    assert not [name for name in files if name.startswith("pfc2/lsp/")]
    assert bundle["files"]["pfc2/gate.py"] == (ROOT / "pfc2/gate.py").read_text(encoding="utf-8")
    assert set(bundle["sha256"]) == files and all(len(digest) == 64 for digest in bundle["sha256"].values())


@pytest.mark.integration
def test_every_example_is_published_with_its_native_result_and_group() -> None:
    listed = site_data.programs(ROOT)
    cases = json.loads((ROOT / "examples" / "examples.json").read_text(encoding="utf-8"))
    assert [p["id"] + ".c" for p in listed] == [case["path"] for case in cases] and len(listed) == 32
    by_id = {p["id"]: p for p in listed}
    assert by_id["01_count/count"]["reference"]["accepted"] and by_id["01_count/count"]["group"] == "functions"
    assert not by_id["wrong/off_by_one"]["reference"]["accepted"] and by_id["wrong/off_by_one"]["group"] == "wrong"
    assert by_id["03_sum/sum"]["level"] == "memory" and by_id["09_calculator/calculator"]["group"] == "programs"
    assert by_id["console/repeat"]["group"] == "programs"
    gallery = site_data.gallery(listed)
    assert "### 05_binary_search/binary_search" in gallery and "(../playground/#example=wrong/off_by_one)" in gallery
    assert "Expected: **refused**" in gallery and "Expected: **certified at level `memory`**" in gallery


def test_documentation_pages_keep_their_text_and_link_to_each_other() -> None:
    pages = site_data.documentation(ROOT)
    assert len(pages) == 12 and "src/content/docs/docs/index.md" in pages
    tour = pages["src/content/docs/docs/01-tour.md"]
    assert 'title: "1. Tour"' in tour and "order: 1" in tour and "source: docs/01-tour.md" in tour
    assert "[the language](../02-language/)" in tour and "](../03-proofs/#termination)" in tour
    assert "[1. Tour](./01-tour/)" in pages["src/content/docs/docs/index.md"]


def test_a_link_that_leaves_the_documentation_or_a_missing_page_is_an_error(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    for page in site_data.ORDER:
        (tmp_path / "docs" / f"{page}.md").write_text(f"# {page}\n\ntext\n", encoding="utf-8")
    assert len(site_data.documentation(tmp_path)) == 12
    (tmp_path / "docs" / "09-limits.md").write_text("# L\n\n[x](../pfc2/gate.py)\n", encoding="utf-8")
    with pytest.raises(site_data.SiteDataError, match="outside the documentation"):
        site_data.documentation(tmp_path)
    (tmp_path / "docs" / "09-limits.md").unlink()
    with pytest.raises(site_data.SiteDataError, match="disagree"):
        site_data.documentation(tmp_path)


@pytest.mark.integration
def test_the_committed_site_files_equal_a_fresh_build_and_a_stale_file_is_noticed(tmp_path: Path) -> None:
    files = site_data.build(ROOT)
    assert site_data.check(ROOT / "site", files) == []
    for name, text in files.items():
        (tmp_path / name).parent.mkdir(parents=True, exist_ok=True)
        (tmp_path / name).write_text(text, encoding="utf-8")
    (tmp_path / "public/data/programs.json").write_text("{}", encoding="utf-8")
    (tmp_path / "src/content/docs/docs/old-page.md").write_text("stale", encoding="utf-8")
    assert site_data.check(tmp_path, files) == ["public/data/programs.json", "src/content/docs/docs/old-page.md"]


@pytest.mark.integration
def test_the_game_data_comes_from_running_the_rules_and_matches_the_board_read_by_hand() -> None:
    data = site_data.game(ROOT)
    wall, opened = data["variants"]["wall"], data["variants"]["open"]
    assert (wall["accepted"], wall["proved"], wall["obligations"], wall["refusal"]) == (True, 40, 40, [])
    assert not opened["accepted"] and [(r["line"], r["meaning"]) for r in opened["refusal"]] == [
        (52, "an iteration may break the loop invariant")
    ]
    # Hand-read from flag.c. Moves: 0 up, 1 down, 2 left, 3 right; the wall is column 4.
    for variant in (wall, opened):
        table = variant["table"]
        assert table[0][2][2] == [0, 2] and table[0][0][0] == [0, 0] and table[2][4][1] == [2, 4]  # Board edges.
        assert table[2][2][3] == [3, 2] and table[2][2][0] == [2, 1] and table[7][2][3] == [7, 2]
    assert wall["table"][3][2][3] == [3, 2] and opened["table"][3][2][3] == [4, 2]  # The wall, and its absence.
    assert wall["shortest_win"] is None  # Exhaustive search over the 40 squares agrees with the proof.
    assert opened["shortest_win"] == [3] * 7  # Seven steps to the right.
