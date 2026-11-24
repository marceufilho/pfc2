"""E10: where loop invariants come from.

Six conditions on each program of the sealed set, every one ending in the same judgement
(`adapter.check` or `adapter.admit` at level `memory`), success meaning a certificate:

    N   nothing: inference off, no invariant
    I   the built-in inference of counter bounds
    B1  Houdini over a fixed family of bounds, inference off
    B2  the same filtering over invariants observed at loop heads by the interpreter, inference off
    L1  a language model with the checker's refusal fed back, at most five attempts, inference off
    L2  the same model, five independent single attempts, no feedback, inference off

A baseline filters its candidates on a probe program: the loop carries the conjunction of the candidates
still alive and each candidate `c` is asserted as `PROBE != j || c` before the loop and at the end of its
body, so that one failing candidate says nothing about another. A candidate is dropped only when its
assertion fails with a counterexample. What is left is judged on the unchanged source by `adapter.admit`:
the probe gives no authority. The model is asked through `pfc2.llm`; its replies are data.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from collections.abc import Callable, Iterable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from random import Random

from pfc2 import bundle, llm, prove
from pfc2.core import ir
from pfc2.core.diagnostics import FrontendError
from pfc2.core.target import Target, read_target
from pfc2.elaborate import Unit
from pfc2.gate import Level
from pfc2_eval import adapter, breakit, campaign, evidence, heldout, interpret, stats

EXPERIMENT = "sources"
CONDITIONS = ("N", "I", "B1", "B2", "L1", "L2")
LEVEL: Level = "memory"
ROUNDS = 5  # The registered budget of a baseline.
ROUNDS_SENSITIVITY = 50
CHUNK = 24  # Candidates asserted in one probe program.
PROBE = "houdini_probe"
INPUTS = 200  # Accepted inputs whose loop-head states B2 observes...
DRAWS = 20_000  # ...out of at most this many draws of the small domain.
MIN_STATES = 20
CAP = 60  # Candidates of one loop in B2, in the order of the grammar.
SMALL = 8
MULTIPLIERS = (-2, -1, 2)
RUNS = 5
ATTEMPTS = 5
BOOTSTRAP = 10_000
THRESHOLD = 0.20
NO_POWER = 0.90
TRUE = "0 == 0"
FAMILY_B1 = "`x <= t` and `t <= x` for each scalar x in scope and each t among the other scalars in scope, 0, 1 "
FAMILY_B1 += "and the integer literals of the function"
FAMILY_B2 = (
    "over the scalars observed at the loop head on accepted inputs: `x == c`; `x == y + c` (|c| <= 8); "
    "`c <= x`, `x <= c` for an observed extreme with |c| <= 8; `x <= y + c` for the largest observed difference "
    "c in {-1, 0, 1}; `x == y + z`; `x == m * y + c` for m in {-2, -1, 2} and |c| <= 8; at most 60 per loop"
)
INSTRUCTION = (
    "The C file below contains one function with loops and no loop invariants. A checker must prove every "
    "`assert`, every array index and every division in it. Signed overflow is trapped at run time and does not "
    "need to be proved. Supply the loop invariants that make the proof go through.\n"
    'Return only JSON {{"invariants": [...]}} with exactly {loops} loop invariant(s), one per loop in source '
    "order. Each is a call-free C integer/Boolean expression over names in scope at that loop. Annotation "
    "arithmetic is mathematical; there are no quantifiers. Do not change the code.\n\n"
)
SCHEMA = evidence.Schema(
    (
        evidence.Column("program", "string"),
        evidence.Column("family", "string"),
        evidence.Column("condition", "string", allowed=CONDITIONS),
        evidence.Column("rounds_budget", "integer", nullable=True),
        evidence.Column("run", "integer", nullable=True),
        evidence.Column("success", "boolean"),
        evidence.Column("status", "string"),
        evidence.Column("loops", "integer"),
        evidence.Column("candidates", "integer", nullable=True),
        evidence.Column("kept", "integer", nullable=True),
        evidence.Column("rounds", "integer", nullable=True),
        evidence.Column("attempts", "integer", nullable=True),
        evidence.Column("seconds", "number"),
    )
)

Ask = Callable[[str], str]
Row = dict[str, object]


# --- The text of a program: where its loops are -------------------------------------------------


@dataclass(frozen=True)
class LoopText:
    keyword: str
    start: int  # Of the keyword.
    open: int  # Of its `(`.
    close: int  # Of the matching `)`.
    body_open: int  # Of the body's `{`.
    body_close: int  # Of the matching `}`.


def _mask(text: str) -> str:
    """The text with comments and literals blanked, so that brackets and keywords can be found."""
    pattern = re.compile(r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', re.S)
    return pattern.sub(lambda match: re.sub(r"[^\n]", " ", match.group()), text)


def _match(masked: str, position: int, opening: str, closing: str) -> int:
    depth = 0
    for index in range(position, len(masked)):
        depth += (masked[index] == opening) - (masked[index] == closing)
        if depth == 0:
            return index
    raise ValueError("unbalanced brackets")


def loops(text: str) -> list[LoopText]:
    """Every loop in source order. A loop this rewriting cannot probe is an error, never skipped."""
    masked = _mask(text)
    if re.search(r"\b(do|continue|goto)\b", masked):
        raise ValueError("a program with do, continue or goto is not probed")
    found = []
    for match in re.finditer(r"\b(for|while)\b", masked):
        opening = masked.index("(", match.end())
        if masked[match.end() : opening].strip():
            raise ValueError("unexpected text after a loop keyword")
        closing = _match(masked, opening, "(", ")")
        body = closing + 1
        while masked[body].isspace():
            body += 1
        if masked[body] != "{":
            raise ValueError("a loop with a clause or without a braced body is not probed")
        found.append(LoopText(match.group(), match.start(), opening, closing, body, _match(masked, body, "{", "}")))
    return found


def _split(head: str) -> tuple[str, str, str]:
    """The three parts of a `for` head, split at its top-level semicolons."""
    parts, depth, last = [], 0, 0
    for index, character in enumerate(head):
        depth += (character == "(") - (character == ")")
        if character == ";" and depth == 0:
            parts.append(head[last:index])
            last = index + 1
    parts.append(head[last:])
    if len(parts) != 3:
        raise ValueError("a for head must have three parts")
    return parts[0].strip(), parts[1].strip(), parts[2].strip()


def conjoin(parts: Sequence[str]) -> str:
    return " && ".join(f"({part})" for part in parts) if parts else TRUE


def build_probe(
    text: str, alive: Sequence[Sequence[str]], asserted: Iterable[tuple[int, int]]
) -> tuple[str, dict[int, tuple[int, int]]]:
    """The probe program and, for each line that holds a probe assertion, its (loop, candidate).

    Every loop carries the conjunction of its candidates in `alive`; only the pairs in `asserted` are
    asserted. A `for` becomes a `while` with its update at the end of the body, before the assertions.
    """
    found = loops(text)
    if len(found) != len(alive):
        raise ValueError("one list of candidates per loop is required")
    wanted: dict[int, list[int]] = {}
    for loop, candidate in asserted:
        wanted.setdefault(loop, []).append(candidate)
    marks: list[tuple[str, int, int]] = []  # (marker, loop, candidate)

    def probes(loop: int) -> str:
        lines = []
        for candidate in wanted.get(loop, []):
            marker = f"/*probe:{len(marks)}*/"
            marks.append((marker, loop, candidate))
            lines.append(f"\nassert({PROBE} != {loop * 1000 + candidate + 1} || ({alive[loop][candidate]})); {marker}")
        return "".join(lines) + "\n"

    out = text
    for index in range(len(found) - 1, -1, -1):
        item = found[index]
        body = out[item.body_open + 1 : _match(_mask(out), item.body_open, "{", "}")]
        end = _match(_mask(out), item.body_open, "{", "}")
        first, condition, update = "", out[item.open + 1 : item.close].strip(), ""
        if item.keyword == "for":
            first, condition, update = _split(out[item.open + 1 : item.close])
        clause = f" invariant({conjoin(alive[index])})" if alive[index] else ""
        before = probes(index)
        after = probes(index)
        rewritten = (
            "{ "
            + (f"{first}; " if first else "")
            + before
            + f"while ({condition or '1'}){clause} {{"
            + body
            + (f"\n{update};" if update else "")
            + after
            + "} }"
        )
        out = out[: item.start] + rewritten + out[end + 1 :]
    include = out.index("\n", out.index("#include")) + 1
    out = out[:include] + f"long {PROBE} = 0;\n" + out[include:]
    lines: dict[int, tuple[int, int]] = {}
    for number, line in enumerate(out.splitlines(), start=1):
        for marker, loop, candidate in marks:
            if marker in line:
                lines[number] = (loop, candidate)
    return out, lines


# --- Candidate families -------------------------------------------------------------------------


def _ir_loops(block: ir.Block, scope: tuple[str, ...], found: list[tuple[ir.While | ir.For, tuple[str, ...]]]) -> None:
    for statement in block.statements:
        if isinstance(statement, ir.Local) and not isinstance(statement.symbol.type, ir.ArrayType):
            scope = (*scope, statement.symbol.name)
        elif isinstance(statement, ir.Block):
            _ir_loops(statement, scope, found)
        elif isinstance(statement, ir.If):
            _ir_loops(statement.then_body, scope, found)
            if statement.else_body is not None:
                _ir_loops(statement.else_body, scope, found)
        elif isinstance(statement, (ir.While, ir.For)):
            inner = scope
            if isinstance(statement, ir.For) and isinstance(statement.initializer, ir.Local):
                inner = (*scope, statement.initializer.symbol.name)
            found.append((statement, inner))
            _ir_loops(statement.body, inner, found)


def scopes(function: ir.Function) -> list[tuple[ir.While | ir.For, tuple[str, ...]]]:
    """Each loop of the function in source order with the scalars in scope at its head."""
    names = tuple(p.symbol.name for p in function.parameters if not isinstance(p.symbol.type, ir.ArrayType))
    found: list[tuple[ir.While | ir.For, tuple[str, ...]]] = []
    _ir_loops(function.body, names, found)
    return found


def constants(text: str) -> tuple[int, ...]:
    literals = {int(match) for match in re.findall(r"(?<![\w.])\d+(?![\w.])", _mask(text))}
    return tuple(sorted({0, 1} | literals))


def family_b1(function: ir.Function, text: str) -> list[list[str]]:
    numbers = constants(text)
    result = []
    for _, names in scopes(function):
        candidates: list[str] = []
        for name in names:
            for other in names:
                if other != name:
                    candidates.append(f"{name} <= {other}")
            for number in numbers:
                candidates += [f"{name} <= {number}", f"{number} <= {name}"]
        result.append(list(dict.fromkeys(candidates)))
    return result


State = Mapping[str, int]


def _offset(base: str, constant: int) -> str:
    return base if constant == 0 else f"{base} + {constant}" if constant > 0 else f"{base} - {-constant}"


def observed_candidates(states: Sequence[State]) -> list[str]:
    """The grammar of B2 instantiated on the states seen at one loop head, in a fixed order."""
    if len(states) < MIN_STATES:
        return []
    names = sorted(set.intersection(*(set(state) for state in states)))
    found: list[str] = []
    for name in names:
        values = {state[name] for state in states}
        if len(values) == 1:
            found.append(f"{name} == {next(iter(values))}")
    for index, left in enumerate(names):
        for right in names[index + 1 :]:
            differences = {state[left] - state[right] for state in states}
            if len(differences) == 1 and abs(next(iter(differences))) <= SMALL:
                found.append(f"{left} == {_offset(right, next(iter(differences)))}")
    for name in names:
        low, high = min(state[name] for state in states), max(state[name] for state in states)
        if abs(low) <= SMALL:
            found.append(f"{low} <= {name}")
        if abs(high) <= SMALL:
            found.append(f"{name} <= {high}")
    for left in names:
        for right in names:
            if left != right:
                largest = max(state[left] - state[right] for state in states)
                if largest in (-1, 0, 1):
                    found.append(f"{left} <= {_offset(right, largest)}")
    for total in names:
        for index, first in enumerate(names):
            for second in names[index + 1 :]:
                if total not in (first, second) and all(s[total] == s[first] + s[second] for s in states):
                    found.append(f"{total} == {first} + {second}")
    for left in names:
        for right in names:
            if left == right:
                continue
            for multiplier in MULTIPLIERS:
                differences = {state[left] - multiplier * state[right] for state in states}
                if len(differences) == 1 and abs(next(iter(differences))) <= SMALL:
                    found.append(f"{left} == {_offset(f'{multiplier} * {right}', next(iter(differences)))}")
    return list(dict.fromkeys(found))[:CAP]


def observe(unit: Unit, function: ir.Function, target: Target, seed: str) -> tuple[list[list[State]], int]:
    """Loop-head states, per loop in source order, on up to INPUTS accepted inputs; and how many were accepted."""
    program = adapter.released(unit)
    entry = next(item for item in program.functions if item.name == function.name)
    places = [(loop.location.line, loop.location.column) for loop, _ in scopes(entry)]
    states: list[list[State]] = [[] for _ in places]
    rng = Random(seed)
    accepted = 0
    for _ in range(DRAWS):
        if accepted == INPUTS:
            break
        seen: list[tuple[int, State]] = []

        def note(head: interpret.LoopHead, seen: list[tuple[int, State]] = seen) -> None:
            place = (head.location.line, head.location.column)
            if head.function == entry.name and place in places:
                seen.append((places.index(place), dict(head.scalars)))

        inputs = breakit.draw(entry, program, rng)
        outcome = interpret.run(program, inputs, target=target, function=entry.name, fuel=breakit.FUEL, observer=note)
        if isinstance(outcome, interpret.Rejection):
            continue
        accepted += 1
        for index, state in seen:
            states[index].append(state)
    return states, accepted


def family_b2(unit: Unit, function: ir.Function, target: Target, seed: str) -> tuple[list[list[str]], int]:
    states, accepted = observe(unit, function, target, seed)
    return [observed_candidates(items) for items in states], accepted


# --- Houdini ------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Filtered:
    invariants: tuple[str, ...]
    status: str  # fixpoint, inconclusive, round-limit or probe-error
    rounds: int
    candidates: int
    kept: int


def houdini(text: str, name: str, families: Sequence[Sequence[str]], target: Target, rounds: int) -> Filtered:
    alive = [list(family) for family in families]
    total = sum(len(family) for family in alive)

    def result(status: str, used: int) -> Filtered:
        return Filtered(tuple(conjoin(family) for family in alive), status, used, total, sum(map(len, alive)))

    for used in range(1, rounds + 1):
        pairs = [(loop, index) for loop, family in enumerate(alive) for index in range(len(family))]
        failed: set[tuple[int, int]] = set()
        unsure = False
        for start in range(0, len(pairs), CHUNK):
            try:
                probe, lines = build_probe(text, alive, pairs[start : start + CHUNK])
                unit = adapter.load_text(probe, name)
                certification = adapter.check(unit, target, level=LEVEL, inference=False)[1]
            except (ValueError, FrontendError):
                alive = [[] for _ in alive]
                return result("probe-error", used)
            for item in certification.proof.results:
                where = lines.get(item.obligation.location.line)
                if where is None or item.obligation.kind != "assert":
                    continue
                if item.status == "failed" and item.counterexample is not None:
                    failed.add(where)
                elif item.status != "proved":
                    unsure = True
        if not failed:
            return result("inconclusive" if unsure else "fixpoint", used)
        alive = [
            [c for index, c in enumerate(family) if (loop, index) not in failed] for loop, family in enumerate(alive)
        ]
    return result("round-limit", rounds)


# --- One program under the conditions that need no model ----------------------------------------


def _row(program: str, family: str, condition: str, loop_count: int, started: float, **fields: object) -> Row:
    row: Row = {
        "program": program,
        "family": family,
        "condition": condition,
        "rounds_budget": None,
        "run": None,
        "success": False,
        "status": "",
        "loops": loop_count,
        "candidates": None,
        "kept": None,
        "rounds": None,
        "attempts": None,
        "seconds": round(time.monotonic() - started, 3),
    }
    row.update(fields)
    return row


def classical(arguments: tuple[str, str, str, str, int]) -> list[Row]:
    """N, I, and both baselines at both round budgets, for one program."""
    name, family, text, compiler, seed = arguments
    target = read_target(compiler)
    unit = adapter.load_text(text, name)
    function = unit.program.functions[0]
    count = len(loops(text))
    rows: list[Row] = []
    for condition, inference in (("N", False), ("I", True)):
        started = time.monotonic()
        certification = adapter.check(adapter.load_text(text, name), target, level=LEVEL, inference=inference)[1]
        status = "certified" if certification.accepted else certification.reason
        rows.append(_row(name, family, condition, count, started, success=certification.accepted, status=status))
    started = time.monotonic()
    observed, accepted = family_b2(unit, function, target, f"{seed}:{name}")
    families = {"B1": family_b1(function, text), "B2": observed}
    for condition, candidates in families.items():
        for budget in (ROUNDS, ROUNDS_SENSITIVITY):
            started = time.monotonic()
            filtered = houdini(text, name, candidates, target, budget)
            certification = adapter.admit(text, name, filtered.invariants, target, level=LEVEL)
            status = filtered.status if condition == "B1" else f"{filtered.status}; {accepted} inputs"
            rows.append(
                _row(
                    name,
                    family,
                    condition,
                    count,
                    started,
                    rounds_budget=budget,
                    success=certification.accepted,
                    status=status,
                    candidates=filtered.candidates,
                    kept=filtered.kept,
                    rounds=filtered.rounds,
                )
            )
    return rows


# --- The model ----------------------------------------------------------------------------------


def instruction(text: str, loop_count: int) -> str:
    return INSTRUCTION.format(loops=loop_count) + text


def model_run(
    text: str, name: str, target: Target, ask: Ask, *, feedback: bool, attempts: int = ATTEMPTS
) -> tuple[bool, int, list[dict[str, object]]]:
    """(certified, attempts used, transcript). With feedback the refusal is appended; without, every attempt is
    the same bare prompt. A failed request or a malformed reply uses up an attempt."""
    count = len(loops(text))
    prompt = instruction(text, count)
    history = ""
    transcript: list[dict[str, object]] = []
    for number in range(1, attempts + 1):
        reply: str | None = None
        entry: dict[str, object] = {
            "attempt": number,
            "prompt_sha256": hashlib.sha256((prompt + history).encode()).hexdigest(),
        }
        try:
            reply = ask(prompt + history)
            entry["reply"] = reply
            invariants = bundle.parse(reply, count)
            certification = adapter.admit(text, name, invariants, target, level=LEVEL)
        except (ValueError, OSError, FrontendError) as error:
            entry["problem"] = str(error)[:500]
            transcript.append(entry)
            if feedback:
                history = "\n\nYour previous reply could not be used: " + str(error)
                history += "\nPrevious reply:\n" + reply if reply is not None else ""
            continue
        entry["accepted"] = certification.accepted
        entry["reason"] = certification.reason
        transcript.append(entry)
        if certification.accepted:
            return True, number, transcript
        if feedback:
            history = "\n\nPrevious reply:\n" + reply + "\n" + prove.feedback(certification)
    return False, attempts, transcript


def _live(prompt: str) -> str:
    return llm.ask(prompt).text


def modelled(arguments: tuple[str, str, str, str, str, int]) -> tuple[Row, list[dict[str, object]]]:
    name, family, text, compiler, condition, run = arguments
    started = time.monotonic()
    success, used, transcript = model_run(text, name, read_target(compiler), _live, feedback=condition == "L1")
    status = "certified" if success else "not certified"
    row = _row(
        name, family, condition, len(loops(text)), started, run=run, success=success, status=status, attempts=used
    )
    return row, transcript


# --- Summary ------------------------------------------------------------------------------------


def _rate(rows: Sequence[Mapping[str, object]]) -> dict[str, object]:
    successes, trials = sum(bool(row["success"]) for row in rows), len(rows)
    if not trials:
        return {"successes": 0, "trials": 0, "proportion": None, "wilson": None, "clopper_pearson": None}
    wilson, exact = stats.wilson(successes, trials), stats.clopper_pearson(successes, trials)
    return {
        "successes": successes,
        "trials": trials,
        "proportion": round(successes / trials, 4),
        "wilson": [round(wilson.low, 4), round(wilson.high, 4)],
        "clopper_pearson": [round(exact.low, 4), round(exact.high, 4)],
    }


def _per_program(rows: Sequence[Mapping[str, object]], condition: str, budget: int | None = None) -> dict[str, float]:
    """The proportion of runs in which each program is certified under one condition."""
    values: dict[str, list[float]] = {}
    for row in rows:
        if row["condition"] == condition and row["rounds_budget"] == budget:
            values.setdefault(str(row["program"]), []).append(float(bool(row["success"])))
    return {program: sum(items) / len(items) for program, items in values.items()}


def contrast(left: Mapping[str, float], right: Mapping[str, float]) -> dict[str, object]:
    """Paired difference of proportions, by program: cluster bootstrap and exact sign test."""
    programs = sorted(set(left) & set(right))
    differences = {program: [left[program] - right[program]] for program in programs}
    boot = stats.cluster_bootstrap(differences, stats.mean, replicates=BOOTSTRAP, seed=0)
    sign = stats.sign_test([values[0] for values in differences.values()])
    return {
        "programs": len(programs),
        "difference": round(boot.estimate, 4),
        "interval": [round(boot.interval.low, 4), round(boot.interval.high, 4)],
        "sign_test": {"positive": sign.positive, "negative": sign.negative, "ties": sign.ties, "p": sign.p_value},
    }


def summarise(rows: Sequence[Mapping[str, object]]) -> dict[str, object]:
    def of(condition: str, budget: int | None = None) -> list[Mapping[str, object]]:
        return [row for row in rows if row["condition"] == condition and row["rounds_budget"] == budget]

    cells = {
        "N": of("N"),
        "I": of("I"),
        "B1": of("B1", ROUNDS),
        "B2": of("B2", ROUNDS),
        "L1": of("L1"),
        "L2": of("L2"),
        f"B1 ({ROUNDS_SENSITIVITY} rounds)": of("B1", ROUNDS_SENSITIVITY),
        f"B2 ({ROUNDS_SENSITIVITY} rounds)": of("B2", ROUNDS_SENSITIVITY),
    }
    families = sorted({str(row["family"]) for row in rows})
    by_family = {
        family: {name: _rate([row for row in items if row["family"] == family]) for name, items in cells.items()}
        for family in families
    }
    per = {
        "N": _per_program(rows, "N"),
        "I": _per_program(rows, "I"),
        "B1": _per_program(rows, "B1", ROUNDS),
        "B2": _per_program(rows, "B2", ROUNDS),
        "L1": _per_program(rows, "L1"),
        "L2": _per_program(rows, "L2"),
    }
    summary: dict[str, object] = {
        "programs": len(per["N"]),
        "conditions": {name: _rate(items) for name, items in cells.items()},
        "by_family": by_family,
        "model_ran": bool(per["L1"]) and bool(per["L2"]),
    }
    registered: dict[str, dict[str, object]] = {"I - N": contrast(per["I"], per["N"])}
    if per["L1"]:
        registered["L1 - I"] = contrast(per["L1"], per["I"])
        registered["L1 - B2"] = contrast(per["L1"], per["B2"])
    adjusted = stats.holm([float(item["sign_test"]["p"]) for item in registered.values()])  # type: ignore[index]
    for (name, item), p_holm in zip(registered.items(), adjusted, strict=True):
        low, high = (float(bound) for bound in item["interval"])  # type: ignore[attr-defined]
        excludes_zero = low > 0 or high < 0
        needed = 0.0 if name == "I - N" else THRESHOLD
        item["p_holm"] = p_holm
        item["supported"] = bool(
            excludes_zero and float(str(item["difference"])) >= needed and float(str(item["difference"])) > 0
        )
    summary["registered_contrasts"] = registered
    inferred = cells["I"]
    share = sum(bool(row["success"]) for row in inferred) / len(inferred) if inferred else 0.0
    summary["no_power_for_model_contrasts"] = share > NO_POWER
    exploratory: dict[str, object] = {}
    if per["L1"] and per["L2"]:
        exploratory["L1 - L2"] = contrast(per["L1"], per["L2"])
        used = [int(str(row["attempts"])) for row in cells["L1"] if row["success"]]
        exploratory["L1 attempts when certified"] = {str(n): used.count(n) for n in sorted(set(used))}
    solved = {name: {program for program, value in values.items() if value > 0} for name, values in per.items()}
    exploratory["certified at least once, by condition"] = {name: len(items) for name, items in solved.items()}
    exploratory["certified under exactly one condition"] = {
        name: sorted(items - set().union(*(other for key, other in solved.items() if key != name)))
        for name, items in solved.items()
    }
    summary["exploratory"] = exploratory
    summary["passed"] = bool(rows)  # E10 has no pass criterion: it is reported, whatever it finds.
    return summary


def table(summary: Mapping[str, object]) -> str:
    conditions = summary["conditions"]
    assert isinstance(conditions, Mapping)
    lines = [
        "# E10: sources of invariants",
        "",
        f"Programs: {summary['programs']}. Success is a certificate at level `{LEVEL}`.",
        "",
        "| Condition | Certified | Trials | Proportion | Wilson 95% | Clopper-Pearson 95% |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for name, rate in conditions.items():
        lines.append(
            f"| {name} | {rate['successes']} | {rate['trials']} | {rate['proportion']} | {rate['wilson']} | "
            f"{rate['clopper_pearson']} |"
        )
    lines += [
        "",
        "## Registered contrasts",
        "",
        "| Contrast | Difference | 95% interval | Sign test p | Holm | Supported |",
    ]
    lines.append("| --- | ---: | --- | ---: | ---: | --- |")
    registered = summary["registered_contrasts"]
    assert isinstance(registered, Mapping)
    for name, item in registered.items():
        lines.append(
            f"| {name} | {item['difference']} | {item['interval']} | {item['sign_test']['p']:.4g} | "
            f"{item['p_holm']:.4g} | {'yes' if item['supported'] else 'no'} |"
        )
    lines += [
        "",
        f"No power for the model contrasts (more than 90% under I): {summary['no_power_for_model_contrasts']}.",
    ]
    by_family = summary["by_family"]
    assert isinstance(by_family, Mapping)
    for family, cells in by_family.items():
        lines += ["", f"## {family}", "", "| Condition | Certified | Trials |", "| --- | ---: | ---: |"]
        lines += [f"| {name} | {rate['successes']} | {rate['trials']} |" for name, rate in cells.items()]
    return "\n".join(lines) + "\n"


def _rows(records: tuple[evidence.Record, ...]) -> Iterable[Mapping[str, object]]:
    return [record.data for record in records if record.shard == "rows"]


def programs(directory: Path) -> list[tuple[str, str, str]]:
    """(name, family, text) of every program of the sealed set, in order."""
    tasks = json.loads((directory / "PROVENANCE.json").read_text(encoding="utf-8"))["tasks"]
    found = []
    for task in tasks:
        if "sha256" in task:
            text = (directory / f"{task['task']}.c").read_text(encoding="utf-8")
            found.append((str(task["task"]), str(task["family"]), text))
    return found


def run(
    *,
    directory: Path,
    output: Path,
    compiler: str,
    seed: int,
    live: bool,
    workers: int = 1,
    model_workers: int = 4,
    dry_run: bool = False,
    progress: Callable[[str], None] = campaign.progress,
) -> bool:
    heldout.require_intact([directory])
    items = programs(directory)
    if dry_run:
        requests = len(items) * RUNS * ATTEMPTS * 2 if live else 0
        progress(f"sources: would judge {len(items)} programs into {output}; at most {requests} model requests")
        return True
    settings = {
        "level": LEVEL,
        "programs": len(items),
        "rounds": ROUNDS,
        "rounds_sensitivity": ROUNDS_SENSITIVITY,
        "chunk": CHUNK,
        "family_b1": FAMILY_B1,
        "family_b2": FAMILY_B2,
        "inputs": INPUTS,
        "draws": DRAWS,
        "runs": RUNS if live else 0,
        "attempts": ATTEMPTS,
        "model": llm.model() if live else None,
        "instruction_sha256": hashlib.sha256(INSTRUCTION.encode()).hexdigest(),
        "live": live,
        "workers": workers,
        "model_workers": model_workers,
    }
    started = campaign.start(EXPERIMENT, output, compiler=compiler, seed=seed, settings=settings, schema=SCHEMA)
    kept: list[Row] = []
    with ProcessPoolExecutor(max_workers=workers) as pool:
        batch = [(name, family, text, compiler, seed) for name, family, text in items]
        for done, rows in enumerate(pool.map(classical, batch), start=1):
            for index, row in enumerate(rows):
                started.evidence.record(str(row["program"]), "rows", f"c{index}", row)
            kept += rows
            progress(f"sources: {done}/{len(items)} programs under N, I, B1, B2")
    if live:
        jobs = [
            (name, family, text, compiler, condition, number)
            for number in range(1, RUNS + 1)
            for name, family, text in items
            for condition in ("L1", "L2")
        ]
        with ProcessPoolExecutor(max_workers=model_workers) as pool:
            for done, (row, transcript) in enumerate(pool.map(modelled, jobs), start=1):
                identifier = f"{row['condition']}-run{row['run']}"
                started.evidence.record(str(row["program"]), "rows", identifier, row)
                started.evidence.record(str(row["program"]), "transcripts", identifier, {"attempts": transcript})
                kept.append(row)
                if done % 20 == 0 or done == len(jobs):
                    progress(f"sources: {done}/{len(jobs)} model runs")
    summary = summarise(kept)
    campaign.finish(started, summary, table(summary), _rows)
    progress(f"sources: sealed; {summary['conditions']}")
    return True
