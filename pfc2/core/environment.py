"""Read toolchain metadata at explicit process and filesystem boundaries."""

import os
import subprocess

from pfc2.core.config import PROCESS_TIMEOUT_SECONDS


class ToolchainError(RuntimeError):
    """An external compiler could not provide usable metadata."""


def compiler_environment() -> dict[str, str]:
    """Remove implicit include paths and dependency-file output directives."""
    environment = os.environ.copy()
    for name in (
        "CPATH",
        "C_INCLUDE_PATH",
        "CPLUS_INCLUDE_PATH",
        "OBJC_INCLUDE_PATH",
        "DEPENDENCIES_OUTPUT",
        "SUNPRO_DEPENDENCIES",
    ):
        environment.pop(name, None)
    return environment


def compiler_output(compiler: str, *arguments: str, source: str | None = None) -> str:
    """Query clang using an argument list and optional fixed stdin source."""
    if not compiler.strip():
        raise ToolchainError("clang executable cannot be empty; set --clang or PFC_CLANG")
    if "\x00" in compiler:
        raise ToolchainError("clang executable cannot contain NUL; set --clang or PFC_CLANG")
    try:
        result = subprocess.run(
            [compiler, *arguments],
            input=source,
            capture_output=True,
            text=True,
            check=True,
            timeout=PROCESS_TIMEOUT_SECONDS,
            env=compiler_environment(),
        )
    except (OSError, subprocess.SubprocessError, UnicodeError) as error:
        raise ToolchainError(
            f"cannot query clang ({type(error).__name__}); install clang or set --clang / PFC_CLANG"
        ) from error
    output = result.stdout.strip()
    if not output:
        raise ToolchainError("clang returned empty metadata")
    return output
