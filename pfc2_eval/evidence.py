"""Exclusive evidence directories with two data layers and a manifest written last.

Layout (evaluation-architecture.md D6/D9):

    configuration.json   provenance plus experiment settings (seeds, budgets, digests)
    environment.json     toolchain metadata, tag, commit and inventory check
    schema.json          columns of observations.jsonl
    raw/<unit>/<shard>.jsonl write-once records, one line per observation, one shard per kernel
    observations.jsonl   tidy table derived from raw/ by a pure function
    tables.md, summary.json and other derived files written by the experiment
    COMPLETE             execution finished; sealed by the manifest
    manifest.json        written last; SHA-256 of every other file

Completion requires both the marker and a closed manifest whose hashes match and whose
file set equals the directory contents. Hashes identify bytes; they do not authenticate
an origin that controls both data and manifest, and no file here is a proof.
"""

import hashlib
import json
import re
import subprocess
from collections.abc import Callable, Iterable, Mapping, Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

MANIFEST_VERSION = "pfc-eval-evidence-v1"
PROVENANCE_COLUMNS = (
    "experiment",
    "evidence_dir",
    "tag",
    "commit",
    "seed",
    "timestamp",
    "vc_model",
    "solver_version",
    "clang",
)
RESERVED = frozenset(
    {"configuration.json", "environment.json", "schema.json", "observations.jsonl", "COMPLETE", "manifest.json"}
)
_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}")
ColumnType = Literal["string", "integer", "number", "boolean"]
Deriver = Callable[[tuple["Record", ...]], Iterable[Mapping[str, object]]]


class SchemaError(ValueError):
    """A derived row does not match schema.json; the run stays incomplete."""


class CommandFailed(RuntimeError):
    """A repository command exited unsuccessfully."""


@dataclass(frozen=True)
class Column:
    name: str
    type: ColumnType
    nullable: bool = False
    allowed: tuple[str, ...] | None = None


@dataclass(frozen=True)
class Schema:
    columns: tuple[Column, ...]

    def __post_init__(self) -> None:
        names = [column.name for column in self.columns]
        if len(set(names)) != len(names) or set(names) & set(PROVENANCE_COLUMNS):
            raise ValueError("schema columns must be unique and distinct from provenance columns")
        if any(not _NAME.fullmatch(name) or name != name.lower() for name in names):
            raise ValueError("column names are snake_case identifiers")

    @classmethod
    def from_data(cls, data: object) -> "Schema":
        if not isinstance(data, dict) or data.get("provenance") != list(PROVENANCE_COLUMNS):
            raise ValueError("invalid schema file")
        columns = []
        for item in data.get("columns", ()):
            if not isinstance(item, dict) or set(item) != {"name", "type", "nullable", "allowed"}:
                raise ValueError("invalid schema column")
            allowed = item["allowed"]
            columns.append(
                Column(item["name"], item["type"], item["nullable"], None if allowed is None else tuple(allowed))
            )
        return cls(tuple(columns))


@dataclass(frozen=True)
class Provenance:
    """Columns repeated in every tidy row so any directory can be concatenated with others."""

    experiment: str
    tag: str | None
    commit: str | None
    seed: int | None
    timestamp: str
    vc_model: str
    solver_version: str
    clang: str


@dataclass(frozen=True)
class Record:
    unit: str
    shard: str | None
    identifier: str
    data: dict[str, object]


@dataclass(frozen=True)
class Status:
    complete: bool
    reason: str


@dataclass(frozen=True)
class Loaded:
    configuration: dict[str, object]
    environment: dict[str, object]
    schema: Schema
    observations: tuple[dict[str, object], ...]


@dataclass(frozen=True)
class RepositoryIdentity:
    commit: str | None
    tag: str | None


@dataclass(frozen=True)
class InventoryCheck:
    checked: int
    mismatched: tuple[str, ...]

    @property
    def verified(self) -> bool:
        return self.checked > 0 and not self.mismatched


