"""The human-readable report of one certification; pure text built from the unit, the verdict and the record."""

from pfc2 import proof
from pfc2.elaborate import Unit
from pfc2.gate import Blocker, Certification


def values(blocker: Blocker) -> str:
    model = blocker.counterexample
    if model is None:
        return ""
    scalars = [f"{value.name} = {value.value}" for value in model.scalars]
    cells = [f"{cell.name}[{cell.index}] = {cell.value}" for cell in model.reads]
    return ", ".join(scalars + cells)


MEANING = {
    "assert": "this assertion may not hold here",
    "entry": "the loop invariant may not hold when the loop starts",
    "preservation": "an iteration may break the loop invariant",
    "postcondition": "the function may return without its ensures holding",
    "call-precondition": "this call may break the callee's requires",
    "bounds": "this index may be outside the array",
    "division": "this division may be by zero or overflow",
    "overflow": "this arithmetic may overflow",
    "conversion": "this value may not fit the element it is stored in",
}


def render(unit: Unit, certification: Certification, record: proof.Record) -> str:
    name = record["source"]["file"]  # type: ignore[index]
    lines = []
    if certification.accepted:
        lines.append(f"{name}: certified ({certification.level})")
    else:
        lines.append(f"{name}: not certified ({certification.level}): {certification.reason}")
    for item in record["law"]:  # type: ignore[attr-defined]
        if item["kind"] == "law":
            lines.append(f"  {item['predicate'].replace('__spec_assert(', 'assert(')}")
        elif item["kind"] == "precondition":
            lines.append(f"  law   {item['function']}: {item['binder']} where {item['predicate']}")
        else:
            lines.append(f"  law   {item['function']}: result where {item['predicate']}")
    for item in record["proof"]:  # type: ignore[attr-defined]
        joiner = "invariant" if item["kind"] == "invariant" else "where"
        lines.append(f"  proof {item['function']}: {item['binder']} {joiner} {item['predicate']}")
    for item in record["inferred"]:  # type: ignore[attr-defined]
        lines.append(
            f"  proof {item['function']}: loop at line {item['line']} invariant {item['invariant']} (inferred)"
        )
    results = certification.proof.results
    proved = sum(result.status == "proved" for result in results)
    lines.append(f"  obligations proved: {proved} of {len(results)} (Z3 {certification.proof.solver_version})")
    primary = [b for b in certification.blockers if not b.status.startswith("depends")]
    for blocker in primary:
        meaning = MEANING.get(blocker.kind, blocker.kind)
        lines.append(f"  {name}:{blocker.location.line}:{blocker.location.column}: {meaning} [{blocker.status}]")
        lines.append(f"      cannot prove: {blocker.goal}")
        if values(blocker):
            lines.append(f"      for example:  {values(blocker)}")
    dependent = len(certification.blockers) - len(primary)
    if dependent:
        lines.append(f"  ({dependent} more obligation(s) depend on the ones above)")
    if not certification.accepted and unit.bare_loops:
        lines.append(
            f"  hint: {unit.bare_loops} loop(s) have no written invariant (inferred bounds may not be enough): "
            "add invariant(...) to the loop, "
            "pass --proof FILE, or let a model try with --prove"
        )
    if certification.accepted:
        emission = certification.emission
        lines.append(f"  bounds/division checks removed: {len(emission.decisions)} of {len(emission.decisions)}")
        kept = len(certification.retained_traps)
        removed = len(emission.overflow) - kept
        note = f"; {kept} overflow trap{'s' if kept != 1 else ''} kept" if kept else ""
        lines.append(f"  overflow checks removed: {removed} of {len(emission.overflow)}{note}")
        for trap in certification.retained_traps:
            lines.append(f"      kept at {name}:{trap.location.line}:{trap.location.column}")
        boundary = record["boundary"]
        assert isinstance(boundary, dict)
        lines.append(f"  entry checks kept for unverified callers: {len(boundary['checked'])}")
        for text in boundary["unchecked"]:
            lines.append(f"      assumed, not checked at entry: {text}")
        lines.append(f"  loops proved to terminate: {len(unit.measures)} of {unit.loops}")
        unverified = record["unverified"]
        assert isinstance(unverified, dict)
        if unverified["functions"]:
            lines.append(f"  declared functions trusted under their contracts: {len(unverified['functions'])}")
            for item in unverified["contracts"]:
                if item["total"] != "total":
                    lines.append(f"      {item['function']}: possible, but not shown to have a result for every input")
    elif certification.level == "full" and certification.memory_would_pass:
        lines.append("  hint: --level memory certifies memory safety and keeps the overflow traps listed above")
    return "\n".join(lines) + "\n"
