"""Structured path VCs using delayed assignment substitution and loop cutpoints.

The environment composes the same substitutions as straight-line WP. Branches
split paths; loops introduce arbitrary states and induction obligations. No
termination or frame property is inferred. See ADR-0013 for memory and admission.
"""

from dataclasses import dataclass, field, replace

from pfc2.core import ir, vc
from pfc2.core.config import MAX_VC_PATHS
from pfc2.core.diagnostics import FrontendError, SourceLocation
from pfc2.core.parse import SpecKind

op = vc._op
MEMORY_NAMING = 200  # Term nodes; see Generator.named.
ENTRY = "pfc2_main"  # The program entry: the only function that may assume the initial values of globals.


@dataclass
class State:
    values: dict[str, vc.Term] = field(default_factory=dict)
    bases: dict[str, vc.Term] = field(default_factory=dict)
    lengths: dict[str, vc.Term] = field(default_factory=dict)
    memory: dict[ir.ScalarType, vc.Term] = field(default_factory=dict)
    hypotheses: tuple[vc.Hypothesis, ...] = ()
    dependencies: tuple[str, ...] = ()
    induction: tuple[str, ...] = ()
    result: vc.Term | None = None

    def copy(self) -> "State":
        return replace(
            self,
            values=self.values.copy(),
            bases=self.bases.copy(),
            lengths=self.lengths.copy(),
            memory=self.memory.copy(),
        )

    def assume(self, kind: str, formula: vc.Term) -> None:
        self.hypotheses += (vc.Hypothesis(kind, formula),)  # type: ignore[arg-type]


def value(expression: ir.Expr, state: State) -> vc.Term:
    """Evaluate with composed substitutions; annotation arithmetic is mathematical."""
    if isinstance(expression, ir.Literal):
        return vc.Integer(expression.value)
    if isinstance(expression, ir.Result):
        if state.result is None:
            raise FrontendError("vc-result", "RESULT requires a return binding", expression.location)
        return state.result
    if isinstance(expression, ir.Variable):
        return state.values.get(expression.symbol.id, vc.Reference(expression.symbol))
    if isinstance(expression, ir.Index):
        assert isinstance(expression.array.type, ir.ArrayType)
        index = value(expression.index, state)
        if not state.memory:
            # Standalone substitution algebra: no program or alias assumptions.
            return op("select", vc.Reference(expression.array), index)
        return vc.Read(
            expression.array,
            state.memory[expression.array.type.element],
            op("+", state.bases[expression.array.id], index),
            index,
        )
    if isinstance(expression, ir.Convert):
        return (
            op("ite", truth(expression.operand, state), vc.Integer(1), vc.Integer(0))
            if expression.type is ir.ScalarType.BOOL
            else value(expression.operand, state)
        )
    if isinstance(expression, ir.Unary):
        if expression.operator == "!":
            return op("ite", truth(expression, state), vc.Integer(1), vc.Integer(0))
        operand = value(expression.operand, state)
        return operand if expression.operator == "+" else op("neg", operand)
    if isinstance(expression, ir.Binary):
        if expression.operator not in {"+", "-", "*", "/", "%"}:
            return op("ite", truth(expression, state), vc.Integer(1), vc.Integer(0))
        return op(
            {"/": "c_div", "%": "c_rem"}.get(expression.operator, expression.operator),
            value(expression.left, state),
            value(expression.right, state),
        )
    if isinstance(expression, ir.Separated):
        left, n, right, m = expression.arguments
        assert isinstance(left, ir.Variable) and isinstance(right, ir.Variable)
        if left.type != right.type:
            # Only typed objects, no casts/character accesses in the subset.
            return op(
                "ite",
                vc._and(op(">=", value(n, state), vc.Integer(0)), op(">=", value(m, state), vc.Integer(0))),
                vc.Integer(1),
                vc.Integer(0),
            )
        a, b = state.bases[left.symbol.id], state.bases[right.symbol.id]
        x, y = value(n, state), value(m, state)
        separated = vc._and(
            op(">=", x, vc.Integer(0)),
            op(">=", y, vc.Integer(0)),
            op(
                "||",
                op("||", op("==", x, vc.Integer(0)), op("==", y, vc.Integer(0))),
                op("||", op("<=", op("+", a, x), b), op("<=", op("+", b, y), a)),
            ),
        )
        return op("ite", separated, vc.Integer(1), vc.Integer(0))
    raise FrontendError("vc-expression", "call must be evaluated at a statement boundary", expression.location)


