"""Compile a variant of a program with a driver and run it on concrete cases.

The driver is host C appended to the translation unit, so it reaches file-scope variables that the certified C
declares `static`. It reads the cases from standard input and runs each one in a child process: a trap, a
sanitizer report or a crash ends that case only, and is reported as what it was. An outcome that is not a
complete, well-formed line is never read as agreement.

Buffers are allocated with exactly the number of elements the case gives, so the address sanitizer sees any
access past them.
"""

import subprocess
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pfc2.core import ir
from pfc2.core.config import C_FLAGS
from pfc2_eval.interpret import Inputs

ROOT = Path(__file__).resolve().parents[1]
INCLUDE = ROOT / "pfc2" / "include"
RUNTIME = ROOT / "pfc2" / "runtime" / "pfc_rt.c"
SANITIZE = ("-fsanitize=address,undefined", "-fno-sanitize-recover=all", "-fno-omit-frame-pointer")
# The source as plain C: clauses are erased, so their parameters look unused; `long a[n]` with n == 0 is an
# array bound of zero there, which the certified C does not have.
PLAIN = (
    "-Wno-unused-parameter",
    "-Wno-unused-variable",
    "-Wno-unused-but-set-variable",
    "-Wno-error",  # Lint about odd but defined source (`x <= x`, `g = g`) is not a difference in behaviour.
    "-fno-sanitize=vla-bound",
)
TRAP_SIGNALS = frozenset({4, 5})  # SIGILL, SIGTRAP: what `__builtin_trap` raises on the supported hosts.
RUN_TIMEOUT_SECONDS = 120
PRELUDE = "#include <stdio.h>\n#include <stdlib.h>\n#include <sys/wait.h>\n#include <unistd.h>\n"
Kind = Literal["ok", "trap", "signal", "exit", "missing"]


class BuildError(RuntimeError):
    """The compiler refused a variant: an outcome to record, never to skip."""


@dataclass(frozen=True)
class Outcome:
    kind: Kind
    result: int | None = None
    arrays: tuple[tuple[int, ...], ...] = ()  # In the order of the function's array parameters.
    globals: tuple[int, ...] = ()
    detail: int | None = None  # Signal or exit status.


def driver(program: ir.Program, function: ir.Function) -> str:
    """Host C that reads cases for `function` and prints one line per case."""
    lines = [
        "",
        "/* pfc2_eval driver: host C, not part of the program. */",
        'static long pfc2_eval_read(void) { long v; if (scanf("%ld", &v) != 1) { exit(3); } return v; }',
        "int main(void)",
        "{",
        "    long pfc2_eval_cases = pfc2_eval_read();",
        "    for (long pfc2_eval_case = 0; pfc2_eval_case < pfc2_eval_cases; pfc2_eval_case++) {",
    ]
    arguments, arrays = [], []
    for position, parameter in enumerate(function.parameters):
        symbol, name = parameter.symbol, f"pfc2_eval_p{position}"
        arguments.append(name)
        if isinstance(symbol.type, ir.ArrayType):
            element = symbol.type.element.value
            arrays.append((name, element))
            lines += [
                f"        long {name}_len = pfc2_eval_read();",
                f"        {element} *{name} = malloc((size_t){name}_len * sizeof({element}));",
                f"        for (long k = 0; k < {name}_len; k++) {{ {name}[k] = ({element})pfc2_eval_read(); }}",
            ]
        else:
            lines.append(f"        {symbol.type} {name} = ({symbol.type})pfc2_eval_read();")
    for item in program.globals:
        lines.append(f"        {item.symbol.name} = ({item.symbol.type})pfc2_eval_read();")
    lines += [
        "        fflush(stdout);",
        "        pid_t pfc2_eval_child = fork();",
        "        if (pfc2_eval_child == 0) {",
        f"            long pfc2_eval_result = (long){function.name}({', '.join(arguments)});",
        '            printf("ok %ld", pfc2_eval_result);',
    ]
    for name, _ in arrays:
        lines.append(
            f'            printf(" |"); for (long k = 0; k < {name}_len; k++) {{ printf(" %ld", (long){name}[k]); }}'
        )
    lines.append('            printf(" G");')
    for item in program.globals:
        lines.append(f'            printf(" %ld", (long){item.symbol.name});')
    lines += [
        '            printf("\\n");',
        "            fflush(stdout);",
        "            _exit(0);",
        "        }",
        "        int pfc2_eval_status = 0;",
        "        if (waitpid(pfc2_eval_child, &pfc2_eval_status, 0) != pfc2_eval_child) { exit(4); }",
        '        if (WIFSIGNALED(pfc2_eval_status)) { printf("signal %d\\n", WTERMSIG(pfc2_eval_status)); }',
        "        else if (WEXITSTATUS(pfc2_eval_status) != 0) {",
        '            printf("exit %d\\n", WEXITSTATUS(pfc2_eval_status));',
        "        }",
    ]
    lines += [f"        free({name});" for name, _ in arrays]
    lines += ["    }", "    return 0;", "}", ""]
    return "\n".join(lines)


