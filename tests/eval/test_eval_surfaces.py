"""E12: a certified, a refused and a rejected program through the three paths."""

import pytest

from pfc2_eval import surfaces

HEADER = '#include "pfc.h"\n'
FILL = (
    "long fill(long n, long a[n])\n{\n    for (long i = 0; i BOUND n; i++) {\n"
    "        a[i] = 0;\n    }\n    return 0;\n}\n"
)


@pytest.mark.integration
@pytest.mark.parametrize(
    ("text", "verdict"),
    [
        (HEADER + FILL.replace("BOUND", "<"), "certified"),
        (HEADER + FILL.replace("BOUND", "<="), "refused"),  # Writes a[n].
        (HEADER + "long f(long n)\n{\n    goto out;\n    return n;\n}\n", "rejected"),  # Outside the language.
    ],
)
def test_the_three_paths_agree(text: str, verdict: str) -> None:
    row = surfaces.compare("t.c", text)
    assert row == {"program": "t.c", "command_line": verdict, "browser_same": True, "editor_same": True, "detail": None}


@pytest.mark.integration
def test_a_program_that_cannot_be_judged_in_time_is_a_row_that_compares_nothing() -> None:
    from pfc2_eval import generate

    row = surfaces.within_budget("g339.c", generate.program(339).text, budget=1)  # Development seed; needs minutes.
    assert row["command_line"] == "not-judged" and "nothing was compared" in str(row["detail"])


@pytest.mark.parametrize(
    ("message", "swallowed"), [("argument 1: _OutOfTime: ", True), ("argument 1: TypeError: x", False)]
)
def test_a_timer_that_fires_inside_a_solver_binding_call_is_still_out_of_time(
    monkeypatch: pytest.MonkeyPatch, message: str, swallowed: bool
) -> None:
    """ctypes reports the timer's exception as its own ArgumentError, by name (amendments 25 and 27)."""
    import ctypes

    def wrapped(*arguments: object, **options: object) -> object:
        raise ctypes.ArgumentError(message)

    monkeypatch.setattr(surfaces, "compare", wrapped)
    if not swallowed:
        with pytest.raises(ctypes.ArgumentError):
            surfaces.within_budget("t.c", HEADER, budget=600)
        return
    row = surfaces.within_budget("t.c", HEADER, budget=600)
    assert row["command_line"] == "not-judged" and "nothing was compared" in str(row["detail"])
