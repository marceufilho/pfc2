"""Read the selected clang target's integer layout without executing user C."""

import re
from dataclasses import dataclass

from pfc2.core.environment import ToolchainError, compiler_output


@dataclass(frozen=True)
class Target:
    compiler: str
    triple: str
    int_bits: int
    long_bits: int
    char_signed: bool = True  # Is plain `char` a signed type on this target? (C11 6.2.5p15 leaves it open.)

    def __post_init__(self) -> None:
        if (
            not self.compiler.strip()
            or not self.triple.strip()
            or type(self.int_bits) is not int
            or type(self.long_bits) is not int
            or not 16 <= self.int_bits <= self.long_bits <= 128
            or type(self.char_signed) is not bool
        ):
            raise ValueError("unsupported target integer layout")


def limits(target: Target, type_: str) -> tuple[int, int]:
    """Smallest and largest value of `char`, `int` or `long` on the target (`char` is 8 bits wide)."""
    if type_ == "char":
        return (-128, 127) if target.char_signed else (0, 255)
    bits = target.int_bits if type_ == "int" else target.long_bits
    return -(2 ** (bits - 1)), 2 ** (bits - 1) - 1


def read_target(compiler: str) -> Target:
    """Probe fixed builtin macros; support clang two's-complement, no padding layouts.

    No arbitrary flags or macros from the input translation unit may redefine
    these limits. The selected compiler's default target is used in this step.
    """
    version = compiler_output(compiler, "--version").splitlines()[0]
    if "clang version" not in version.lower():
        raise ToolchainError("selected executable does not identify itself as clang")
    triple = compiler_output(compiler, "-dumpmachine")
    text = compiler_output(compiler, "-std=c11", "-nostdinc", "-dM", "-E", "-x", "c", "-", source="")
    names = {"__CHAR_BIT__", "__SIZEOF_INT__", "__SIZEOF_LONG__", "__INT_MAX__", "__LONG_MAX__", "__clang__"}
    macros: dict[str, int] = {}
    char_signed = True
    for line in text.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "__CHAR_UNSIGNED__":
            char_signed = False
        if len(parts) >= 2 and parts[1] in names:
            if len(parts) != 3 or not re.fullmatch(r"[0-9]{1,40}[Ll]?", parts[2]) or parts[1] in macros:
                raise ToolchainError("invalid integer layout macro from clang")
            macros[parts[1]] = int(parts[2].rstrip("lL"))
    if set(macros) != names or macros["__CHAR_BIT__"] != 8 or macros["__clang__"] != 1:
        raise ToolchainError("clang did not provide a supported integer layout")
    try:
        target = Target(
            version, triple, 8 * macros["__SIZEOF_INT__"], 8 * macros["__SIZEOF_LONG__"], char_signed=char_signed
        )
    except ValueError as error:
        raise ToolchainError(str(error)) from error
    if (
        macros["__INT_MAX__"] != 2 ** (target.int_bits - 1) - 1
        or macros["__LONG_MAX__"] != 2 ** (target.long_bits - 1) - 1
    ):
        raise ToolchainError("clang integer maxima disagree with the reported storage widths")
    return target
