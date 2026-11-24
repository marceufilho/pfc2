"""Immutable structured IR and annotation-preserving C reconstruction.

No proof authority is attached to these nodes. Convert records C's implicit
conversions; the printer relies on the original C context to perform them.
"""

from dataclasses import dataclass, fields, is_dataclass
from enum import StrEnum
from typing import TypeAlias

from pfc2.core.diagnostics import SourceLocation
from pfc2.core.parse import SpecKind


class ScalarType(StrEnum):
    LONG = "long"
    BOOL = "_Bool"
    INT = "int"  # In expressions (C promotions, comparisons, small literals) and as an array element.
    CHAR = "char"  # Array elements only; signed or unsigned as the target says.


@dataclass(frozen=True)
class ArrayType:
    element: ScalarType


CType: TypeAlias = ScalarType | ArrayType


@dataclass(frozen=True, kw_only=True)
class Node:
    location: SourceLocation


@dataclass(frozen=True)
class Symbol(Node):
    id: str
    name: str
    type: CType
    const: bool = False  # Element qualification for array parameters.


@dataclass(frozen=True)
class Parameter:
    symbol: Symbol
    length: Symbol | None = None


@dataclass(frozen=True)
class Expr(Node):
    type: CType


@dataclass(frozen=True)
class Literal(Expr):
    spelling: str
    value: int


@dataclass(frozen=True)
class Variable(Expr):
    symbol: Symbol


@dataclass(frozen=True)
class Result(Expr):
    """The return value, bound only in ENSURES."""


@dataclass(frozen=True)
class Index(Expr):
    array: Symbol
    index: Expr


@dataclass(frozen=True)
class Unary(Expr):
    operator: str
    operand: Expr


@dataclass(frozen=True)
class Binary(Expr):
    operator: str
    left: Expr
    right: Expr


@dataclass(frozen=True)
class Convert(Expr):
    operand: Expr


@dataclass(frozen=True)
class Call(Expr):
    function: str
    arguments: tuple[Expr, ...]


@dataclass(frozen=True)
class Separated(Expr):
    # Typed transport only: no memory interpretation or proof authority yet.
    arguments: tuple[Expr, ...]


@dataclass(frozen=True)
class Contract(Node):
    kind: SpecKind
    condition: Expr


@dataclass(frozen=True)
class Local(Node):
    symbol: Symbol
    initializer: Expr


_WIDTH_ORDER = {ScalarType.BOOL: 0, ScalarType.CHAR: 1, ScalarType.INT: 2, ScalarType.LONG: 3}


def narrowing(expression: "Expr") -> bool:
    """Is this a conversion to `char` or `int` from a type with values the target type may not hold?

    C11 6.3.1.3p3 makes the result implementation-defined when the value does not fit, so each such
    conversion carries an obligation that it does. Conversions to `long` and `_Bool` never lose a value's
    meaning (`_Bool` is "not zero"), and `_Bool`'s 0 and 1 fit every type.
    """
    if not isinstance(expression, Convert) or expression.type not in {ScalarType.CHAR, ScalarType.INT}:
        return False
    source = expression.operand.type
    assert isinstance(source, ScalarType) and isinstance(expression.type, ScalarType)
    return _WIDTH_ORDER[source] > _WIDTH_ORDER[expression.type]


MAX_LOCAL_ARRAY = 65536  # Elements; a local array lives on the stack.
EXACT_LOCAL_ARRAY = 64  # Up to this length every element's initial value is stated to the prover.


@dataclass(frozen=True)
class LocalArray(Node):
    """`T a[N] = {v0, v1, ...};`: a new array of N elements; elements after the listed ones are zero."""

    symbol: Symbol
    size: int
    initial: tuple[Literal | Unary, ...]


@dataclass(frozen=True)
class Assign(Node):
    target: Variable | Index
    value: Expr


@dataclass(frozen=True)
class Block(Node):
    statements: tuple["Statement", ...]


@dataclass(frozen=True)
class If(Node):
    condition: Expr
    then_body: Block
    else_body: Block | None


@dataclass(frozen=True)
class While(Node):
    condition: Expr
    invariant: Contract | None
    body: Block


@dataclass(frozen=True)
class For(Node):
    initializer: Local | Assign | None
    condition: Expr | None
    update: Assign | None
    invariant: Contract | None
    body: Block


@dataclass(frozen=True)
class Return(Node):
    value: Expr


@dataclass(frozen=True)
class Break(Node):
    """Leave the innermost loop."""


@dataclass(frozen=True)
class Continue(Node):
    """End this iteration of the innermost loop: go to the update of a `for`, then to the condition."""


Statement: TypeAlias = Local | LocalArray | Assign | Block | If | While | For | Return | Contract | Break | Continue


def continues(block: Block) -> bool:
    """Does a `continue` in this loop body belong to this loop (not to a loop nested in it)?"""
    for statement in block.statements:
        if isinstance(statement, Continue):
            return True
        if isinstance(statement, Block) and continues(statement):
            return True
        if isinstance(statement, If) and (
            continues(statement.then_body) or statement.else_body is not None and continues(statement.else_body)
        ):
            return True
    return False


@dataclass(frozen=True)
class Function(Node):
    name: str
    return_type: ScalarType
    parameters: tuple[Parameter, ...]
    contracts: tuple[Contract, ...]
    body: Block
    external: bool = False  # Declared with a contract and no body: called under its contract, never verified.


@dataclass(frozen=True)
class Global:
    symbol: Symbol
    initial: Literal | Unary  # A literal, possibly negated: the value when the program starts.


