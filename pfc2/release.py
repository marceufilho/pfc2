"""The C that leaves the checker: the emitted functions plus the few lines the proof does not cover.

Those lines are fixed text built from the source: one function per string literal that returns its
address, and the C entry point that calls the checked `pfc2_main`. They are listed in the proof file.
"""

from pfc2.clauses import ENTRY, STRING
from pfc2.elaborate import Unit

BANNER = "/* PFC2 boundary (not part of the proof): string constants and the program entry. */"


def boundary(unit: Unit) -> list[str]:
    lines = [f"long {STRING}{number}(void) {{ return (long){token}; }}" for number, token in enumerate(unit.strings, 1)]
    if unit.entry:
        lines.append(f"int main(void) {{ return (int){ENTRY}(); }}")
    return lines


def finish(c: str, unit: Unit) -> str:
    """Append the boundary lines to the emitted C; the emitted text itself is not changed."""
    lines = boundary(unit)
    return c if not lines else c.rstrip("\n") + "\n\n" + "\n".join([BANNER, *lines]) + "\n"
