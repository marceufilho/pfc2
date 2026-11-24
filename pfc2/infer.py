"""Loop bounds proposed from the shape of a counting loop and kept only when the checker proves them.

For a loop whose condition compares a counter `i` with an expression the loop does not change, and
whose body moves `i` by a positive constant exactly once, the candidates are

    up-counter    `init <= i`  and, for a step of one,  `i <= limit`
    down-counter  `i <= init`  and, for a step of one,  `limit <= i`

They are conjoined with whatever invariant the loop already has. A candidate is only text until
the checker proves its initiation and preservation: when a loop's invariant obligations fail, its
candidates are weakened (all, each alone, none) until they hold. Nothing here admits a proof, and
a wrong candidate costs a solver call, never soundness.
"""

from dataclasses import replace

from pfc2.core import ir, smt, vc
from pfc2.core.authorization import expressions
from pfc2.core.config import SOLVER_TIMEOUT_MS
from pfc2.core.parse import SpecKind
from pfc2.core.target import Target
from pfc2.elaborate import Inferred, Unit, conjoin, released

_FLIP = {"<": ">", "<=": ">=", ">": "<", ">=": "<=", "!=": "!="}
Site = tuple[int, int | None]


def _bare(expression: ir.Expr) -> ir.Expr:
    while isinstance(expression, ir.Convert):
        expression = expression.operand
    return expression


def _written(statement: ir.Statement | None) -> frozenset[str]:
    """Scalar symbols assigned or declared anywhere inside one statement."""
    if isinstance(statement, ir.Assign):
        return frozenset({statement.target.symbol.id}) if isinstance(statement.target, ir.Variable) else frozenset()
    if isinstance(statement, ir.Local):
        return frozenset({statement.symbol.id})
    if isinstance(statement, ir.Block):
        return frozenset().union(*(_written(child) for child in statement.statements))
    if isinstance(statement, ir.If):
        return _written(statement.then_body) | _written(statement.else_body)
    if isinstance(statement, ir.While):
        return _written(statement.body)
    if isinstance(statement, ir.For):
        return _written(statement.initializer) | _written(statement.update) | _written(statement.body)
    return frozenset()


def _stable(expression: ir.Expr, written: frozenset[str]) -> bool:
    """True when the loop cannot change the value: no memory read, no call, no written variable."""
    for node in expressions(expression):
        if isinstance(node, (ir.Index, ir.Call, ir.Separated, ir.Result)):
            return False
        if isinstance(node, ir.Variable) and node.symbol.id in written:
            return False
    return True


def _compare(operator: str, left: ir.Expr, right: ir.Expr) -> ir.Expr:
    long = ir.ScalarType.LONG
    common = long if long in (left.type, right.type) else ir.ScalarType.INT
    sides = [
        side if side.type == common else ir.Convert(common, side, location=side.location) for side in (left, right)
    ]
    return ir.Binary(ir.ScalarType.INT, operator, sides[0], sides[1], location=left.location)


def _step(loop: ir.While | ir.For, counter: ir.Symbol) -> int | None:
    """Signed constant the loop adds to the counter each iteration, when it does so exactly once."""
    updates = [loop.update] if isinstance(loop, ir.For) and loop.update is not None else []
    top = [*loop.body.statements, *updates]
    moves = [s for s in top if isinstance(s, ir.Assign) and _written(s) == {counter.id}]
    elsewhere = [s for s in top if s not in moves and counter.id in _written(s)]
    if len(moves) != 1 or elsewhere:
        return None
    value = _bare(moves[0].value)
    if not isinstance(value, ir.Binary) or value.operator not in {"+", "-"}:
        return None
    left, right = _bare(value.left), _bare(value.right)
    if isinstance(left, ir.Variable) and left.symbol.id == counter.id and isinstance(right, ir.Literal):
        amount = right.value
    elif value.operator == "+" and isinstance(right, ir.Variable) and right.symbol.id == counter.id:
        amount = left.value if isinstance(left, ir.Literal) else 0
    else:
        return None
    return (amount if value.operator == "+" else -amount) or None


