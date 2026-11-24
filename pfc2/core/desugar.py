"""Everyday C spelled out in the explicit subset, on the parsed tree and before validation.

    i++; ++i; i--; --i;     ->  i = i + 1;  /  i = i - 1;
    x += e;  (-=, *=, /=)   ->  x = x + e;
    f(x);                   ->  long pfc2_tK = f(x);
    y = f(a) + g(b);        ->  long pfc2_t1 = f(a); long pfc2_t2 = g(b); y = pfc2_t1 + pfc2_t2;

A call that is not the whole initializer, assigned value or returned value is evaluated first into
a fresh local. The calls of one statement run left to right and before its other operands are
read (an order C permits: operand evaluation order is unspecified); the proof is about that order.
Where C makes the evaluation conditional or repeated (the right operand of `&&`/`||`, loop
conditions and updates) the call is refused instead of moved, so meaning never changes.

A call in the index of `a[f()] += e` or `a[f()]++` is evaluated once, as in C. A call inside
`assert` is refused in a function that is emitted: an ordinary compiler never evaluates an assert,
so moving the call out would make the checked program do something the source does not. In a law,
which is proved and never emitted, the call is part of the property and is moved like any other.
"""

# pycparser node constructors and children() carry no annotations.
# mypy: disable-error-code="no-untyped-call"

import copy
from typing import NoReturn

from pycparser import c_ast

from pfc2.core.diagnostics import FrontendError, SourceLocation

TEMPORARY = "pfc2_"
_STEP = {"p++": "+", "++": "+", "p--": "-", "--": "-"}
_COMPOUND = {"+=": "+", "-=": "-", "*=": "*", "/=": "/", "%=": "%"}
_ORDER = "the call would run conditionally or repeatedly here; assign it to a variable first"


def _location(node: c_ast.Node, filename: str) -> SourceLocation:
    coord = node.coord
    return SourceLocation(filename) if coord is None else SourceLocation(coord.file, coord.line, coord.column)


def _is_call(node: c_ast.Node) -> bool:
    return (
        isinstance(node, c_ast.FuncCall)
        and isinstance(node.name, c_ast.ID)
        and not node.name.name.startswith("__spec_")
    )


def _has_call(node: c_ast.Node | None) -> bool:
    if node is None:
        return False
    return _is_call(node) or any(_has_call(child) for _, child in node.children())


