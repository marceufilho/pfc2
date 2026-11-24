"""Seeded random programs of the PFC2 language, with the inputs to run them on.

In the spirit of Csmith and of XDsmith for Dafny: many small programs nobody chose by hand, so that an engine
and an interpreter that disagree somewhere have a chance to show it. A program is a few functions over a
`long` array, optionally a `char` or `int` array, scalars and globals, built from every statement the language
has: locals, assignments, array writes, `if`, `for`, counted `while` loops with a measure, `break`, `continue`,
early `return`, local arrays, calls to the functions generated before it, `/` and `%`.

What the generator promises is small on purpose:

- every program is accepted by the front end (a test checks a range of seeds);
- array indices are in range by construction, except in programs marked `defect`, where one index is
  deliberately off by one;
- nothing is promised about arithmetic: sums and products of array elements may overflow on some inputs.

It does not decide what is valid. The interpreter does, input by input; the generator only tries to make
valid inputs common and invalid ones present. Nor does it know whether PFC2 certifies a program.

The same seed always gives the same program and the same cases: the generator uses its own `random.Random`
and no global state.
"""

from dataclasses import dataclass
from random import Random

from pfc2_eval.interpret import Inputs

GENERATOR = "pfc2-eval-generator-v1"
MAX_LENGTH = 8  # Largest array length a contract allows.
SCALAR_RANGE = (-50, 50)
DEFECT_RATE = 0.08  # Share of programs with one index deliberately off by one.
LONG_MAX = 2**63 - 1


@dataclass(frozen=True)
class Parameter:
    name: str
    role: str  # "length", "array", "index", "scalar"
    element: str = "long"
    length: str = ""  # For an array: the name of its length parameter.
    const: bool = False


@dataclass(frozen=True)
class Signature:
    name: str
    parameters: tuple[Parameter, ...]


@dataclass(frozen=True)
class Generated:
    seed: int
    text: str
    entry: Signature
    globals: tuple[str, ...]
    defect: bool
    generator: str = GENERATOR


