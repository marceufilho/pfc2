"""Package boundaries: which modules may reach a process, the network or the command line."""

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "pfc2"
# Modules allowed to leave the process: the compiler query, the model service, the commands, the editor server.
OUTWARD = {"core/environment.py", "core/target.py", "llm.py", "cli.py", "__main__.py", "lsp/server.py"}


def _imports(path: Path) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"), filename=str(path))):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            names.add(module)
            names.update(f"{module}.{alias.name}" for alias in node.names)
    return names


def test_only_the_named_modules_can_spawn_a_process_or_open_a_connection() -> None:
    banned = ("subprocess", "socket", "urllib", "http", "openai", "pygls", "pfc2.cli", "pfc2.llm", "pfc2.lsp.server")
    for path in sorted(PACKAGE.rglob("*.py")):
        name = path.relative_to(PACKAGE).as_posix()
        if name in OUTWARD:
            continue
        offending = sorted(n for n in _imports(path) if n.startswith(banned))
        # prove.py receives its `ask` function from the caller and core.target goes through core.environment.
        assert not offending, (name, offending)


def test_the_package_depends_on_nothing_outside_itself_but_its_declared_libraries() -> None:
    allowed = ("pfc2", "z3", "pycparser", "openai", "pygls", "lsprotocol")
    stdlib = __import__("sys").stdlib_module_names
    for path in sorted(PACKAGE.rglob("*.py")):
        for name in _imports(path):
            top = name.split(".")[0]
            assert not top or top in stdlib or top in allowed, (path.name, name)


def test_the_compiler_core_does_not_import_the_language_layer() -> None:
    for path in sorted((PACKAGE / "core").glob("*.py")):
        outside = sorted(n for n in _imports(path) if n.startswith("pfc2") and not n.startswith("pfc2.core"))
        assert not outside, (path.name, outside)
