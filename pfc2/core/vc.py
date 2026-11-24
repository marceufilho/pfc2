"""Solver-independent term algebra and verification report interface.

Backward substitution establishes partial-correctness conditions, not termination.
Mathematical arithmetic is conditional on defined C execution; limits remain
symbolic until a target is supplied in step 6. Nothing here authorizes deletion.
"""

import json
from dataclasses import dataclass
from typing import Literal, TypeAlias

from pfc2.core import ir
from pfc2.core.config import MAX_VC_TERM_DEPTH
from pfc2.core.config import MAX_VC_TERM_NODES as MAX_VC_TERM_NODES
from pfc2.core.diagnostics import FrontendError, SourceLocation
from pfc2.core.digest import sha256_text

MODEL = (
    "vc-v4: mathematical integers on defined C executions; target limits not instantiated; "
    "shared typed memory; typed reads are representable; substantive obligations; entry consistency"
)


@dataclass(frozen=True)
class Integer:
    value: int


@dataclass(frozen=True)
class Boolean:
    value: bool


TRUE = Boolean(True)


@dataclass(frozen=True)
class Reference:
    symbol: ir.Symbol


@dataclass(frozen=True)
class Limit:
    type: ir.ScalarType
    side: Literal["MIN", "MAX"]


@dataclass(frozen=True)
class Operation:
    operator: str
    arguments: tuple["Term", ...]


@dataclass(frozen=True)
class Read:
    array: ir.Symbol
    memory: "Term"
    address: "Term"
    index: "Term"


Term: TypeAlias = Integer | Boolean | Reference | Limit | Operation | Read
Kind: TypeAlias = Literal[
    "entry",
    "preservation",
    "bounds",
    "division",
    "overflow",
    "conversion",
    "assert",
    "postcondition",
    "call-precondition",
]


@dataclass(frozen=True)
class Hypothesis:
    kind: Literal[
        "type-domain", "allocation", "requires", "invariant", "induction-hypothesis", "guard", "assert", "postcondition"
    ]
    formula: Term


@dataclass(frozen=True)
class Obligation:
    id: str
    context_id: str
    kind: Kind
    category: Literal["required", "reported"]
    location: SourceLocation
    hypotheses: tuple[Hypothesis, ...]
    goal: Term
    dependencies: tuple[str, ...] = ()
    c_type: ir.ScalarType | None = None
    status: Literal["not-run"] = "not-run"
    observations: tuple[tuple[ir.Symbol, Term], ...] = ()


@dataclass(frozen=True)
class EntryCheck:
    """Consistency of declared entry hypotheses, separate from validity obligations."""

    context_id: str
    function: str
    location: SourceLocation
    hypotheses: tuple[Hypothesis, ...]


@dataclass(frozen=True)
class ExternalCheck:
    """Is the contract of a declared-only function possible at all? Callers assume it without a body to check.

    `hypotheses` are the parameter domains and the REQUIRES; `guarantees` the result domain and the ENSURES over
    `result`. `reads_memory` records that the ENSURES mentions array contents. `written_from` pairs each memory
    the function may have changed with the one before the call, and `frozen` gives the (memory before, memory
    after, base, length) of each array it received as `const` and therefore must leave as it found it.
    """

    context_id: str
    function: str
    location: SourceLocation
    hypotheses: tuple[Hypothesis, ...]
    result: Reference
    guarantees: tuple[Term, ...]
    reads_memory: bool
    written_from: tuple[tuple[Term, Term], ...] = ()  # (memory after the call, the memory it replaces).
    frozen: tuple[tuple[Term, Term, Term, Term], ...] = ()
    # (memory, lowest value, highest value, does the function choose it?): each element holds a value of its type.
    domains: tuple[tuple[Term, Term, Term, bool], ...] = ()


@dataclass(frozen=True)
class VCReport:
    context_id: str
    function: str
    obligations: tuple[Obligation, ...]
    model: str = MODEL
    verification: Literal["not-run"] = "not-run"
    entry_checks: tuple[EntryCheck, ...] = ()
    external_checks: tuple[ExternalCheck, ...] = ()


