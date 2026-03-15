from __future__ import annotations

from typing import Any, ClassVar

from textual.binding import Binding
from textual.containers import Vertical
from textual.message import Message
from textual.widgets import Label, ListItem, ListView

from justx.justfiles.models import Recipe, Source
from justx.justfiles.utils import group_recipes


class RecipeListItem(ListItem):
    """A ListItem that carries a reference to its Recipe."""

    def __init__(self, *args: Any, recipe: Recipe, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.recipe = recipe


class RecipesPane(ListView):
    """Right pane — lists recipes for the selected source."""

    DEFAULT_CSS = """
    .recipe-name {
        color: $success;
        text-style: bold;
        height: auto;
    }
    .recipe-doc {
        color: $text-muted;
        padding-left: 2;
        height: auto;
    }
    .recipe-wrap {
        height: auto;
    }
    ListItem {
        margin-bottom: 0;
    }
    RecipesPane > ListItem.header {
        background: $panel;
        color: $accent;
        text-style: bold;
    }
    RecipesPane > ListItem.header:hover {
        background: $panel;
    }
    RecipesPane > ListItem.grouped {
        padding-left: 2;
    }
    """

    BINDINGS: ClassVar = [
        Binding("enter", "run", "Run", show=True, priority=True),
        Binding("d", "details", "Details"),
    ]

    class RecipeRun(Message):
        def __init__(self, recipe: Recipe) -> None:
            self.recipe = recipe
            super().__init__()

    class RecipeDetails(Message):
        def __init__(self, recipe: Recipe) -> None:
            self.recipe = recipe
            super().__init__()

    def __init__(self) -> None:
        super().__init__(id="recipes")
        self.border_title = "Recipes"
        self._source: Source | None = None
        self._query = ""

    def set_source(self, source: Source) -> None:
        """Replace recipe list when the source changes."""
        self._source = source
        self._rebuild()

    def filter(self, query: str) -> None:
        self._query = query
        self._rebuild()

    def _rebuild(self) -> None:
        self.clear()
        if self._source is None:
            return

        visible = self._source.filter_recipes(self._query)
        groups = group_recipes(visible)
        has_groups = not (len(groups) == 1 and groups[0].name is None)

        for group_name, recipes in groups:
            if has_groups and group_name is not None:
                header = ListItem(Label(f" {group_name} "), classes="header")
                header.disabled = True
                self.append(header)
            for recipe in recipes:
                item = self._build_item(recipe)
                if has_groups and group_name is not None:
                    item.add_class("grouped")
                self.append(item)

        from justx.tui.widgets import first_enabled_index

        # Skip disabled group headers so the highlight lands on the first selectable recipe.
        self.call_after_refresh(lambda: setattr(self, "index", first_enabled_index(self)))

    @staticmethod
    def _param_signature(recipe: Recipe) -> str:
        return " ".join(f"<{p.name}>" for p in recipe.parameters)

    def _build_item(self, recipe: Recipe) -> RecipeListItem:
        parts: list[str] = []
        if recipe.parameters:
            parts.append(self._param_signature(recipe))
        if recipe.dependencies:
            parts.append(f"→ {', '.join(recipe.dependencies)}")
        meta = "  ".join(parts)

        name_text = f"{recipe.name} [dim]{meta}[/dim]" if meta else recipe.name

        if recipe.doc:
            content = Vertical(
                Label(name_text, classes="recipe-name", markup=True),
                Label(recipe.doc, classes="recipe-doc"),
                classes="recipe-wrap",
            )
        else:
            content = Label(name_text, classes="recipe-name", markup=True)

        return RecipeListItem(content, recipe=recipe)

    def _highlighted_recipe(self) -> Recipe | None:
        child = self.highlighted_child
        return child.recipe if isinstance(child, RecipeListItem) else None

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        # Handles mouse clicks; keyboard Enter is intercepted by action_run
        event.stop()
        if recipe := self._highlighted_recipe():
            self.post_message(self.RecipeRun(recipe))

    def action_run(self) -> None:
        if recipe := self._highlighted_recipe():
            self.post_message(self.RecipeRun(recipe))

    def action_details(self) -> None:
        if recipe := self._highlighted_recipe():
            self.post_message(self.RecipeDetails(recipe))
