"""Shared scaffolding of every experiment: which PFC2 was run, on which toolchain, sealed how.

An experiment supplies its schema, settings and rows. This module records the candidate (the frozen
inventories and whether the tree matches them), the repository commit and tag when they exist, the solver and
the compiler, and seals the directory. A tree that differs from the frozen candidate is recorded as such; it is
never refused silently and never described as the candidate.
"""

import hashlib
import json
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from pfc2.core import smt, vc
from pfc2.core.target import Target, read_target
from pfc2_eval import evidence

ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "validation" / "freeze"
PROTECTED_ROOTS = ("pfc2",)
SKIPPED = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


@dataclass(frozen=True)
class Candidate:
    name: str | None
    protected_sha256: str | None  # Identity of the candidate: the digest of its protected inventory.
    protected: evidence.InventoryCheck
    baseline: evidence.InventoryCheck
    unlisted: tuple[str, ...]  # Files under the protected roots that the inventory does not list.

    @property
    def intact(self) -> bool:
        return self.protected.verified and not self.unlisted


@dataclass(frozen=True)
class Run:
    evidence: evidence.Evidence
    target: Target
    compiler: str
    candidate: Candidate


def candidate(root: Path = ROOT) -> Candidate:
    """Compare the tree with the frozen inventories; never raises for a tree that differs."""
    freeze = root / "validation" / "freeze"
    inventory = freeze / "protected.sha256"
    try:
        name = json.loads((freeze / "CANDIDATE.json").read_text(encoding="utf-8")).get("candidate")
        digest = hashlib.sha256(inventory.read_bytes()).hexdigest()
        protected = evidence.verify_inventory(root, inventory)
        baseline = evidence.verify_inventory(root, freeze / "baseline.sha256")
        listed = {line.partition("  ")[2] for line in inventory.read_text(encoding="utf-8").splitlines()}
    except (OSError, ValueError, AttributeError):
        empty = evidence.InventoryCheck(0, ())
        return Candidate(None, None, empty, empty, ())
    present = {
        path.relative_to(root).as_posix()
        for top in PROTECTED_ROOTS
        for path in (root / top).rglob("*")
        if path.is_file() and not SKIPPED & set(path.parts)
    }
    return Candidate(
        name if isinstance(name, str) else None, digest, protected, baseline, tuple(sorted(present - listed))
    )


def start(
    experiment: str,
    output: Path,
    *,
    compiler: str,
    seed: int | None,
    settings: Mapping[str, object],
    schema: evidence.Schema,
) -> Run:
    """Create the exclusive evidence directory with provenance, environment and the candidate's identity."""
    if output.exists() or output.is_symlink():
        raise FileExistsError(f"evidence directory {output} exists; choose a new path")
    target = read_target(compiler)
    identity = evidence.repository_identity(ROOT)
    frozen = candidate()
    provenance = evidence.Provenance(
        experiment,
        identity.tag,
        identity.commit,
        seed,
        datetime.now(UTC).isoformat(timespec="seconds"),
        vc.MODEL,
        smt.solver_version(),
        target.compiler,
    )
    configuration = {
        "seed": seed,
        "compiler": compiler,
        "smt_encoding": smt.ENCODING,
        "candidate": frozen.name,
        "candidate_protected_sha256": frozen.protected_sha256,
        "candidate_intact": frozen.intact,
        **dict(settings),
    }
    toolchain = {
        "clang": target.compiler,
        "triple": target.triple,
        "int_bits": target.int_bits,
        "long_bits": target.long_bits,
        "char_signed": target.char_signed,
        "python": sys.version.split()[0],
        "z3": smt.solver_version(),
    }
    environment = evidence.environment_record(
        toolchain, identity, [("protected", frozen.protected), ("baseline", frozen.baseline)]
    )
    environment["unlisted_protected_files"] = list(frozen.unlisted)
    run = evidence.create(
        output, provenance=provenance, configuration=configuration, environment=environment, schema=schema
    )
    return Run(run, target, compiler, frozen)


def finish(run: Run, summary: Mapping[str, object], table: str, derive: evidence.Deriver) -> None:
    """Write summary.json and tables.md, then derive the tidy table and seal."""
    run.evidence.write_text("summary.json", json.dumps(summary, indent=2, sort_keys=True) + "\n")
    run.evidence.write_text("tables.md", table)
    run.evidence.complete(derive)


def progress(text: str) -> None:
    print(text, file=sys.stderr)
