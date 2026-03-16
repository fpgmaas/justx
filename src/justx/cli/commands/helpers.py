from __future__ import annotations

from justx.justfiles.models import Source


def resolve_target(target: str, sources: list[Source]) -> tuple[Source | None, str]:
    """Resolve a CLI target string to a source and recipe name.

    Uses just-native ``::`` syntax throughout: ``source::recipe`` or
    ``module::submodule::recipe``.  The longest matching source prefix
    determines the source; the remaining segment is the recipe.
    """
    segments = target.split("::")
    for i in range(len(segments) - 1, 0, -1):
        source_name = "::".join(segments[:i])
        source = _find_source_by_name(sources, source_name)
        if source is not None:
            recipe = "::".join(segments[i:])
            return source, recipe
    return None, target


def _find_source_by_name(sources: list[Source], name: str) -> Source | None:
    for source in sources:
        if source.display_name == name:
            return source
    return None
