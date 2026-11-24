"""The added words become ordinary contracts of the core IR.

A `where` on a variable is a type: it must hold whenever the variable, or anything its predicate
mentions, has just been written. In the core contract language that is

    * `REQUIRES`  at entry, for a parameter;
    * `ASSERT`    after the declaration and after every assignment to a mentioned variable or array;
    * a conjunct of the `INVARIANT` of every loop that writes a mentioned variable.

`decreases(e)` becomes a ghost local and two assertions; `long a[n]` adds `REQUIRES(0 <= n)`. Every
clause is *checked*; none is assumed without a proof (a loop head assumes only an invariant whose
initiation and preservation are obligations of the same report).

A `law` is a function that is verified and never emitted. It is proved modularly, through the
contracts of the functions it calls, so those contracts must be strong enough: a function states
its own contract, and a law never supplies one.
"""

from dataclasses import dataclass, replace

from pfc2.clauses import STRING, Clause, rewrite
from pfc2.core import ir
from pfc2.core.authorization import expressions, statements
from pfc2.core.diagnostics import FrontendError
from pfc2.core.lower import lower
from pfc2.core.parse import SpecKind, parse_preprocessed
from pfc2.core.wp import calls, statement_expressions
from pfc2.surface import Law, Loop, Where, extract
from pfc2.text import moved


@dataclass(frozen=True)
class Refinement:
    where: Where
    symbol: ir.Symbol
    condition: ir.Expr
    mentions: frozenset[str]  # Symbol ids whose assignment re-checks the type.


@dataclass(frozen=True)
class Unit:
    filename: str
    preprocessed: str
    wheres: tuple[Where, ...]
    program: ir.Program  # Functions and laws: what is proved.
    source_text: str | None = None
    laws: tuple[Law, ...] = ()
    code: ir.Program | None = None  # Functions only: what is emitted (None when there is no law).
    loops: int = 0
    invariants: tuple[str, ...] = ()  # Supplied proof, one per loop in source order.
    loop_sites: tuple[Loop, ...] = ()
    bare_loops: int = 0  # Loops with neither a type nor an invariant: likely to need a proof.
    measures: tuple[Clause, ...] = ()  # `decreases` clauses: loops whose termination is proved.
    inferred: tuple["Inferred", ...] = ()  # Loop bounds proposed from the loop shape and proved (infer.py).
    externals: tuple[str, ...] = ()  # Functions declared and not defined: called under their contract, unverified.
    strings: tuple[str, ...] = ()  # String literal tokens; number K is the value of pfc2_str_K().
    entry: bool = False  # The file has `int main(void)`, checked as pfc2_main.


@dataclass(frozen=True)
class Inferred:
    function: str
    line: int
    invariant: str


GHOST = "pfc2_d"  # Locals that hold a loop measure; they exist only in the program that is proved.


def _mentions(condition: ir.Expr) -> frozenset[str]:
    names = set()
    for node in expressions(condition):
        if isinstance(node, ir.Variable):
            names.add(node.symbol.id)
        elif isinstance(node, ir.Index):
            names.add(node.array.id)
    return frozenset(names)


def _refinement(where: Where, symbol: ir.Symbol, contract: ir.Contract) -> Refinement:
    mentions = _mentions(contract.condition)
    if symbol.id not in mentions:
        raise FrontendError(
            "where-binder", f"the predicate must mention `{where.binder}`, the name it types", where.location
        )
    return Refinement(where, symbol, contract.condition, mentions)


def _bare(condition: ir.Expr) -> ir.Expr:
    return condition.operand if isinstance(condition, ir.Convert) else condition


def conjoin(conditions: tuple[ir.Expr, ...]) -> ir.Expr:
    result = _bare(conditions[0])
    for condition in conditions[1:]:
        result = ir.Binary(ir.ScalarType.INT, "&&", result, _bare(condition), location=condition.location)
    if result.type is ir.ScalarType.BOOL:
        return result
    return ir.Convert(ir.ScalarType.BOOL, result, location=conditions[0].location)


def _target(statement: ir.Assign) -> str:
    return statement.target.symbol.id if isinstance(statement.target, ir.Variable) else statement.target.array.id


