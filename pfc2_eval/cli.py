"""`uv run --locked python -m pfc2_eval SUBCOMMAND`, from the repository root.

Every command that writes takes a new `--output` and supports `--dry-run`. Exit codes: 0 success, 1 failure,
2 usage error.
"""

import argparse
import json
import os
import sys
from pathlib import Path

from pfc2.core.diagnostics import FrontendError
from pfc2.core.environment import ToolchainError
from pfc2.core.target import read_target
from pfc2_eval import (
    adapter,
    breakit,
    build,
    campaign,
    corpus,
    crosscheck,
    differential,
    generate,
    heldout,
    inject,
    interpret,
    mutate,
    robustness,
    runtime,
    selfcheck,
    sources,
    surfaces,
    verifier,
)

DEFAULT_CLANG = "clang-19"
CLANG_ENV = "PFC2_CLANG"
PLANNED = {
    "oracle": "E7",
    "traps": "E8",
    "replay": "E9",
    "proposers": "E10",
}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pfc2_eval", description="Evaluation harness for PFC2.")
    commands = parser.add_subparsers(dest="command", required=True)

    check = commands.add_parser(
        "selfcheck",
        help="harness validation: the interpreter against the source compiled as plain C",
        epilog="example: python -m pfc2_eval selfcheck --output out/selfcheck --programs 200 --cases 50",
    )
    check.add_argument("--output", required=True, type=Path)
    check.add_argument("--seed", type=int, default=0)
    check.add_argument("--programs", type=int, default=200)
    check.add_argument("--cases", type=int, default=50)
    check.add_argument("--clang")
    check.add_argument("--dry-run", action="store_true")

    diff = commands.add_parser(
        "differential",
        help="E1, E8, E9: certified, checked and plain C against the interpreter; expected traps; replay",
        epilog="example: python -m pfc2_eval differential --output out/differential --seed 100000",
    )
    diff.add_argument("--output", required=True, type=Path)
    diff.add_argument("--seed", type=int, required=True)
    diff.add_argument("--programs", type=int, default=1000)
    diff.add_argument("--cases", type=int, default=100)
    diff.add_argument("--workers", type=int, default=1)
    diff.add_argument("--clang")
    diff.add_argument("--dry-run", action="store_true")

    cross = commands.add_parser(
        "crosscheck",
        help="E6: every query answered again by cvc5",
        epilog="example: python -m pfc2_eval crosscheck examples --cvc5 PATH --output NEW --seed 100000",
    )
    cross.add_argument("directories", nargs="*", type=Path)
    cross.add_argument("--cvc5", required=True, type=Path)
    cross.add_argument("--output", required=True, type=Path)
    cross.add_argument("--seed", type=int, required=True)
    cross.add_argument("--programs", type=int, default=300)
    cross.add_argument("--workers", type=int, default=1)
    cross.add_argument("--clang")
    cross.add_argument("--dry-run", action="store_true")

    paths = commands.add_parser(
        "surfaces",
        help="E12: the editor and browser paths against the command line",
        epilog="example: python -m pfc2_eval surfaces examples --output NEW --seed 100000 --programs 100",
    )
    paths.add_argument("directories", nargs="*", type=Path)
    paths.add_argument("--output", required=True, type=Path)
    paths.add_argument("--seed", type=int, required=True)
    paths.add_argument("--programs", type=int, default=100)
    paths.add_argument("--clang")
    paths.add_argument("--dry-run", action="store_true")

    damage = commands.add_parser(
        "inject",
        help="E3: damaged loop invariants through the admission path",
        epilog="example: python -m pfc2_eval inject --output NEW --seed 100000 --programs 200",
    )
    damage.add_argument("--output", required=True, type=Path)
    damage.add_argument("--seed", type=int, required=True)
    damage.add_argument("--programs", type=int, default=200)
    damage.add_argument("--workers", type=int, default=1)
    damage.add_argument("--clang")
    damage.add_argument("--dry-run", action="store_true")

    weaken = commands.add_parser(
        "breakit",
        help="E2: each requires conjunct removed alone; the interpreter says what must follow",
        epilog="example: python -m pfc2_eval breakit examples --output NEW --seed 100000 --programs 200",
    )
    weaken.add_argument("directories", nargs="*", type=Path, help="example programs, reported apart")
    weaken.add_argument("--output", required=True, type=Path)
    weaken.add_argument("--seed", type=int, required=True)
    weaken.add_argument("--programs", type=int, default=200)
    weaken.add_argument("--workers", type=int, default=1)
    weaken.add_argument("--clang")
    weaken.add_argument("--dry-run", action="store_true")

    second = commands.add_parser(
        "verifier",
        help="E7: Frama-C/WP on hand-written ACSL transcriptions, beside PFC2's own verdicts",
        epilog="example: python -m pfc2_eval verifier corpus/independent-verifier --output NEW",
    )
    second.add_argument("cases", type=Path)
    second.add_argument("--output", required=True, type=Path)
    second.add_argument("--clang")
    second.add_argument("--dry-run", action="store_true")

    origin = commands.add_parser(
        "sources",
        help="E10: no invariant, inference, Houdini, Daikon-style and a language model on the sealed loop set",
        epilog="example: python -m pfc2_eval sources corpus/heldout-loops --output NEW --seed 100000 --live",
    )
    origin.add_argument("directory", type=Path)
    origin.add_argument("--output", required=True, type=Path)
    origin.add_argument("--seed", type=int, required=True)
    origin.add_argument("--live", action="store_true", help="make the model requests (reads OPENAI_API_KEY)")
    origin.add_argument("--workers", type=int, default=1)
    origin.add_argument("--model-workers", type=int, default=4)
    origin.add_argument("--clang")
    origin.add_argument("--dry-run", action="store_true")

    timing = commands.add_parser(
        "runtime",
        help="E11: run time of the plain, checked and certified builds of the array programs (descriptive)",
        epilog="example: python -m pfc2_eval runtime --output NEW --seed 100000 --cpu 3",
    )
    timing.add_argument("--output", required=True, type=Path)
    timing.add_argument("--seed", type=int, required=True)
    timing.add_argument("--cpu", type=int, help="pin every run to this processor with taskset")
    timing.add_argument("--clang")
    timing.add_argument("--dry-run", action="store_true")

    rewrite = commands.add_parser(
        "robustness",
        help="E5: renaming, reordering, operand swap and re-layout must not change the verdict",
        epilog="example: python -m pfc2_eval robustness --output NEW --seed 100000 --programs 300",
    )
    rewrite.add_argument("--output", required=True, type=Path)
    rewrite.add_argument("--seed", type=int, required=True)
    rewrite.add_argument("--programs", type=int, default=300)
    rewrite.add_argument("--workers", type=int, default=1)
    rewrite.add_argument("--clang")
    rewrite.add_argument("--dry-run", action="store_true")

    mutants = commands.add_parser(
        "mutate",
        help="E4: every mutant of the engine against the tests, then E1 on 50 programs",
        epilog="example: python -m pfc2_eval mutate --output NEW --workers 10 --durations FILE",
    )
    mutants.add_argument("--output", required=True, type=Path)
    mutants.add_argument("--workers", type=int, default=1)
    mutants.add_argument("--durations", type=Path, help="lines of `SECONDS tests/FILE.py`: quickest files run first")
    mutants.add_argument("--limit", type=int, help="rehearsal: only the first N mutants (never the experiment)")
    mutants.add_argument("--clang")
    mutants.add_argument("--dry-run", action="store_true")

    ported = commands.add_parser(
        "corpus",
        help="upstream tests and mutants against ported units",
        epilog="example: python -m pfc2_eval corpus corpus/pilot --upstream DIR/exercises/practice --output NEW",
    )
    ported.add_argument("units", type=Path)
    ported.add_argument("--upstream", required=True, type=Path)
    ported.add_argument("--output", required=True, type=Path)
    ported.add_argument("--selection", type=Path, help="SELECTION.json: every candidate, ported or excluded by rule")
    ported.add_argument("--ports", type=Path, help="sealed ports the units must equal once clauses are erased")
    ported.add_argument("--workers", type=int, default=1, help="mutants and laws of one unit judged at once")
    ported.add_argument(
        "--laws-beside-definitions",
        action="store_true",
        help="exploratory: assertions only, each law beside the definitions instead of bare declarations",
    )
    ported.add_argument("--clang")
    ported.add_argument("--dry-run", action="store_true")

    make = commands.add_parser(
        "generate", help="print the program of a seed", epilog="example: python -m pfc2_eval generate --seed 7"
    )
    make.add_argument("--seed", type=int, required=True)

    execute = commands.add_parser(
        "interpret",
        help="run one function in the reference interpreter",
        epilog='example: python -m pfc2_eval interpret FILE --function f --input \'{"scalars": {"n": 2}}\'',
    )
    execute.add_argument("file", type=Path)
    execute.add_argument("--function")
    execute.add_argument("--input", default="{}", help="JSON with scalars, arrays and globals by name")
    execute.add_argument("--clang")

    sealed = commands.add_parser("heldout", help="seal or verify a held-out directory")
    actions = sealed.add_subparsers(dest="action", required=True)
    sealing = actions.add_parser("seal", epilog='example: python -m pfc2_eval heldout seal DIR --rule "..."')
    sealing.add_argument("directory", type=Path)
    sealing.add_argument("--rule", required=True, help="the selection rule the set was drawn by")
    actions.add_parser("verify").add_argument("directory", type=Path)

    commands.add_parser("candidate", help="show which frozen candidate this tree is, as JSON")
    for name, step in PLANNED.items():
        commands.add_parser(name, help=f"not implemented yet (plan step {step})")
    return parser


