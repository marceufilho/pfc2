"""Strict gate: C is produced only when the requested level is completely proved.

The frozen checker, authorization and emitter decide everything; this module only refuses.

    memory  every required obligation (laws, types, contracts, bounds, division, call preconditions)
            is admitted with its dependencies and every bounds/division guard is removed.
            Overflow traps that are not proved stay in the C and are listed.
    full    additionally every reported obligation is admitted: no guard and no trap remains.

Both levels require a satisfiable law for every function (a contradictory law proves everything)
and keep the emitter's entry checks: the proof covers the function, not its unverified callers.
Arithmetic in annotations is mathematical, so at `memory` a law describes every execution that
does not stop at a kept overflow trap; at `full` there is no such trap.
Timeout, unknown and solver errors never certify. A refusal carries no C.
"""

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

import z3

from pfc2.core import ir, smt, vc
from pfc2.core.authorization import authorize
from pfc2.core.config import SOLVER_TIMEOUT_MS
from pfc2.core.diagnostics import SourceLocation
from pfc2.core.emit import GUARD_LINE, OVERFLOW_LINE, Decision, Emission, emit
from pfc2.core.target import Target

Level = Literal["memory", "full"]
LEVELS: tuple[Level, ...] = ("memory", "full")


@dataclass(frozen=True)
class Blocker:
    obligation_id: str
    kind: str
    function: str
    location: SourceLocation
    goal: str
    status: str
    counterexample: smt.Counterexample | None


@dataclass(frozen=True)
class Certification:
    level: Level
    accepted: bool
    reason: str
    blockers: tuple[Blocker, ...]
    proof: smt.CheckReport  # Functions and laws.
    emission: Emission  # Functions only; its C is released through `c`.
    c: str | None
    retained_traps: tuple[Decision, ...]
    memory_would_pass: bool


def _function_of(obligation: vc.Obligation, program: ir.Program) -> str:
    """Name of the function whose source range holds the obligation (reporting only)."""
    best = ""
    for function in program.functions:
        same_file = function.location.file == obligation.location.file
        if same_file and function.location.line <= obligation.location.line:
            best = function.name
    return best


def _verdict(
    level: Level,
    program: ir.Program,
    conditions: vc.VCReport,
    proof: smt.CheckReport,
    target: Target,
    code: Emission | None,
) -> tuple[bool, str, tuple[Blocker, ...]]:
    """Judge one program. `code` is its emission when the program is the one released as C.

    The program that also holds the laws is never emitted, so only its obligations and entry
    consistency are judged; whether arithmetic may influence a removed check is a question about
    the emitted functions and is answered there (`authorization.allowed`).
    """
    authorization = authorize(program, conditions, target, proof)
    admitted = set(authorization.proved)
    wanted = [r for r in proof.results if level == "full" or r.obligation.category == "required"]
    blockers = tuple(
        Blocker(
            r.obligation.id,
            r.obligation.kind,
            _function_of(r.obligation, program),
            r.obligation.location,
            vc.render_term(r.obligation.goal),
            r.status if r.status != "proved" else "depends on an unproved obligation",
            r.counterexample,
        )
        for r in wanted
        if r.obligation.id not in admitted
    )
    unsatisfiable = [e for e in proof.entry_results if e.status != "sat"]
    if unsatisfiable:
        first = unsatisfiable[0]
        detail = "is contradictory" if first.status == "unsat" else f"was not shown consistent ({first.status})"
        return False, f"the law of {first.query.function} cannot be satisfied: it {detail}", blockers
    for external in proof.external_results:
        name = external.query.function
        if external.consistent != "sat":
            detail = (
                "is contradictory"
                if external.consistent == "unsat"
                else f"was not shown possible ({external.consistent})"
            )
            return False, f"the contract of {name} cannot be satisfied: it {detail}", blockers
        if external.total not in {"total", "partial"}:
            return False, f"the contract of {name} was not shown possible for every input ({external.total})", blockers
        if external.total == "partial":
            return (
                False,
                f"the contract of {name} promises a result that some input has no result for: {external.witness}",
                blockers,
            )
    if blockers:
        return False, f"{len(blockers)} obligation(s) not proved", blockers
    if code is None:
        return True, "every obligation of this level is proved", blockers
    if not authorization.allowed:
        return False, authorization.reason, blockers
    guards = [d for d in code.decisions if not d.removed]
    traps = [d for d in code.overflow if not d.removed] if level == "full" else []
    pattern = re.compile(f"{GUARD_LINE.pattern}|{OVERFLOW_LINE.pattern}", re.M) if level == "full" else GUARD_LINE
    if guards or traps or pattern.search(code.c):
        return False, "the emitter kept a runtime check that the proof does not cover", blockers
    return True, "every obligation of this level is proved", blockers


def certify(
    program: ir.Program,
    target: Target,
    *,
    level: Level = "full",
    code: ir.Program | None = None,
    timeout_ms: int = SOLVER_TIMEOUT_MS,
    solver_factory: Callable[[], smt.Solver] = z3.Solver,
) -> Certification:
    """Check `program` (functions and laws) and emit `code` (functions only; defaults to `program`)."""
    if level not in LEVELS:
        raise ValueError("level must be memory or full")
    cache = smt.SolverCache()
    conditions = vc.generate(program)
    proof = smt.check(program, target, timeout_ms=timeout_ms, solver_factory=solver_factory, cache=cache)
    emitted = code if code is not None else program
    emitted_proof = (
        proof
        if emitted is program
        else smt.check(emitted, target, timeout_ms=timeout_ms, solver_factory=solver_factory, cache=cache)
    )
    emission = emit(emitted, target, mode="verified", proof=emitted_proof)
    code_verdict = {
        name: _verdict(name, emitted, vc.generate(emitted), emitted_proof, target, emission) for name in LEVELS
    }
    verdict = (
        code_verdict
        if emitted is program
        else {name: _verdict(name, program, conditions, proof, target, None) for name in LEVELS}
    )
    accepted, reason, blockers = verdict[level]
    if accepted and not code_verdict[level][0]:
        accepted, reason, blockers = code_verdict[level]
    return Certification(
        level,
        accepted,
        reason,
        blockers,
        proof,
        emission,
        emission.c if accepted else None,
        tuple(d for d in emission.overflow if not d.removed) if accepted else (),
        verdict["memory"][0] and code_verdict["memory"][0],
    )