def _written(statement: ir.Statement | None) -> frozenset[str]:
    """Symbols assigned anywhere inside one statement."""
    if isinstance(statement, ir.Assign):
        return frozenset({_target(statement)})
    if isinstance(statement, ir.Block):
        return frozenset().union(*(_written(child) for child in statement.statements))
    if isinstance(statement, ir.If):
        return _written(statement.then_body) | _written(statement.else_body)
    if isinstance(statement, ir.While):
        return _written(statement.body)
    if isinstance(statement, ir.For):
        initial = statement.initializer if isinstance(statement.initializer, ir.Assign) else None
        return _written(initial) | _written(statement.update) | _written(statement.body)
    return frozenset()


def _inside(statement: ir.Statement) -> list[ir.Statement]:
    """The statement and every statement nested in it."""
    if isinstance(statement, ir.Block):
        return list(statements(statement))
    return list(statements(ir.Block((statement,), location=statement.location)))


def _calls(statement: ir.Statement) -> bool:
    """Does the statement, or anything inside it, call a function?"""
    return any(
        isinstance(node, ir.Call)
        for inner in _inside(statement)
        for root in statement_expressions(inner)
        for node in expressions(root)
    )


class _Elaborator:
    def __init__(
        self,
        function: ir.Function,
        wheres: tuple[Where, ...],
        measures: dict[tuple[int, int | None], Clause],
        shared: frozenset[str] = frozenset(),
    ) -> None:
        self.function = function
        self.measures = measures
        self.attached: set[tuple[int, int | None]] = set()
        # What a call may change behind this function's back: any global, and the contents of any array.
        arrays = {p.symbol.id for p in function.parameters if isinstance(p.symbol.type, ir.ArrayType)}
        arrays |= {item.symbol.id for item in statements(function.body) if isinstance(item, ir.LocalArray)}
        self.shared = shared | arrays
        self.ghosts = 0
        self.pending = {(w.binder, w.binder_line): w for w in wheres if w.kind == "local"}
        self.signature = [w for w in wheres if w.kind != "local"]
        self.bare = 0  # Loops left without any stated invariant or type.

    def _invariant(self, loop: ir.While | ir.For, active: tuple[Refinement, ...]) -> ir.Contract | None:
        written = _written(loop) | (self.shared if _calls(loop) else frozenset())
        relevant = tuple(item.condition for item in active if item.mentions & written)
        if not relevant and loop.invariant is None:
            # The frozen generator needs an invariant at every loop; `1` claims nothing, so a loop
            # that needed a real one fails its dependent obligations instead of the whole file.
            self.bare += 1
            true = ir.Literal(ir.ScalarType.INT, "1", 1, location=loop.location)
            return ir.Contract(
                SpecKind.INVARIANT, ir.Convert(ir.ScalarType.BOOL, true, location=loop.location), location=loop.location
            )
        if not relevant:
            return loop.invariant
        existing = (loop.invariant.condition,) if loop.invariant is not None else ()
        location = loop.invariant.location if loop.invariant is not None else loop.location
        return ir.Contract(SpecKind.INVARIANT, conjoin(relevant + existing), location=location)

    def block(self, block: ir.Block, active: tuple[Refinement, ...]) -> ir.Block:
        result: list[ir.Statement] = []
        statements = list(block.statements)
        index = 0
        while index < len(statements):
            statement = statements[index]
            index += 1
            if isinstance(statement, ir.Local):
                result.append(statement)
                result.extend(self._after_call(statement, active))
                where = self.pending.pop((statement.symbol.name, statement.location.line), None)
                if where is not None:
                    marker = statements[index] if index < len(statements) else None
                    if not isinstance(marker, ir.Contract) or marker.kind is not SpecKind.ASSERT:
                        raise FrontendError(
                            "where-position", "cannot attach the type to its declaration", where.location
                        )
                    active += (_refinement(where, statement.symbol, marker),)
                    result.append(marker)
                    index += 1
            elif isinstance(statement, ir.Assign):
                result.append(statement)
                target = _target(statement)
                changed = {target} | (self.shared if _calls(statement) else frozenset())
                result.extend(
                    ir.Contract(SpecKind.ASSERT, item.condition, location=statement.location)
                    for item in active
                    if item.mentions & changed
                )
            elif isinstance(statement, ir.Block):
                result.append(self.block(statement, active))
            elif isinstance(statement, ir.If):
                else_body = self.block(statement.else_body, active) if statement.else_body is not None else None
                result.append(
                    replace(statement, then_body=self.block(statement.then_body, active), else_body=else_body)
                )
            elif isinstance(statement, (ir.While, ir.For)):
                invariant = self._invariant(statement, active)
                loop = replace(statement, invariant=invariant, body=self.block(statement.body, active))
                site = (statement.location.line, statement.location.column)
                measure = self.measures.get(site)
                if measure is not None:
                    self.attached.add(site)
                result.append(self._terminating(loop, measure) if measure is not None else loop)
            else:
                result.append(statement)
        return replace(block, statements=tuple(result))

    def _after_call(self, statement: ir.Local, active: tuple[Refinement, ...]) -> list[ir.Statement]:
        """A call may write any global, so the types that mention one are proved again after it."""
        if not _calls(statement):
            return []
        return [
            ir.Contract(SpecKind.ASSERT, item.condition, location=statement.location)
            for item in active
            if item.mentions & self.shared
        ]

    def _terminating(self, loop: ir.While | ir.For, clause: Clause) -> ir.Statement:
        """Prove `decreases(e)`: e is never negative when the body starts and is smaller when it ends.

        The clause arrived as `ASSERT(0 <= e)` at the start of the body. The value of e is kept in a
        ghost local, and after the body (and the update of a `for`, which therefore becomes a `while`)
        e must be below it. With both facts the loop cannot run forever.
        """
        if ir.continues(loop.body):
            # The measure is compared at the end of the body, and `continue` does not pass there.
            raise FrontendError(
                "decreases-continue",
                "a loop with `continue` cannot carry decreases() yet; restructure with `if`/`else`",
                clause.location,
            )
        marker = loop.body.statements[0] if loop.body.statements else None
        bound = _bare(marker.condition) if isinstance(marker, ir.Contract) and marker.kind is SpecKind.ASSERT else None
        if not isinstance(bound, ir.Binary) or bound.operator != "<=":
            raise FrontendError("clause-position", "cannot attach decreases() to its loop", clause.location)
        self.ghosts += 1
        where = clause.location
        long = ir.ScalarType.LONG
        measure = bound.right if bound.right.type is long else ir.Convert(long, bound.right, location=where)
        symbol = ir.Symbol(f"{self.function.name}:ghost{self.ghosts}", f"{GHOST}{self.ghosts}", long, location=where)
        ghost = ir.Variable(long, symbol, location=where)
        zero = ir.Convert(long, ir.Literal(ir.ScalarType.INT, "0", 0, location=where), location=where)

        def fact(operator: str, left: ir.Expr, right: ir.Expr) -> ir.Contract:
            condition = ir.Binary(ir.ScalarType.INT, operator, left, right, location=where)
            return ir.Contract(
                SpecKind.ASSERT, ir.Convert(ir.ScalarType.BOOL, condition, location=where), location=where
            )

        update = (loop.update,) if isinstance(loop, ir.For) and loop.update is not None else ()
        body = replace(
            loop.body,
            statements=(
                ir.Local(symbol, measure, location=where),
                fact("<=", zero, ghost),
                *loop.body.statements[1:],
                *update,
                fact("<", measure, ghost),
            ),
        )
        if isinstance(loop, ir.While):
            return replace(loop, body=body)
        true = ir.Convert(
            ir.ScalarType.BOOL, ir.Literal(ir.ScalarType.INT, "1", 1, location=loop.location), location=loop.location
        )
        condition = loop.condition if loop.condition is not None else true
        initial = (loop.initializer,) if loop.initializer is not None else ()
        looping = ir.While(condition, loop.invariant, body, location=loop.location)
        return ir.Block((*initial, looping), location=loop.location)

    def run(self) -> ir.Function:
        function = self.function
        parameters = {parameter.symbol.name: parameter.symbol for parameter in function.parameters}
        active: tuple[Refinement, ...] = ()
        typed = [w for w in self.signature if w.kind == "parameter"]
        # The surface pass wrote these markers first, parameters before the result, in source order.
        for where, contract in zip(typed, function.contracts, strict=False):
            symbol = parameters.get(where.binder)
            if symbol is None or contract.kind is not SpecKind.REQUIRES or not isinstance(symbol.type, ir.ScalarType):
                raise FrontendError("where-position", f"`{where.binder}` is not a scalar parameter", where.location)
            active += (_refinement(where, symbol, contract),)
        if len(function.contracts) < len(self.signature):
            raise FrontendError("where-position", "cannot attach the types to the function", self.signature[0].location)
        body = self.block(function.body, active)
        if self.pending:
            where = next(iter(self.pending.values()))
            raise FrontendError(
                "where-position", "write the typed declaration on one line: `long i where(p) = e;`", where.location
            )
        return replace(function, body=body)