@dataclass(frozen=True)
class Program:
    functions: tuple[Function, ...]
    verification: str = "not-run"
    globals: tuple[Global, ...] = ()


def render_expression(expression: Expr) -> str:
    if isinstance(expression, Literal):
        return expression.spelling
    if isinstance(expression, Result):
        return "RESULT"
    if isinstance(expression, Variable):
        return expression.symbol.name
    if isinstance(expression, Index):
        return f"{expression.array.name}[{render_expression(expression.index)}]"
    if isinstance(expression, Unary):
        return f"({expression.operator}{render_expression(expression.operand)})"
    if isinstance(expression, Binary):
        return f"({render_expression(expression.left)} {expression.operator} {render_expression(expression.right)})"
    if isinstance(expression, Convert):
        return render_expression(expression.operand)
    if isinstance(expression, (Call, Separated)):
        name = expression.function if isinstance(expression, Call) else "SEPARATED"
        return f"{name}({', '.join(render_expression(argument) for argument in expression.arguments)})"
    raise TypeError(f"unsupported IR expression: {type(expression).__name__}")


def _declaration(symbol: Symbol) -> str:
    qualifier = "const " if symbol.const else ""
    if isinstance(symbol.type, ArrayType):
        return f"{qualifier}{symbol.type.element} {symbol.name}[]"
    return f"{qualifier}{symbol.type} {symbol.name}"


def array_declaration(statement: LocalArray) -> str:
    assert isinstance(statement.symbol.type, ArrayType)
    qualifier = "const " if statement.symbol.const else ""
    values = ", ".join(render_expression(value) for value in statement.initial)
    return f"{qualifier}{statement.symbol.type.element} {statement.symbol.name}[{statement.size}] = {{{values}}}"


def _simple(statement: Local | Assign | Return | Contract) -> str:
    if isinstance(statement, Local):
        return f"{_declaration(statement.symbol)} = {render_expression(statement.initializer)}"
    if isinstance(statement, Assign):
        return f"{render_expression(statement.target)} = {render_expression(statement.value)}"
    if isinstance(statement, Return):
        return f"return {render_expression(statement.value)}"
    return f"{statement.kind}({render_expression(statement.condition)})"


def _block(block: Block, depth: int, invariant: Contract | None = None) -> list[str]:
    lines = ["    " * depth + _simple(invariant) + ";"] if invariant else []
    for statement in block.statements:
        lines.extend(_statement(statement, depth))
    return lines


def _condition(expression: Expr) -> str:
    text = render_expression(expression)
    # Clang diagnoses double parentheses around == in control conditions under -Wall.
    return text[1:-1] if isinstance(expression, Binary) and expression.operator == "==" else text


def _statement(statement: Statement, depth: int) -> list[str]:
    indent = "    " * depth
    if isinstance(statement, (Local, Assign, Return, Contract)):
        return [indent + _simple(statement) + ";"]
    if isinstance(statement, (Break, Continue)):
        return [indent + ("break;" if isinstance(statement, Break) else "continue;")]
    if isinstance(statement, LocalArray):
        return [indent + array_declaration(statement) + ";"]
    if isinstance(statement, Block):
        return [indent + "{", *_block(statement, depth + 1), indent + "}"]
    if isinstance(statement, If):
        lines = [indent + f"if ({_condition(statement.condition)}) {{", *_block(statement.then_body, depth + 1)]
        if statement.else_body is not None:
            lines.append(indent + "} else {")
            lines.extend(_block(statement.else_body, depth + 1))
        return [*lines, indent + "}"]
    if isinstance(statement, While):
        header = f"while ({_condition(statement.condition)})"
    else:
        initial = _simple(statement.initializer) if statement.initializer else ""
        condition = render_expression(statement.condition) if statement.condition else ""
        update = _simple(statement.update) if statement.update else ""
        header = f"for ({initial}; {condition}; {update})"
    return [indent + header + " {", *_block(statement.body, depth + 1, statement.invariant), indent + "}"]


def print_c(program: Program) -> str:
    """Reconstruct annotated C from lowered IR, without checks or assumptions.

    Accepts IR produced by lower(), not arbitrary or deserialized IR. Implicit
    conversions are valid in the retained operator/assignment/return contexts.
    """
    lines = [
        "/* PFC2: the program as the checker reads it, contracts spelled as markers. Not checked, not emitted. */",
        "",
    ]
    for item in program.globals:
        lines.append(f"{_declaration(item.symbol)} = {render_expression(item.initial)};")
    if len(program.functions) > 1:
        for function in program.functions:
            parameters = ", ".join(_declaration(parameter.symbol) for parameter in function.parameters) or "void"
            lines.append(f"{function.return_type} {function.name}({parameters});")
        lines.append("")
    for function in program.functions:
        parameters = ", ".join(_declaration(parameter.symbol) for parameter in function.parameters) or "void"
        lines.extend([f"{function.return_type} {function.name}({parameters})", "{"])
        lines.extend("    " + _simple(contract) + ";" for contract in function.contracts)
        lines.extend(_block(function.body, 1))
        lines.extend(["}", ""])
    return "\n".join(lines)


JSONValue: TypeAlias = str | int | float | bool | None | list["JSONValue"] | dict[str, "JSONValue"]


def to_data(value: object) -> JSONValue:
    """Serialize for inspection only, with node tags; not a proof/cache format."""
    if is_dataclass(value) and not isinstance(value, type):
        return {
            "node": type(value).__name__,
            **{field.name: to_data(getattr(value, field.name)) for field in fields(value)},
        }
    if isinstance(value, tuple):
        return [to_data(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    raise TypeError(f"unsupported IR data: {type(value).__name__}")
