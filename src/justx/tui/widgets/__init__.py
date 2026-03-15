from textual.widgets import ListView

from justx.tui.widgets.recipes_pane import RecipesPane
from justx.tui.widgets.sources_pane import SourcesPane


def first_enabled_index(view: ListView) -> int | None:
    """Return the index of the first non-disabled item, or None."""
    for i, child in enumerate(view.children):
        if not child.disabled:
            return i
    return None


__all__ = ["RecipesPane", "SourcesPane", "first_enabled_index"]
