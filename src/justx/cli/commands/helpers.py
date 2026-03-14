from __future__ import annotations

from justx.justfiles.models import Source


def parse_target(target: str) -> tuple[str | None, str]:
    """Split a ``group:recipe`` target string into its components.

    When no colon is present the target is treated as a plain recipe on the root justfile.

    Args:
        target: A raw CLI argument such as ``"docker:build"`` or ``"build"``.
    """
    if ":" in target:
        group, recipe = target.split(":", 1)
        return group, recipe
    return None, target


def find_source(sources: list[Source], group: str | None) -> Source | None:
    """Look up a source by group name, or return the root justfile.

    Sources are identified by their file name.  The root justfile has no
    group name, so we match on the conventional ``justfile`` / ``Justfile``
    filenames rather than requiring callers to know the exact casing.

    Args:
        sources: The list of sources to search (local or global).
        group: The group name to match, or ``None`` to find the root justfile.
    """
    for source in sources:
        if group is None and source.name in ("justfile", "Justfile"):
            return source
        if group is not None and source.name == group:
            return source
    return None
