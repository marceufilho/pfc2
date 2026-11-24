"""Explicit syntax policy and call-graph validation; typed rules reuse lower.py."""

from collections.abc import Callable
from typing import TYPE_CHECKING, NoReturn, cast

from pycparser import c_ast

from pfc2.core.diagnostics import FrontendError, SourceLocation

if TYPE_CHECKING:
    pass

BINARY_OPERATORS = {"+", "-", "*", "/", "%", "<", "<=", ">", ">=", "==", "!=", "&&", "||"}
SYNTAX_NODES = {
    "FuncDef",
    "Decl",
    "TypeDecl",
    "IdentifierType",
    "ArrayDecl",
    "FuncDecl",
    "ParamList",
    "Typename",
    "Compound",
    "DeclList",
    "EmptyStatement",
    "Assignment",
    "While",
    "For",
    "If",
    "Return",
    "Break",
    "Continue",
    "Constant",
    "ID",
    "BinaryOp",
    "UnaryOp",
    "ArrayRef",
    "InitList",
}


def _location(node: c_ast.Node, filename: str) -> SourceLocation:
    coord = node.coord
    if coord is None:
        return SourceLocation(filename)
    return SourceLocation(coord.file, coord.line, coord.column)


def _scalar_type(node: c_ast.Node) -> str | None:
    if isinstance(node, c_ast.TypeDecl) and isinstance(node.type, c_ast.IdentifierType):
        return " ".join(node.type.names)
    return None


def check_node(node: c_ast.Node, filename: str, contract: bool = False) -> None:
    def fail(rule: str, message: str, target: c_ast.Node) -> NoReturn:
        raise FrontendError(rule, message, _location(target, filename))

    name = type(node).__name__
    if contract and (
        isinstance(node, c_ast.Assignment) or isinstance(node, c_ast.UnaryOp) and node.op not in {"+", "-", "!"}
    ):
        fail("contract-effect", "contract expressions must be side-effect free", node)
    if name not in SYNTAX_NODES:
        fail(f"subset-{name.lower()}", f"{name} is outside the supported syntax", node)
    if isinstance(node, c_ast.IdentifierType) and node.names not in [["long"], ["_Bool"], ["void"], ["char"], ["int"]]:
        fail("subset-type", "types are long and _Bool, with char and int as array elements; no unsigned types", node)
    if isinstance(node, c_ast.Constant) and node.type not in {"int", "long int", "char", "string"}:
        fail("subset-literal", "only signed integer literals and character constants are supported", node)
    if isinstance(node, c_ast.BinaryOp) and node.op not in BINARY_OPERATORS:
        fail("subset-operator", "binary operator is outside the supported syntax", node)
    if isinstance(node, c_ast.UnaryOp) and node.op not in {"+", "-", "!"}:
        fail("subset-operator", "unary operator is outside the supported syntax", node)
    if isinstance(node, c_ast.Assignment) and node.op != "=":
        fail("subset-assignment", "use explicit assignment in the supported syntax", node)
    if isinstance(node, c_ast.Decl):
        if _scalar_type(node.type) == "void":
            fail("subset-type", "void is only supported in parameter lists", node)
        if node.storage or node.funcspec or any(qualifier != "const" for qualifier in node.quals):
            fail("subset-declaration", "storage/function specifiers and non-const qualifiers are unsupported", node)
    if isinstance(node, c_ast.FuncDecl) and _scalar_type(node.type) not in {"long", "_Bool"}:
        fail("subset-type", "functions must return long or bool in the supported syntax", node)
    if isinstance(node, c_ast.FuncDef) and node.param_decls:
        fail("subset-function", "old-style function definitions are unsupported", node)


def validate_calls(tree: c_ast.FileAST, filename: str) -> None:
    """Reject external/heap calls and cycles without Python recursion on long call chains."""
    definitions = {node.decl.name: node for node in tree.ext if isinstance(node, c_ast.FuncDef)}
    visible: set[str] = set()
    visible_at: dict[str, frozenset[str]] = {}
    for declaration in tree.ext:
        if isinstance(declaration, c_ast.Decl):
            visible.add(declaration.name)
        elif isinstance(declaration, c_ast.FuncDef):
            visible.add(declaration.decl.name)
            visible_at[declaration.decl.name] = frozenset(visible)
    graph: dict[str, list[tuple[str, c_ast.FuncCall]]] = {name: [] for name in definitions}
    for name, function in definitions.items():
        pending: list[c_ast.Node] = [function.body]
        while pending:
            node = pending.pop()
            if isinstance(node, c_ast.FuncCall):
                assert isinstance(node.name, c_ast.ID)  # Normalizer rejects indirect calls first.
                callee = node.name.name
                if callee in {"malloc", "calloc", "realloc", "free", "alloca"}:
                    raise FrontendError(
                        "subset-heap", "heap allocation and deallocation are excluded", _location(node, filename)
                    )
                if callee not in definitions:
                    raise FrontendError(
                        "subset-call", "calls require a definition in this translation unit", _location(node, filename)
                    )
                if callee not in visible_at[name]:
                    raise FrontendError(
                        "subset-call-declaration", "callee must be declared before use", _location(node, filename)
                    )
                graph[name].append((callee, node))
            children = cast(Callable[[], tuple[tuple[str, c_ast.Node], ...]], node.children)
            pending.extend(child for _, child in reversed(children()))
    complete: set[str] = set()
    for root in graph:
        active: set[str] = set()
        stack: list[tuple[str, int]] = [(root, 0)]
        while stack:
            name, index = stack[-1]
            if name in complete or index == len(graph[name]):
                complete.add(name)
                active.discard(name)
                stack.pop()
                continue
            active.add(name)
            callee, call = graph[name][index]
            stack[-1] = name, index + 1
            if callee in active:
                raise FrontendError(
                    "subset-recursion", "direct and indirect recursion are excluded", _location(call, filename)
                )
            if callee not in complete:
                stack.append((callee, 0))
