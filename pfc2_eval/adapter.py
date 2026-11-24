"""The harness's view of PFC2: load a source, judge it, and obtain each kind of C it can be compared with.

Everything here calls the frozen package and adds nothing to what it decides. One condition exists only for
experiments: `check(..., inference=False)` skips the inference of counter bounds, so that a proposer of loop
invariants is not compared with a tool that has already answered. It still ends in the same gate.
"""

from dataclasses import replace
from pathlib import Path

from pfc2 import frontend, infer, release
from pfc2.core.config import SOLVER_TIMEOUT_MS
from pfc2.core.emit import emit
from pfc2.core.ir import Program
from pfc2.core.target import Target
from pfc2.elaborate import Unit
from pfc2.gate import Certification, Level, certify

__all__ = ["admit", "check", "checked_c", "load", "load_text", "plain_c", "released"]


def load(path: Path) -> Unit:
    return frontend.load(path)


def load_text(text: str, name: str, *, invariants: tuple[str, ...] | None = None) -> Unit:
    return frontend.load_text(text, name, invariants=invariants)


def released(unit: Unit) -> Program:
    """The program that is emitted and run: no laws, no ghost measures."""
    return unit.code if unit.code is not None else unit.program


def check(
    unit: Unit,
    target: Target,
    *,
    level: Level = "full",
    inference: bool = True,
    timeout_ms: int = SOLVER_TIMEOUT_MS,
) -> tuple[Unit, Certification]:
    """The verdict of `pfc2.check.check`, or the same judgement without inferred loop bounds."""
    if inference:
        unit = infer.apply(unit, target, timeout_ms=timeout_ms)
    certification = certify(unit.program, target, level=level, code=unit.code, timeout_ms=timeout_ms)
    if certification.c is not None:
        certification = replace(certification, c=release.finish(certification.c, unit))
    return unit, certification


def admit(
    text: str,
    name: str,
    invariants: tuple[str, ...],
    target: Target,
    *,
    level: Level = "full",
    timeout_ms: int = SOLVER_TIMEOUT_MS,
) -> Certification:
    """Judge a source with one supplied invariant per loop and nothing inferred: the path every proposer uses."""
    unit = frontend.load_text(text, name, invariants=invariants)
    return check(unit, target, level=level, inference=False, timeout_ms=timeout_ms)[1]


def checked_c(unit: Unit, target: Target) -> str:
    """C with every runtime check in place and no solver consulted: the reference for 'traps where it must'."""
    return release.finish(emit(released(unit), target, mode="checked").c, unit)


def plain_c(unit: Unit) -> str:
    """The source as an ordinary compiler reads it (the clauses erase themselves through `pfc.h`)."""
    if unit.source_text is None:
        raise ValueError("this unit was not loaded from source text")
    return unit.source_text