class _Function:
    """One function being written: its names in scope and its lines."""

    def __init__(self, rng: Random, signature: Signature, helpers: list[Signature], globals_: list[str], defect: bool):
        self.rng = rng
        self.signature = signature
        self.helpers = helpers
        self.globals = globals_
        self.defect = defect  # Still to be planted in this function.
        self.serial = 0
        self.lines: list[str] = []
        self.readable = [p.name for p in signature.parameters if p.role in {"scalar", "index", "length"}] + globals_
        self.writable = list(globals_)
        self.arrays = [p for p in signature.parameters if p.role == "array"]
        self.counters: list[tuple[str, str]] = []  # (loop variable, the length it stays below), innermost last.
        self.locals: list[tuple[str, int]] = []  # Local arrays: name and length.

    def fresh(self, prefix: str) -> str:
        self.serial += 1
        return f"{prefix}{self.serial}"

    def line(self, depth: int, text: str) -> None:
        self.lines.append("    " * depth + text)

    # -- expressions --------------------------------------------------------------------------------------

    def index(self, array: Parameter) -> str:
        choices = ["0", f"{array.length} - 1"]
        choices += [counter for counter, bound in self.counters if bound == array.length]
        if array.length == "n":
            choices.append("k")
        chosen = self.rng.choice(choices)
        if self.defect and self.rng.random() < 0.5:
            self.defect = False
            return self.rng.choice([array.length, f"{chosen} + 1"])
        return chosen

    def read(self) -> str:
        if self.locals and self.rng.random() < 0.3:
            name, size = self.rng.choice(self.locals)
            return f"{name}[{self.rng.randrange(size)}]"
        array = self.rng.choice(self.arrays)
        return f"{array.name}[{self.index(array)}]"

    def expression(self, depth: int = 0) -> str:
        roll = self.rng.random()
        if depth >= 2 or roll < 0.25:
            return str(self.rng.randint(0, 9))
        if roll < 0.5:
            return self.rng.choice(self.readable)
        if roll < 0.7:
            return self.read()
        left, right = self.expression(depth + 1), self.expression(depth + 1)
        if roll < 0.9:
            return f"({left} {self.rng.choice(['+', '-', '*'])} {right})"
        divisor = self.rng.choice([2, 3, 7, -3])
        return f"({left} {self.rng.choice(['/', '%'])} {divisor})"

    def condition(self, depth: int = 0) -> str:
        roll = self.rng.random()
        if depth < 1 and roll < 0.25:
            return f"({self.condition(1)}) {self.rng.choice(['&&', '||'])} ({self.condition(1)})"
        if depth < 1 and roll < 0.32:
            return f"!({self.condition(1)})"
        operator = self.rng.choice(["<", "<=", ">", ">=", "==", "!="])
        return f"{self.expression(1)} {operator} {self.expression(1)}"  # The caller supplies the parentheses.

    # -- statements ---------------------------------------------------------------------------------------

    def block(self, depth: int, nesting: int, loop: str | None, size: int) -> None:
        """`size` statements; `loop` is the kind of the innermost loop ("for", "while") or None."""
        for _ in range(size):
            self.statement(depth, nesting, loop)
        if nesting > 0 and self.rng.random() < 0.15:
            self.leave(depth, loop)

    def leave(self, depth: int, loop: str | None) -> None:
        """A jump as the last statement of a block, under a condition, so nothing after it is dead."""
        options = ["return"] + (["break"] if loop else []) + (["continue"] if loop == "for" else [])
        chosen = self.rng.choice(options)
        self.line(depth, f"if ({self.condition()}) {{")
        self.line(depth + 1, f"return {self.expression()};" if chosen == "return" else f"{chosen};")
        self.line(depth, "}")

    def statement(self, depth: int, nesting: int, loop: str | None) -> None:
        roll = self.rng.random()
        if roll < 0.22:
            name = self.fresh("t")
            self.line(depth, f"long {name} = {self.expression()};")
            # Visible to later statements of this block only when it is the function's top block: C scoping.
            if nesting == 0:
                self.readable.append(name)
                self.writable.append(name)
        elif roll < 0.38 and self.writable:
            target = self.rng.choice(self.writable)
            operator = self.rng.choice(["=", "=", "+=", "-="])
            self.line(depth, f"{target} {operator} {self.expression()};")
        elif roll < 0.55:
            self.write(depth)
        elif roll < 0.68 and nesting < 2:
            self.line(depth, f"if ({self.condition()}) {{")
            self.block(depth + 1, nesting + 1, loop, self.rng.randint(1, 2))
            if self.rng.random() < 0.4:
                self.line(depth, "} else {")
                self.block(depth + 1, nesting + 1, loop, 1)
            self.line(depth, "}")
        elif roll < 0.80 and nesting < 2:
            self.counted(depth, nesting)
        elif roll < 0.86 and nesting < 2:
            self.countdown(depth, nesting)
        elif roll < 0.92 and self.helpers:
            self.call(depth, nesting)
        elif roll < 0.97 and nesting == 0 and len(self.locals) < 2:
            name, size = self.fresh("buf"), self.rng.randint(2, 4)
            values = ", ".join(str(self.rng.randint(-5, 5)) for _ in range(self.rng.randint(1, size)))
            self.line(depth, f"long {name}[{size}] = {{{values}}};")
            self.locals.append((name, size))
        else:
            self.increment(depth)

    def write(self, depth: int) -> None:
        writable = [array for array in self.arrays if not array.const]
        if self.locals and (not writable or self.rng.random() < 0.3):
            name, size = self.rng.choice(self.locals)
            self.line(depth, f"{name}[{self.rng.randrange(size)}] = {self.expression()};")
            return
        if not writable:
            self.increment(depth)
            return
        array = self.rng.choice(writable)
        place = f"{array.name}[{self.index(array)}]"
        if array.element == "char":
            self.line(depth, f"{place} = {self.expression(1)} % 100;")  # Always within a char.
        elif self.rng.random() < 0.3:
            self.line(depth, f"{place}{self.rng.choice(['++', '--'])};")
        else:
            self.line(depth, f"{place} {self.rng.choice(['=', '+=', '-='])} {self.expression()};")

    def increment(self, depth: int) -> None:
        if self.writable:
            self.line(depth, f"{self.rng.choice(self.writable)}{self.rng.choice(['++', '--'])};")

    def counted(self, depth: int, nesting: int) -> None:
        bound = self.rng.choice(sorted({array.length for array in self.arrays}))
        counter = self.fresh("i")
        self.line(depth, f"for (long {counter} = 0; {counter} < {bound}; {counter}++) {{")
        self.counters.append((counter, bound))
        self.readable.append(counter)
        self.block(depth + 1, nesting + 1, "for", self.rng.randint(1, 3))
        self.readable.remove(counter)
        self.counters.pop()
        self.line(depth, "}")

    def countdown(self, depth: int, nesting: int) -> None:
        counter = self.fresh("w")
        measure = f" decreases({counter})" if self.rng.random() < 0.5 else ""
        self.line(depth, f"long {counter} = {self.rng.randint(1, 4)};")
        self.line(depth, f"while ({counter} > 0) invariant(0 <= {counter}){measure} {{")
        self.block(depth + 1, nesting + 1, "while", self.rng.randint(1, 2))
        self.line(depth + 1, f"{counter}--;")
        self.line(depth, "}")

    def call(self, depth: int, nesting: int) -> None:
        callee = self.rng.choice(self.helpers)
        arguments = []
        for parameter in callee.parameters:
            if parameter.role in {"length", "array", "index"}:
                arguments.append(parameter.name)  # Helpers share n, a and k with their caller.
            else:
                arguments.append(str(self.rng.randint(*SCALAR_RANGE)))
        name = self.fresh("c")
        self.line(depth, f"long {name} = {callee.name}({', '.join(arguments)});")
        if nesting == 0:
            self.readable.append(name)


