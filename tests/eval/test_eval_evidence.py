"""Exclusive evidence directories, two data layers and a manifest written last (EV-R5, EV-R21)."""

import hashlib
import json

import pytest

from pfc2_eval import evidence

SCHEMA = evidence.Schema(
    (
        evidence.Column("case_id", "string"),
        evidence.Column("agreement", "boolean"),
        evidence.Column("wall_ms", "number", nullable=True),
        evidence.Column("failure_kind", "string", nullable=True, allowed=("timeout", "crash")),
    )
)
PROVENANCE = evidence.Provenance(
    experiment="differential",
    tag=None,
    commit="28e3704",
    seed=0,
    timestamp="2026-11-05T12:00:00+00:00",
    vc_model="vc-v4-test",
    solver_version="4.16.0",
    clang="clang version 19.1.1",
)


def derive(records):
    return [
        {"case_id": r.identifier, "agreement": r.data["agreed"], "wall_ms": r.data.get("ms"), "failure_kind": None}
        for r in records
    ]


def _create(tmp_path, name="differential-test"):
    return evidence.create(
        tmp_path / name,
        provenance=PROVENANCE,
        configuration={"cases": 2},
        environment={"python": "3.12"},
        schema=SCHEMA,
    )


def test_refuses_existing_directory(tmp_path):
    (tmp_path / "taken").mkdir()
    with pytest.raises(FileExistsError):
        _create(tmp_path, "taken")
    assert not (tmp_path / "taken" / "configuration.json").exists()


def test_create_writes_configuration_environment_and_schema_only(tmp_path):
    run = _create(tmp_path)
    names = sorted(p.name for p in run.directory.iterdir())
    assert names == ["configuration.json", "environment.json", "schema.json"]
    configuration = json.loads((run.directory / "configuration.json").read_text(encoding="utf-8"))
    assert configuration["provenance"]["commit"] == "28e3704" and configuration["settings"] == {"cases": 2}
    schema = json.loads((run.directory / "schema.json").read_text(encoding="utf-8"))
    assert schema["provenance"] == list(evidence.PROVENANCE_COLUMNS)
    assert schema["columns"][3]["allowed"] == ["timeout", "crash"]
    assert evidence.status(run.directory).complete is False


def test_raw_records_are_write_once_shards(tmp_path):
    run = _create(tmp_path)
    path = run.record("case", "sum", "0001", {"agreed": True, "ms": 1.5})
    assert path == run.directory / "raw" / "case" / "sum.jsonl"
    run.record("case", "sum", "0002", {"agreed": False})
    with pytest.raises(FileExistsError):
        run.record("case", "sum", "0001", {"agreed": False})
    with pytest.raises(ValueError):
        run.record("case", "../escape", "x", {"agreed": False})
    lines = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert lines == [{"id": "0001", "data": {"agreed": True, "ms": 1.5}}, {"id": "0002", "data": {"agreed": False}}]
    assert [(r.unit, r.shard, r.identifier) for r in evidence.records(run.directory)] == [
        ("case", "sum", "0001"),
        ("case", "sum", "0002"),
    ]


def test_legacy_single_file_records_are_still_read(tmp_path):
    run = _create(tmp_path)
    legacy = run.directory / "raw" / "case" / "0007.json"
    legacy.parent.mkdir(parents=True)
    legacy.write_text('{"agreed": true}\n', encoding="utf-8")
    assert [(r.unit, r.shard, r.identifier, r.data) for r in evidence.records(run.directory)] == [
        ("case", None, "0007", {"agreed": True})
    ]


