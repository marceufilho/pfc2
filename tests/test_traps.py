"""A guard removed by a proof over mathematical integers is covered by the overflow trap that stays (real clang)."""

import signal
import subprocess
from pathlib import Path

import pytest

from pfc2 import frontend
from pfc2.core.config import C_FLAGS
from pfc2.core.emit import GUARD_LINE, OVERFLOW_LINE
from pfc2.core.target import read_target
from pfc2.gate import certify

FIXTURES = Path(__file__).parent / "fixtures"
DRIVER = """
#include <stdio.h>
#include <stdlib.h>
long pick(long n, const long a[], long i, long w);
int main(int argc, char **argv) {
    long a[4] = {10, 11, 12, 13};
    (void)argc;
    printf("%ld\\n", pick(4, a, atol(argv[1]), atol(argv[2])));
    return 0;
}
"""


@pytest.mark.integration
def test_unproved_arithmetic_keeps_its_trap_and_the_proved_bounds_check_is_removed(tmp_path: Path) -> None:
    unit = frontend.load(FIXTURES / "wrapped_index.c")
    target = read_target("clang-19")
    full = certify(unit.program, target, level="full", code=unit.code)
    assert not full.accepted and full.c is None
    assert [(b.kind, b.location.line) for b in full.blockers] == [("overflow", 8)]
    memory = certify(unit.program, target, level="memory", code=unit.code)
    assert memory.accepted and memory.c is not None
    assert [(d.location.line, d.removed) for d in memory.emission.decisions] == [(9, True), (10, True)]
    assert [(d.location.line, d.removed) for d in memory.retained_traps] == [(8, False)]
    assert not GUARD_LINE.search(memory.c) and len(OVERFLOW_LINE.findall(memory.c)) == 1
    (tmp_path / "pick.c").write_text(memory.c, encoding="utf-8")
    (tmp_path / "main.c").write_text(DRIVER, encoding="utf-8")
    binary = tmp_path / "pick"
    command = ["clang-19", *C_FLAGS, str(tmp_path / "pick.c"), str(tmp_path / "main.c"), "-o", str(binary)]
    assert subprocess.run(command, capture_output=True, text=True, check=False).returncode == 0

    def run(i: str, w: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([str(binary), i, w], capture_output=True, text=True, check=False, timeout=10)

    assert (run("1", "5").stdout, run("3", "-7").stdout) == ("11\n", "13\n")
    # 2**62 * 2 wraps: without the trap the index would be 1 - 2**63.
    assert run("1", "4611686018427387904").returncode == -signal.SIGILL
    # A violated precondition is stopped by the entry check.
    assert run("4", "0").returncode == -signal.SIGILL