def _signature(rng: Random, name: str, *, helper: bool) -> Signature:
    parameters = [Parameter("n", "length"), Parameter("a", "array", "long", "n"), Parameter("k", "index")]
    parameters.append(Parameter("x", "scalar"))
    if not helper:
        if rng.random() < 0.5:
            parameters.append(Parameter("y", "scalar"))
        extra = rng.random()
        if extra < 0.3:
            parameters += [Parameter("m", "length"), Parameter("s", "array", "char", "m", rng.random() < 0.5)]
        elif extra < 0.5:
            parameters.append(Parameter("v", "array", "int", "n", True))
    return Signature(name, tuple(parameters))


def _declaration(parameter: Parameter) -> str:
    if parameter.role == "array":
        qualifier = "const " if parameter.const else ""
        return f"{qualifier}{parameter.element} {parameter.name}[{parameter.length}]"
    return f"long {parameter.name}"


def _requires(signature: Signature) -> list[str]:
    low, high = SCALAR_RANGE
    clauses = []
    for parameter in signature.parameters:
        if parameter.role == "length":
            clauses.append(f"requires(1 <= {parameter.name} && {parameter.name} <= {MAX_LENGTH})")
        elif parameter.role == "index":
            clauses.append(f"requires(0 <= {parameter.name} && {parameter.name} < n)")
        elif parameter.role == "scalar":
            clauses.append(f"requires({low} <= {parameter.name} && {parameter.name} <= {high})")
    return clauses


def program(seed: int) -> Generated:
    """The program of a seed: one to three functions, the last of which is the entry."""
    rng = Random(f"{GENERATOR}:program:{seed}")
    globals_ = [f"g{index}" for index in range(rng.randint(0, 2))]
    lines = ['#include "pfc.h"', ""]
    lines += [f"long {name} = {rng.randint(-3, 3)};" for name in globals_]
    defect = rng.random() < DEFECT_RATE
    helpers: list[Signature] = []
    count = rng.randint(1, 3)
    entry = _signature(rng, "entry", helper=False)
    for position in range(count):
        last = position == count - 1
        signature = entry if last else _signature(rng, f"helper{position}", helper=True)
        writer = _Function(rng, signature, list(helpers), globals_, defect and last)
        writer.block(1, 0, None, rng.randint(2, 6 if last else 4))
        writer.line(1, f"return {writer.expression()};")
        lines.append("")
        lines.append(f"long {signature.name}({', '.join(_declaration(p) for p in signature.parameters)})")
        lines += [f"    {clause}" for clause in _requires(signature)]
        lines += ["{", *writer.lines, "}"]
        helpers.append(signature)
        if last:
            defect = defect and not writer.defect  # True only if the defect was actually planted.
    return Generated(seed, "\n".join(lines) + "\n", entry, tuple(globals_), defect)


def _element(rng: Random, element: str) -> int:
    roll = rng.random()
    if element == "char":
        return rng.randint(-128, 127) if roll < 0.1 else rng.randint(0, 120)
    limit = 2**31 - 1 if element == "int" else LONG_MAX
    if roll < 0.8:
        return rng.randint(-9, 9)
    if roll < 0.95:
        return rng.randint(-1_000_000, 1_000_000)
    return rng.choice([limit, -limit - 1, limit - 1, 1, -1, 0])


def cases(generated: Generated, count: int, *, stress: float = 0.05) -> list[Inputs]:
    """`count` inputs for the entry function. A `stress` share steps outside the contract on purpose."""
    rng = Random(f"{GENERATOR}:cases:{generated.seed}")
    low, high = SCALAR_RANGE
    drawn = []
    for _ in range(count):
        outside = rng.random() < stress
        scalars: dict[str, int] = {}
        arrays: dict[str, list[int]] = {}
        for parameter in generated.entry.parameters:
            if parameter.role == "length":
                scalars[parameter.name] = rng.randint(1, MAX_LENGTH)
            elif parameter.role == "scalar":
                scalars[parameter.name] = rng.randint(low, high)
        for parameter in generated.entry.parameters:
            if parameter.role == "index":
                scalars[parameter.name] = rng.randrange(scalars["n"])
            elif parameter.role == "array":
                extra = rng.choice([0, 0, 0, 2])  # Sometimes the buffer is longer than the function is told.
                length = scalars[parameter.length] + extra
                arrays[parameter.name] = [_element(rng, parameter.element) for _ in range(length)]
        if outside:
            name = rng.choice(sorted(scalars))
            scalars[name] = rng.choice([-1, 0, MAX_LENGTH + 1, high + 1, low - 1, LONG_MAX])
            # Buffers always hold what the function is told they hold: the driver never lies about memory.
            for parameter in generated.entry.parameters:
                if parameter.role == "array":
                    needed = max(0, min(scalars[parameter.length], 4 * MAX_LENGTH))
                    while len(arrays[parameter.name]) < needed:
                        arrays[parameter.name].append(_element(rng, parameter.element))
            if any(scalars[p.length] > len(arrays[p.name]) for p in generated.entry.parameters if p.role == "array"):
                scalars[name] = 0  # A length the buffers cannot honour is replaced by another outside value.
        globals_ = {name: rng.randint(-9, 9) for name in generated.globals}
        drawn.append(Inputs(scalars, arrays, globals_))
    return drawn
