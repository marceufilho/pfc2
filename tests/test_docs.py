"""The programs printed in docs get the verdict the page states, and the pages link to files that exist."""

import re
from pathlib import Path

import pytest

from pfc2 import frontend
from pfc2.check import check
from pfc2.core.target import Target

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TARGET = Target("static LP64 layout (test)", "x86_64-pc-linux-gnu", 32, 64)
SNIPPET = re.compile(r"<!-- check: (full|memory|refused) -->\n```c\n(.*?)```", re.DOTALL)
LINK = re.compile(r"\]\(([^)#]+\.md)(?:#[^)]*)?\)")
PAGES = sorted(DOCS.glob("*.md"))
SNIPPETS = [
    (page.name, number, verdict, code)
    for page in PAGES
    for number, (verdict, code) in enumerate(SNIPPET.findall(page.read_text(encoding="utf-8")), 1)
]


def test_the_documentation_set_is_complete_and_its_links_resolve() -> None:
    assert [page.name for page in PAGES] == [
        "01-tour.md",
        "02-language.md",
        "03-proofs.md",
        "04-programs.md",
        "05-commands.md",
        "06-examples.md",
        "07-design.md",
        "08-implementation.md",
        "09-limits.md",
        "10-pfc-and-pfc2.md",
        "11-editor.md",
        "README.md",
    ]
    for page in PAGES:
        for target in LINK.findall(page.read_text(encoding="utf-8")):
            assert (page.parent / target).is_file(), (page.name, target)
    assert len(SNIPPETS) >= 5


def test_every_example_and_test_file_named_in_the_documentation_exists() -> None:
    named = re.compile(r"`((?:examples|tests|pfc2/runtime|pfc2/include)/[A-Za-z0-9_./-]+\.(?:c|h|py|json|txt))`")
    short = re.compile(r"`((?:\d\d_[a-z_]+|console|wrong)/[a-z_]+\.c)`")
    for page in PAGES:
        text = page.read_text(encoding="utf-8")
        for path in named.findall(text):
            assert (ROOT / path).is_file(), (page.name, path)
        for path in short.findall(text):
            assert (ROOT / "examples" / path).is_file(), (page.name, path)


@pytest.mark.integration
@pytest.mark.parametrize("snippet", SNIPPETS, ids=lambda s: f"{s[0]}#{s[1]}-{s[2]}")
def test_a_documented_program_gets_the_documented_verdict(snippet: tuple[str, int, str, str], tmp_path: Path) -> None:
    _, _, verdict, code = snippet
    source = tmp_path / "snippet.c"
    source.write_text(code, encoding="utf-8")
    full = check(frontend.load(source), TARGET)[1]
    memory = check(frontend.load(source), TARGET, level="memory")[1]
    assert (full.accepted, memory.accepted) == {
        "full": (True, True),
        "memory": (False, True),
        "refused": (False, False),
    }[verdict]
