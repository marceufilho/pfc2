"""Reference interpreter for PFC2's typed IR: the independent observation of the differential experiments.

It executes a lowered program over unbounded Python integers and rejects, instead of guessing, every
execution that C leaves undefined or implementation-defined, or that the contracts exclude:

- each C arithmetic result is checked against its type on the target (`Overflow`);
- `/` truncates toward zero and `%` is its remainder; a zero divisor is `DivisionByZero`; `MIN / -1` and
  `MIN % -1` are `Overflow` (C11 6.5.5p6);
- a value stored into a `char` or `int` element must fit it (`ConversionOutOfRange`, C11 6.3.1.3p3);
- `&&` and `||` short-circuit; `!` and comparisons yield 0 or 1;
- every index is checked against the capacity the array was declared with: the value of its length
  parameter when the function was entered, or the literal length of a local array (`OutOfBounds`);
- a local array starts with its listed values followed by zeros, and is a new object on every execution
  of its declaration;
- `break` leaves the innermost loop; `continue` goes to the update of a `for`;
- `requires` of the entry function and of every callee is evaluated with unbounded arithmetic; a false one is
  `PreconditionViolated`; an annotation that divides by zero or reads outside an array is
  `AnnotationUndefined`;
- `invariant`, `assert` and `ensures` are evaluated the same way and reported as violations without stopping
  the run: they are claims about the program, not part of it;
- globals hold their initial values when the entry point `pfc2_main` starts, and the given values otherwise;
- a declared-only function is run by the host model passed in, and its contract is checked around the call;
  without a model for it the run is `Unsupported`;
- a step budget guards non-termination (`Inconclusive`).

Independence: this module shares the front end's result (the IR) and the target's integer layout with the
compiler and nothing else. It imports neither the generator of verification conditions, nor the solver layer,
nor the emitter, nor the authorization module; a test enforces this. It is not a proof of anything, and it shares
with the compiler every mistake the front end makes.
"""

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, field, replace
from typing import Literal

from pfc2.core import ir
from pfc2.core.diagnostics import SourceLocation
from pfc2.core.parse import SpecKind
from pfc2.core.target import Target, limits

DEFAULT_FUEL = 50_000_000
ENTRY = "pfc2_main"
RejectionKind = Literal[
    "InvalidInput",
    "PreconditionViolated",
    "OutOfBounds",
    "Overflow",
    "DivisionByZero",
    "ConversionOutOfRange",
    "AnnotationUndefined",
    "Inconclusive",
    "Unsupported",
]
# What the checked C must stop at with a trap: the operations the emitter guards.
TRAPPING: frozenset[str] = frozenset({"OutOfBounds", "Overflow", "DivisionByZero", "ConversionOutOfRange"})