def _sized(function: ir.Function) -> ir.Function:
    """`long a[n]` declares n elements, so n is not negative: a precondition like any other.

    It is assumed in the body, proved at every call and checked at entry for unverified callers. The older
    spelling `a[], a_len` is left alone: there the capacity is whatever the written contract says.
    """
    long = ir.ScalarType.LONG
    added: dict[str, ir.Contract] = {}
    for parameter in function.parameters:
        length = parameter.length
        if length is None or length.name == f"{parameter.symbol.name}_len" or length.id in added:
            continue
        where = parameter.symbol.location
        zero = ir.Convert(long, ir.Literal(ir.ScalarType.INT, "0", 0, location=where), location=where)
        bound = ir.Binary(ir.ScalarType.INT, "<=", zero, ir.Variable(long, length, location=where), location=where)
        condition = ir.Convert(ir.ScalarType.BOOL, bound, location=where)
        added[length.id] = ir.Contract(SpecKind.REQUIRES, condition, location=where)
    return replace(function, contracts=(*function.contracts, *added.values())) if added else function


def _without_ghosts(block: ir.Block) -> ir.Block:
    kept: list[ir.Statement] = []
    for statement in block.statements:
        if isinstance(statement, ir.Local) and statement.symbol.name.startswith(GHOST):
            continue
        if isinstance(statement, ir.Contract) and any(
            isinstance(node, ir.Variable) and node.symbol.name.startswith(GHOST)
            for node in expressions(statement.condition)
        ):
            continue
        if isinstance(statement, ir.Block):
            statement = _without_ghosts(statement)
        elif isinstance(statement, ir.If):
            else_body = _without_ghosts(statement.else_body) if statement.else_body is not None else None
            statement = replace(statement, then_body=_without_ghosts(statement.then_body), else_body=else_body)
        elif isinstance(statement, (ir.While, ir.For)):
            statement = replace(statement, body=_without_ghosts(statement.body))
        kept.append(statement)
    return replace(block, statements=tuple(kept))


