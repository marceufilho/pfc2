"""Structured frontend diagnostics without echoing arbitrary source text."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SourceLocation:
    file: str
    line: int = 1
    column: int | None = None

    def __str__(self) -> str:
        suffix = f":{self.column}" if self.column is not None else ""
        return f"{self.file}:{self.line}{suffix}"


@dataclass(frozen=True)
class Diagnostic:
    rule: str
    message: str
    location: SourceLocation


class FrontendError(Exception):
    """An expected source, preprocessing or syntax failure."""

    def __init__(self, rule: str, message: str, location: SourceLocation) -> None:
        self.diagnostic = Diagnostic(rule, message, location)
        super().__init__(f"{location}: [{rule}] {message}")
