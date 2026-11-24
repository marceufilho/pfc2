"""Dependency admission: the same answers as the path-walking definition, in time linear in the graph.

Decision 0069. The reference below is the definition used up to candidate `pfc2-v2`, copied here so that the
memoised closure is compared with it and not with itself.
"""

import random
import subprocess
import sys
from pathlib import Path

from pfc2.core import smt

ROOT = Path(__file__).resolve().parents[1]


def reference(proved: set[str], needs: dict[str, tuple[str, ...]]) -> set[str]:
    def holds(identifier: str, visiting: frozenset[str] = frozenset()) -> bool:
        if identifier in visiting or identifier not in needs or identifier not in proved:
            return False
        return all(holds(dependency, visiting | {identifier}) for dependency in needs[identifier])

    return {identifier for identifier in needs if holds(identifier)}


def test_a_proof_counts_only_with_the_proofs_it_depends_on() -> None:
    needs = {"a": (), "b": ("a",), "c": ("b",), "d": ("c", "x"), "x": ()}
    assert smt.admitted({"a", "b", "c", "d"}, needs) == {"a", "b", "c"}
    assert smt.admitted({"b", "c", "d", "x"}, needs) == {"x"}


def test_a_dependency_that_has_no_result_admits_nothing() -> None:
    assert smt.admitted({"a"}, {"a": ("absent",)}) == frozenset()


def test_an_obligation_on_a_cycle_is_not_admitted_and_neither_is_one_that_needs_it() -> None:
    needs = {"a": ("b",), "b": ("a",), "c": ("a",), "d": ("d",), "e": ()}
    assert smt.admitted(set(needs), needs) == {"e"}


def test_it_agrees_with_the_path_walking_definition_on_random_graphs() -> None:
    generator = random.Random(20261119)
    for _ in range(2000):
        names = [f"o{index}" for index in range(generator.randint(1, 9))]
        needs = {
            name: tuple(generator.sample(names + ["absent"], generator.randint(0, min(3, len(names)))))
            for name in names
        }
        proved = {name for name in names if generator.random() < 0.8}
        assert smt.admitted(proved, needs) == reference(proved, needs), (proved, needs)


def test_a_ladder_of_shared_dependencies_is_decided_at_once() -> None:
    # Each rung needs both obligations of the rung below: 2**200 walks for the path-walking definition.
    needs: dict[str, tuple[str, ...]] = {"l0": (), "r0": ()}
    for rung in range(1, 200):
        needs[f"l{rung}"] = needs[f"r{rung}"] = (f"l{rung - 1}", f"r{rung - 1}")
    assert smt.admitted(set(needs), needs) == set(needs)


def chain(calls: int) -> str:
    body = "\n".join("    v = step(v);" for _ in range(calls))
    return (
        '#include "pfc.h"\n\n'
        "long step(long x)\n    requires(0 <= x && x < 1000)\n    ensures(result == x + 1)\n{\n    return x + 1;\n}\n\n"
        f"long chain(long x)\n    requires(x == 0)\n    ensures(result == {calls})\n{{\n    long v = x;\n{body}\n"
        "    return v;\n}\n"
    )


def test_a_long_chain_of_proved_calls_is_certified_within_a_minute(tmp_path: Path) -> None:
    # With `pfc2-v2` the time doubled with every call: 20 calls took 9 s, so 40 would take months.
    source = tmp_path / "chain.c"
    source.write_text(chain(40), encoding="utf-8")
    done = subprocess.run(
        [sys.executable, "-m", "pfc2", "check", str(source)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert done.returncode == 0, done.stdout + done.stderr
    assert "certified" in done.stdout
