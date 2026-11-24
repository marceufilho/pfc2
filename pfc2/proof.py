"""The proof file: a separate, self-contained record written beside the certified C.

It states the law (what the author asked for), the proof (types and invariants that carry it),
every obligation with its formula, status and query identity, and the C that was released. It
embeds the preprocessed program, so `replay` needs neither the source tree nor a network.

The file is evidence to be recomputed, never a certificate to be trusted: `replay` elaborates the
embedded program again, runs the same checker with the recorded target and budget, and reports
every field that differs. Hashes identify text; they do not authenticate an author.
"""

from pathlib import PurePath

from pfc2 import release
from pfc2.bundle import check as check_invariants
from pfc2.check import check
from pfc2.core import smt, vc
from pfc2.core.diagnostics import FrontendError
from pfc2.core.digest import sha256_text
from pfc2.core.ir import to_data
from pfc2.core.target import Target
from pfc2.elaborate import Unit, elaborate_text
from pfc2.gate import LEVELS, Certification

FORMAT = "pfc-proof-v3"
Record = dict[str, object]


def _site(decision: object) -> Record:
    data = to_data(decision)
    assert isinstance(data, dict) and isinstance(data["location"], dict)
    return {
        "kind": data["kind"],
        "line": data["location"]["line"],
        "column": data["location"]["column"],
        "condition": data["condition"],
        "removed": data["removed"],
        "obligations": data["obligation_ids"],
    }


def build(unit: Unit, certification: Certification) -> Record:
    """Describe one certification as plain JSON data, without wall-clock or machine-path fields."""
    laws = {law.name for law in unit.laws}
    kinds = {"parameter": "precondition", "result": "postcondition", "local": "type"}
    stated = [
        {"function": w.function, "kind": kinds[w.kind], "binder": w.binder, "predicate": w.predicate}
        | {"line": w.location.line}
        for w in unit.wheres
        if w.function not in laws
    ]
    proof = certification.proof
    emission = certification.emission
    return {
        "format": FORMAT,
        "level": certification.level,
        "accepted": certification.accepted,
        "reason": certification.reason,
        "source": {
            "file": PurePath(unit.filename).name,
            "sha256": sha256_text(unit.source_text) if unit.source_text is not None else None,
        },
        "preprocessed": unit.preprocessed,
        "target": to_data(proof.target),
        "solver": {"z3": proof.solver_version, "timeout_ms": proof.timeout_ms, "encoding": proof.encoding},
        "vc_model": proof.vc_model,
        "emitter": emission.emitter,
        "law": [
            {"function": law.name, "kind": "law", "binder": law.name, "predicate": law.text}
            | {"line": law.location.line}
            for law in unit.laws
        ]
        + [item for item in stated if item["kind"] != "type"],
        "proof": [item for item in stated if item["kind"] == "type"]
        + [
            {"function": site.function, "kind": "invariant", "binder": f"loop {number}", "predicate": invariant}
            | {"line": site.line}
            for number, (site, invariant) in enumerate(zip(unit.loop_sites, unit.invariants, strict=False), 1)
        ],
        "bundle": {"invariants": list(unit.invariants)} if unit.invariants else None,
        "inferred": [
            {"function": item.function, "line": item.line, "invariant": item.invariant} for item in unit.inferred
        ],
        "termination": {
            "loops": unit.loops,
            "proved": [
                {"function": m.function, "line": m.location.line, "measure": m.predicate} for m in unit.measures
            ],
        },
        "obligations": [
            {
                "id": result.obligation.id,
                "kind": result.obligation.kind,
                "category": result.obligation.category,
                "line": result.obligation.location.line,
                "column": result.obligation.location.column,
                "goal": vc.render_term(result.obligation.goal),
                "hypotheses": [hypothesis.kind for hypothesis in result.obligation.hypotheses],
                "dependencies": list(result.obligation.dependencies),
                "status": result.status,
                "query_id": result.query_id,
            }
            for result in proof.results
        ],
        "entry": [
            {"function": entry.query.function, "status": entry.status, "query_id": entry.query_id}
            for entry in proof.entry_results
        ],
        "guards": [_site(decision) for decision in emission.decisions],
        "overflow": [_site(decision) for decision in emission.overflow],
        "retained_traps": [_site(decision) for decision in certification.retained_traps],
        "boundary": {
            "checked": [check.text for check in emission.requires_checks if check.rendered is not None],
            "unchecked": [check.text for check in emission.requires_checks if check.rendered is None],
        },
        "unverified": {
            "functions": list(unit.externals),
            "contracts": [
                {"function": e.query.function, "consistent": e.consistent, "total": e.total, "witness": e.witness}
                for e in proof.external_results
                if e.query.function in unit.externals
            ],
            "lines": release.boundary(unit),
        },
        "c": certification.c,
        "c_sha256": sha256_text(certification.c) if certification.c is not None else None,
    }


def replay(record: object) -> list[str]:
    """Recompute a proof file from its embedded program; return the names of the fields that differ."""
    if not isinstance(record, dict) or record.get("format") != FORMAT:
        return ["format"]
    try:
        solver, target, source = record["solver"], record["target"], record["source"]
        if solver["z3"] != smt.solver_version() or solver["encoding"] != smt.ENCODING:
            return ["solver"]
        if record["level"] not in LEVELS or type(solver["timeout_ms"]) is not int:
            return ["format"]
        layout = Target(
            target["compiler"],
            target["triple"],
            target["int_bits"],
            target["long_bits"],
            char_signed=target.get("char_signed", True),
        )
        supplied = record.get("bundle")
        invariants = check_invariants(supplied["invariants"]) if supplied is not None else None
        unit = elaborate_text(record["preprocessed"], source["file"], invariants=invariants)
        unit, certification = check(unit, layout, level=record["level"], timeout_ms=solver["timeout_ms"])
    except FrontendError:
        return ["preprocessed"]
    except (KeyError, TypeError, ValueError, AttributeError):
        return ["format"]
    recomputed = build(unit, certification)
    recomputed["source"] = source  # The source file is not needed, so its recorded identity is not re-derived.
    return sorted(key for key in recomputed.keys() | record.keys() if recomputed.get(key) != record.get(key))