def _op(operator: str, *arguments: Term) -> Operation:
    return Operation(operator, arguments)


def _digest(value: object) -> str:
    return sha256_text(json.dumps(ir.to_data(value), sort_keys=True, separators=(",", ":")))


def _and(*terms: Term) -> Term:
    remaining = tuple(term for term in terms if term != Boolean(True))
    if not remaining:
        return Boolean(True)
    result = remaining[0]
    for term in remaining[1:]:
        result = _op("&&", result, term)
    return result


def _implies(path: Term, goal: Term) -> Term:
    return goal if path == Boolean(True) else _op("=>", path, goal)


def _range(term: Term, type_: ir.ScalarType) -> Term:
    low: Term = Integer(0) if type_ is ir.ScalarType.BOOL else Limit(type_, "MIN")
    high: Term = Integer(1) if type_ is ir.ScalarType.BOOL else Limit(type_, "MAX")
    return _and(_op("<=", low, term), _op("<=", term, high))


def _measure(term: Term) -> int:
    """Count expanded output, memoizing shared subtrees to avoid exponential work."""
    memo: dict[int, tuple[int, int]] = {}

    def visit(current: Term) -> tuple[int, int]:
        if id(current) not in memo:
            terms = (
                current.arguments
                if isinstance(current, Operation)
                else ((current.memory, current.address, current.index) if isinstance(current, Read) else ())
            )
            children = [visit(child) for child in terms]
            size = 1 + sum(item[0] for item in children)
            depth = 1 + max((item[1] for item in children), default=0)
            if size > MAX_VC_TERM_NODES or depth > MAX_VC_TERM_DEPTH:
                raise FrontendError("vc-complexity", "expanded VC exceeds the formula limit", SourceLocation("<VC>"))
            memo[id(current)] = size, depth
        return memo[id(current)]

    return visit(term)[0]


def _children(expression: ir.Expr) -> tuple[ir.Expr, ...]:
    if isinstance(expression, (ir.Convert, ir.Unary)):
        return (expression.operand,)
    if isinstance(expression, ir.Binary):
        return expression.left, expression.right
    if isinstance(expression, ir.Index):
        return (expression.index,)
    if isinstance(expression, (ir.Call, ir.Separated)):
        return expression.arguments
    return ()


def generate(program: ir.Program) -> VCReport:
    """Generate obligations from lowered IR, without solving or granting trust.

    The context digest covers canonical IR (including contracts and logical source
    locations) and this model version. It is not a solver cache or raw-file hash.
    """
    if not program.functions:
        location = program.functions[0].location if program.functions else SourceLocation("<IR>")
        raise FrontendError("vc-subset", "VC generation requires a function", location)
    try:
        from pfc2.core.wp import Generator

        return Generator(_digest((MODEL, program)), program).run()
    except FrontendError as error:
        if error.diagnostic.location.file != "<VC>":
            raise
        raise FrontendError(error.diagnostic.rule, error.diagnostic.message, program.functions[0].location) from None
    except RecursionError:
        raise FrontendError(
            "vc-complexity", "VC expression nesting exceeds the implementation limit", program.functions[0].location
        ) from None


def render_term(term: Term) -> str:
    """Human-readable mathematical notation; c_div means truncation toward zero."""
    if isinstance(term, Integer):
        return str(term.value)
    if isinstance(term, Boolean):
        return "true" if term.value else "false"
    if isinstance(term, Reference):
        return term.symbol.name
    if isinstance(term, Read):
        return f"{term.array.name}[{render_term(term.index)}]"
    if isinstance(term, Limit):
        return f"{term.type.value.upper()}_{term.side}"
    arguments = tuple(render_term(argument) for argument in term.arguments)
    if term.operator in {"!", "neg"}:
        operator = "-" if term.operator == "neg" else "!"
        return f"({operator}{arguments[0]})"
    if term.operator == "select":
        return f"{arguments[0]}[{arguments[1]}]"
    if term.operator in {"ite", "c_div", "c_rem", "store"}:
        return f'{term.operator}({", ".join(arguments)})'
    return f"({arguments[0]} {term.operator} {arguments[1]})"
