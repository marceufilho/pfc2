"""Whole programs: globals, functions declared with a contract and no body, strings, console I/O and main."""

import subprocess
from pathlib import Path

import pytest

from pfc2 import frontend
from pfc2.check import check
from pfc2.cli import main
from pfc2.core.config import C_FLAGS
from pfc2.core.target import Target
from pfc2.elaborate import Unit
from pfc2.gate import Certification

ROOT = Path(__file__).resolve().parents[1]
TARGET = Target("static LP64 layout (test)", "x86_64-pc-linux-gnu", 32, 64)
pytestmark = pytest.mark.integration
GLOBALS = """long counter = 0;
long limit = 10;

long bump(void)
    requires(counter < 1000)
    ensures(result == counter)
{
    counter = counter + 1;
    return counter;
}
"""


def _check(tmp_path: Path, body: str, header: str = '#include "pfc.h"\n') -> tuple[Unit, Certification]:
    source = tmp_path / "t.c"
    source.write_text(header + body, encoding="utf-8")
    return check(frontend.load(source), TARGET)


def test_a_call_changes_only_the_globals_its_callee_writes(tmp_path: Path) -> None:
    head = "long f(void)\n    requires(counter < 100)\n{\n"
    kept = head + "    long before = limit;\n    long a = bump();\n    assert(before == limit);\n    return a;\n}\n"
    assert _check(tmp_path, GLOBALS + kept)[1].accepted
    lost = head + "    long before = counter;\n    long a = bump();\n    assert(before == counter);\n    return a;\n}\n"
    refused = _check(tmp_path, GLOBALS + lost)[1]
    assert not refused.accepted and [b.kind for b in refused.blockers] == ["assert"]
    # The postcondition speaks about the global after the call.
    used = head + "    long a = bump();\n    assert(a == counter);\n    return a;\n}\n"
    assert _check(tmp_path, GLOBALS + used)[1].accepted


def test_a_loop_that_calls_a_writer_forgets_the_global_and_the_emitted_global_is_static(tmp_path: Path) -> None:
    loop = (
        "long f(void)\n    requires(counter == 0)\n{\n    for (long i = 0; i < 3; i++) {\n        bump();\n    }\n"
        "    assert(counter == 0);\n    return 0;\n}\n"
    )
    assert not _check(tmp_path, GLOBALS + loop)[1].accepted
    unit, accepted = _check(tmp_path, GLOBALS)
    assert accepted.accepted and accepted.c is not None
    assert "static long counter = 0;" in accepted.c and "static long limit = 10;" in accepted.c


def test_only_the_program_entry_knows_the_initial_values(tmp_path: Path) -> None:
    body = "\n{\n    assert(seed == -5);\n    return 0;\n}\n"
    assert _check(tmp_path, "long seed = -5;\nint main(void)" + body)[1].accepted
    assert not _check(tmp_path, "long seed = -5;\nlong f(void)" + body)[1].accepted


def test_a_declared_function_is_called_under_its_contract_and_listed_as_unverified(tmp_path: Path) -> None:
    sensor = "long sensor(void)\n    ensures(0 <= result && result <= 100);\n"
    use = "long use(void)\n    ensures(result <= 200)\n{\n    return sensor() + sensor();\n}\n"
    unit, accepted = _check(tmp_path, sensor + use)
    assert accepted.accepted and accepted.c is not None and unit.externals == ("sensor",)
    assert "long sensor(void);" in accepted.c and "long sensor(void)\n{" not in accepted.c
    put = "long put(long x)\n    requires(0 <= x);\n"
    refused = _check(tmp_path, put + "long use(void)\n{\n    put(-1);\n    return 0;\n}\n")[1]
    assert not refused.accepted and "call-precondition" in [b.kind for b in refused.blockers]
    assert not _check(tmp_path, sensor + use.replace("200", "100"))[1].accepted


PROGRAM = """#include "pfc.h"
#include "pfc_rt.h"

long greetings = 0;

long count(long n)
    requires(0 <= n)
    ensures(result == n)
{
    long i = 0;
    while (i < n) decreases(n - i) {
        i++;
    }
    return i;
}

long greet(string name)
{
    print_str("hello, ");
    println_str(name);
    if (greetings < 1000) {
        greetings++;
    }
    return greetings;
}

int main(void)
{
    println_str("how many?");
    long n = read_int();
    string who = read_line();
    if (0 <= n && n <= 100) {
        greet(who);
        greet("again \\"quoted\\"");
        print_int(count(n));
        print_str(" counted, greetings: ");
        print_int(greetings);
        println();
    }
    if (str_eq(who, "pfc2")) {
        println_str("that is my name");
    }
    return 0;
}
"""
EXPECTED = 'how many?\nhello, pfc2\nhello, again "quoted"\n7 counted, greetings: 2\nthat is my name\n'


def test_a_console_program_is_certified_and_behaves_like_its_plain_c_build(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "hello.c"
    source.write_text(PROGRAM, encoding="utf-8")
    assert main(["build", str(source), "--output", str(tmp_path / "out")]) == 0
    capsys.readouterr()
    runtime = ROOT / "pfc2" / "runtime" / "pfc_rt.c"
    include = ["-I", str(ROOT / "pfc2" / "include")]
    for name, sources, extra in (
        ("certified", [tmp_path / "out" / "hello.c", runtime], []),
        ("plain", [source, runtime], include),
    ):
        command = ["clang-19", *C_FLAGS, *extra, *map(str, sources), "-o", str(tmp_path / name)]
        compiled = subprocess.run(command, capture_output=True, text=True, check=False)
        assert compiled.returncode == 0, compiled.stderr
        run = subprocess.run([str(tmp_path / name)], input="7\npfc2\n", capture_output=True, text=True, check=False)
        assert (run.returncode, run.stdout) == (0, EXPECTED), name


def test_run_certifies_compiles_and_executes(tmp_path: Path, capfd: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "hello.c"
    source.write_text(PROGRAM, encoding="utf-8")
    answers = tmp_path / "answers.txt"
    answers.write_text("7\npfc2\n", encoding="utf-8")
    assert main(["run", str(source), "--stdin", str(answers)]) == 0
    assert capfd.readouterr().out == EXPECTED
    source.write_text(
        PROGRAM.replace("if (greetings < 1000)", "if (greetings < 1000 || greetings == greetings)"), encoding="utf-8"
    )
    assert main(["run", str(source), "--stdin", str(answers)]) == 1
    assert "not certified" in capfd.readouterr().out