@dataclass(frozen=True)
class Inputs:
    """Concrete arguments by parameter name, and values for the globals (by name) of a non-entry function."""

    scalars: Mapping[str, int] = field(default_factory=dict)
    arrays: Mapping[str, Sequence[int]] = field(default_factory=dict)
    globals: Mapping[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class Observation:
    result: int
    arrays: dict[str, tuple[int, ...]]  # Final contents of the entry function's array parameters.
    globals: dict[str, int]
    output: str  # What the host model printed.
    steps: int
    annotation_violations: tuple[str, ...]


@dataclass(frozen=True)
class Rejection:
    kind: RejectionKind
    message: str
    location: SourceLocation | None
    annotation_violations: tuple[str, ...] = ()
    output: str = ""  # Printed before the rejection.


Argument = int | list[int]


class Host:
    """The world outside the program: one method per declared-only function. The base host knows none."""

    def __init__(self) -> None:
        self.output: list[str] = []

    def call(self, name: str, arguments: Sequence[Argument]) -> int | None:
        """The function's result, or None when this host has no model for it. Array arguments may be written."""
        return None


class _Reject(Exception):
    def __init__(self, kind: RejectionKind, message: str, location: SourceLocation | None) -> None:
        super().__init__(message)
        self.rejection = Rejection(kind, message, location)


class _Return(Exception):
    def __init__(self, value: int) -> None:
        super().__init__()
        self.value = value


class _Break(Exception):
    pass


class _Continue(Exception):
    pass


@dataclass(frozen=True)
class LoopHead:
    """One loop-head state handed to an observer: function, loop position and the named scalars in scope."""

    function: str
    location: SourceLocation
    scalars: Mapping[str, int]


Observer = Callable[[LoopHead], None]


@dataclass
class _Frame:
    scalars: dict[str, int]
    arrays: dict[str, list[int]]
    capacity: dict[str, int]  # Array symbol id -> the number of elements it was declared with.
    names: dict[str, str] = field(default_factory=dict)  # Symbol id -> source name, for observers.
    result: int | None = None


class _Interpreter:
    def __init__(
        self, program: ir.Program, target: Target, fuel: int, host: Host, observer: Observer | None = None
    ) -> None:
        self.functions = {function.name: function for function in program.functions}
        self.target = target
        self.fuel = fuel
        self.steps = 0
        self.violations: list[str] = []
        self.host = host
        self.observer = observer
        self.globals: dict[str, int] = {}
        self.global_ids = {item.symbol.id for item in program.globals}
        self.stack: list[str] = []

    # -- ranges -------------------------------------------------------------------------------------------

    def _range(self, type_: ir.CType) -> tuple[int, int]:
        if type_ is ir.ScalarType.BOOL:
            return 0, 1
        if isinstance(type_, ir.ScalarType):
            return limits(self.target, type_.value)
        raise _Reject("Unsupported", f"no value range for {type_}", None)

    def _fits(self, value: int, type_: ir.CType, location: SourceLocation, kind: RejectionKind = "Overflow") -> int:
        low, high = self._range(type_)
        if not low <= value <= high:
            raise _Reject(kind, f"{type_} value {value} is outside [{low}, {high}]", location)
        return value

    # -- expressions --------------------------------------------------------------------------------------

    def _scalar(self, symbol: ir.Symbol, frame: _Frame) -> int:
        return self.globals[symbol.id] if symbol.id in self.global_ids else frame.scalars[symbol.id]

    def evaluate(self, expression: ir.Expr, frame: _Frame, *, annotation: bool) -> int:
        self._tick(expression.location)
        if isinstance(expression, ir.Literal):
            return expression.value
        if isinstance(expression, ir.Result):
            if not annotation or frame.result is None:
                raise _Reject("Unsupported", "result outside a postcondition", expression.location)
            return frame.result
        if isinstance(expression, ir.Variable):
            if isinstance(expression.type, ir.ArrayType):
                raise _Reject("Unsupported", "array used as a scalar value", expression.location)
            return self._scalar(expression.symbol, frame)
        if isinstance(expression, ir.Index):
            buffer, index = self._index(expression, frame, annotation)
            return buffer[index]
        if isinstance(expression, ir.Convert):
            return self._convert(expression, frame, annotation)
        if isinstance(expression, ir.Unary):
            return self._unary(expression, frame, annotation)
        if isinstance(expression, ir.Binary):
            return self._binary(expression, frame, annotation)
        if isinstance(expression, ir.Separated):
            return self._separated(expression, frame)
        if isinstance(expression, ir.Call):
            raise _Reject("Unsupported", "call outside a statement boundary", expression.location)
        raise _Reject("Unsupported", f"expression {type(expression).__name__}", expression.location)

    def _index(self, expression: ir.Index, frame: _Frame, annotation: bool) -> tuple[list[int], int]:
        index = self.evaluate(expression.index, frame, annotation=annotation)
        buffer = frame.arrays[expression.array.id]
        declared = frame.capacity[expression.array.id]
        if not 0 <= index < declared or index >= len(buffer):
            kind: RejectionKind = "AnnotationUndefined" if annotation else "OutOfBounds"
            raise _Reject(
                kind, f"{expression.array.name}[{index}] with declared length {declared}", expression.location
            )
        return buffer, index

    def _convert(self, expression: ir.Convert, frame: _Frame, annotation: bool) -> int:
        operand = self.evaluate(expression.operand, frame, annotation=annotation)
        if expression.type is ir.ScalarType.BOOL:
            return int(operand != 0)
        if annotation or expression.type is ir.ScalarType.LONG:
            return operand  # Annotations are mathematical; every scalar value is representable in long.
        return self._fits(operand, expression.type, expression.location, "ConversionOutOfRange")

    def _unary(self, expression: ir.Unary, frame: _Frame, annotation: bool) -> int:
        operand = self.evaluate(expression.operand, frame, annotation=annotation)
        if expression.operator == "!":
            return int(operand == 0)
        if expression.operator == "+":
            return operand
        if expression.operator == "-":
            return -operand if annotation else self._fits(-operand, expression.type, expression.location)
        raise _Reject("Unsupported", f"unary operator {expression.operator}", expression.location)

    def _binary(self, expression: ir.Binary, frame: _Frame, annotation: bool) -> int:
        operator = expression.operator
        left = self.evaluate(expression.left, frame, annotation=annotation)
        if operator == "&&":
            return int(left != 0 and self.evaluate(expression.right, frame, annotation=annotation) != 0)
        if operator == "||":
            return int(left != 0 or self.evaluate(expression.right, frame, annotation=annotation) != 0)
        right = self.evaluate(expression.right, frame, annotation=annotation)
        comparisons = {
            "==": left == right,
            "!=": left != right,
            "<": left < right,
            "<=": left <= right,
            ">": left > right,
            ">=": left >= right,
        }
        if operator in comparisons:
            return int(comparisons[operator])
        if operator in {"/", "%"}:
            if right == 0:
                kind: RejectionKind = "AnnotationUndefined" if annotation else "DivisionByZero"
                raise _Reject(kind, "division by zero", expression.location)
            magnitude = abs(left) // abs(right)
            quotient = magnitude if (left < 0) == (right < 0) else -magnitude
            if not annotation:
                self._fits(quotient, expression.type, expression.location)  # MIN / -1, also for the remainder.
            return quotient if operator == "/" else left - quotient * right
        if operator == "+":
            result = left + right
        elif operator == "-":
            result = left - right
        elif operator == "*":
            result = left * right
        else:
            raise _Reject("Unsupported", f"binary operator {operator}", expression.location)
        return result if annotation else self._fits(result, expression.type, expression.location)

    def _separated(self, expression: ir.Separated, frame: _Frame) -> int:
        arguments = expression.arguments
        if (
            len(arguments) != 4
            or not isinstance(arguments[0], ir.Variable)
            or not isinstance(arguments[2], ir.Variable)
        ):
            raise _Reject("Unsupported", "separated needs two array/length pairs", expression.location)
        n = self.evaluate(arguments[1], frame, annotation=True)
        m = self.evaluate(arguments[3], frame, annotation=True)
        if n < 0 or m < 0:
            return 0
        left, right = frame.arrays[arguments[0].symbol.id], frame.arrays[arguments[2].symbol.id]
        return int(n == 0 or m == 0 or left is not right)

    # -- statements ---------------------------------------------------------------------------------------

    def _tick(self, location: SourceLocation) -> None:
        self.steps += 1
        if self.steps > self.fuel:
            raise _Reject("Inconclusive", f"step budget of {self.fuel} exhausted", location)

    def _truth(self, expression: ir.Expr, frame: _Frame, *, annotation: bool = False) -> bool:
        return self.evaluate(expression, frame, annotation=annotation) != 0

    def _annotation(self, contract: ir.Contract, frame: _Frame) -> None:
        if not self._truth(contract.condition, frame, annotation=True):
            location = contract.location
            text = f"{contract.kind} at {location.line}:{location.column}"
            if text not in self.violations:  # One entry per annotation site, in order of first violation.
                self.violations.append(text)

    def _head(self, loop: ir.While | ir.For, frame: _Frame) -> bool:
        """The loop head: the invariant is a claim about every arrival here, the last one included."""
        if loop.invariant is not None:
            self._annotation(loop.invariant, frame)
        if self.observer is not None:
            scalars = {frame.names[key]: value for key, value in frame.scalars.items() if key in frame.names}
            self.observer(LoopHead(self.stack[-1], loop.location, scalars))
        return True

    def _value(self, expression: ir.Expr, frame: _Frame) -> int:
        if isinstance(expression, ir.Call):
            return self._call(expression, frame)
        return self.evaluate(expression, frame, annotation=False)

    def _call(self, call: ir.Call, frame: _Frame) -> int:
        self._tick(call.location)
        callee = self.functions.get(call.function)
        if callee is None:
            raise _Reject("Unsupported", f"call to undefined function {call.function}", call.location)
        scalars: dict[str, int] = {}
        arrays: dict[str, list[int]] = {}
        caller_capacity: dict[str, int] = {}
        for parameter, argument in zip(callee.parameters, call.arguments, strict=True):
            if isinstance(parameter.symbol.type, ir.ArrayType):
                if not isinstance(argument, ir.Variable):
                    raise _Reject("Unsupported", "array argument must name an array", call.location)
                arrays[parameter.symbol.id] = frame.arrays[argument.symbol.id]
                caller_capacity[parameter.symbol.id] = frame.capacity[argument.symbol.id]
            else:
                scalars[parameter.symbol.id] = self.evaluate(argument, frame, annotation=False)
        capacity = {}
        for parameter in callee.parameters:
            if parameter.length is None:
                continue
            declared = scalars[parameter.length.id]
            if not 0 <= declared <= caller_capacity[parameter.symbol.id]:
                message = f"{callee.name} is given {caller_capacity[parameter.symbol.id]} element(s) as {declared}"
                raise _Reject("PreconditionViolated", message, call.location)
            capacity[parameter.symbol.id] = declared
        inner = _Frame(scalars, arrays, capacity, _names(callee))
        return self._execute(callee, inner, call.location)

    def _external(self, function: ir.Function, frame: _Frame, where: SourceLocation) -> int:
        arguments: list[Argument] = [
            frame.arrays[p.symbol.id] if isinstance(p.symbol.type, ir.ArrayType) else frame.scalars[p.symbol.id]
            for p in function.parameters
        ]
        result = self.host.call(function.name, arguments)
        if result is None:
            raise _Reject("Unsupported", f"no host model for the declared function {function.name}", where)
        for parameter in function.parameters:  # A host that stores a value the element type cannot hold is wrong.
            if isinstance(parameter.symbol.type, ir.ArrayType):
                for value in frame.arrays[parameter.symbol.id]:
                    self._fits(value, parameter.symbol.type.element, where, "Unsupported")
        return self._fits(result, function.return_type, where, "Unsupported")

    def _execute(self, function: ir.Function, frame: _Frame, call_site: SourceLocation | None) -> int:
        for contract in function.contracts:
            if contract.kind is SpecKind.REQUIRES and not self._truth(contract.condition, frame, annotation=True):
                where = call_site or contract.location
                raise _Reject("PreconditionViolated", f"requires of {function.name} is false", where)
        self.stack.append(function.name)
        try:
            if function.external:
                value = self._external(function, frame, call_site or function.location)
            else:
                try:
                    self._block(function.body, frame)
                except _Return as returned:
                    value = returned.value
                else:
                    raise _Reject("Unsupported", f"{function.name} ended without a return", function.location)
        finally:
            self.stack.pop()
        frame.result = self._fits(value, function.return_type, function.location)
        for contract in function.contracts:
            if contract.kind is SpecKind.ENSURES:
                self._annotation(contract, frame)
        return frame.result

    def _block(self, block: ir.Block, frame: _Frame) -> None:
        for statement in block.statements:
            self._statement(statement, frame)

    def _iterate(self, loop: ir.While | ir.For, frame: _Frame) -> None:
        while self._head(loop, frame) and (loop.condition is None or self._truth(loop.condition, frame)):
            self._tick(loop.location)  # An empty `for (;;) {}` still spends its budget.
            try:
                self._block(loop.body, frame)
            except _Break:
                return
            except _Continue:
                pass
            if isinstance(loop, ir.For) and loop.update is not None:
                self._statement(loop.update, frame)

    def _statement(self, statement: ir.Statement, frame: _Frame) -> None:
        self._tick(statement.location)
        if isinstance(statement, ir.Local):
            value = self._fits(self._value(statement.initializer, frame), statement.symbol.type, statement.location)
            frame.scalars[statement.symbol.id] = value
            frame.names[statement.symbol.id] = statement.symbol.name
        elif isinstance(statement, ir.LocalArray):
            listed = [self.evaluate(item, frame, annotation=False) for item in statement.initial]
            frame.arrays[statement.symbol.id] = listed + [0] * (statement.size - len(listed))
            frame.capacity[statement.symbol.id] = statement.size
        elif isinstance(statement, ir.Assign):
            self._assign(statement, frame)
        elif isinstance(statement, ir.Block):
            self._block(statement, frame)
        elif isinstance(statement, ir.If):
            if self._truth(statement.condition, frame):
                self._block(statement.then_body, frame)
            elif statement.else_body is not None:
                self._block(statement.else_body, frame)
        elif isinstance(statement, ir.While):
            self._iterate(statement, frame)
        elif isinstance(statement, ir.For):
            if statement.initializer is not None:
                self._statement(statement.initializer, frame)
            self._iterate(statement, frame)
        elif isinstance(statement, ir.Return):
            raise _Return(self._value(statement.value, frame))
        elif isinstance(statement, ir.Break):
            raise _Break
        elif isinstance(statement, ir.Continue):
            raise _Continue
        elif isinstance(statement, ir.Contract):
            self._annotation(statement, frame)
        else:
            raise _Reject("Unsupported", f"statement {type(statement).__name__}", statement.location)

    def _assign(self, statement: ir.Assign, frame: _Frame) -> None:
        value = self._value(statement.value, frame)
        target = statement.target
        if isinstance(target, ir.Variable):
            value = self._fits(value, target.type, statement.location)
            if target.symbol.id in self.global_ids:
                self.globals[target.symbol.id] = value
            else:
                frame.scalars[target.symbol.id] = value
            return
        buffer, index = self._index(target, frame, False)
        buffer[index] = self._fits(value, target.type, statement.location, "ConversionOutOfRange")


def _names(function: ir.Function) -> dict[str, str]:
    return {p.symbol.id: p.symbol.name for p in function.parameters if not isinstance(p.symbol.type, ir.ArrayType)}


def _initial(item: ir.Global) -> int:
    value = item.initial
    if isinstance(value, ir.Literal):
        return value.value
    operand = value.operand
    while isinstance(operand, ir.Convert):
        operand = operand.operand
    assert isinstance(operand, ir.Literal) and value.operator == "-"
    return -operand.value


def _bind(interpreter: _Interpreter, program: ir.Program, function: ir.Function, inputs: Inputs) -> _Frame:
    """Validate the concrete entry state before any statement runs."""
    target = interpreter.target
    names = {p.symbol.name for p in function.parameters}
    given = set(inputs.scalars) | set(inputs.arrays)
    if given != names or set(inputs.scalars) & set(inputs.arrays):
        missing, extra = sorted(names - given), sorted(given - names)
        raise _Reject("InvalidInput", f"missing parameters {missing}, unexpected {extra}", function.location)
    known = {item.symbol.name: item for item in program.globals}
    if set(inputs.globals) - set(known):
        raise _Reject("InvalidInput", f"unknown globals {sorted(set(inputs.globals) - set(known))}", function.location)
    if function.name == ENTRY and inputs.globals:
        raise _Reject("InvalidInput", "the program entry starts from the initial values of the globals", None)
    for name, item in known.items():
        value = inputs.globals.get(name, _initial(item))
        low, high = interpreter._range(item.symbol.type)
        if type(value) is not int or not low <= value <= high:
            raise _Reject("InvalidInput", f"global {name}={value!r} outside its type", item.symbol.location)
        interpreter.globals[item.symbol.id] = value
    scalars: dict[str, int] = {}
    arrays: dict[str, list[int]] = {}
    copies: dict[int, list[int]] = {}  # One buffer object passed under two names stays one buffer (aliasing).
    for parameter in function.parameters:
        symbol = parameter.symbol
        if isinstance(symbol.type, ir.ArrayType):
            values = inputs.arrays[symbol.name]
            low, high = interpreter._range(symbol.type.element)
            if any(type(v) is not int or not low <= v <= high for v in values):
                raise _Reject("InvalidInput", f"{symbol.name} holds a value outside {symbol.type.element}", None)
            arrays[symbol.id] = copies.setdefault(id(values), list(values))
            continue
        value = inputs.scalars[symbol.name]
        low, high = interpreter._range(symbol.type)
        if type(value) is not int or not low <= value <= high:
            raise _Reject("InvalidInput", f"{symbol.name}={value!r} outside the {symbol.type} range", symbol.location)
        scalars[symbol.id] = value
    capacity = {}
    for parameter in function.parameters:
        if parameter.length is None:
            continue
        # A negative length is a value a caller can pass: the array then has no element to access, and it is
        # for the function's own `requires` to say whether the call is allowed.
        declared = max(0, scalars[parameter.length.id])
        if len(arrays[parameter.symbol.id]) < declared:
            message = f"buffer {parameter.symbol.name} is shorter than its declared length {declared}"
            raise _Reject("InvalidInput", message, parameter.symbol.location)
        capacity[parameter.symbol.id] = declared
    del target
    return _Frame(scalars, arrays, capacity, _names(function))


def run(
    program: ir.Program,
    inputs: Inputs,
    *,
    target: Target,
    function: str | None = None,
    host: Host | None = None,
    fuel: int = DEFAULT_FUEL,
    observer: Observer | None = None,
) -> Observation | Rejection:
    """Execute one function on concrete inputs; return the complete final state or a typed rejection."""
    functions = {f.name: f for f in program.functions}
    if not functions:
        raise ValueError("program has no functions")
    name = function if function is not None else program.functions[0].name
    if name not in functions:
        raise ValueError(f"unknown function {name!r}")
    if type(fuel) is not int or fuel <= 0:
        raise ValueError("fuel must be a positive integer")
    entry = functions[name]
    world = host if host is not None else Host()
    interpreter = _Interpreter(program, target, fuel, world, observer)
    try:
        frame = _bind(interpreter, program, entry, inputs)
        result = interpreter._execute(entry, frame, None)
    except _Reject as rejected:
        return replace(
            rejected.rejection, annotation_violations=tuple(interpreter.violations), output="".join(world.output)
        )
    arrays = {p.symbol.name: tuple(frame.arrays[p.symbol.id]) for p in entry.parameters if p.length is not None}
    final = {item.symbol.name: interpreter.globals[item.symbol.id] for item in program.globals}
    return Observation(result, arrays, final, "".join(world.output), interpreter.steps, tuple(interpreter.violations))


def evaluate_condition(
    program: ir.Program, inputs: Inputs, expression: ir.Expr, *, target: Target, function: str | None = None
) -> bool | None:
    """Truth of an annotation (a `requires` conjunct) on concrete inputs at function entry, read mathematically.

    None when the inputs do not fit the signature or the expression is undefined on them. It never consults the
    compiler; the expected-trap experiment uses it to decide whether an emitted entry check must fire.
    """
    functions = {f.name: f for f in program.functions}
    name = function if function is not None else program.functions[0].name
    if name not in functions:
        raise ValueError(f"unknown function {name!r}")
    interpreter = _Interpreter(program, target, DEFAULT_FUEL, Host(), None)
    try:
        frame = _bind(interpreter, program, functions[name], inputs)
        return interpreter._truth(expression, frame, annotation=True)
    except _Reject:
        return None