def test_complete_run_has_marker_sealed_in_a_closed_manifest(tmp_path):
    run = _create(tmp_path)
    run.record("case", "sum", "0002", {"agreed": False, "ms": None})
    run.record("case", "sum", "0001", {"agreed": True, "ms": 1.5})
    run.write_text("tables.md", "| a |\n")
    run.complete(derive)
    files = {p.relative_to(run.directory).as_posix() for p in run.directory.rglob("*") if p.is_file()}
    manifest = json.loads((run.directory / "manifest.json").read_text(encoding="utf-8"))
    assert set(manifest["files"]) == files - {"manifest.json"}
    assert "COMPLETE" in manifest["files"] and "observations.jsonl" in manifest["files"]
    for name, digest in manifest["files"].items():
        assert hashlib.sha256((run.directory / name).read_bytes()).hexdigest() == digest
    rows = [
        json.loads(line) for line in (run.directory / "observations.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert [r["case_id"] for r in rows] == ["0001", "0002"]  # records are sorted by unit, shard, identifier
    assert rows[0]["experiment"] == "differential" and rows[0]["evidence_dir"] == "differential-test"
    assert rows[0]["tag"] is None and rows[1]["wall_ms"] is None
    assert evidence.status(run.directory).complete is True
    loaded = evidence.load(run.directory)
    assert loaded.observations == tuple(rows) and loaded.configuration["settings"] == {"cases": 2}


def test_schema_violation_leaves_the_run_incomplete(tmp_path):
    run = _create(tmp_path)
    run.record("case", "sum", "0001", {"agreed": "yes"})
    with pytest.raises(evidence.SchemaError, match="agreement"):
        run.complete(derive)
    assert not (run.directory / "COMPLETE").exists() and not (run.directory / "manifest.json").exists()
    assert not (run.directory / "observations.jsonl").exists()
    assert evidence.status(run.directory).complete is False


@pytest.mark.parametrize(
    "row, message",
    [
        ({"case_id": "x", "agreement": True, "wall_ms": 1, "failure_kind": "late"}, "allowed"),
        ({"case_id": "x", "agreement": True, "wall_ms": 1}, "columns"),
        ({"case_id": "x", "agreement": True, "wall_ms": True, "failure_kind": None}, "number"),
        ({"case_id": None, "agreement": True, "wall_ms": 1, "failure_kind": None}, "null"),
    ],
)
def test_row_validation_messages(row, message):
    with pytest.raises(evidence.SchemaError, match=message):
        evidence.validate_row(SCHEMA, row)


def test_marker_alone_or_tampering_is_not_completion(tmp_path):
    run = _create(tmp_path)
    run.record("case", "sum", "0001", {"agreed": True})
    (run.directory / "COMPLETE").write_text("", encoding="utf-8")
    assert evidence.status(run.directory).complete is False
    (run.directory / "COMPLETE").unlink()
    run.complete(derive)
    (run.directory / "raw" / "case" / "sum.jsonl").write_text(
        '{"id": "0001", "data": {"agreed": false}}\n', encoding="utf-8"
    )
    status = evidence.status(run.directory)
    assert status.complete is False and "checksum" in status.reason
    with pytest.raises(ValueError):
        evidence.load(run.directory)


def test_unlisted_file_breaks_the_closed_manifest(tmp_path):
    run = _create(tmp_path)
    run.record("case", "sum", "0001", {"agreed": True})
    run.complete(derive)
    (run.directory / "extra.txt").write_text("late", encoding="utf-8")
    assert evidence.status(run.directory).complete is False


def test_observations_rebuild_from_raw_records_byte_for_byte(tmp_path):
    run = _create(tmp_path)
    for shard, identifier in (("k2", "b"), ("k1", "a"), ("k2", "c")):
        run.record("case", shard, identifier, {"agreed": True, "ms": 2})
    run.complete(derive)
    rebuilt = evidence.rebuild_observations(run.directory, derive)
    assert rebuilt == (run.directory / "observations.jsonl").read_bytes()


def test_complete_requires_at_least_one_record_and_refuses_double_completion(tmp_path):
    run = _create(tmp_path)
    with pytest.raises(ValueError, match="raw record"):
        run.complete(derive)
    run.record("case", "sum", "0001", {"agreed": True})
    run.complete(derive)
    with pytest.raises(FileExistsError):
        run.complete(derive)


def test_reserved_names_cannot_be_written_as_derived_files(tmp_path):
    run = _create(tmp_path)
    for name in ("manifest.json", "COMPLETE", "raw/x.json", "observations.jsonl", "../x", "/abs", "a/../b"):
        with pytest.raises(ValueError):
            run.write_text(name, "x")
    assert run.write_text("sources/sum-plain.c", "int x;\n") == run.directory / "sources" / "sum-plain.c"


def test_repository_identity_reads_tag_and_commit_through_an_injected_runner(tmp_path):
    answers = {("git", "rev-parse", "HEAD"): "abc123\n", ("git", "describe", "--tags", "--exact-match"): "freeze-v4\n"}

    def run(arguments):
        return answers[arguments]

    identity = evidence.repository_identity(tmp_path, run=run)
    assert identity == evidence.RepositoryIdentity(commit="abc123", tag="freeze-v4")

    def untagged(arguments):
        if arguments[1] == "describe":
            raise evidence.CommandFailed("no tag")
        return "abc123\n"

    assert evidence.repository_identity(tmp_path, run=untagged) == evidence.RepositoryIdentity("abc123", None)


def test_inventory_verification_detects_a_changed_protected_file(tmp_path):
    (tmp_path / "pfc").mkdir()
    (tmp_path / "pfc" / "a.py").write_text("x = 1\n", encoding="utf-8")
    digest = hashlib.sha256(b"x = 1\n").hexdigest()
    inventory = tmp_path / "protected.sha256"
    inventory.write_text(f"{digest}  pfc/a.py\n", encoding="utf-8")
    assert evidence.verify_inventory(tmp_path, inventory) == evidence.InventoryCheck(1, ())
    (tmp_path / "pfc" / "a.py").write_text("x = 2\n", encoding="utf-8")
    assert evidence.verify_inventory(tmp_path, inventory) == evidence.InventoryCheck(1, ("pfc/a.py",))
