from textual.widgets import ListView


def first_enabled_index(view: ListView) -> int | None:
    """Return the index of the first non-disabled item, or None."""
    for i, child in enumerate(view.children):
        if not child.disabled:
            return i
    return None
