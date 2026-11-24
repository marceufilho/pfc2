"""Command line of the certified front end: check, build, replay, elaborate.

    pfc2 check FILE              prove the laws and types; write nothing
    pfc2 build FILE              the same, then write FILE's C and a separate proof file
    pfc2 replay FILE.proof.json  recompute a proof file offline
    pfc2 elaborate FILE          show the contracts the checker sees

The proof may be written in the source (`where` on locals, `INVARIANT`), come from a file
(`--proof FILE`: a bundle or the proof file of an earlier build) or be requested from a model
(`--prove`, opt-in: it sends the source file to the configured service).

stdout carries results, stderr diagnostics. Exit 0 success, 1 failure, 2 usage error.
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path

from pfc2 import bundle, frontend, llm, proof, report
from pfc2.check import check
from pfc2.core import ir, smt
from pfc2.core.config import (
    C_FLAGS,
    CLANG_ENV_VAR,
    DEFAULT_CLANG,
    MAX_REPORT_BYTES,
    MAX_SOLVER_TIMEOUT_MS,
    OPENAI_KEY_ENV,
    PROCESS_TIMEOUT_SECONDS,
    SOLVER_TIMEOUT_MS,
)
from pfc2.core.diagnostics import FrontendError
from pfc2.core.environment import ToolchainError
from pfc2.core.target import Target, read_target
from pfc2.elaborate import Unit
from pfc2.gate import LEVELS, Certification
from pfc2.prove import prove

DEFAULT_OUTPUT = Path("build") / "pfc2"
RUNTIME = Path(__file__).resolve().parent / "runtime" / "pfc_rt.c"


def _timeout(value: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("timeout must be an integer number of milliseconds") from None
    if not 1 <= number <= MAX_SOLVER_TIMEOUT_MS:
        raise argparse.ArgumentTypeError(f"timeout must be 1..{MAX_SOLVER_TIMEOUT_MS} milliseconds")
    return number


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pfc2",
        description="PFC2: prove the contracts and laws of a C program, then emit C without the proved checks.",
        epilog="Example: pfc2 build examples/02_fill/fill.c",
    )
    commands = parser.add_subparsers(dest="command", required=True, metavar="{check,build,run,replay,elaborate,lsp}")

    def source_command(name: str, summary: str, example: str) -> argparse.ArgumentParser:
        command = commands.add_parser(name, help=summary, description=summary, epilog=f"Example: {example}")
        command.add_argument("file", type=Path, help="C source using pfc.h")
        return command

    for name, summary in (
        ("check", "Prove the laws and types of one file; write nothing."),
        ("build", "Prove one file, then write its C and a separate proof file."),
        ("run", "Prove one program, compile its certified C with the console runtime and run it."),
    ):
        command = source_command(name, summary, f"pfc2 {name} examples/02_fill/fill.c")
        command.add_argument(
            "--level",
            choices=LEVELS,
            default="full",
            help="full: no runtime check remains (default); memory: unproved overflow traps are kept and listed",
        )
        command.add_argument(
            "--clang", default=os.environ.get(CLANG_ENV_VAR, DEFAULT_CLANG), help="clang for the target"
        )
        command.add_argument("--timeout-ms", type=_timeout, default=SOLVER_TIMEOUT_MS, help="Z3 budget per obligation")
        command.add_argument("--json", action="store_true", help="print the proof record as JSON")
        supplied = command.add_mutually_exclusive_group()
        supplied.add_argument(
            "--proof", type=Path, help="loop invariants as JSON, or the proof file of an earlier build"
        )
        supplied.add_argument(
            "--prove",
            action="store_true",
            help=f"ask the configured model for the proof (sends the source file; needs {OPENAI_KEY_ENV} set)",
        )
        if name == "run":
            command.add_argument("--stdin", type=Path, help="file given to the program as standard input")
        if name == "build":
            command.add_argument(
                "--output", type=Path, help=f"directory for the two files (default {DEFAULT_OUTPUT}/NAME)"
            )
            command.add_argument("--force", action="store_true", help="replace the two files of an earlier build")
            command.add_argument("--dry-run", action="store_true", help="prove and report, write nothing")
    source_command("elaborate", "Print the program with the contracts the checker sees.", "pfc2 elaborate FILE")
    commands.add_parser(
        "lsp",
        help="Serve an editor over stdin/stdout (Language Server Protocol).",
        description="Serve an editor over stdin/stdout: diagnostics, hover and document symbols.",
        epilog="Example: pfc2 lsp   (started by the editor extension, not by hand)",
    )
    replay = commands.add_parser(
        "replay",
        help="Recompute a proof file offline and compare every field.",
        description="Recompute a proof file offline and compare every field.",
        epilog="Example: pfc2 replay build/pfc2/count/count.proof.json",
    )
    replay.add_argument("file", type=Path, help="a .proof.json written by build")
    return parser


def _write(directory: Path, stem: str, record: proof.Record, *, force: bool) -> tuple[Path, Path]:
    code, record_path = directory / f"{stem}.c", directory / f"{stem}.proof.json"
    existing = [path for path in (code, record_path) if path.exists()]
    if existing and not force:
        raise FileExistsError(f"{existing[0]} exists; choose another --output or pass --force to replace it")
    directory.mkdir(parents=True, exist_ok=True)
    c = record["c"]
    assert isinstance(c, str)
    code.write_text(c, encoding="utf-8")
    record_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return code, record_path


def _run(arguments: argparse.Namespace, record: proof.Record) -> int:
    """Compile the certified C with the unverified console runtime in a temporary directory and run it."""
    c = record["c"]
    assert isinstance(c, str)
    if not unit_has_entry(record):
        raise ToolchainError("run needs a program with `int main(void)`")
    with tempfile.TemporaryDirectory(prefix="pfc2-run-") as directory:
        code, binary = Path(directory) / f"{arguments.file.stem}.c", Path(directory) / "program"
        code.write_text(c, encoding="utf-8")
        command = [arguments.clang, *C_FLAGS, str(code), str(RUNTIME), "-o", str(binary)]
        try:
            compiled = subprocess.run(
                command, capture_output=True, text=True, check=False, timeout=PROCESS_TIMEOUT_SECONDS
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            raise ToolchainError(f"cannot compile the certified C ({type(error).__name__})") from None
        if compiled.returncode != 0:
            raise ToolchainError("clang refused the certified C:\n" + compiled.stderr.strip())
        sys.stdout.flush()
        if arguments.stdin is None:
            return subprocess.run([str(binary)], check=False).returncode
        with arguments.stdin.open("rb") as answers:
            return subprocess.run([str(binary)], stdin=answers, check=False).returncode


def unit_has_entry(record: proof.Record) -> bool:
    unverified = record["unverified"]
    assert isinstance(unverified, dict)
    return any(line.startswith("int main(void)") for line in unverified["lines"])


def _ask(prompt: str, attempt: int) -> str:
    """One request to the single LLM adapter; the key is read from the environment only."""
    return llm.ask(prompt).text


def _prove(arguments: argparse.Namespace, target: Target) -> tuple[Unit, Certification] | None:
    key = os.environ.get(OPENAI_KEY_ENV, "")
    if not key.strip():
        raise ToolchainError(f"--prove needs {OPENAI_KEY_ENV} in the environment (never as an argument)")
    outcome = prove(arguments.file, target, ask=_ask, level=arguments.level, timeout_ms=arguments.timeout_ms)
    for attempt in outcome.attempts:
        verdict = "accepted" if attempt.accepted else f"rejected: {attempt.problem}"
        sys.stderr.write(f"proof attempt {attempt.number}: {verdict}\n")
    if outcome.unit is None or outcome.certification is None:
        return None
    return outcome.unit, outcome.certification


def _check_or_build(arguments: argparse.Namespace) -> int:
    unit = frontend.load(arguments.file)
    target = read_target(arguments.clang)
    if arguments.proof is not None:
        try:
            text = arguments.proof.read_bytes()[: MAX_REPORT_BYTES + 1].decode("utf-8")
            invariants = bundle.parse(text, unit.loops)
        except (OSError, ValueError) as error:
            raise ToolchainError(f"cannot use the proof in {arguments.proof}: {error}") from None
        unit = frontend.load(arguments.file, invariants=invariants)
    unit, certification = check(unit, target, level=arguments.level, timeout_ms=arguments.timeout_ms)
    if arguments.prove and not certification.accepted:
        proved = _prove(arguments, target)
        if proved is not None:
            unit, certification = proved
    record = proof.build(unit, certification)
    if arguments.command == "run":
        if not certification.accepted:
            sys.stdout.write(report.render(unit, certification, record))
            return 1
        return _run(arguments, record)
    if arguments.json:
        sys.stdout.write(json.dumps(record, indent=2, sort_keys=True) + "\n")
    else:
        sys.stdout.write(report.render(unit, certification, record))
    if not certification.accepted:
        return 1
    if arguments.command == "build":
        stem = arguments.file.stem
        directory = arguments.output if arguments.output is not None else DEFAULT_OUTPUT / stem
        if arguments.dry_run:
            sys.stderr.write(f"dry run: nothing written to {directory}\n")
            if not arguments.json:
                sys.stdout.write(f"  would write {directory / (stem + '.c')}\n")
                sys.stdout.write(f"  would write {directory / (stem + '.proof.json')}\n")
            return 0
        written = _write(directory, stem, record, force=arguments.force)
        if not arguments.json:
            sys.stdout.write("".join(f"  wrote {path}\n" for path in written))
    return 0


def _replay(arguments: argparse.Namespace) -> int:
    try:
        data = arguments.file.read_bytes()[: MAX_REPORT_BYTES + 1]
        if len(data) > MAX_REPORT_BYTES:
            raise ValueError("proof file is too large")
        record = json.loads(data.decode("utf-8"))
    except (OSError, ValueError) as error:
        sys.stderr.write(f"{arguments.file}: cannot read proof file ({type(error).__name__})\n")
        return 1
    differences = proof.replay(record)
    if differences == ["solver"]:
        sys.stdout.write(f"{arguments.file}: not replayed: it was checked with another Z3 or encoding ")
        sys.stdout.write(f"(here: Z3 {smt.solver_version()})\n")
        return 1
    if differences:
        sys.stdout.write(f"{arguments.file}: NOT reproduced; differing fields: {', '.join(differences)}\n")
        return 1
    verdict = "certified" if record["accepted"] else "refused"
    sys.stdout.write(f"{arguments.file}: reproduced ({verdict}, level {record['level']}, 0 network requests)\n")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        if arguments.command == "lsp":
            from pfc2.lsp import server  # Imported on demand: only this command needs the protocol library.

            server.main()
            return 0
        if arguments.command == "replay":
            return _replay(arguments)
        if arguments.command == "elaborate":
            sys.stdout.write(ir.print_c(frontend.load(arguments.file).program))
            return 0
        return _check_or_build(arguments)
    except FrontendError as error:
        sys.stderr.write(f"{error}\n")
    except (ToolchainError, FileExistsError) as error:
        sys.stderr.write(f"error: {error}\n")
    except OSError as error:
        sys.stderr.write(f"error: cannot write output ({type(error).__name__})\n")
    return 1
