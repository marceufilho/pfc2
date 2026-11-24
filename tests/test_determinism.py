"""A verdict, its identities and the released C must not depend on the process that computed them.

Python randomises the hash of strings per process, so iterating a set of names gives a different order in each
run. Anything that numbers symbols in that order makes proof files irreproducible. Found on 2026-11-18 by the
replay step of the differential shake-down (decision 0067).
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = """
import json, sys
from pfc2 import frontend, proof
from pfc2.check import check
from pfc2.core.target import Target
target = Target("static LP64 layout (test)", "x86_64-pc-linux-gnu", 32, 64)
unit, certification = check(frontend.load_text(sys.stdin.read(), "t.c"), target, level="memory")
record = proof.build(unit, certification) if certification.accepted else {"refused": certification.reason}
print(json.dumps(record, sort_keys=True))
"""
# Two globals written by a callee that is called inside a loop: the loop head renames both.
GLOBALS = """#include "pfc.h"
long first = 0;
long second = 0;
long third = 0;
long touch(long x)
    requires(0 <= x && x <= 9)
    ensures(result == x)
{
    third = x;
    first = x;
    second = x;
    return x;
}
long sweep(long n)
    requires(0 <= n && n <= 9)
{
    long total = 0;
    for (long i = 0; i < n; i++) invariant(0 <= total && total <= 9 * i) {
        total += touch(i);
    }
    return total;
}
"""


def _record(text: str, seed: int) -> object:
    environment = {**os.environ, "PYTHONHASHSEED": str(seed)}
    result = subprocess.run(
        [sys.executable, "-c", SCRIPT],
        input=text,
        capture_output=True,
        text=True,
        env=environment,
        cwd=ROOT,
        timeout=600,
    )
    assert result.returncode == 0, result.stderr[-800:]
    return json.loads(result.stdout)


@pytest.mark.integration
def test_the_proof_record_is_the_same_under_every_hash_seed() -> None:
    records = [_record(GLOBALS, seed) for seed in (0, 1, 2, 3, 4, 5, 6, 7)]
    assert "refused" not in records[0]  # type: ignore[operator]
    assert all(record == records[0] for record in records)


@pytest.mark.integration
@pytest.mark.parametrize("path", ["08_counter/counter.c", "12_rest_api/api.c", "15_matrix/matrix.c", "17_text/text.c"])
def test_examples_give_the_same_record_under_different_hash_seeds(path: str) -> None:
    text = (ROOT / "examples" / path).read_text(encoding="utf-8")
    assert _record(text, 1) == _record(text, 2) == _record(text, 3)


@pytest.mark.integration
def test_released_c_compiles_under_the_documented_flags_when_the_source_is_odd_but_valid(tmp_path: Path) -> None:
    """`g = g;` and `n != n` are defined C. The certified C must not fail to build because clang finds them odd."""
    from pfc2 import frontend
    from pfc2.check import check
    from pfc2.core.config import C_FLAGS
    from pfc2.core.target import read_target

    text = (
        '#include "pfc.h"\nlong g = 0;\nlong f(long n)\n{\n    g = g;\n    if (n != n) {\n        return 1;\n    }\n'
        "    if (n <= n) {\n        return 2;\n    }\n    return 0;\n}\n"
    )
    certification = check(frontend.load_text(text, "odd.c"), read_target("clang-19"))[1]
    assert certification.accepted and certification.c is not None
    source = tmp_path / "odd.c"
    source.write_text(certification.c, encoding="utf-8")
    built = subprocess.run(
        ["clang-19", *C_FLAGS, "-c", str(source), "-o", str(tmp_path / "odd.o")], capture_output=True, text=True
    )
    assert built.returncode == 0, built.stderr
