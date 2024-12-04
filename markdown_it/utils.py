from __future__ import annotations

from collections.abc import MutableMapping
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, TypedDict

if TYPE_CHECKING:
    from typing_extensions import NotRequired


EnvType = MutableMapping[str, Any]  # note: could use TypeAlias in python 3.10
"""Type for the environment sandbox used in parsing and rendering,
which stores mutable variables for use by plugins and rules.
"""


class OptionsType(TypedDict):
    """Options for parsing."""

    maxNesting: int
    """Internal protection, recursion limit."""
    html: bool
    """Enable HTML tags in source."""
    linkify: bool
    """Enable autoconversion of URL-like texts to links."""
    typographer: bool
    """Enable smartquotes and replacements."""
    quotes: str
    """Quote characters."""
    xhtmlOut: bool
    """Use '/' to close single tags (<br />)."""
    breaks: bool
    """Convert newlines in paragraphs into <br>."""
    langPrefix: str
    """CSS language prefix for fenced blocks."""
    highlight: Callable[[str, str, str], str] | None
    """Highlighter function: (content, lang, attrs) -> str."""
    store_labels: NotRequired[bool]
    """Store link label in link/image token's metadata (under Token.meta['label']).

    This is a Python only option, and is intended for the use of round-trip parsing.
    """
    inline_definitions: NotRequired[bool]


class PresetType(TypedDict):
    """Preset configuration for markdown-it."""

    options: OptionsType
    """Options for parsing."""
    components: MutableMapping[str, MutableMapping[str, list[str]]]
    """Components for parsing and rendering."""


def read_fixture_file(path: str | Path) -> list[list[Any]]:
    text = Path(path).read_text(encoding="utf-8")
    tests = []
    section = 0
    last_pos = 0
    lines = text.splitlines(keepends=True)
    for i in range(len(lines)):
        if lines[i].rstrip() == ".":
            if section == 0:
                tests.append([i, lines[i - 1].strip()])
                section = 1
            elif section == 1:
                tests[-1].append("".join(lines[last_pos + 1 : i]))
                section = 2
            elif section == 2:
                tests[-1].append("".join(lines[last_pos + 1 : i]))
                section = 0

            last_pos = i
    return tests