def compile_c(
    text: str,
    output: Path,
    *,
    clang: str,
    plain: bool = False,
    sanitize: bool = True,
    runtime: bool = False,
) -> None:
    """Compile one translation unit (already holding its driver or `main`) into `output`."""
    source = output.with_suffix(".c")
    source.write_text(text, encoding="utf-8")
    command = [clang, *C_FLAGS, "-Wno-unused-function", *(SANITIZE if sanitize else ())]
    if plain:
        command += [*PLAIN, "-I", str(INCLUDE)]
    command += [str(source), *([str(RUNTIME)] if runtime else []), "-o", str(output)]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=False, timeout=RUN_TIMEOUT_SECONDS)
    except (OSError, subprocess.SubprocessError) as error:
        raise BuildError(f"cannot run {clang} ({type(error).__name__})") from error
    if result.returncode != 0:
        raise BuildError(result.stderr.strip()[-2000:] or f"{clang} exited {result.returncode}")


def with_driver(text: str, program: ir.Program, function: ir.Function) -> str:
    return PRELUDE + text.rstrip("\n") + "\n" + driver(program, function)


def encode(program: ir.Program, function: ir.Function, cases: Sequence[Inputs]) -> str:
    """The cases as the driver reads them; a global without a given value starts at 0."""
    lines = [str(len(cases))]
    for case in cases:
        numbers: list[int] = []
        for parameter in function.parameters:
            name = parameter.symbol.name
            if isinstance(parameter.symbol.type, ir.ArrayType):
                values = case.arrays[name]
                numbers += [len(values), *values]
            else:
                numbers.append(case.scalars[name])
        numbers += [case.globals.get(item.symbol.name, 0) for item in program.globals]
        lines.append(" ".join(map(str, numbers)))
    return "\n".join(lines) + "\n"


def parse(output: str, cases: int, arrays: int) -> list[Outcome]:
    """One outcome per case; a missing or malformed line is `missing`, never a result."""
    outcomes: list[Outcome] = []
    for line in output.splitlines()[:cases]:
        words = line.split()
        try:
            if words[:1] == ["ok"]:
                rest = " ".join(words[2:])
                body, _, tail = rest.rpartition("G")
                groups = [group.split() for group in body.split("|")[1:]]
                if len(groups) != arrays or not (body.strip() == "" or body.lstrip().startswith("|")):
                    raise ValueError("array groups")
                outcomes.append(
                    Outcome(
                        "ok",
                        int(words[1]),
                        tuple(tuple(int(v) for v in group) for group in groups),
                        tuple(int(v) for v in tail.split()),
                    )
                )
            elif words[:1] == ["signal"] and len(words) == 2:
                number = int(words[1])
                outcomes.append(Outcome("trap" if number in TRAP_SIGNALS else "signal", detail=number))
            elif words[:1] == ["exit"] and len(words) == 2:
                outcomes.append(Outcome("exit", detail=int(words[1])))
            else:
                raise ValueError("unknown line")
        except (ValueError, IndexError):
            outcomes.append(Outcome("missing"))
    return outcomes + [Outcome("missing")] * (cases - len(outcomes))


def run_cases(binary: Path, program: ir.Program, function: ir.Function, cases: Sequence[Inputs]) -> list[Outcome]:
    count = sum(isinstance(p.symbol.type, ir.ArrayType) for p in function.parameters)
    try:
        result = subprocess.run(
            [str(binary)],
            input=encode(program, function, cases),
            capture_output=True,
            text=True,
            check=False,
            timeout=RUN_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError):
        return [Outcome("missing")] * len(cases)
    return parse(result.stdout, len(cases), count)


def run_program(binary: Path, stdin: str) -> tuple[int, str]:
    """Exit status (negative for a signal) and standard output of a whole program."""
    result = subprocess.run(
        [str(binary)], input=stdin, capture_output=True, text=True, check=False, timeout=RUN_TIMEOUT_SECONDS
    )
    return result.returncode, result.stdout
