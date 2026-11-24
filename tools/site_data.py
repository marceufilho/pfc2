"""Write the files the site is built from: the checker bundle, the example programs and the documentation pages.

Everything is derived from the repository: `pfc2/` sources with their digests, `examples/examples.json` with the
result of a native run of each example, and `docs/*.md`. `--check` compares what is on disk with a fresh build
and writes nothing. Generated files are never edited by hand.
"""

import argparse
import hashlib
import json
import os
import posixpath
import re
import subprocess
import sys
import tempfile
from collections import deque
from pathlib import Path
from typing import Any

from pfc2 import web
from pfc2.core.config import C_FLAGS, CLANG_ENV_VAR, DEFAULT_CLANG

BUNDLE_PATTERNS = ("pfc2/*.py", "pfc2/core/*.py", "pfc2/include/*.h")
# The browser checks programs; it does not run commands, call a model service or serve an editor.
BUNDLE_EXCLUDED = {"pfc2/cli.py", "pfc2/prove.py", "pfc2/llm.py", "pfc2/__main__.py"}
DOCS = "docs"
PAGES = "src/content/docs/docs"
ORDER = (
    "README",
    "01-tour",
    "02-language",
    "03-proofs",
    "04-programs",
    "05-commands",
    "06-examples",
    "07-design",
    "08-implementation",
    "09-limits",
    "10-pfc-and-pfc2",
    "11-editor",
)
GROUPS = {
    "functions": "Functions",
    "programs": "Programs",
    "wrong": "Programs that must be refused",
}
_LINK = re.compile(r"\]\(([^)\s]+)\)")


class SiteDataError(Exception):
    """A source of the site is missing or inconsistent."""


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"


def bundle(root: Path) -> dict[str, Any]:
    """The Python sources and headers the browser loads, each with its digest."""
    files: dict[str, str] = {}
    for pattern in BUNDLE_PATTERNS:
        for path in sorted(root.glob(pattern)):
            name = path.relative_to(root).as_posix()
            if name not in BUNDLE_EXCLUDED:
                files[name] = path.read_text(encoding="utf-8")
    digests = {name: hashlib.sha256(text.encode("utf-8")).hexdigest() for name, text in files.items()}
    return {"files": files, "sha256": digests}


def programs(root: Path) -> list[dict[str, Any]]:
    """Every example with the summary of a native run, which the browser run must equal."""
    listing = json.loads((root / "examples" / "examples.json").read_text(encoding="utf-8"))
    result = []
    for case in listing:
        path = root / "examples" / case["path"]
        source = path.read_text(encoding="utf-8")
        level = case.get("level", "full")
        outcome = web.analyze(source, name=path.name, level=level, timeout_ms=web.MAX_TIMEOUT_MS)
        if not outcome["ok"]:
            raise SiteDataError(f"{case['path']} is not accepted as a source: {outcome['diagnostic']['rule']}")
        if outcome["accepted"] == ("refused" in case):
            raise SiteDataError(f"{case['path']} does not get the verdict examples.json states")
        folder = case["path"].split("/")[0]
        group = "wrong" if folder == "wrong" else "programs" if "expected" in case else "functions"
        result.append(
            {
                "id": case["path"][:-2],
                "group": group,
                "name": path.name,
                "level": level,
                "source": source,
                "reference": web.summary(outcome),
            }
        )
    return result


def _rewrite(text: str, page: str, root: Path) -> str:
    def replace(match: re.Match[str]) -> str:
        target = match.group(1)
        if re.match(r"[a-z]+:", target) or target.startswith("#"):
            return match.group(0)
        path, _, fragment = target.partition("#")
        anchor = f"#{fragment}" if fragment else ""
        stem = path[:-3] if path.endswith(".md") else path
        if "/" in path or stem not in ORDER:
            resolved = posixpath.normpath(posixpath.join(DOCS, path))
            raise SiteDataError(f"{DOCS}/{page}.md links outside the documentation set: {target} ({resolved})")
        up = "./" if page == "README" else "../"
        return f"]({up}{anchor})" if stem == "README" else f"]({up}{stem}/{anchor})"

    return _LINK.sub(replace, text)


