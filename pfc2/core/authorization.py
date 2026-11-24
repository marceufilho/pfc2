"""Conservative check deletion for trusted in-process solver results.

No deserialized reports are accepted by the CLI. Matching hashes detects stale
contexts, not a malicious Python caller able to fabricate a solver verdict.
"""

from dataclasses import dataclass

from pfc2.core import ir, smt, vc
from pfc2.core.config import MAX_SOLVER_TIMEOUT_MS
from pfc2.core.diagnostics import SourceLocation
from pfc2.core.target import Target
from pfc2.core.wp import walk


def expressions(expression: ir.Expr) -> tuple[ir.Expr, ...]:
    """Visit an expression using the canonical VC child relation."""
    return (expression,) + tuple(node for child in vc._children(expression) for node in expressions(child))


def statements(block: ir.Block) -> tuple[ir.Statement, ...]:
    """Use the canonical structured statement traversal."""
    return walk(block)


def arithmetic_locations(program: ir.Program) -> set[SourceLocation]:
    """Backward closure through scalars and possibly aliased memory influencing safety.

    Calls currently use the conservative whole-program arithmetic closure. Data-only
    accumulation in kernels remains reported separately when it cannot affect guards.
    """
    assignments: list[tuple[ir.Symbol, ir.Expr]] = []
    writes: list[tuple[ir.ArrayType, ir.Expr]] = []
    roots: list[ir.Expr] = []
    all_expressions: list[ir.Expr] = []
    for function in program.functions:
        roots.extend(contract.condition for contract in function.contracts)
        for statement in statements(function.body):
            if isinstance(statement, (ir.While, ir.For, ir.If)):
                if statement.condition:
                    roots.append(statement.condition)
                    all_expressions.append(statement.condition)
                if isinstance(statement, (ir.While, ir.For)) and statement.invariant:
                    roots.append(statement.invariant.condition)
            elif isinstance(statement, ir.Contract):
                roots.append(statement.condition)
            elif isinstance(statement, ir.Local):
                assignments.append((statement.symbol, statement.initializer))
                all_expressions.append(statement.initializer)
            elif isinstance(statement, ir.Assign):
                all_expressions.append(statement.value)
                if isinstance(statement.target, ir.Variable):
                    assignments.append((statement.target.symbol, statement.value))
                else:
                    assert isinstance(statement.target.array.type, ir.ArrayType)
                    writes.append((statement.target.array.type, statement.value))
                    roots.append(statement.target.index)
                    all_expressions.append(statement.target.index)
            elif isinstance(statement, ir.Return):
                all_expressions.append(statement.value)
                if any(c.kind.value == "ENSURES" for c in function.contracts):
                    roots.append(statement.value)
    nodes = tuple(node for expression in all_expressions for node in expressions(expression))
    if any(isinstance(node, ir.Call) for node in nodes):
        return {node.location for node in nodes}
    for node in nodes:
        if isinstance(node, ir.Index):
            roots.append(node.index)
        elif isinstance(node, ir.Binary) and node.operator in {"/", "%"}:
            roots.extend((node.left, node.right))
    pending_assignments = assignments.copy()
    pending_writes = writes.copy()
    while True:
        relevant = tuple(node for root in roots for node in expressions(root))
        bindings = {node.symbol.id for node in relevant if isinstance(node, ir.Variable)}
        memory = {node.array.type for node in relevant if isinstance(node, ir.Index)}
        selected = [(symbol, expr) for symbol, expr in pending_assignments if symbol.id in bindings]
        stores = [(type_, expr) for type_, expr in pending_writes if type_ in memory]
        if not selected and not stores:
            return {node.location for node in relevant}
        roots.extend(expr for _, expr in (*selected, *stores))
        pending_assignments = [item for item in pending_assignments if item not in selected]
        pending_writes = [item for item in pending_writes if item not in stores]


@dataclass(frozen=True)
class Authorization:
    """Per-obligation admission under one exactly matched evidence report.

    `allowed` is the whole-unit verdict (every required obligation admitted; unproved
    arithmetic is covered by its retained overflow trap). `proved` lists obligations
    individually admitted with their dependency closure, so an independent failure
    elsewhere does not retain a guard whose own proof is complete (ADR-0023).
    Unadmitted internal call preconditions block every optimization: a callee's own
    proofs assume its contract and do not include incoming call obligations (ADR-0026).
    """

    allowed: bool
    reason: str
    proved: tuple[str, ...] = ()
    arithmetic_proved: bool = False


def authorize(
    program: ir.Program, conditions: vc.VCReport, target: Target, proof: smt.CheckReport | None
) -> Authorization:
    """Recompute admission from canonical obligations; never trust summary flags."""
    locations = arithmetic_locations(program)
    arithmetic = tuple(
        item.id for item in conditions.obligations if item.kind == "overflow" and item.location in locations
    )

    def reject(reason: str) -> Authorization:
        return Authorization(False, reason)

    if proof is None:
        return reject("missing proof report")
    if (
        proof.context_id != conditions.context_id
        or proof.function != conditions.function
        or proof.target != target
        or proof.encoding != smt.ENCODING
        or proof.vc_model != conditions.model
        or proof.solver_version != smt.solver_version()
        or type(proof.timeout_ms) is not int
        or not 1 <= proof.timeout_ms <= MAX_SOLVER_TIMEOUT_MS
    ):
        return reject("proof context, target or solver settings mismatch")
    if len(proof.entry_results) != len(conditions.entry_checks):
        return reject("missing or extra entry consistency results")
    for query, entry_result in zip(conditions.entry_checks, proof.entry_results, strict=True):
        if entry_result.query != query or entry_result.query_id != smt.entry_query_id(
            query, target, proof.timeout_ms, proof.solver_version
        ):
            return reject("entry consistency identity mismatch")
        if entry_result.status != "sat":
            return reject(f"entry consistency not established: {entry_result.status}")
    expected = {item.id: item for item in conditions.obligations}
    results = {item.obligation.id: item for item in proof.results}
    if len(results) != len(proof.results) or results.keys() != expected.keys():
        return reject("missing, duplicate or extra proof results")
    for identifier, result in results.items():
        if result.obligation != expected[identifier] or result.query_id != smt.query_id(
            expected[identifier], target, proof.timeout_ms, proof.solver_version
        ):
            return reject("obligation or query identity mismatch")

    counted = smt.admitted(
        {identifier for identifier, result in results.items() if result.status == "proved"},
        {identifier: item.dependencies for identifier, item in expected.items()},
    )
    admitted = tuple(identifier for identifier in expected if identifier in counted)
    if any(item.kind == "call-precondition" and item.id not in admitted for item in conditions.obligations):
        return reject("internal call precondition or its dependencies not proved")
    arithmetic_proved = all(identifier in admitted for identifier in arithmetic)
    if not all(item.id in admitted for item in conditions.obligations if item.category == "required"):
        reason = "required proof or invariant dependency not proved"
        return Authorization(False, reason, admitted, arithmetic_proved)
    # PFC2 (ADR-0061): unproved arithmetic no longer retains guards. Every `+ - *` and unary `-` whose overflow
    # obligation is not admitted keeps its trap in the emitted C, so an execution either stops at that trap or has
    # computed exactly the mathematical values the proofs talk about; a guard proved over mathematical integers is
    # therefore redundant on every execution that reaches it. `arithmetic_proved` is still reported.
    return Authorization(True, "exact proofs and invariant admission", admitted, arithmetic_proved)
