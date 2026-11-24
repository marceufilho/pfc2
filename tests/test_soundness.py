"""Evidence for the admission rule: a check proved over mathematical integers may be removed beside unproved
arithmetic, because that arithmetic keeps its overflow trap.

Ten constructed programs make a wrapped value able to send an index (or a divisor) wrong while the
mathematical value is fine. For each: the hand-derived verdict, inputs that must run and inputs that must
stop at a trap; then a seeded differential in which the certified C and the checked C (every guard kept)
run under AddressSanitizer and UndefinedBehaviorSanitizer and must behave identically, with no sanitizer
report. A last test removes one kept trap by hand and requires the differential to notice.
"""

import json
import random
import signal
import subprocess
from pathlib import Path

import pytest

from pfc2 import frontend
from pfc2.check import check
from pfc2.core.config import C_FLAGS
from pfc2.core.emit import GUARD_LINE, OVERFLOW_LINE, emit
from pfc2.core.target import read_target

HERE = Path(__file__).parent / "soundness"
CASES = {
    name: case
    for name, case in json.loads((HERE / "cases.json").read_text(encoding="utf-8")).items()
    if name != "comment"
}
SANITIZE = ["-fsanitize=address,undefined", "-fno-sanitize-recover=all", "-g"]
LIMIT = 2**63
EDGES = [0, 1, -1, 2, -2, LIMIT - 1, -LIMIT, 2**62, -(2**62), 2**62 + 1, 2**32, -(2**32), 3037000499, 3037000500]
RUNS = 40
DRIVER = """
#include <stdio.h>
#include <stdlib.h>
long probe(long n, long a[], long x, long y);
int main(int argc, char **argv) {
    long *a = malloc(8 * sizeof(long));
    if (argc != 3 || a == NULL) return 2;
    for (long i = 0; i < 8; i++) a[i] = 100 + i;
    printf("%ld", probe(8, a, strtol(argv[1], NULL, 10), strtol(argv[2], NULL, 10)));
    free(a);
    return 0;
}
"""
pytestmark = pytest.mark.integration


def _compile(directory: Path, name: str, c: str, *flags: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    source, driver, binary = directory / f"{name}.c", directory / "driver.c", directory / name
    source.write_text(c, encoding="utf-8")
    driver.write_text(DRIVER, encoding="utf-8")
    command = ["clang-19", *C_FLAGS, *flags, str(source), str(driver), "-o", str(binary)]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stderr
    return binary


def _run(binary: Path, x: int, y: int) -> tuple[int, str, str]:
    result = subprocess.run([str(binary), str(x), str(y)], capture_output=True, text=True, check=False, timeout=20)
    return result.returncode, result.stdout, result.stderr


def _certified_and_checked(name: str) -> tuple[str, str]:
    unit, certification = check(frontend.load(HERE / "programs" / f"{name}.c"), read_target("clang-19"), level="memory")
    assert certification.accepted and certification.c is not None, certification.reason
    checked = emit(unit.code or unit.program, read_target("clang-19"), mode="checked").c
    return certification.c, checked


def test_the_ten_programs_are_listed() -> None:
    assert sorted(CASES) == sorted(path.stem for path in (HERE / "programs").glob("*.c")) and len(CASES) == 10


@pytest.mark.parametrize("name", sorted(CASES))
def test_the_guard_is_removed_the_trap_stays_and_a_wrapping_input_stops_at_it(name: str, tmp_path: Path) -> None:
    case = CASES[name]
    unit, certification = check(frontend.load(HERE / "programs" / f"{name}.c"), read_target("clang-19"), level="memory")
    assert certification.accepted and certification.c is not None, certification.reason
    assert [d.removed for d in certification.emission.decisions] == [True] * case["guards"]
    assert len(certification.retained_traps) == case["kept"]
    assert not GUARD_LINE.search(certification.c) and len(OVERFLOW_LINE.findall(certification.c)) == case["kept"]
    assert not check(unit, read_target("clang-19"), level="full")[1].accepted
    binary = _compile(tmp_path, name, certification.c)
    for x, y, expected in case["safe"]:
        assert _run(binary, x, y)[:2] == (0, expected), (x, y)
    for x, y in case["trap"]:
        assert _run(binary, x, y)[0] == -signal.SIGILL, (x, y)


@pytest.mark.parametrize("name", sorted(CASES))
def test_certified_and_fully_checked_c_behave_alike_under_sanitizers(name: str, tmp_path: Path) -> None:
    certified, checked = _certified_and_checked(name)
    binaries = [
        _compile(tmp_path / kind, name, c, *SANITIZE) for kind, c in (("certified", certified), ("checked", checked))
    ]
    generator = random.Random(f"pfc2-soundness-{name}")
    inputs = [(generator.randrange(-2, 10), generator.choice(EDGES)) for _ in range(RUNS // 2)]
    inputs += [(generator.randrange(0, 8), generator.randrange(-LIMIT, LIMIT)) for _ in range(RUNS // 2)]
    trapped = 0
    for x, y in inputs:
        first, second = (_run(binary, x, y) for binary in binaries)
        assert "Sanitizer" not in first[2] and "runtime error" not in first[2], (x, y, first[2][-400:])
        assert "Sanitizer" not in second[2] and "runtime error" not in second[2], (x, y, second[2][-400:])
        assert first[0] in (0, -signal.SIGILL) and second[0] in (0, -signal.SIGILL), (x, y, first[0], second[0])
        if 0 <= x < 8:  # Inside the precondition the two builds must agree exactly.
            assert first[:2] == second[:2], (x, y, first[:2], second[:2])
        else:  # Outside it the certified build stops at its entry check; the checked build has none.
            assert first[0] == -signal.SIGILL, (x, y, first[0])
        trapped += first[0] != 0
    assert 0 < trapped < len(inputs)  # The inputs exercise both outcomes.


def test_the_differential_notices_a_trap_that_was_dropped(tmp_path: Path) -> None:
    """The check has teeth: with the multiplication's trap removed by hand, a wrapping input is caught."""
    certified, _ = _certified_and_checked("p01_mul")
    trap = OVERFLOW_LINE.search(certified)
    assert trap is not None
    line = certified[trap.start() : certified.index("\n", trap.start())]
    left, right, target = line[line.index("(", line.index("__builtin")) + 1 : line.index(")")].split(", ")
    broken = certified.replace(
        line, f"{line[: len(line) - len(line.lstrip())]}{target.lstrip('&')} = {left} * {right};"
    )
    assert broken != certified and len(OVERFLOW_LINE.findall(broken)) == 0
    binary = _compile(tmp_path, "broken", broken, *SANITIZE)
    code, _, errors = _run(binary, 3, 2**62)
    assert code not in (0, -signal.SIGILL) and ("runtime error" in errors or "AddressSanitizer" in errors)
