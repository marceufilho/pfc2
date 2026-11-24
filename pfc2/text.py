"""Position-preserving access to preprocessed text, shared by the surface passes."""

import re
from typing import NoReturn

from pfc2.core.diagnostics import FrontendError, SourceLocation

IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
SPACE = " \t\n\r\f\v"
_LINE_MARKER = re.compile(r'#\s*(?:line\s+)?(\d+)\s+"((?:[^"\\]|\\.)*)"')


Shift = tuple[str, int, int, int]  # File, line and column where text was inserted, and how many characters.


def moved(location: SourceLocation, shifts: tuple[Shift, ...]) -> SourceLocation:
    """Where a token of the text a pass read stands in the text it wrote (insertions never add a line)."""
    if location.column is None:
        return location
    added = sum(
        length
        for file, line, column, length in shifts
        if file == location.file and line == location.line and column <= location.column
    )
    return SourceLocation(location.file, location.line, location.column + added)


class SourceText:
    """Text with logical positions that follow line markers."""

    def __init__(self, text: str, filename: str) -> None:
        self.text = text
        self.filename = filename
        self.lines = self._line_table()

    def _line_table(self) -> list[tuple[int, str, int]]:
        """(start offset, file, logical line) of every physical line, following line markers."""
        table = []
        file, line, offset = self.filename, 1, 0
        for physical in self.text.splitlines(keepends=True):
            marker = _LINE_MARKER.match(physical) if physical.startswith("#") else None
            table.append((offset, file, line))
            if marker:
                file = marker.group(2).replace('\\"', '"').replace("\\\\", "\\")
                line = int(marker.group(1))
            elif not physical.startswith("#"):
                line += 1
            offset += len(physical)
        return table

    def locate(self, offset: int) -> SourceLocation:
        low, high = 0, len(self.lines) - 1
        while low < high:
            middle = (low + high + 1) // 2
            if self.lines[middle][0] <= offset:
                low = middle
            else:
                high = middle - 1
        start, file, line = self.lines[low]
        return SourceLocation(file, line, offset - start + 1)

    def shifts(self, insertions: list[tuple[int, str]]) -> tuple[Shift, ...]:
        result = []
        for offset, inserted in insertions:
            assert "\n" not in inserted
            location = self.locate(offset)
            result.append((location.file, location.line, location.column or 1, len(inserted)))
        return tuple(result)

    def fail(self, rule: str, message: str, offset: int) -> NoReturn:
        raise FrontendError(rule, message, self.locate(offset))

    def skip_literal(self, index: int) -> int:
        """Offset just after the string or character literal that starts at `index`."""
        quote = self.text[index]
        index += 1
        while index < len(self.text) and self.text[index] != quote:
            if self.text[index] == "\n":
                return index
            index += 2 if self.text[index] == "\\" else 1
        return index + 1

    def skip_directive(self, index: int) -> int:
        """Offset of the end of the `#` line that starts at `index`."""
        end = self.text.find("\n", index)
        return len(self.text) if end < 0 else end

    def starts_line(self, index: int) -> bool:
        return index == 0 or self.text[index - 1] == "\n"

    def before(self, offset: int) -> int:
        """Offset just after the last character that is not white space before `offset`."""
        while offset > 0 and self.text[offset - 1] in SPACE:
            offset -= 1
        return offset

    def identifier_before(self, offset: int) -> tuple[str, int] | None:
        """The identifier that ends just before `offset`, ignoring white space."""
        end = self.before(offset)
        start = end
        while start > 0 and (self.text[start - 1].isalnum() or self.text[start - 1] == "_"):
            start -= 1
        name = self.text[start:end]
        return (name, start) if IDENTIFIER.fullmatch(name) else None

    def argument(self, word: int, length: int, rule: str, name: str) -> tuple[str, int]:
        """Text between the parentheses that follow the word at `word`, and the offset of the closing one."""
        opening = word + length
        while opening < len(self.text) and self.text[opening] in " \t\n":
            opening += 1
        if opening >= len(self.text) or self.text[opening] != "(":
            self.fail(rule, f"write the predicate in parentheses: {name}(predicate)", word)
        depth, index = 0, opening
        while index < len(self.text):
            character = self.text[index]
            if character == "'":  # A character constant may hold a parenthesis or a quote.
                index = self.skip_literal(index)
                continue
            if character in '"{};#':
                break
            if character == "(":
                depth += 1
            elif character == ")":
                depth -= 1
                if depth == 0:
                    predicate = " ".join(self.text[opening + 1 : index].split())
                    if not predicate:
                        self.fail(rule, f"{name}() needs a predicate", word)
                    return predicate, index
            index += 1
        self.fail(rule, f"unbalanced parentheses in {name}(predicate)", word)
