"""A declared-only function is trusted under its contract, so the contract itself must be possible."""

from pathlib import Path

import pytest

from pfc2 import frontend, proof
from pfc2.check import check
from pfc2.core.target import Target
from pfc2.elaborate import Unit
from pfc2.gate import Certification

TARGET = Target("static LP64 layout (test)", "x86_64-pc-linux-gnu", 32, 64)
pytestmark = pytest.mark.integration
ABSURD = "long use(void)\n{\n    long r = f(1);\n    assert(1 == 2);\n    return r;\n}\n"


def _check(tmp_path: Path, body: str) -> tuple[Unit, Certification]:
    source = tmp_path / "t.c"
    source.write_text('#include "pfc.h"\n' + body, encoding="utf-8")
    return check(frontend.load(source), TARGET)


@pytest.mark.parametrize(
    "contract",
    [
        "    ensures(result < 0 && result > 0);\n",  # No result at all.
        "    ensures(result > x && result < x);\n",
        "    requires(x > 0 && x < 0);\n",  # Can never be called.
    ],
)
def test_a_contract_nothing_can_satisfy_is_refused_instead_of_proving_everything(tmp_path: Path, contract: str) -> None:
    unit, certification = _check(tmp_path, "long f(long x)\n" + contract + ABSURD)
    assert not certification.accepted and certification.c is None
    assert "contract of f" in certification.reason and "cannot be satisfied" in certification.reason
    assert [(e.query.function, e.consistent) for e in certification.proof.external_results] == [("f", "unsat")]


def test_a_contract_that_promises_a_result_some_input_cannot_have_is_refused_with_that_input(tmp_path: Path) -> None:
    half = "long f(long x)\n    requires(0 <= x && x <= 100)\n    ensures(result + result == x);\n"
    unit, certification = _check(tmp_path, half + "long use(void)\n{\n    return f(4);\n}\n")
    assert not certification.accepted and certification.c is None
    assert "contract of f" in certification.reason and "no result" in certification.reason
    (result,) = certification.proof.external_results
    assert (result.consistent, result.total) == ("sat", "partial")
    assert result.witness is not None and result.witness.startswith("x = ")
    assert int(result.witness.split(" = ")[1]) % 2 == 1  # Hand-derived: only odd inputs have no half.


def test_a_possible_contract_is_accepted_and_recorded(tmp_path: Path) -> None:
    sensor = "long sensor(long x)\n    requires(0 <= x)\n    ensures(0 <= result && result <= x);\n"
    unit, certification = _check(
        tmp_path, sensor + "long use(void)\n    ensures(result <= 5)\n{\n    return sensor(5);\n}\n"
    )
    assert certification.accepted
    record = proof.build(unit, certification)
    assert record["unverified"]["contracts"] == [  # type: ignore[index]
        {"function": "sensor", "consistent": "sat", "total": "total", "witness": None}
    ]


# Each contract is classified by hand: can a function exist that keeps the promise for every allowed input?
# A function may write the arrays it receives without `const`, and nothing else.
ARRAY_CONTRACTS = {
    "returns what it reads": (
        "long f(long n, const long a[n])\n    requires(1 <= n)\n    ensures(result == a[0]);",
        True,
    ),
    "needs the caller's data to be positive": (
        "long f(long n, const long a[n])\n    requires(1 <= n)\n    ensures(result == a[0] && a[0] > 0);",
        False,
    ),
    "writes a cell": ("long f(long n, long a[n])\n    requires(1 <= n)\n    ensures(a[0] == 5);", True),
    "would have to change a const array": (
        "long f(long n, const long a[n], long m, long b[m])\n    requires(1 <= n && 1 <= m)\n    ensures(a[0] == 5);",
        False,
    ),
    "copies between separate arrays": (
        "long f(long n, const long a[n], long m, long b[m])\n"
        "    requires(1 <= n && 1 <= m && separated(a, b))\n    ensures(b[0] == a[0]);",
        True,
    ),
    "copies plus one where the arrays may be the same": (
        "long f(long n, const long a[n], long m, long b[m])\n    requires(1 <= n && 1 <= m)\n"
        "    ensures(b[0] == a[0] + 1);",
        False,
    ),
    "adds one to a value that may be the largest": (
        "long f(long n, const long a[n], long m, long b[m])\n"
        "    requires(1 <= n && 1 <= m && separated(a, b))\n    ensures(b[0] == a[0] + 1);",
        False,
    ),
    "stores 2 in a _Bool": ("long f(long n, _Bool a[n])\n    requires(1 <= n)\n    ensures(a[0] == 2);", False),
    "two values for what may be one cell": (
        "long f(long n, long a[n], long i, long j)\n    requires(0 <= i && i < n && 0 <= j && j < n)\n"
        "    ensures(a[i] == 1 && a[j] == 2);",
        False,
    ),
    "two values for two different cells": (
        "long f(long n, long a[n], long i, long j)\n    requires(0 <= i && i < j && j < n)\n"
        "    ensures(a[i] == 1 && a[j] == 2);",
        True,
    ),
    "orders two cells": ("long f(long n, long a[n])\n    requires(2 <= n)\n    ensures(a[0] <= a[1]);", True),
}


@pytest.mark.parametrize("name", sorted(ARRAY_CONTRACTS))
def test_a_contract_about_array_contents_is_accepted_only_when_some_function_can_keep_it(
    tmp_path: Path, name: str
) -> None:
    contract, possible = ARRAY_CONTRACTS[name]
    unit, certification = _check(tmp_path, contract + "\nlong use(void)\n{\n    return 0;\n}\n")
    (result,) = certification.proof.external_results
    assert result.consistent == "sat"
    assert certification.accepted == possible
    assert (result.total == "total") == possible
    if not possible:
        assert "contract of f" in certification.reason


def test_the_console_runtime_contracts_are_possible(tmp_path: Path) -> None:
    program = '#include "pfc_rt.h"\nint main(void)\n{\n    println_str("x");\n    return 0;\n}\n'
    unit, certification = _check(tmp_path, program)
    assert certification.accepted
    assert {(e.consistent, e.total) for e in certification.proof.external_results} == {("sat", "total")}
