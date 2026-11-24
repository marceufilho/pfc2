"""The freeze inventories: what they notice, and that the committed ones describe this tree."""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("freeze", ROOT / "tools" / "freeze.py")
assert spec is not None and spec.loader is not None
freeze = importlib.util.module_from_spec(spec)
sys.modules["freeze"] = freeze
spec.loader.exec_module(freeze)


def test_an_inventory_round_trips_and_a_change_a_loss_and_an_addition_are_each_noticed() -> None:
    recorded = {"pfc2/a.py": "0" * 64, "pfc2/b.py": "1" * 64}
    assert freeze.parse(freeze.render(recorded)) == recorded
    current = {"pfc2/a.py": "f" * 64, "pfc2/c.py": "2" * 64}
    assert freeze.compare(recorded, current) == {
        "changed": ["pfc2/a.py"],
        "missing": ["pfc2/b.py"],
        "not in the inventory": ["pfc2/c.py"],
    }
    assert freeze.compare(recorded, recorded) == {"changed": [], "missing": [], "not in the inventory": []}


def test_the_committed_inventories_describe_this_tree() -> None:
    passed, report = freeze.check()
    assert passed, report
    protected = freeze.parse((freeze.FREEZE / "protected.sha256").read_text(encoding="utf-8"))
    assert "pfc2/core/wp.py" in protected and "uv.lock" in protected and "pfc2/include/pfc.h" in protected
    assert not any("__pycache__" in name for name in protected)
