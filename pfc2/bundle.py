"""Proof bundles: the part of a proof that arrives as data, from a person, a file or a model.

A bundle is JSON `{"invariants": [...]}` with one call-free C expression per loop, in source order.
It is parsed and placed as annotation text; nothing in it is executed, and it carries no authority:
the same gate decides, whoever wrote it. The rules are those of the frozen `admit()`.
"""

import json
import re

from pfc2.core.config import MAX_PROPOSAL_BYTES

_EXPRESSION = re.compile(r"[a-zA-Z0-9_ ()\[\]+*/<>=!&|\-]+")
_CALL = re.compile(r"[a-zA-Z_]\w*\s*\(")


def check(expressions: object) -> tuple[str, ...]:
    """Validate a list of invariant expressions as inert annotation text."""
    if not isinstance(expressions, list) or not expressions:
        raise ValueError("expected a non-empty list of invariants")
    for expression in expressions:
        if (
            not isinstance(expression, str)
            or not expression.strip()
            or not _EXPRESSION.fullmatch(expression)
            or any(token in expression for token in ("//", "/*", "*/"))
            or _CALL.search(expression)
        ):
            raise ValueError("invariants must be call-free C subset expressions")
    return tuple(expression.strip() for expression in expressions)


def parse(reply: str, loops: int) -> tuple[str, ...]:
    """Read a bundle, or a proof file that contains one, for a program with `loops` loops."""
    if len(reply.encode("utf-8")) > MAX_PROPOSAL_BYTES * 64:
        raise ValueError("proof is too large")
    try:
        data = json.loads(reply)
    except json.JSONDecodeError:
        raise ValueError("the proof is not JSON") from None
    if isinstance(data, dict) and "format" in data and isinstance(data.get("bundle"), dict):
        data = data["bundle"]  # A proof file written by an earlier build.
    elif len(reply.encode("utf-8")) > MAX_PROPOSAL_BYTES:
        raise ValueError(f"proof exceeds {MAX_PROPOSAL_BYTES} bytes")
    if not isinstance(data, dict) or set(data) != {"invariants"}:
        raise ValueError('expected {"invariants": [...]} with one expression per loop')
    invariants = check(data["invariants"])
    if len(invariants) != loops:
        raise ValueError(f"expected {loops} invariant(s), one per loop in source order, got {len(invariants)}")
    return invariants
