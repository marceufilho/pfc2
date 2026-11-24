"""Bounded search for a proof: ask, check, explain the refusal, ask again.

The asker is untrusted and replaceable (a model, a file, a person). Each reply is parsed as data
by `bundle.parse` and judged by the same gate as a handwritten proof; a transport failure or a
malformed reply uses up an attempt. Nothing here can certify: only `gate.certify` does.
"""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from pfc2 import bundle, frontend
from pfc2.check import check
from pfc2.core.config import PROPOSER_ATTEMPTS, SOLVER_TIMEOUT_MS
from pfc2.core.diagnostics import FrontendError
from pfc2.core.target import Target
from pfc2.elaborate import Unit
from pfc2.gate import Certification, Level

Ask = Callable[[str, int], str]


@dataclass(frozen=True)
class Attempt:
    number: int
    reply: str | None
    accepted: bool
    problem: str | None


@dataclass(frozen=True)
class Outcome:
    attempts: tuple[Attempt, ...]
    unit: Unit | None
    certification: Certification | None


def instruction(source: str, loops: int) -> str:
    return (
        "The C file below contains functions and laws. A law is a property that must hold for every input "
        "allowed by the `where` types of its parameters. Supply the loop invariants that let a checker prove "
        "every law, every array index, every division and the absence of signed overflow.\n"
        f'Return only JSON {{"invariants": [...]}} with exactly {loops} loop invariant(s), one per loop in source '
        f"order ({loops} loop{'s' if loops != 1 else ''}). Each is a call-free C integer/Boolean expression over "
        "names in scope at that loop. Annotation arithmetic is mathematical; there are no quantifiers. "
        "Do not change the code or the laws.\n\n" + source
    )


def feedback(certification: Certification) -> str:
    lines = [f"The checker refused: {certification.reason}."]
    for blocker in [b for b in certification.blockers if b.counterexample is not None or b.status != "proved"][:3]:
        lines.append(
            f"- {blocker.kind} at line {blocker.location.line} [{blocker.status}]: cannot prove {blocker.goal}"
        )
        if blocker.counterexample is not None:
            values = [f"{v.name} = {v.value}" for v in blocker.counterexample.scalars]
            values += [f"{c.name}[{c.index}] = {c.value}" for c in blocker.counterexample.reads]
            lines.append("  counterexample state: " + ", ".join(values))
    return "\n".join(lines)


def prove(
    source: Path,
    target: Target,
    *,
    ask: Ask,
    level: Level = "full",
    timeout_ms: int = SOLVER_TIMEOUT_MS,
    attempts: int = PROPOSER_ATTEMPTS,
) -> Outcome:
    """At most `attempts` proposals; the first one the gate accepts is returned with its certification."""
    plain = frontend.load(source)
    assert plain.source_text is not None
    prompt = instruction(plain.source_text, plain.loops)
    history = ""
    made: list[Attempt] = []
    for number in range(1, attempts + 1):
        reply = None
        try:
            reply = ask(prompt + history, number)
            unit = frontend.load(source, invariants=bundle.parse(reply, plain.loops))
            unit, certification = check(unit, target, level=level, timeout_ms=timeout_ms)
        except (ValueError, OSError, FrontendError) as error:
            made.append(Attempt(number, reply, False, str(error)))
            history = "\n\nYour previous reply could not be used: " + str(error)
            if reply is not None:
                history += "\nPrevious reply:\n" + reply
            continue
        if certification.accepted:
            made.append(Attempt(number, reply, True, None))
            return Outcome(tuple(made), unit, certification)
        made.append(Attempt(number, reply, False, certification.reason))
        history = "\n\nPrevious reply:\n" + reply + "\n" + feedback(certification)
    return Outcome(tuple(made), None, None)
