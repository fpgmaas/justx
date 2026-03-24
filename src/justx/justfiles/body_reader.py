from __future__ import annotations

import re
import textwrap
from pathlib import Path


class JustfileBodyReader:
    """Reads recipe bodies directly from justfile source files."""

    def read(self, justfile_path: Path, recipe_name: str) -> list[str]:
        """Read the body of a recipe from a justfile.

        Locates the recipe header line and collects all subsequent indented lines.
        Returns the body lines with leading indentation stripped.

        If the recipe cannot be found or the file cannot be read, returns an empty list.
        """
        try:
            lines = justfile_path.read_text().splitlines()
        except OSError:
            return []

        header_index = self._find_recipe_header(lines, recipe_name)
        if header_index is None:
            return []

        return self._collect_body_lines(lines, header_index + 1)

    @staticmethod
    def _find_recipe_header(lines: list[str], recipe_name: str) -> int | None:
        """Find the line index of a recipe header.

        Handles both regular and quiet recipes (prefixed with @).
        If duplicates exist (via set allow-duplicate-recipes), returns the last match.
        """
        pattern = re.compile(rf"^@?{re.escape(recipe_name)}\b")
        last_match = None
        for index, line in enumerate(lines):
            stripped = line.strip()
            if pattern.match(stripped) and ":" in stripped:
                last_match = index
        return last_match

    @staticmethod
    def _collect_body_lines(lines: list[str], start: int) -> list[str]:
        """Collect indented body lines starting from a given index.

        Body lines are indented with spaces or tabs. Empty lines within the body
        are preserved. The body ends at the first non-empty, non-indented line.
        """
        body = []
        for line in lines[start:]:
            if line and not line[0].isspace():
                break
            body.append(line)

        while body and not body[-1].strip():
            body.pop()

        return textwrap.dedent("\n".join(body)).splitlines()
