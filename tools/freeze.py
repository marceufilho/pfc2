"""Hash inventories that pin a frozen candidate of PFC2.

    uv run python tools/freeze.py --check          compare the tree with the committed inventories
    uv run python tools/freeze.py --write NAME     write them, for a new candidate called NAME

`protected.sha256` lists what a result depends on: the package (engine, surface passes, headers, runtime), the
locked dependencies and the configuration. `baseline.sha256` lists what the candidate was checked against when it
was frozen: tests, examples and the agreement recording. A file that is listed must be unchanged. A file that is
not listed is reported by `--check` under "not in the inventory" and fails it for the protected set: new trusted
code is a new candidate, not an addition.

Both files use the format of `sha256sum`, so `sha256sum --check validation/freeze/protected.sha256` verifies the
listed files without this tool.
"""

import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT / "validation" / "freeze"
PROTECTED = ("pfc2", "pyproject.toml", "uv.lock", ".python-version")
BASELINE = ("tests", "examples")
SKIPPED = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}


def files(roots: tuple[str, ...]) -> list[Path]:
    found: list[Path] = []
    for root in roots:
        path = ROOT / root
        if path.is_file():
            found.append(path)
        elif path.is_dir():
            found.extend(item for item in sorted(path.rglob("*")) if item.is_file() and not SKIPPED & set(item.parts))
    return sorted(found)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(roots: tuple[str, ...]) -> dict[str, str]:
    return {path.relative_to(ROOT).as_posix(): digest(path) for path in files(roots)}


def render(entries: dict[str, str]) -> str:
    return "".join(f"{value}  {name}\n" for name, value in sorted(entries.items()))


def parse(text: str) -> dict[str, str]:
    entries = {}
    for line in text.splitlines():
        value, _, name = line.partition("  ")
        if len(value) != 64 or not name:
            raise ValueError(f"not an inventory line: {line[:80]!r}")
        entries[name] = value
    return entries


def compare(recorded: dict[str, str], current: dict[str, str]) -> dict[str, list[str]]:
    return {
        "changed": sorted(name for name in recorded if name in current and recorded[name] != current[name]),
        "missing": sorted(name for name in recorded if name not in current),
        "not in the inventory": sorted(name for name in current if name not in recorded),
    }


def check() -> tuple[bool, dict[str, dict[str, list[str]]]]:
    """Compare the tree with both inventories; extra baseline files are reported but do not fail."""
    report = {}
    passed = True
    for name, roots in (("protected", PROTECTED), ("baseline", BASELINE)):
        difference = compare(parse((FREEZE / f"{name}.sha256").read_text(encoding="utf-8")), inventory(roots))
        report[name] = difference
        failing = [
            kind
            for kind, names in difference.items()
            if names and (name == "protected" or kind != "not in the inventory")
        ]
        passed = passed and not failing
    return passed, report


def write(name: str) -> None:
    FREEZE.mkdir(parents=True, exist_ok=True)
    counts = {}
    for label, roots in (("protected", PROTECTED), ("baseline", BASELINE)):
        entries = inventory(roots)
        (FREEZE / f"{label}.sha256").write_text(render(entries), encoding="utf-8")
        counts[label] = len(entries)
    record = {"candidate": name, "files": counts, "format": "sha256sum"}
    (FREEZE / "CANDIDATE.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Write or check the hash inventories of a frozen PFC2 candidate.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="compare the tree with the committed inventories")
    group.add_argument("--write", metavar="NAME", help="write the inventories for a new candidate")
    options = parser.parse_args(arguments)
    if options.write:
        write(options.write)
        print(f"freeze: wrote inventories for {options.write}")
        return 0
    try:
        passed, report = check()
    except (OSError, ValueError) as error:
        print(f"freeze: cannot read the inventories: {error}", file=sys.stderr)
        return 1
    for name, difference in report.items():
        for kind, names in difference.items():
            for item in names:
                print(f"{name}: {kind}: {item}")
    print("freeze: the tree is the frozen candidate" if passed else "freeze: the tree differs from the candidate")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