def _dump(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def _write_new(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        stream.write(text)
    return path


def _check_name(name: str) -> str:
    if not _NAME.fullmatch(name):
        raise ValueError(f"invalid evidence file name: {name!r}")
    return name


def validate_row(schema: Schema, row: Mapping[str, object]) -> None:
    expected = {column.name for column in schema.columns}
    if set(row) != expected:
        raise SchemaError(f"row columns {sorted(row)} differ from schema columns {sorted(expected)}")
    for column in schema.columns:
        value = row[column.name]
        if value is None:
            if not column.nullable:
                raise SchemaError(f"column {column.name} is null but not nullable")
            continue
        if column.type == "boolean":
            valid = isinstance(value, bool)
        elif column.type == "integer":
            valid = type(value) is int
        elif column.type == "number":
            valid = type(value) in (int, float)
        else:
            valid = isinstance(value, str) and (column.allowed is None or value in column.allowed)
        if not valid:
            detail = f"not among allowed values {column.allowed}" if column.allowed else f"not a {column.type}"
            raise SchemaError(f"column {column.name}: {value!r} is {detail}")


def _observations(
    records: tuple[Record, ...], derive: Deriver, schema: Schema, provenance: Provenance, name: str
) -> bytes:
    if not records:
        raise ValueError("an experiment needs at least one raw record before completion")
    lines = []
    fixed = {**asdict(provenance), "evidence_dir": name}
    for row in derive(records):
        validate_row(schema, row)
        lines.append(json.dumps({**fixed, **row}, sort_keys=True, separators=(",", ":")))
    if not lines:
        raise ValueError("the deriver produced no observation rows")
    return ("\n".join(lines) + "\n").encode("utf-8")


def records(directory: Path) -> tuple[Record, ...]:
    """Raw records in a deterministic order: by unit, shard, identifier.

    Shards are `raw/<unit>/<shard>.jsonl` with one `{"id", "data"}` object per line. Legacy campaigns
    with one `raw/<unit>/<id>.json` file per record are still read, with `shard` None.
    """
    items = []
    root = directory / "raw"
    for path in sorted(root.rglob("*")) if root.is_dir() else ():
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if len(relative.parts) != 2 or path.suffix not in (".json", ".jsonl"):
            raise ValueError(f"unexpected raw record layout: {relative}")
        unit = relative.parts[0]
        if path.suffix == ".json":
            data = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(data, dict):
                raise ValueError(f"raw record is not an object: {relative}")
            items.append(Record(unit, None, path.stem, data))
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            entry = json.loads(line)
            if not isinstance(entry, dict) or set(entry) != {"id", "data"} or not isinstance(entry["data"], dict):
                raise ValueError(f"malformed shard line in {relative}")
            items.append(Record(unit, path.stem, str(entry["id"]), entry["data"]))
    return tuple(sorted(items, key=lambda r: (r.unit, r.shard or "", r.identifier)))


def _hashes(directory: Path) -> dict[str, str]:
    return {
        path.relative_to(directory).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(directory.rglob("*"))
        if path.is_file() and not path.is_symlink()
    }


class Evidence:
    """One experiment run; `create` is the only constructor."""

    def __init__(self, directory: Path, provenance: Provenance, schema: Schema) -> None:
        self.directory = directory
        self.provenance = provenance
        self.schema = schema
        self._seen: set[tuple[str, str, str]] = set()

    def record(self, unit: str, shard: str, identifier: str, data: Mapping[str, object]) -> Path:
        """Append one write-once record to the unit's shard; a second record with the same identity fails."""
        self._open()
        key = (_check_name(unit), _check_name(shard), _check_name(identifier))
        if key in self._seen:
            raise FileExistsError(f"raw record {unit}/{shard}/{identifier} already written")
        self._seen.add(key)
        path = self.directory / "raw" / key[0] / f"{key[1]}.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as stream:
            stream.write(
                json.dumps({"id": identifier, "data": dict(data)}, sort_keys=True, separators=(",", ":")) + "\n"
            )
        return path

    def write_text(self, name: str, text: str) -> Path:
        """Derived human/machine outputs such as tables.md or summary.json."""
        self._open()
        parts = name.split("/")
        if (
            name in RESERVED
            or "\\" in name
            or parts[0] in RESERVED
            or parts[0] == "raw"
            or any(not _NAME.fullmatch(part) or part in (".", "..") for part in parts)
        ):
            raise ValueError(f"reserved, absolute or unsafe evidence file name: {name!r}")
        return _write_new(self.directory.joinpath(*parts), text)

    def complete(self, derive: Deriver) -> dict[str, str]:
        """Derive the tidy table, mark completion, then seal everything in the manifest."""
        self._open()
        table = _observations(records(self.directory), derive, self.schema, self.provenance, self.directory.name)
        with (self.directory / "observations.jsonl").open("xb") as stream:
            stream.write(table)
        _write_new(self.directory / "COMPLETE", "")
        hashes = _hashes(self.directory)
        _write_new(self.directory / "manifest.json", _dump({"schema_version": MANIFEST_VERSION, "files": hashes}))
        return hashes

    def _open(self) -> None:
        if (self.directory / "manifest.json").exists():
            raise FileExistsError("evidence directory is already sealed")


def create(
    directory: Path,
    *,
    provenance: Provenance,
    configuration: Mapping[str, object],
    environment: Mapping[str, object],
    schema: Schema,
) -> Evidence:
    """Exclusive creation; existing paths are refused so sealed evidence is never touched."""
    if directory.exists() or directory.is_symlink():
        raise FileExistsError(f"choose a new evidence directory; {directory} exists")
    directory.mkdir(parents=True, exist_ok=False)
    _write_new(
        directory / "configuration.json",
        _dump({"experiment": provenance.experiment, "provenance": asdict(provenance), "settings": dict(configuration)}),
    )
    _write_new(directory / "environment.json", _dump(dict(environment)))
    columns = [asdict(column) for column in schema.columns]
    _write_new(directory / "schema.json", _dump({"provenance": list(PROVENANCE_COLUMNS), "columns": columns}))
    return Evidence(directory, provenance, schema)


def status(directory: Path) -> Status:
    """Both the marker and a valid closed manifest are required; neither alone suffices."""
    manifest_path = directory / "manifest.json"
    if not (directory / "COMPLETE").is_file():
        return Status(False, "COMPLETE marker missing")
    if not manifest_path.is_file():
        return Status(False, "manifest missing; the run did not finish sealing")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return Status(False, "manifest unreadable")
    if not isinstance(manifest, dict) or manifest.get("schema_version") != MANIFEST_VERSION:
        return Status(False, "unknown manifest schema")
    listed = manifest.get("files")
    if not isinstance(listed, dict) or "COMPLETE" not in listed or "observations.jsonl" not in listed:
        return Status(False, "manifest does not seal COMPLETE and observations.jsonl")
    present = _hashes(directory)
    present.pop("manifest.json", None)
    if set(present) != set(listed):
        return Status(False, "directory contents differ from the sealed file set")
    if any(present[name] != digest for name, digest in listed.items()):
        return Status(False, "checksum mismatch against the sealed manifest")
    return Status(True, "complete and sealed")


def load(directory: Path) -> Loaded:
    """Read a complete directory; incomplete or altered evidence raises."""
    state = status(directory)
    if not state.complete:
        raise ValueError(f"evidence is not complete: {state.reason}")
    configuration = json.loads((directory / "configuration.json").read_text(encoding="utf-8"))
    environment = json.loads((directory / "environment.json").read_text(encoding="utf-8"))
    schema = Schema.from_data(json.loads((directory / "schema.json").read_text(encoding="utf-8")))
    rows = tuple(
        json.loads(line) for line in (directory / "observations.jsonl").read_text(encoding="utf-8").splitlines()
    )
    if not isinstance(configuration, dict) or not isinstance(environment, dict):
        raise ValueError("configuration and environment must be JSON objects")
    return Loaded(configuration, environment, schema, rows)


def rebuild_observations(directory: Path, derive: Deriver) -> bytes:
    """Recompute the tidy table from raw records and saved provenance/schema; never edits files."""
    configuration = json.loads((directory / "configuration.json").read_text(encoding="utf-8"))
    schema = Schema.from_data(json.loads((directory / "schema.json").read_text(encoding="utf-8")))
    provenance = Provenance(**configuration["provenance"])
    return _observations(records(directory), derive, schema, provenance, directory.name)


def _git(arguments: tuple[str, ...], cwd: Path) -> str:
    result = subprocess.run(arguments, cwd=cwd, capture_output=True, text=True, check=False, timeout=30)
    if result.returncode != 0:
        raise CommandFailed(f"{arguments[1]} exited {result.returncode}")
    return result.stdout


def repository_identity(repository: Path, *, run: Callable[[tuple[str, ...]], str] | None = None) -> RepositoryIdentity:
    """Commit and exact tag of the checked-out tree; a missing tag is recorded as None, never invented."""

    def execute(arguments: tuple[str, ...]) -> str:
        return run(arguments) if run is not None else _git(arguments, repository)

    try:
        commit: str | None = execute(("git", "rev-parse", "HEAD")).strip() or None
    except (CommandFailed, OSError):
        commit = None
    try:
        tag: str | None = execute(("git", "describe", "--tags", "--exact-match")).strip() or None
    except (CommandFailed, OSError):
        tag = None
    return RepositoryIdentity(commit, tag)


def verify_inventory(repository: Path, inventory: Path) -> InventoryCheck:
    """Recompute a `sha256sum`-style inventory; mismatches name the drifted files."""
    mismatched = []
    checked = 0
    for line in inventory.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        digest, _, name = line.partition("  ")
        checked += 1
        path = repository / name
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        if actual != digest:
            mismatched.append(name)
    return InventoryCheck(checked, tuple(mismatched))


def environment_record(
    toolchain: Mapping[str, object], identity: RepositoryIdentity, inventories: Sequence[tuple[str, InventoryCheck]]
) -> dict[str, object]:
    """environment.json content: toolchain metadata plus repository identity and inventory results."""
    return {
        "toolchain": dict(toolchain),
        "commit": identity.commit,
        "tag": identity.tag,
        "inventories": {
            name: {"checked": check.checked, "mismatched": list(check.mismatched), "verified": check.verified}
            for name, check in inventories
        },
    }