def _interpret(options: argparse.Namespace, compiler: str) -> int:
    data = json.loads(options.input)
    if not isinstance(data, dict) or set(data) - {"scalars", "arrays", "globals"}:
        raise ValueError("--input is a JSON object with scalars, arrays and globals")
    inputs = interpret.Inputs(data.get("scalars", {}), data.get("arrays", {}), data.get("globals", {}))
    unit = adapter.load(options.file)
    observed = interpret.run(adapter.released(unit), inputs, target=read_target(compiler), function=options.function)
    if isinstance(observed, interpret.Observation):
        record = {
            "result": observed.result,
            "arrays": {name: list(values) for name, values in observed.arrays.items()},
            "globals": observed.globals,
            "output": observed.output,
            "annotation_violations": list(observed.annotation_violations),
        }
        print(json.dumps(record, indent=2, sort_keys=True))
        return 0
    print(json.dumps({"rejected": observed.kind, "message": observed.message}, indent=2, sort_keys=True))
    return 1


def main(arguments: list[str] | None = None) -> int:
    options = _parser().parse_args(arguments)
    compiler = getattr(options, "clang", None) or os.environ.get(CLANG_ENV, DEFAULT_CLANG)
    try:
        if options.command in PLANNED:
            print(
                f"pfc2_eval: {options.command} is plan step {PLANNED[options.command]} and is not implemented",
                file=sys.stderr,
            )
            return 1
        if options.command == "selfcheck":
            passed = selfcheck.run(
                output=options.output,
                compiler=compiler,
                seed=options.seed,
                programs=options.programs,
                cases=options.cases,
                dry_run=options.dry_run,
            )
            return 0 if passed else 1
        if options.command == "differential":
            passed = differential.run(
                output=options.output,
                compiler=compiler,
                seed=options.seed,
                programs=options.programs,
                cases=options.cases,
                workers=options.workers,
                dry_run=options.dry_run,
            )
            return 0 if passed else 1
        if options.command == "crosscheck":
            passed = crosscheck.run(
                output=options.output,
                compiler=compiler,
                cvc5=options.cvc5,
                seed=options.seed,
                programs=options.programs,
                directories=options.directories,
                workers=options.workers,
                dry_run=options.dry_run,
            )
            return 0 if passed else 1
        if options.command == "surfaces":
            passed = surfaces.run(
                output=options.output,
                compiler=compiler,
                seed=options.seed,
                programs=options.programs,
                directories=options.directories,
                dry_run=options.dry_run,
            )
            return 0 if passed else 1
        if options.command == "inject":
            passed = inject.run(
                output=options.output,
                compiler=compiler,
                seed=options.seed,
                programs=options.programs,
                workers=options.workers,
                dry_run=options.dry_run,
            )
            return 0 if passed else 1
        if options.command == "breakit":
            passed = breakit.run(
                output=options.output,
                compiler=compiler,
                seed=options.seed,
                programs=options.programs,
                directories=options.directories,
                workers=options.workers,
                dry_run=options.dry_run,
            )
            return 0 if passed else 1
        if options.command == "verifier":
            passed = verifier.run(
                cases=options.cases, output=options.output, compiler=compiler, dry_run=options.dry_run
            )
            return 0 if passed else 1
        if options.command == "sources":
            passed = sources.run(
                directory=options.directory,
                output=options.output,
                compiler=compiler,
                seed=options.seed,
                live=options.live,
                workers=options.workers,
                model_workers=options.model_workers,
                dry_run=options.dry_run,
            )
            return 0 if passed else 1
        if options.command == "runtime":
            passed = runtime.run(
                output=options.output, compiler=compiler, seed=options.seed, cpu=options.cpu, dry_run=options.dry_run
            )
            return 0 if passed else 1
        if options.command == "robustness":
            passed = robustness.run(
                output=options.output,
                compiler=compiler,
                seed=options.seed,
                programs=options.programs,
                workers=options.workers,
                dry_run=options.dry_run,
            )
            return 0 if passed else 1
        if options.command == "mutate":
            passed = mutate.run(
                output=options.output,
                compiler=compiler,
                durations=options.durations,
                workers=options.workers,
                limit=options.limit,
                dry_run=options.dry_run,
            )
            return 0 if passed else 1
        if options.command == "corpus":
            passed = corpus.run(
                output=options.output,
                compiler=compiler,
                units=options.units,
                upstream=options.upstream,
                chosen_from=options.selection,
                ports=options.ports,
                workers=options.workers,
                defined=options.laws_beside_definitions,
                dry_run=options.dry_run,
            )
            return 0 if passed else 1
        if options.command == "generate":
            print(generate.program(options.seed).text, end="")
            return 0
        if options.command == "interpret":
            return _interpret(options, compiler)
        if options.command == "candidate":
            frozen = campaign.candidate()
            record = {
                "candidate": frozen.name,
                "protected_sha256": frozen.protected_sha256,
                "intact": frozen.intact,
                "changed": list(frozen.protected.mismatched),
                "unlisted": list(frozen.unlisted),
            }
            print(json.dumps(record, indent=2, sort_keys=True))
            return 0 if frozen.intact else 1
        if options.action == "seal":
            count = heldout.seal(options.directory, rule=options.rule, candidate=campaign.candidate().name)
            print(f"sealed {count} files in {options.directory}")
            return 0
        state = heldout.verify(options.directory)
        print("intact" if state.intact else "; ".join(state.problems))
        return 0 if state.intact else 1
    except FileExistsError as error:
        print(f"pfc2_eval: {error}", file=sys.stderr)
        return 1
    except (FrontendError, ToolchainError, build.BuildError, OSError, ValueError) as error:
        print(f"pfc2_eval: {error}", file=sys.stderr)
        return 1