class _Function:
    def __init__(self, filename: str, returns: dict[str, list[str]], ghost: bool = False) -> None:
        self.filename = filename
        self.returns = returns
        self.ghost = ghost  # A law: never emitted, so a call inside `assert` may be moved out.
        self.serial = 0

    def fail(self, rule: str, message: str, node: c_ast.Node) -> NoReturn:
        raise FrontendError(rule, message, _location(node, self.filename))

    def temporary(self, call: c_ast.FuncCall) -> tuple[c_ast.Decl, c_ast.ID]:
        self.serial += 1
        name = f"{TEMPORARY}t{self.serial}"
        names = list(self.returns.get(call.name.name, ["long"]))
        type_ = c_ast.TypeDecl(name, [], None, c_ast.IdentifierType(names, call.coord), call.coord)
        return c_ast.Decl(name, [], [], [], [], type_, call, None, call.coord), c_ast.ID(name, call.coord)

    def lift(self, node: c_ast.Node, prefix: list[c_ast.Node], *, whole: bool = False) -> c_ast.Node:
        """Replace calls inside `node` by fresh locals appended to `prefix`; `whole` keeps a top-level call."""
        if _is_call(node):
            assert isinstance(node, c_ast.FuncCall)
            if node.args:
                node.args.exprs = [self.lift(argument, prefix) for argument in node.args.exprs]
            if whole:
                return node
            declaration, name = self.temporary(node)
            prefix.append(declaration)
            return name
        if isinstance(node, c_ast.BinaryOp) and node.op in {"&&", "||"}:
            node.left = self.lift(node.left, prefix)
            if _has_call(node.right):
                self.fail("subset-call-order", _ORDER, node.right)
            return node
        for name, child in node.children():
            lifted = self.lift(child, prefix)
            field, separator, index = name.partition("[")
            if separator:
                getattr(node, field)[int(index[:-1])] = lifted
            else:
                setattr(node, field, lifted)
        return node

    def once(self, target: c_ast.Node, prefix: list[c_ast.Node]) -> c_ast.Node:
        """The value read by `target op= e`: the same place, with its index evaluated once.

        An index that is more than a name or a number goes into a fresh local first, so a call in it runs
        once and its arithmetic is one operation, not two. The read is a different operation from the write
        at the same place, so it is given the column after it, where no other operation can start.
        """
        if not isinstance(target, c_ast.ArrayRef):
            return copy.deepcopy(target)
        if not isinstance(target.subscript, (c_ast.ID, c_ast.Constant)):
            index = self.lift(target.subscript, prefix)
            self.serial += 1
            name = f"{TEMPORARY}t{self.serial}"
            type_ = c_ast.TypeDecl(name, [], None, c_ast.IdentifierType(["long"], index.coord), index.coord)
            prefix.append(c_ast.Decl(name, [], [], [], [], type_, index, None, index.coord))
            target.subscript = c_ast.ID(name, index.coord)
        read = copy.deepcopy(target)
        if target.coord is not None and target.coord.column is not None:
            read.coord = copy.copy(target.coord)
            read.coord.column = target.coord.column + 1
        return read

    def assignment(self, node: c_ast.Node, prefix: list[c_ast.Node]) -> c_ast.Node:
        """The explicit assignment for `x op= e`, `x++` and `x--`; other nodes are returned unchanged."""
        if isinstance(node, c_ast.UnaryOp) and node.op in _STEP:
            one = c_ast.Constant("int", "1", node.coord)
            value = c_ast.BinaryOp(_STEP[node.op], self.once(node.expr, prefix), one, node.coord)
            return c_ast.Assignment("=", node.expr, value, node.coord)
        if isinstance(node, c_ast.Assignment) and node.op in _COMPOUND:
            value = c_ast.BinaryOp(_COMPOUND[node.op], self.once(node.lvalue, prefix), node.rvalue, node.coord)
            return c_ast.Assignment("=", node.lvalue, value, node.coord)
        return node

    def body(self, node: c_ast.Node | None) -> c_ast.Node | None:
        """A sub-statement; it becomes a block when statements were added before it."""
        if node is None or isinstance(node, c_ast.Compound):
            return self.block(node) if node is not None else None
        statements = self.statement(node)
        return statements[0] if len(statements) == 1 else c_ast.Compound(statements, node.coord)

    def block(self, node: c_ast.Compound) -> c_ast.Compound:
        items: list[c_ast.Node] = []
        for item in node.block_items or []:
            items.extend(self.statement(item))
        node.block_items = items
        return node

    def statement(self, node: c_ast.Node) -> list[c_ast.Node]:
        prefix: list[c_ast.Node] = []
        node = self.assignment(node, prefix)
        if isinstance(node, c_ast.Compound):
            return [self.block(node)]
        if isinstance(node, c_ast.Decl):
            if node.init is not None:
                node.init = self.lift(node.init, prefix, whole=True)
        elif isinstance(node, c_ast.Assignment):
            node.lvalue = self.lift(node.lvalue, prefix)
            node.rvalue = self.lift(node.rvalue, prefix, whole=isinstance(node.lvalue, c_ast.ID))
        elif _is_call(node):
            self.lift(node, prefix)
            return prefix
        elif isinstance(node, c_ast.FuncCall):
            if isinstance(node.name, c_ast.ID) and node.name.name == "__spec_assert" and node.args:
                if _has_call(node.args) and not self.ghost:
                    self.fail(
                        "assert-call",
                        "an assert is proved and never run, so it cannot call a function; "
                        "assign the call to a variable first, or state the property in a law",
                        node,
                    )
                node.args.exprs = [self.lift(argument, prefix) for argument in node.args.exprs]
        elif isinstance(node, c_ast.Return):
            if node.expr is not None:
                node.expr = self.lift(node.expr, prefix, whole=True)
        elif isinstance(node, c_ast.If):
            node.cond = self.lift(node.cond, prefix)
            node.iftrue, node.iffalse = self.body(node.iftrue), self.body(node.iffalse)
        elif isinstance(node, c_ast.While):
            if _has_call(node.cond):
                self.fail("subset-call-order", _ORDER, node.cond)
            node.stmt = self.body(node.stmt)
        elif isinstance(node, c_ast.For):
            if isinstance(node.init, c_ast.DeclList):
                for declaration in node.init.decls:
                    if declaration.init is not None:
                        declaration.init = self.lift(declaration.init, prefix, whole=True)
            elif node.init is not None:
                node.init = self.assignment(node.init, prefix)
                if isinstance(node.init, c_ast.Assignment):
                    node.init.lvalue = self.lift(node.init.lvalue, prefix)
                    node.init.rvalue = self.lift(node.init.rvalue, prefix, whole=isinstance(node.init.lvalue, c_ast.ID))
            for part in (node.cond, node.next):
                if part is not None and _has_call(part):
                    self.fail("subset-call-order", _ORDER, part)
            if node.next is not None:
                moved: list[c_ast.Node] = []
                node.next = self.assignment(node.next, moved)
                if moved:  # The index would need a temporary, and an update has no place to declare one.
                    self.fail(
                        "subset-for-update",
                        "this update needs a computed index twice; write it as the last statement of the body",
                        node.next,
                    )
            node.stmt = self.body(node.stmt)
        return [*prefix, node]


def _reserved(node: c_ast.Node, filename: str) -> None:
    name = getattr(node, "name", None) if isinstance(node, (c_ast.Decl, c_ast.ID)) else None
    if isinstance(name, str) and name.startswith(f"{TEMPORARY}t"):
        raise FrontendError("ir-name", f"names starting with {TEMPORARY}t are reserved", _location(node, filename))
    for _, child in node.children():
        _reserved(child, filename)


def desugar(tree: c_ast.FileAST, filename: str, ghost: frozenset[str] = frozenset()) -> c_ast.FileAST:
    """Rewrite a freshly parsed tree in place and return it; `ghost` names the functions that are never emitted."""
    _reserved(tree, filename)
    returns: dict[str, list[str]] = {}
    for node in tree.ext:
        declaration = node.decl if isinstance(node, c_ast.FuncDef) else node
        function = getattr(declaration, "type", None)
        if isinstance(function, c_ast.FuncDecl) and isinstance(function.type, c_ast.TypeDecl):
            if isinstance(function.type.type, c_ast.IdentifierType):
                returns[declaration.name] = function.type.type.names
    for node in tree.ext:
        if isinstance(node, c_ast.FuncDef) and isinstance(node.body, c_ast.Compound):
            _Function(filename, returns, node.decl.name in ghost).block(node.body)
    return tree