def released(program: ir.Program, laws: frozenset[str]) -> ir.Program | None:
    """The program that is emitted: no laws and no ghost measures. None when nothing has to be removed."""
    functions = tuple(
        replace(function, body=_without_ghosts(function.body))
        for function in program.functions
        if function.name not in laws
    )
    return None if functions == program.functions else replace(program, functions=functions)


def _proved_to_terminate(program: ir.Program, measures: tuple[Clause, ...]) -> tuple[Clause, ...]:
    """The measures that establish termination: those of loops in which everything else ends too.

    A measure says each iteration gets closer to the end, provided the iteration itself ends. So a loop counts
    only if every loop nested in it counts and every function it calls ends on all its paths (all its loops
    count, and so on down the calls, which cannot be recursive). Declared functions are assumed to return.
    """
    functions = {function.name: function for function in program.functions}
    total: dict[str, bool] = {}
    counted: set[object] = set()

    def measured(loop: ir.While | ir.For) -> ir.Local | None:
        first = loop.body.statements[0] if loop.body.statements else None
        return first if isinstance(first, ir.Local) and first.symbol.name.startswith(GHOST) else None

    def returns(name: str) -> bool:
        if name not in total:
            function = functions[name]
            total[name] = function.external or ends(function.body)
        return total[name]

    def ends(statement: ir.Statement) -> bool:
        if isinstance(statement, ir.Block):
            return all([ends(child) for child in statement.statements])  # A list: visit every loop, even after a no.
        if isinstance(statement, ir.If):
            branches = [statement.then_body, *([statement.else_body] if statement.else_body is not None else [])]
            return all([ends(branch) for branch in branches])
        if isinstance(statement, (ir.While, ir.For)):
            inside = ends(statement.body)
            ghost = measured(statement)
            if ghost is not None and inside:
                counted.add(ghost.location)
            return ghost is not None and inside
        return all(returns(call.function) for root in statement_expressions(statement) for call in calls(root))

    for function in program.functions:
        if not function.external:
            returns(function.name)
    return tuple(clause for clause in measures if clause.location in counted)


def _check_laws(program: ir.Program, laws: tuple[Law, ...]) -> None:
    names = {law.name for law in laws}
    for function in program.functions:
        for statement in statements(function.body):
            for root in statement_expressions(statement):
                for node in expressions(root):
                    if isinstance(node, ir.Call) and node.function in names:
                        law = next(item for item in laws if item.name == node.function)
                        raise FrontendError("law-call", "a law is proved, not called", law.location)