def candidates(loop: ir.While | ir.For, initial: dict[str, ir.Expr]) -> tuple[ir.Expr, ...]:
    """Bound candidates for one loop; `initial` maps a symbol to the value it holds when the loop starts."""
    condition = _bare(loop.condition) if loop.condition is not None else None
    if not isinstance(condition, ir.Binary) or condition.operator not in _FLIP:
        return ()
    written = _written(loop.body) | (_written(loop.update) if isinstance(loop, ir.For) else frozenset())
    left, right, operator = _bare(condition.left), _bare(condition.right), condition.operator
    if not (isinstance(left, ir.Variable) and left.symbol.id in written):
        left, right, operator = right, left, _FLIP[operator]
    if not isinstance(left, ir.Variable) or left.symbol.id not in written or not _stable(right, written):
        return ()
    step = _step(loop, left.symbol)
    if step is None or (step > 0) != (operator in {"<", "<=", "!="}) and operator != "!=":
        return ()
    result = []
    start = initial.get(left.symbol.id)
    if start is not None and _stable(start, written):
        result.append(_compare("<=", start, left) if step > 0 else _compare("<=", left, start))
    if abs(step) == 1 and operator in {"<", ">", "!="}:
        result.append(_compare("<=", left, right) if step > 0 else _compare("<=", right, left))
    return tuple(result)


class _Finder:
    """Walk one function in source order, tracking the value each scalar holds at each loop."""

    def __init__(self) -> None:
        self.found: dict[Site, tuple[ir.Expr, ...]] = {}

    def block(self, block: ir.Block, initial: dict[str, ir.Expr]) -> None:
        for statement in block.statements:
            if isinstance(statement, ir.Local):
                initial[statement.symbol.id] = statement.initializer
            elif isinstance(statement, ir.Assign) and isinstance(statement.target, ir.Variable):
                initial[statement.target.symbol.id] = statement.value
            elif isinstance(statement, ir.Block):
                self.block(statement, initial)
            elif isinstance(statement, ir.If):
                for branch in (statement.then_body, statement.else_body):
                    if branch is not None:
                        self.block(branch, dict(initial))
            elif isinstance(statement, (ir.While, ir.For)):
                if isinstance(statement, ir.For) and statement.initializer is not None:
                    self.block(ir.Block((statement.initializer,), location=statement.location), initial)
                proposed = candidates(statement, initial)
                if proposed:
                    self.found[(statement.location.line, statement.location.column)] = proposed
                self.block(statement.body, dict(initial))
            for name in _written(statement) if not isinstance(statement, (ir.Local, ir.Assign)) else ():
                initial.pop(name, None)
            # A value that mentions a variable changed by this statement is no longer the initial one.
            changed = _written(statement)
            for name in [n for n, value in initial.items() if not _stable(value, changed - {n})]:
                if not isinstance(statement, (ir.Local, ir.Assign)) or name not in changed:
                    initial.pop(name, None)


def _options(proposed: tuple[ir.Expr, ...]) -> list[tuple[ir.Expr, ...]]:
    singles = [(item,) for item in proposed] if len(proposed) > 1 else []
    return [proposed, *singles, ()]


def _strengthen(block: ir.Block, chosen: dict[Site, tuple[ir.Expr, ...]]) -> ir.Block:
    result: list[ir.Statement] = []
    for statement in block.statements:
        if isinstance(statement, ir.Block):
            statement = _strengthen(statement, chosen)
        elif isinstance(statement, ir.If):
            else_body = _strengthen(statement.else_body, chosen) if statement.else_body is not None else None
            statement = replace(statement, then_body=_strengthen(statement.then_body, chosen), else_body=else_body)
        elif isinstance(statement, (ir.While, ir.For)):
            extra = chosen.get((statement.location.line, statement.location.column), ())
            invariant = statement.invariant
            if extra and invariant is not None:
                stated = _bare(invariant.condition)
                trivial = isinstance(stated, ir.Literal) and stated.value == 1
                invariant = replace(invariant, condition=conjoin(extra if trivial else (*extra, invariant.condition)))
            elif extra:
                invariant = ir.Contract(SpecKind.INVARIANT, conjoin(extra), location=statement.location)
            statement = replace(statement, invariant=invariant, body=_strengthen(statement.body, chosen))
        result.append(statement)
    return replace(block, statements=tuple(result))


