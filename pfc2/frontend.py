"""From a source file to an elaborated unit: bounded reading, PFC2's own preprocessing, elaboration."""

import stat
from pathlib import Path

from pfc2.core.config import MAX_SOURCE_BYTES
from pfc2.core.diagnostics import FrontendError, SourceLocation
from pfc2.elaborate import Unit, elaborate_text
from pfc2.preprocess import preprocess

INCLUDE = Path(__file__).resolve().parent / "include"
HEADER_NAMES = ("pfc.h", "pfc_rt.h", "stdbool.h")


def headers() -> dict[str, str]:
    """The headers a PFC2 source may include, by the name it includes them with."""
    try:
        return {name: (INCLUDE / name).read_text(encoding="utf-8") for name in HEADER_NAMES}
    except (OSError, UnicodeError):
        raise FrontendError(
            "preprocess-resources", "missing PFC2 headers; run from a repository checkout", SourceLocation(str(INCLUDE))
        ) from None


def read_source(source: Path) -> str:
    """Read one bounded UTF-8 regular file; the path is reported as given."""
    location = SourceLocation(str(source))
    try:
        if not stat.S_ISREG(source.stat().st_mode):
            raise FrontendError("source-read", "source must be a regular file", location)
        data = source.read_bytes()[: MAX_SOURCE_BYTES + 1]
    except FrontendError:
        raise
    except (OSError, ValueError):
        raise FrontendError("source-read", "cannot read source file", location) from None
    if len(data) > MAX_SOURCE_BYTES:
        raise FrontendError("source-size", "source exceeds the size limit", location)
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        raise FrontendError("source-encoding", "source is not valid UTF-8", location) from None
    if "\x00" in text or not text.strip():
        raise FrontendError("source-empty", "source is empty or contains a NUL byte", location)
    return text


def load_text(text: str, name: str, *, invariants: tuple[str, ...] | None = None) -> Unit:
    """Preprocess and elaborate source text; positions carry the file name only, never a machine path."""
    return elaborate_text(preprocess(text, name, headers()), name, source_text=text, invariants=invariants)


def load(source: Path, *, invariants: tuple[str, ...] | None = None) -> Unit:
    """Read, preprocess and elaborate one translation unit, optionally with a supplied proof."""
    try:
        source = source.resolve()
    except (OSError, RuntimeError, ValueError):
        raise FrontendError("source-read", "cannot resolve source path", SourceLocation(str(source))) from None
    return load_text(read_source(source), source.name, invariants=invariants)