def truth(expression: ir.Expr, state: State) -> vc.Term:
    if isinstance(expression, ir.Convert):
        return truth(expression.operand, state)
    if isinstance(expression, ir.Unary) and expression.operator == "!":
        return op("!", truth(expression.operand, state))
    if isinstance(expression, ir.Binary):
        if expression.operator in {"&&", "||"}:
            return op(expression.operator, truth(expression.left, state), truth(expression.right, state))
        if expression.operator in {"==", "!=", "<", "<=", ">", ">="}:
            return op(expression.operator, value(expression.left, state), value(expression.right, state))
    return op("!=", value(expression, state), vc.Integer(0))


def _nodes(expression: ir.Expr) -> tuple[ir.Expr, ...]:
    return (expression,) + tuple(node for child in vc._children(expression) for node in _nodes(child))


def walk(block: ir.Block) -> tuple[ir.Statement, ...]:
    result: list[ir.Statement] = []
    for statement in block.statements:
        result.append(statement)
        if isinstance(statement, (ir.While, ir.For)):
            result.extend(walk(statement.body))
            if isinstance(statement, ir.For):
                result.extend(item for item in (statement.initializer, statement.update) if item)
        elif isinstance(statement, ir.If):
            result.extend(walk(statement.then_body))
            if statement.else_body:
                result.extend(walk(statement.else_body))
        elif isinstance(statement, ir.Block):
            result.extend(walk(statement))
    return tuple(result)


def calls(expression: ir.Expr) -> tuple[ir.Call, ...]:
    return ((expression,) if isinstance(expression, ir.Call) else ()) + tuple(
        call for child in vc._children(expression) for call in calls(child)
    )


def statement_expressions(statement: ir.Statement) -> tuple[ir.Expr, ...]:
    if isinstance(statement, ir.Local):
        return (statement.initializer,)
    if isinstance(statement, (ir.Return, ir.Assign)):
        return (statement.value,)
    return ()