def _loops(block: ir.Block) -> list[ir.While | ir.For]:
    found: list[ir.While | ir.For] = []
    for statement in block.statements:
        if isinstance(statement, ir.Block):
            found += _loops(statement)
        elif isinstance(statement, ir.If):
            found += _loops(statement.then_body) + (_loops(statement.else_body) if statement.else_body else [])
        elif isinstance(statement, (ir.While, ir.For)):
            found += [statement, *_loops(statement.body)]
    return found


def apply(unit: Unit, target: Target, *, timeout_ms: int = SOLVER_TIMEOUT_MS) -> Unit:
    """Return the unit with every provable candidate bound added to its loops (and listed in `inferred`)."""
    found: dict[str, dict[Site, tuple[ir.Expr, ...]]] = {}
    for function in unit.program.functions:
        finder = _Finder()
        finder.block(function.body, {})
        if finder.found:
            found[function.name] = finder.found
    if not found:
        return unit
    level = {(name, site): 0 for name, sites in found.items() for site in sites}
    cache = smt.SolverCache()
    while True:
        functions = tuple(
            (
                replace(
                    function,
                    body=_strengthen(
                        function.body,
                        {
                            site: _options(found[function.name][site])[level[function.name, site]]
                            for site in found[function.name]
                        },
                    ),
                )
                if function.name in found
                else function
            )
            for function in unit.program.functions
        )
        program = replace(unit.program, functions=functions)
        conditions = vc.generate(program)
        proof = smt.check(program, target, timeout_ms=timeout_ms, cache=cache)
        status = {result.obligation.id: str(result.status) for result in proof.results}
        needs = {item.id: item.dependencies for item in conditions.obligations}
        # A proof counts with the proofs it depends on; an unrelated failure elsewhere does not matter here.
        counted = smt.admitted({identifier for identifier, value in status.items() if value == "proved"}, needs)
        failing = {
            (o.location.line, o.location.column)
            for o in conditions.obligations
            if o.kind in {"entry", "preservation"} and o.id not in counted
        }
        weakened = False
        refuted = set()  # Loops whose invariant fails in this program, whatever option it carries.
        for function in functions:
            for loop in _loops(function.body):
                where = loop.invariant.location if loop.invariant is not None else loop.location
                if (where.line, where.column) in failing:
                    refuted.add((function.name, (loop.location.line, loop.location.column)))
        for function in functions:
            for loop in _loops(function.body):
                site = (loop.location.line, loop.location.column)
                key = (function.name, site)
                where = loop.invariant.location if loop.invariant is not None else loop.location
                last = len(_options(found[function.name][site])) - 1 if key in level else 0
                if key in level and level[key] < last and (where.line, where.column) in failing:
                    level[key] += 1
                    weakened = True
                    break
            if weakened:
                break
        if not weakened:
            break
    inferred = tuple(
        Inferred(name, site[0], ir.render_expression(conjoin(_options(found[name][site])[level[name, site]])))
        for (name, site) in sorted(level, key=lambda key: (key[1][0], key[1][1] or 0))
        if _options(found[name][site])[level[name, site]]
    )
    # A loop whose invariant fails with every option, even with no candidate at all, fails because of what was
    # written. Keep its candidates as part of that (unproved) invariant so the one error reported is the written
    # invariant, with the accesses that rely on the bounds shown as depending on it. They are not listed as
    # inferred: nothing about that loop is proved, and the file is refused either way.
    exhausted = {
        key
        for key in level
        if level[key] == len(_options(found[key[0]][key[1]])) - 1 and found[key[0]][key[1]] and key in refuted
    }
    if exhausted:
        functions = tuple(
            (
                replace(
                    function,
                    body=_strengthen(
                        function.body,
                        {
                            site: _options(found[function.name][site])[
                                0 if (function.name, site) in exhausted else level[function.name, site]
                            ]
                            for site in found[function.name]
                        },
                    ),
                )
                if function.name in found
                else function
            )
            for function in unit.program.functions
        )
        program = replace(unit.program, functions=functions)
    laws = frozenset(law.name for law in unit.laws)
    return replace(unit, program=program, code=released(program, laws), inferred=inferred)