def documentation(root: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    present = {path.stem for path in (root / DOCS).glob("*.md")}
    if present != set(ORDER):
        raise SiteDataError(f"{DOCS}/ and the page order disagree: {sorted(present ^ set(ORDER))}")
    for position, page in enumerate(ORDER):
        data = (root / DOCS / f"{page}.md").read_bytes()
        heading, _, body = data.decode("utf-8").partition("\n")
        if not heading.startswith("# "):
            raise SiteDataError(f"{DOCS}/{page}.md does not start with a title")
        title = "Documentation" if page == "README" else heading[2:].strip().replace('"', '\\"')
        meta = (
            f'---\ntitle: "{title}"\nsidebar:\n  order: {position}\n'
            f"source: {DOCS}/{page}.md\nsource_sha256: {hashlib.sha256(data).hexdigest()}\n---\n"
        )
        files[f"{PAGES}/{'index' if page == 'README' else page}.md"] = meta + _rewrite(body, page, root)
    return files


def gallery(listed: list[dict[str, Any]]) -> str:
    """One page with every example, its expected verdict and a link that opens it in the playground."""
    lines = [
        "---",
        'title: "Examples"',
        "description: Every example program, with the verdict it must get and a link that opens it in the playground.",
        "---",
        "",
        "Each program below opens in the [playground](../playground/). The verdicts are the ones written by hand in",
        "`examples/examples.json`; the test suite and this site's browser tests hold PFC2 to them.",
        "",
    ]
    for group, label in GROUPS.items():
        lines += [f"## {label}", ""]
        for program in (p for p in listed if p["group"] == group):
            accepted = program["reference"]["accepted"]
            verdict = f"certified at level `{program['level']}`" if accepted else "refused"
            lines += [
                f"### {program['id']}",
                "",
                f"Expected: **{verdict}**. [Open in the playground](../playground/#example={program['id']})",
                "",
                "```c",
                program["source"].rstrip("\n"),
                "```",
                "",
            ]
    return "\n".join(lines)


GAME = {"wall": "11_flag/flag", "open": "wrong/flag_without_wall"}
GAME_START, GAME_FLAG = (0, 2), (7, 2)
GAME_BOARD = {"width": 8, "height": 5, "start": list(GAME_START), "flag": list(GAME_FLAG), "wall_column": 4}
_GAME_DRIVER = """
#include <stdio.h>
long step_x(long x, long move);
long step_y(long y, long move);
int main(void) {
    for (long x = 0; x < 8; x++)
        for (long y = 0; y < 5; y++)
            for (long move = 0; move < 4; move++)
                printf("%ld %ld\\n", step_x(x, move), step_y(y, move));
    return 0;
}
"""


def _moves(c: str, flags: list[str]) -> list[list[list[list[int]]]]:
    """Run the compiled rules on every square and move: `table[x][y][move]` is the square the player lands on."""
    clang = os.environ.get(CLANG_ENV_VAR, DEFAULT_CLANG)
    with tempfile.TemporaryDirectory(prefix="pfc2-game-") as directory:
        rules, driver, binary = Path(directory) / "rules.c", Path(directory) / "driver.c", Path(directory) / "game"
        rules.write_text(c, encoding="utf-8")
        driver.write_text(_GAME_DRIVER, encoding="utf-8")
        command = [clang, *C_FLAGS, *flags, str(rules), str(driver), "-o", str(binary)]
        try:
            subprocess.run(command, capture_output=True, text=True, check=True, timeout=60)
            output = subprocess.run([str(binary)], capture_output=True, text=True, check=True, timeout=60).stdout
        except (OSError, subprocess.SubprocessError) as error:
            raise SiteDataError(f"cannot compile or run the game rules ({type(error).__name__})") from None
    cells = iter([int(a), int(b)] for a, b in (line.split() for line in output.splitlines()))
    return [[[next(cells) for _ in range(4)] for _ in range(5)] for _ in range(8)]


def _shortest_win(table: list[list[list[list[int]]]]) -> list[int] | None:
    """The shortest sequence of moves from the start to the flag, by exhaustive search; None when there is none."""
    start, flag = GAME_START, GAME_FLAG
    seen: dict[tuple[int, int], list[int]] = {start: []}
    queue = deque([start])
    while queue:
        square = queue.popleft()
        if square == flag:
            return seen[square]
        for move in range(4):
            landed = table[square[0]][square[1]][move]
            reached = (landed[0], landed[1])
            if reached not in seen:
                seen[reached] = [*seen[square], move]
                queue.append(reached)
    return None


def game(root: Path) -> dict[str, Any]:
    """The capture-the-flag page: for each variant, the verdict of the checker and the moves of the compiled rules.

    With the wall the rules are the certified C. Without it nothing is certified, so the same source is compiled
    as plain C. The table is produced by running the program; the page contains no second copy of the rules.
    """
    include = ["-I", str(root / "pfc2" / "include")]
    variants: dict[str, Any] = {}
    for name, example in GAME.items():
        source = (root / "examples" / f"{example}.c").read_text(encoding="utf-8")
        outcome = web.analyze(source, name=f"{example.split('/')[1]}.c", timeout_ms=web.MAX_TIMEOUT_MS)
        if not outcome["ok"] or outcome["accepted"] != (name == "wall"):
            raise SiteDataError(f"{example} does not get the verdict the game page relies on")
        obligations = outcome["record"]["obligations"]
        failed = [b for b in outcome["blockers"] if not str(b["status"]).startswith("depends")]
        table = _moves(outcome["c"], []) if outcome["accepted"] else _moves(source, include)
        variants[name] = {
            "example": example,
            "source": source,
            "accepted": outcome["accepted"],
            "certified_c": outcome["accepted"],
            "obligations": len(obligations),
            "proved": sum(o["status"] == "proved" for o in obligations),
            "refusal": [{"line": b["line"], "column": b["column"], "meaning": b["meaning"]} for b in failed],
            "table": table,
            "shortest_win": _shortest_win(table),
        }
    return {**GAME_BOARD, "variants": variants}


_LOCK_DRIVER = """
#include <stdio.h>
long opens(long n, const long keys[]);
int main(void) {
    for (long a = 0; a < 10; a++)
        for (long b = 0; b < 10; b++)
            for (long c = 0; c < 10; c++)
                for (long d = 0; d < 10; d++) {
                    long keys[4] = {a, b, c, d};
                    if (opens(4, keys) == 1) printf("%ld%ld%ld%ld\\n", a, b, c, d);
                }
    return 0;
}
"""


def _openers(c: str, flags: list[str]) -> list[str]:
    """The digit combinations, of all 10,000, for which the compiled `opens` returns 1."""
    clang = os.environ.get(CLANG_ENV_VAR, DEFAULT_CLANG)
    with tempfile.TemporaryDirectory(prefix="pfc2-lock-") as directory:
        lock, driver, binary = Path(directory) / "lock.c", Path(directory) / "driver.c", Path(directory) / "lock"
        lock.write_text(c, encoding="utf-8")
        driver.write_text(_LOCK_DRIVER, encoding="utf-8")
        command = [clang, *C_FLAGS, *flags, str(lock), str(driver), "-o", str(binary)]
        try:
            subprocess.run(command, capture_output=True, text=True, check=True, timeout=60)
            return subprocess.run([str(binary)], capture_output=True, text=True, check=True, timeout=60).stdout.split()
        except (OSError, subprocess.SubprocessError) as error:
            raise SiteDataError(f"cannot compile or run the lock ({type(error).__name__})") from None


def showcase(root: Path) -> dict[str, Any]:
    """The programs the front page and the lock page show: verdict, refusal with its counterexample, and, for a
    lock, which digit combinations open it. A certified lock is run from its certified C; a refused one releases
    no C, so its source is compiled as plain C, as the game page does."""
    listing = json.loads((root / "showcase" / "showcase.json").read_text(encoding="utf-8"))
    include = ["-I", str(root / "pfc2" / "include")]
    result = []
    for case in listing:
        path = root / "showcase" / case["path"]
        source = path.read_text(encoding="utf-8")
        level = case.get("level", "full")
        outcome = web.analyze(source, name=path.name, level=level, timeout_ms=web.MAX_TIMEOUT_MS)
        if not outcome["ok"] or outcome["accepted"] == ("refused" in case):
            raise SiteDataError(f"showcase/{case['path']} does not get the verdict showcase.json states")
        obligations = outcome["record"]["obligations"]
        failed = [b for b in outcome["blockers"] if not str(b["status"]).startswith("depends")]
        summary = web.summary(outcome)
        entry: dict[str, Any] = {
            "id": "showcase/" + case["path"][:-2],
            "group": "showcase",
            "path": case["path"],
            "name": path.name,
            "level": level,
            "source": source,
            "accepted": outcome["accepted"],
            "obligations": len(obligations),
            "proved": sum(o["status"] == "proved" for o in obligations),
            "guards_removed": sum(bool(removed) for _, _, removed in summary["guards"]),
            "overflow_removed": sum(bool(removed) for _, _, removed in summary["overflow"]),
            "laws": len(outcome["record"]["law"]),
            # The solver's example inputs are not stored: models differ from one run to the next.
            "refusal": [
                {"line": b["line"], "column": b["column"], "meaning": b["meaning"], "goal": b["goal"]} for b in failed
            ],
            "reference": summary,
        }
        if "openers" in case:
            entry["certified_c"] = outcome["accepted"]
            entry["tried"] = 10_000
            entry["openers"] = _openers(outcome["c"], []) if outcome["accepted"] else _openers(source, include)
            if entry["openers"] != case["openers"]:
                raise SiteDataError(f"showcase/{case['path']} does not open for the combinations showcase.json states")
        result.append(entry)
    return {"programs": result}


def build(root: Path) -> dict[str, str]:
    """Every generated file by path relative to the site directory."""
    listed = programs(root)
    files = {
        "public/engine/pfc2-bundle.json": _json(bundle(root)),
        "public/data/programs.json": _json({"programs": listed}),
        "public/data/game.json": _json(game(root)),
        "public/data/showcase.json": _json(showcase(root)),
        "src/content/docs/examples.md": gallery(listed),
    }
    files.update(documentation(root))
    return files


def check(output: Path, files: dict[str, str]) -> list[str]:
    """Paths that are missing, different or unexpected under the generated directories."""
    problems = {name for name, text in files.items() if not (output / name).is_file()}
    problems |= {
        name
        for name, text in files.items()
        if (output / name).is_file() and (output / name).read_text(encoding="utf-8") != text
    }
    existing: set[str] = set()
    for directory, pattern in (("public/data", "*.json"), (PAGES, "*.md")):
        existing |= {path.relative_to(output).as_posix() for path in (output / directory).rglob(pattern)}
    return sorted(problems | (existing - set(files)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python tools/site_data.py",
        description="Write the site's checker bundle, example data and documentation pages from the repository.",
        epilog="Example: uv run python tools/site_data.py --check",
    )
    parser.add_argument("--output", type=Path, default=Path("site"), help="site directory")
    parser.add_argument("--check", action="store_true", help="compare with a fresh build; write nothing")
    arguments = parser.parse_args(argv)
    try:
        files = build(Path.cwd())
    except (SiteDataError, OSError, KeyError, ValueError) as error:
        print(f"site_data: {error}", file=sys.stderr)
        return 1
    if arguments.check:
        problems = check(arguments.output, files)
        for name in problems:
            print(f"site_data: differs from a fresh build: {name}", file=sys.stderr)
        return 1 if problems else 0
    for name, text in files.items():
        path = arguments.output / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    print(f"wrote {len(files)} files, {sum(len(text.encode('utf-8')) for text in files.values()) // 1024} KiB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