def _relocate_block(block: ir.Block, anchors: dict[tuple[int, int | None], Clause]) -> ir.Block:
    result: list[ir.Statement] = []
    for statement in block.statements:
        if isinstance(statement, ir.Block):
            statement = _relocate_block(statement, anchors)
        elif isinstance(statement, ir.If):
            else_body = _relocate_block(statement.else_body, anchors) if statement.else_body is not None else None
            statement = replace(statement, then_body=_relocate_block(statement.then_body, anchors), else_body=else_body)
        elif isinstance(statement, (ir.While, ir.For)):
            clause = anchors.get((statement.location.line, statement.location.column))
            invariant = statement.invariant
            if clause is not None and invariant is not None:
                invariant = replace(invariant, location=clause.location)
            statement = replace(statement, invariant=invariant, body=_relocate_block(statement.body, anchors))
        result.append(statement)
    return replace(block, statements=tuple(result))


def _relocate(
    program: ir.Program, clauses: tuple[Clause, ...], anchors: dict[tuple[int, int | None], Clause]
) -> ir.Program:
    """Give each contract written as a clause the position of the clause, not of the `{` it was restated at."""
    functions = []
    for function in program.functions:
        stated = [c for c in clauses if c.function == function.name and c.kind in ("requires", "ensures")]
        contracts = list(function.contracts)
        # The clause markers were written after the markers of the parameter and result types.
        for offset, clause in enumerate(stated, start=len(contracts) - len(stated)):
            if offset >= 0:
                contracts[offset] = replace(contracts[offset], location=clause.location)
        functions.append(replace(function, contracts=tuple(contracts), body=_relocate_block(function.body, anchors)))
    return replace(program, functions=tuple(functions))


def elaborate_text(
    preprocessed: str,
    filename: str,
    *,
    source_text: str | None = None,
    invariants: tuple[str, ...] | None = None,
) -> Unit:
    """Pure elaboration of preprocessed text (and an optional supplied proof) into a program of the core IR."""
    clauses = rewrite(preprocessed, filename)
    surface = extract(clauses.text, filename, invariants=invariants)
    external = frozenset(clauses.externals) | {f"{STRING}{n}" for n in range(1, len(clauses.strings) + 1)}
    law_names = frozenset(law.name for law in surface.laws)

    def site(clause: Clause) -> tuple[int, int | None]:
        """The loop keyword of a clause, where the parser saw it: after what both surface passes inserted."""
        anchor = moved(moved(clause.anchor, clauses.shifts), surface.shifts)
        return anchor.line, anchor.column

    parsed = parse_preprocessed(surface.text, filename, ghost=law_names)
    anchors = {site(c): c for c in reversed(clauses.clauses) if c.kind == "invariant"}
    program = _relocate(lower(parsed, external=external), clauses.clauses, anchors)
    _check_laws(program, surface.laws)
    named = [g.symbol for g in program.globals] + [p.symbol for f in program.functions for p in f.parameters]
    for symbol in named:
        if symbol.name == "result":
            raise FrontendError(
                "ir-name",
                "`result` names the returned value in ensures(); give this variable another name",
                symbol.location,
            )
    names = {function.name for function in program.functions}
    for where in surface.wheres:
        if where.function not in names:
            raise FrontendError("where-position", "where() is not inside a function of this file", where.location)
    measures = {site(c): c for c in clauses.clauses if c.kind == "decreases"}
    shared = frozenset(item.symbol.id for item in program.globals)
    elaborators = [
        _Elaborator(function, tuple(w for w in surface.wheres if w.function == function.name), measures, shared)
        for function in program.functions
    ]
    functions = tuple(_sized(elaborator.run()) for elaborator in elaborators)
    attached = set().union(*(elaborator.attached for elaborator in elaborators))
    for place, clause in measures.items():
        if place not in attached:  # Never report a measure that no loop received.
            raise FrontendError("clause-position", "cannot attach decreases() to its loop", clause.location)
    code = released(replace(program, functions=functions), law_names)
    if code is not None and not code.functions:
        raise FrontendError("law-syntax", "a file of laws needs the functions they are about", surface.laws[0].location)
    return Unit(
        filename,
        preprocessed,
        surface.wheres,
        replace(program, functions=functions),
        source_text,
        surface.laws,
        code,
        len(surface.loops),
        invariants or (),
        surface.loops,
        sum(elaborator.bare for elaborator in elaborators),
        _proved_to_terminate(
            replace(program, functions=functions), tuple(c for c in clauses.clauses if c.kind == "decreases")
        ),
        externals=clauses.externals,
        strings=clauses.strings,
        entry=clauses.entry,
    )