class Generator:
    def __init__(self, context_id: str, program: ir.Program) -> None:
        self.context_id = context_id
        self.program = program
        self.functions = {function.name: function for function in program.functions}
        self.obligations: list[vc.Obligation] = []
        self.entry_checks: list[vc.EntryCheck] = []
        self.external_checks: list[vc.ExternalCheck] = []
        self.required: dict[str, tuple[str, ...]] = {}
        self.effects: dict[str, set[ir.ScalarType]] = {}
        self.globals = {item.symbol.id: item for item in program.globals}
        self.writes: dict[str, frozenset[str]] = {}  # Globals a function may assign, through its callees too.
        self.serial = 0
        self.term_count = 0
        # One memory per element type. The two narrower ones exist only in programs that use them, so that
        # programs without them keep the identities they had before these types were added.
        used = {
            symbol.type.element
            for function in program.functions
            for symbol in (
                *(parameter.symbol for parameter in function.parameters),
                *(item.symbol for item in walk(function.body) if isinstance(item, ir.LocalArray)),
            )
            if isinstance(symbol.type, ir.ArrayType)
        }
        narrow = sorted(used & {ir.ScalarType.INT, ir.ScalarType.CHAR})
        self.memories: tuple[ir.ScalarType, ...] = (ir.ScalarType.LONG, ir.ScalarType.BOOL, *narrow)
        self.elements: dict[str, ir.ScalarType] = {}  # Array symbol id -> element type, for arrays in scope.
        self.exits: list[tuple[list[State], list[State]]] = []  # Per enclosing loop: states at break, at continue.

    def fresh(self, name: str, type_: ir.CType, location: SourceLocation) -> vc.Reference:
        self.serial += 1
        return vc.Reference(ir.Symbol(f"vc:{self.serial}", name, type_, location=location))

    def add(
        self,
        kind: vc.Kind,
        location: SourceLocation,
        state: State,
        goal: vc.Term,
        c_type: ir.ScalarType | None = None,
        *,
        dependencies: tuple[str, ...] | None = None,
        observations: tuple[tuple[ir.Symbol, vc.Term], ...] = (),
    ) -> str:
        self.term_count += vc._measure(goal) + sum(vc._measure(h.formula) for h in state.hypotheses)
        if self.term_count > vc.MAX_VC_TERM_NODES:
            raise FrontendError("vc-complexity", "VC report exceeds the cumulative formula limit", location)
        identifier = str(len(self.obligations))  # Internal slot; replaced by complete content identity in finish().
        self.obligations.append(
            vc.Obligation(
                identifier,
                self.context_id,
                kind,
                "reported" if kind == "overflow" else "required",
                location,
                state.hypotheses,
                goal,
                state.dependencies if dependencies is None else dependencies,
                c_type,
                observations=observations,
            )
        )
        return identifier

    def safety(self, expression: ir.Expr, state: State, path: vc.Term = vc.TRUE, *, annotation: bool = False) -> None:
        for index, child in enumerate(vc._children(expression)):
            child_path = path
            if isinstance(expression, ir.Binary) and index == 1 and expression.operator in {"&&", "||"}:
                condition = truth(expression.left, state)
                child_path = vc._and(path, condition if expression.operator == "&&" else op("!", condition))
            self.safety(child, state, child_path, annotation=annotation)

        def record(kind: vc.Kind, goal: vc.Term, type_: ir.ScalarType | None = None) -> None:
            self.add(kind, expression.location, state, vc._implies(path, goal), type_)

        if isinstance(expression, ir.Index):
            index_value = value(expression.index, state)
            record(
                "bounds",
                vc._and(op("<=", vc.Integer(0), index_value), op("<", index_value, state.lengths[expression.array.id])),
            )
            # vc-v3 (ADR-0025): on this path, the object read holds a value representable in its type.
            # The target rejects padding bits and treats the minimum as a normal value (target.py), so
            # every defined read of a long/bool object lies in its range; this only adds a hypothesis.
            assert isinstance(expression.array.type, ir.ArrayType)
            if state.memory:
                domain = vc._range(value(expression, state), expression.array.type.element)
                state.assume("type-domain", vc._implies(path, domain))
        if isinstance(expression, ir.Binary) and expression.operator in {"/", "%"}:
            # C11 6.5.5p6: if a / b is not representable, both a / b and a % b are undefined.
            left, right = value(expression.left, state), value(expression.right, state)
            goal: vc.Term = op("!=", right, vc.Integer(0))
            if not annotation:
                assert isinstance(expression.type, ir.ScalarType)
                goal = vc._and(
                    goal,
                    op("!", vc._and(op("==", left, vc.Limit(expression.type, "MIN")), op("==", right, vc.Integer(-1)))),
                )
            record("division", goal)
        arithmetic = (
            isinstance(expression, ir.Binary)
            and expression.operator in {"+", "-", "*", "/"}
            or isinstance(expression, ir.Unary)
            and expression.operator == "-"
        )
        if arithmetic and not annotation:
            assert isinstance(expression.type, ir.ScalarType)
            record("overflow", vc._range(value(expression, state), expression.type), expression.type)

    def contract_safety(self, expression: ir.Expr, state: State) -> None:
        start = len(self.obligations)
        premise = state.copy()
        premise.dependencies = tuple(dep for dep in state.dependencies if dep not in state.induction)
        self.safety(expression, premise, annotation=True)
        # safety only appends read domains to these hypotheses. Keep them for the
        # annotation's goal, while retaining its definedness obligations below.
        state.hypotheses = premise.hypotheses
        state.dependencies += tuple(item.id for item in self.obligations[start:])

    def evaluate(self, expression: ir.Expr, state: State) -> vc.Term:
        if isinstance(expression, ir.Convert):
            operand = self.evaluate(expression.operand, state)
            if ir.narrowing(expression):
                # C11 6.3.1.3p3: the stored value is the computed one only if the element type can hold it.
                assert isinstance(expression.type, ir.ScalarType)
                self.add("conversion", expression.location, state, vc._range(operand, expression.type))
            return (
                op("ite", op("!=", operand, vc.Integer(0)), vc.Integer(1), vc.Integer(0))
                if expression.type is ir.ScalarType.BOOL
                else operand
            )
        if isinstance(expression, ir.Call):
            return self.call(expression, state)
        self.safety(expression, state)
        return value(expression, state)

    def call(self, expression: ir.Call, state: State) -> vc.Term:
        callee = self.functions.get(expression.function)
        if callee is None or callee.name not in self.required:
            raise FrontendError("vc-expression", "callee requires an acyclic in-unit definition", expression.location)
        bound = state.copy()
        bound.dependencies = tuple(dep for dep in state.dependencies if dep not in state.induction)
        bound.values = {}
        bound.bases = {}
        bound.lengths = {}
        for parameter, argument in zip(callee.parameters, expression.arguments, strict=True):
            symbol = parameter.symbol
            if isinstance(symbol.type, ir.ArrayType):
                assert isinstance(argument, ir.Variable)
                bound.bases[symbol.id] = state.bases[argument.symbol.id]
                bound.lengths[symbol.id] = state.lengths[argument.symbol.id]
            else:
                bound.values[symbol.id] = self.evaluate(argument, state)
        for identifier in self.globals:
            bound.values[identifier] = state.values[identifier]
        for parameter in callee.parameters:
            if parameter.length:
                length = bound.values[parameter.length.id]
                identifier = self.add(
                    "call-precondition",
                    expression.location,
                    bound,
                    vc._and(op("<=", vc.Integer(0), length), op("<=", length, bound.lengths[parameter.symbol.id])),
                )
                bound.dependencies += (identifier,)
                bound.lengths[parameter.symbol.id] = length
        for contract in callee.contracts:
            if contract.kind is SpecKind.REQUIRES:
                self.contract_safety(contract.condition, bound)
                condition = truth(contract.condition, bound)
                identifier = self.add("call-precondition", expression.location, bound, condition)
                bound.dependencies += (identifier,)
                bound.assume("requires", condition)
        state.dependencies = tuple(
            dict.fromkeys((*state.dependencies, *bound.dependencies, *self.required[callee.name]))
        )
        for type_ in sorted(self.effects[callee.name]):
            state.memory[type_] = self.fresh("memory", ir.ArrayType(type_), expression.location)
        for identifier in sorted(self.writes[callee.name]):
            symbol = self.globals[identifier].symbol
            changed = self.fresh(symbol.name, symbol.type, expression.location)
            assert isinstance(symbol.type, ir.ScalarType)
            state.values[identifier] = bound.values[identifier] = changed
            state.assume("type-domain", vc._range(changed, symbol.type))
        bound.memory = state.memory.copy()
        bound.hypotheses = state.hypotheses
        bound.dependencies = state.dependencies
        # By-value parameters may change. Postconditions refer to their final values.
        for statement in walk(callee.body):
            if isinstance(statement, ir.Assign) and isinstance(statement.target, ir.Variable):
                symbol = statement.target.symbol
                if symbol.id in bound.values and symbol.id not in self.globals:
                    bound.values[symbol.id] = self.fresh(symbol.name, symbol.type, expression.location)
        result = self.fresh("result", callee.return_type, expression.location)
        bound.result = result
        state.assume("type-domain", vc._range(result, callee.return_type))
        for contract in callee.contracts:
            if contract.kind is SpecKind.ENSURES:
                state.assume("postcondition", truth(contract.condition, bound))
        return result

    def sequence(self, block: ir.Block, states: list[State], function: ir.Function) -> list[State]:
        for statement in block.statements:
            next_states: list[State] = []
            for state in states:
                next_states.extend(self.statement(statement, state, function))
            states = next_states
            if len(states) > MAX_VC_PATHS:
                raise FrontendError("vc-complexity", "too many structured execution paths", statement.location)
        return states

    def statement(self, statement: ir.Statement, state: State, function: ir.Function) -> list[State]:
        if isinstance(statement, ir.Block):
            return self.sequence(statement, [state], function)
        if isinstance(statement, ir.Local):
            state.values[statement.symbol.id] = self.evaluate(statement.initializer, state)
        elif isinstance(statement, ir.LocalArray):
            self.allocate(statement, state)
        elif isinstance(statement, ir.Assign):
            result = self.evaluate(statement.value, state)
            if isinstance(statement.target, ir.Variable):
                state.values[statement.target.symbol.id] = result
            else:
                self.safety(statement.target, state)
                target = value(statement.target, state)
                assert isinstance(target, vc.Read) and isinstance(statement.target.array.type, ir.ArrayType)
                element = statement.target.array.type.element
                stored = op("store", target.memory, target.address, result)
                state.memory[element] = self.named(stored, element, state, statement.location)
        elif isinstance(statement, ir.Contract):
            self.contract_safety(statement.condition, state)
            condition = truth(statement.condition, state)
            identifier = self.add(
                "assert",
                statement.location,
                state,
                condition,
                dependencies=tuple(dep for dep in state.dependencies if dep not in state.induction),
            )
            state.dependencies += (identifier,)
            state.assume("assert", condition)
        elif isinstance(statement, ir.Return):
            state.result = self.evaluate(statement.value, state)
            for contract in function.contracts:
                if contract.kind is SpecKind.ENSURES:
                    self.contract_safety(contract.condition, state)
                    self.add("postcondition", statement.location, state, truth(contract.condition, state))
            return []
        elif isinstance(statement, ir.If):
            self.safety(statement.condition, state)
            condition = truth(statement.condition, state)
            left, right = state.copy(), state.copy()
            left.assume("guard", condition)
            right.assume("guard", op("!", condition))
            return self.sequence(statement.then_body, [left], function) + (
                self.sequence(statement.else_body, [right], function) if statement.else_body else [right]
            )
        elif isinstance(statement, (ir.Break, ir.Continue)):
            if not self.exits:
                raise FrontendError("vc-subset", "break or continue outside a loop", statement.location)
            self.exits[-1][isinstance(statement, ir.Continue)].append(state)
            return []  # Nothing after it runs on this path; the loop takes the state up again.
        elif isinstance(statement, (ir.While, ir.For)):
            if isinstance(statement, ir.For) and statement.initializer:
                self.statement(statement.initializer, state, function)
            return self.loop(statement, state, function)
        else:
            raise FrontendError("vc-subset", "unsupported statement", statement.location)
        return [state]

    def allocate(self, statement: ir.LocalArray, state: State) -> None:
        """A local array: a new object (C11 6.2.4) with its initial contents (6.7.9p21).

        It gets an address of its own that overlaps no array of the same element type that exists here; arrays
        of other element types live in a different memory. The listed values are stored; the elements after
        them are zero, which is stated for arrays of at most `ir.EXACT_LOCAL_ARRAY` elements and otherwise
        left unknown (a weaker, still true, description).
        """
        symbol = statement.symbol
        assert isinstance(symbol.type, ir.ArrayType)
        element = symbol.type.element
        base = self.fresh(f"base_{symbol.name}", ir.ScalarType.LONG, statement.location)
        size = vc.Integer(statement.size)
        for other, other_base in state.bases.items():
            if self.elements.get(other) == element:
                apart = op(
                    "||",
                    op("<=", op("+", base, size), other_base),
                    op("<=", op("+", other_base, state.lengths[other]), base),
                )
                state.assume("allocation", apart)
        self.elements[symbol.id] = element
        state.bases[symbol.id], state.lengths[symbol.id] = base, size
        stated = statement.size if statement.size <= ir.EXACT_LOCAL_ARRAY else len(statement.initial)
        memory = state.memory[element]
        for index in range(stated):
            initial = value(statement.initial[index], state) if index < len(statement.initial) else vc.Integer(0)
            memory = op("store", memory, op("+", base, vc.Integer(index)), initial)
        state.memory[element] = self.named(memory, element, state, statement.location)

    def named(self, memory: vc.Term, element: ir.ScalarType, state: State, location: SourceLocation) -> vc.Term:
        """Give a memory that has grown through many writes a name of its own.

        Every later read repeats the memory it reads from, so a chain of writes would make formulas grow with
        the square of its length. Past `MEMORY_NAMING` the chain is replaced by a fresh memory that is stated
        equal to it: the same facts, written once. Shorter chains are left as they are.
        """
        if vc._measure(memory) <= MEMORY_NAMING:
            return memory
        name = self.fresh("memory", ir.ArrayType(element), location)
        state.assume("allocation", op("same-memory", name, memory))
        return name

    def modified(self, block: ir.Block) -> tuple[dict[str, ir.Symbol], set[ir.ScalarType]]:
        scalars: dict[str, ir.Symbol] = {}
        memory: set[ir.ScalarType] = set()
        for statement in walk(block):
            if isinstance(statement, ir.Assign):
                if isinstance(statement.target, ir.Variable):
                    scalars[statement.target.symbol.id] = statement.target.symbol
                else:
                    assert isinstance(statement.target.array.type, ir.ArrayType)
                    memory.add(statement.target.array.type.element)
            for expression in statement_expressions(statement):
                for call in calls(expression):
                    if call.function not in self.effects:
                        raise FrontendError("vc-expression", "callee effects are unavailable", call.location)
                    memory.update(self.effects[call.function])
                    # Sorted: the order decides how the loop's fresh symbols are numbered, and the order of a set
                    # of names differs from one process to the next.
                    for identifier in sorted(self.writes[call.function]):
                        scalars[identifier] = self.globals[identifier].symbol
        return scalars, memory

    def loop(self, loop: ir.While | ir.For, state: State, function: ir.Function) -> list[State]:
        if loop.invariant is None:
            raise FrontendError("vc-invariant", "a loop invariant is required to generate dependent VCs", loop.location)
        invariant = loop.invariant.condition
        self.contract_safety(invariant, state)
        # Outer induction is a premise when validating a nested loop, not a circular certificate.
        validation_deps = tuple(dep for dep in state.dependencies if dep not in state.induction)
        symbols = {item.symbol.id: item.symbol for item in walk(function.body) if isinstance(item, ir.Local)}
        observations = tuple((symbols[key], term) for key, term in state.values.items() if key in symbols)
        entry = self.add(
            "entry",
            loop.invariant.location,
            state,
            truth(invariant, state),
            dependencies=validation_deps,
            observations=observations,
        )
        head = state.copy()
        body = loop.body
        if isinstance(loop, ir.For) and loop.update:
            body = replace(body, statements=(*body.statements, loop.update))
        modified, memory = self.modified(body)
        for key, symbol in modified.items():
            if key in head.values:
                fresh = self.fresh(symbol.name, symbol.type, symbol.location)
                head.values[key] = fresh
                assert isinstance(symbol.type, ir.ScalarType)
                head.assume("type-domain", vc._range(fresh, symbol.type))
        for type_ in sorted(memory):
            head.memory[type_] = self.fresh("memory", ir.ArrayType(type_), loop.location)
        head.assume("invariant", truth(invariant, head))
        guard = truth(loop.condition, head) if loop.condition else vc.TRUE
        induction = head.copy()
        induction.hypotheses = tuple(
            replace(h, kind="induction-hypothesis") if h.kind == "invariant" else h for h in induction.hypotheses
        )
        induction.assume("guard", guard)
        preservation = self.add(
            "preservation", loop.invariant.location, induction, vc.TRUE, dependencies=validation_deps
        )
        head.dependencies += (entry, preservation)
        after = head.copy()
        after.assume("guard", op("!", guard))
        if loop.condition:
            self.safety(loop.condition, head)
        active = head.copy()
        active.induction += (entry, preservation)
        active.assume("guard", guard)
        premise_count = len(active.hypotheses)
        induction_ids = active.induction
        # C11 6.8.6.2/6.8.6.3: `continue` ends the iteration and the update of a `for` still runs; `break` leaves
        # the loop at once, so its state goes on after the loop without passing the condition or the invariant.
        self.exits.append(([], []))
        endings = self.sequence(loop.body, [active], function)
        breaks, continues = self.exits.pop()
        endings = endings + continues
        if isinstance(loop, ir.For) and loop.update:
            if not endings:
                # Every path through the body leaves the loop, so the update never runs. Its operations still
                # stand in the emitted C: give them their obligations, under a premise that cannot hold.
                unreachable = active.copy()
                unreachable.assume("guard", vc.Boolean(False))
                self.statement(loop.update, unreachable, function)
            endings = [later for ending in endings for later in self.statement(loop.update, ending, function)]
        for left in breaks:
            left.induction = head.induction  # Outside the loop its invariant is a proved fact, as for `after`.
        goals: list[vc.Term] = []
        dependencies = list(validation_deps)
        for ending in endings:
            self.contract_safety(invariant, ending)
            extra = ending.hypotheses[premise_count:]
            goals.append(vc._implies(vc._and(*(h.formula for h in extra)), truth(invariant, ending)))
            dependencies.extend(dep for dep in ending.dependencies if dep not in induction_ids)
        item = self.obligations[int(preservation)]
        goal = vc._and(*goals)
        vc._measure(goal)
        self.obligations[int(preservation)] = replace(item, goal=goal, dependencies=tuple(dict.fromkeys(dependencies)))
        return [after, *breaks]

    def entry_state(self, function: ir.Function) -> State:
        """Symbolic state when `function` is entered: globals, fresh memory, parameters with their domains."""
        state = State()
        for item in self.program.globals:
            symbol = item.symbol
            assert isinstance(symbol.type, ir.ScalarType)
            state.values[symbol.id] = vc.Reference(symbol)
            state.assume("type-domain", vc._range(vc.Reference(symbol), symbol.type))
            if function.name == ENTRY:  # Nothing has run before the program entry.
                state.assume("requires", op("==", vc.Reference(symbol), value(item.initial, state)))
        for type_ in self.memories:
            state.memory[type_] = self.fresh("memory", ir.ArrayType(type_), function.location)
        for parameter in function.parameters:
            symbol = parameter.symbol
            if isinstance(symbol.type, ir.ArrayType):
                self.elements[symbol.id] = symbol.type.element
                state.bases[symbol.id] = self.fresh(f"base_{symbol.name}", ir.ScalarType.LONG, symbol.location)
                assert parameter.length is not None
                state.lengths[symbol.id] = vc.Reference(parameter.length)
            else:
                state.values[symbol.id] = vc.Reference(symbol)
                state.assume("type-domain", vc._range(vc.Reference(symbol), symbol.type))
        return state

    def external(self, function: ir.Function) -> None:
        """Record the query that asks whether the contract of a declared-only function can be met."""
        state = self.entry_state(function)
        for contract in function.contracts:
            if contract.kind is SpecKind.REQUIRES:
                state.assume("requires", truth(contract.condition, state))
        after = state.copy()
        written = []

        def domain(type_: ir.ScalarType, memory: vc.Term, chosen: bool) -> tuple[vc.Term, vc.Term, vc.Term, bool]:
            boolean = type_ is ir.ScalarType.BOOL
            low: vc.Term = vc.Integer(0) if boolean else vc.Limit(type_, "MIN")
            high: vc.Term = vc.Integer(1) if boolean else vc.Limit(type_, "MAX")
            return memory, low, high, chosen

        domains = [domain(type_, memory, False) for type_, memory in sorted(state.memory.items())]
        for type_ in sorted(self.effects[function.name]):
            after.memory[type_] = self.fresh("memory", ir.ArrayType(type_), function.location)
            written.append((after.memory[type_], state.memory[type_]))
            domains.append(domain(type_, after.memory[type_], True))
        frozen = tuple(
            (
                state.memory[parameter.symbol.type.element],
                after.memory[parameter.symbol.type.element],
                state.bases[parameter.symbol.id],
                state.lengths[parameter.symbol.id],
            )
            for parameter in function.parameters
            if isinstance(parameter.symbol.type, ir.ArrayType)
            and parameter.symbol.const
            and parameter.symbol.type.element in self.effects[function.name]
        )
        result = self.fresh("result", function.return_type, function.location)
        after.result = result
        promised = [c.condition for c in function.contracts if c.kind is SpecKind.ENSURES]
        guarantees = (vc._range(result, function.return_type), *(truth(condition, after) for condition in promised))
        reads = any(isinstance(node, ir.Index) for condition in promised for node in _nodes(condition))
        self.external_checks.append(
            vc.ExternalCheck(
                self.context_id,
                function.name,
                function.location,
                state.hypotheses,
                result,
                guarantees,
                reads,
                tuple(written),
                frozen,
                tuple(domains),
            )
        )

    def function(self, function: ir.Function) -> None:
        if function.external:
            # Declared only: callers check its REQUIRES and assume its ENSURES. It may write the arrays it is
            # given; it cannot name this unit's globals, which have internal linkage in the emitted C.
            self.required[function.name] = ()
            self.writes[function.name] = frozenset()
            self.effects[function.name] = {
                parameter.symbol.type.element
                for parameter in function.parameters
                if isinstance(parameter.symbol.type, ir.ArrayType) and not parameter.symbol.const
            }
            self.external(function)
            return
        state = self.entry_state(function)
        start = len(self.obligations)
        for contract in function.contracts:
            if contract.kind is SpecKind.REQUIRES:
                self.contract_safety(contract.condition, state)
                state.assume("requires", truth(contract.condition, state))
        self.entry_checks.append(vc.EntryCheck(self.context_id, function.name, function.location, state.hypotheses))
        self.sequence(function.body, [state], function)
        self.required[function.name] = tuple(
            item.id for item in self.obligations[start:] if item.category == "required"
        )
        # What a caller can observe: writes through the arrays the function was given, and what its callees
        # write. A write to an array the function declared itself ends with the function.
        own = {item.symbol.id for item in walk(function.body) if isinstance(item, ir.LocalArray)}
        visible: set[ir.ScalarType] = set()
        for item in walk(function.body):
            if isinstance(item, ir.Assign) and isinstance(item.target, ir.Index) and item.target.array.id not in own:
                assert isinstance(item.target.array.type, ir.ArrayType)
                visible.add(item.target.array.type.element)
            for expression in statement_expressions(item):
                for call in calls(expression):
                    visible.update(self.effects[call.function])
        self.effects[function.name] = visible
        self.writes[function.name] = frozenset(key for key in self.modified(function.body)[0] if key in self.globals)

    def run(self) -> vc.VCReport:
        visiting: set[str] = set()

        def visit(function: ir.Function) -> None:
            if function.name in self.required:
                return
            if function.name in visiting:
                raise FrontendError("vc-call-cycle", "recursive verification is unsupported", function.location)
            visiting.add(function.name)
            for statement in walk(function.body):
                for expression in statement_expressions(statement):
                    for call in calls(expression):
                        callee = self.functions.get(call.function)
                        if callee is None:
                            raise FrontendError("vc-expression", "callee definition is missing", call.location)
                        visit(callee)
            self.function(function)
            visiting.remove(function.name)

        for function in self.program.functions:
            visit(function)
        return self.finish()

    def finish(self) -> vc.VCReport:
        finished: dict[str, vc.Obligation] = {}

        def resolve(identifier: str, visiting: frozenset[str] = frozenset()) -> vc.Obligation:
            if identifier in visiting:
                raise FrontendError(
                    "vc-dependency", "cyclic proof dependency", self.obligations[int(identifier)].location
                )
            if identifier not in finished:
                item = self.obligations[int(identifier)]
                dependencies = tuple(resolve(dep, visiting | {identifier}).id for dep in item.dependencies)
                canonical = replace(item, dependencies=dependencies)
                finished[identifier] = replace(canonical, id=f"{item.kind}:{vc._digest(canonical)}")
            return finished[identifier]

        return vc.VCReport(
            self.context_id,
            ", ".join(f.name for f in self.program.functions),
            tuple(resolve(item.id) for item in self.obligations),
            entry_checks=tuple(self.entry_checks),
            external_checks=tuple(self.external_checks),
        )
