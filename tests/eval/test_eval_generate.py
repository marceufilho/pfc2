"""The generator: reproducible, inside the language, and useful (valid runs are common, invalid ones exist)."""

import shutil
from collections import Counter
from pathlib import Path

import pytest

from pfc2.core.target import Target, read_target
from pfc2_eval import adapter, build, generate, interpret
from pfc2_eval.interpret import Observation

TARGET = Target("static LP64 layout (test)", "x86_64-pc-linux-gnu", 32, 64)
CLANG = shutil.which("clang-19") or shutil.which("clang") or "clang"


def test_a_seed_always_gives_the_same_program_and_cases() -> None:
    first, again = generate.program(7), generate.program(7)
    assert first == again and generate.cases(first, 20) == generate.cases(again, 20)
    assert generate.program(8).text != first.text


def test_every_generated_program_is_in_the_language_and_uses_all_of_it() -> None:
    texts = []
    for seed in range(300):
        generated = generate.program(seed)
        adapter.load_text(generated.text, f"g{seed}.c")  # Raises if the front end refuses it.
        texts.append(generated.text)
    corpus = "\n".join(texts)
    for feature in ("for (", "while (", "decreases(", "break;", "continue;", " % ", " / ", "char s[", "int v["):
        assert feature in corpus, feature
    for feature in ("buf", "helper0(", "++;", "+= ", "&&", "||", "return"):
        assert feature in corpus, feature
    defects = sum(generate.program(seed).defect for seed in range(300))
    assert 5 <= defects <= 60  # Present, and a minority.


def test_most_cases_are_valid_runs_and_the_rest_are_rejected_for_several_reasons() -> None:
    kinds: Counter[str] = Counter()
    for seed in range(60):
        generated = generate.program(seed)
        program = adapter.released(adapter.load_text(generated.text, "g.c"))
        for case in generate.cases(generated, 20):
            observed = interpret.run(program, case, target=TARGET, function="entry", fuel=200_000)
            kinds["ok" if isinstance(observed, Observation) else observed.kind] += 1
    assert kinds["ok"] >= 0.5 * sum(kinds.values()), kinds
    assert kinds["PreconditionViolated"] > 0 and kinds["Overflow"] > 0, kinds
    assert kinds["Unsupported"] == 0 and kinds["InvalidInput"] == 0, kinds


@pytest.mark.integration
def test_the_interpreter_and_plain_c_agree_on_every_valid_case_of_forty_programs(tmp_path: Path) -> None:
    target = read_target(CLANG)
    compared = 0
    for seed in range(40):
        generated = generate.program(seed)
        unit = adapter.load_text(generated.text, f"g{seed}.c")
        program = adapter.released(unit)
        function = next(f for f in program.functions if f.name == "entry")
        references = [
            (case, interpret.run(program, case, target=target, function="entry", fuel=200_000))
            for case in generate.cases(generated, 25)
        ]
        valid = [(case, observed) for case, observed in references if isinstance(observed, Observation)]
        if not valid:
            continue
        binary = tmp_path / f"plain{seed}"
        build.compile_c(build.with_driver(adapter.plain_c(unit), program, function), binary, clang=CLANG, plain=True)
        outcomes = build.run_cases(binary, program, function, [case for case, _ in valid])
        arrays = [p.symbol.name for p in function.parameters if p.length is not None]
        for (_, expected), outcome in zip(valid, outcomes, strict=True):
            assert outcome.kind == "ok", (seed, outcome)
            assert outcome.result == expected.result, seed
            assert outcome.arrays == tuple(expected.arrays[name] for name in arrays), seed
            assert outcome.globals == tuple(expected.globals[item.symbol.name] for item in program.globals), seed
            compared += 1
    assert compared >= 500
