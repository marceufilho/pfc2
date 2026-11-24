"""Seal a directory of programs once, and verify the seal before every use.

A held-out set is opened for the first time by the experiment that reports on it. Sealing writes the SHA-256
of every file and a record of when and under which rule; after that any change, addition or removal is
detected. A seal identifies bytes. It does not make a set blind, and it does not stop anyone from reading it.
"""

import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

INVENTORY = "HELDOUT.sha256"
RECORD = "SEALING.json"


@dataclass(frozen=True)
class Verification:
    sealed: bool
    intact: bool
    problems: tuple[str, ...]


def _files(directory: Path) -> dict[str, str]:
    return {
        path.relative_to(directory).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.rglob("*"))
        if path.is_file() and path.name != INVENTORY
    }


def seal(directory: Path, *, rule: str, candidate: str | None) -> int:
    """Seal `directory` under a stated selection rule; a directory that is already sealed is refused."""
    if not directory.is_dir():
        raise ValueError(f"{directory} is not a directory")
    if (directory / INVENTORY).exists() or (directory / RECORD).exists():
        raise FileExistsError(f"{directory} is already sealed; a changed set is a new directory")
    if not rule.strip():
        raise ValueError("state the rule by which the set was selected")
    record = {
        "sealed": datetime.now(UTC).isoformat(timespec="seconds"),
        "rule": rule,
        "candidate": candidate,
        "files": len(_files(directory)),
    }
    if record["files"] == 0:
        raise ValueError("an empty directory cannot be a held-out set")
    (directory / RECORD).write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    listed = _files(directory)
    (directory / INVENTORY).write_text("".join(f"{v}  {k}\n" for k, v in sorted(listed.items())), encoding="utf-8")
    return len(listed)


def verify(directory: Path) -> Verification:
    inventory = directory / INVENTORY
    if not inventory.is_file():
        return Verification(False, False, ("not sealed",))
    recorded = {}
    for line in inventory.read_text(encoding="utf-8").splitlines():
        digest, _, name = line.partition("  ")
        recorded[name] = digest
    current = _files(directory)
    problems = [f"changed: {name}" for name in sorted(recorded) if name in current and current[name] != recorded[name]]
    problems += [f"missing: {name}" for name in sorted(set(recorded) - set(current))]
    problems += [f"added: {name}" for name in sorted(set(current) - set(recorded))]
    return Verification(True, not problems, tuple(problems))


def require_intact(directories: list[Path]) -> None:
    """Refuse to run on a directory that lies under a sealed set whose seal no longer holds."""
    for directory in directories:
        for candidate in (directory, *directory.resolve().parents):
            if (candidate / INVENTORY).is_file():
                state = verify(candidate)
                if not state.intact:
                    raise ValueError(f"held-out set {candidate} differs from its seal: {', '.join(state.problems[:5])}")
                break
