from __future__ import annotations

from justx.justfiles.models import Source


def parse_target(target: str) -> tuple[str | None, str]:
    """Split a ``source:recipe`` target string into its components.

    When no colon is present the target is treated as a plain recipe on the root justfile.

    Args:
        target: A raw CLI argument such as ``"docker:build"`` or ``"build"``.
    """
    if ":" in target:
        source_name, recipe = target.rsplit(":", 1)
        return source_name, recipe
    return None, target


def find_source(sources: list[Source], source_name: str | None) -> Source | None:
    """Look up a source by name, or return the root justfile.

    Sources are identified by their file name.  The root justfile has no
    source name, so we match on the conventional ``justfile`` / ``Justfile``
    filenames rather than requiring callers to know the exact casing.

    Args:
        sources: The list of sources to search (local or global).
        source_name: The source name to match, or ``None`` to find the root justfile.
    """
    for source in sources:
        if source_name is None and source.display_name in ("justfile", "Justfile"):
            return source
        if source_name is not None and source.display_name == source_name:
            return source
    return None
