"""The one path from an elaborated unit to a verdict: infer what can be inferred, then let the gate judge."""

from dataclasses import replace

from pfc2 import infer, release
from pfc2.core.config import SOLVER_TIMEOUT_MS
from pfc2.core.target import Target
from pfc2.elaborate import Unit
from pfc2.gate import Certification, Level, certify


def check(
    unit: Unit, target: Target, *, level: Level = "full", timeout_ms: int = SOLVER_TIMEOUT_MS
) -> tuple[Unit, Certification]:
    """Return the unit as it was judged (with the loop bounds that were inferred and proved) and its verdict."""
    unit = infer.apply(unit, target, timeout_ms=timeout_ms)
    certification = certify(unit.program, target, level=level, code=unit.code, timeout_ms=timeout_ms)
    if certification.c is not None:
        certification = replace(certification, c=release.finish(certification.c, unit))
    return unit, certification
