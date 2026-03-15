from __future__ import annotations

from typing import ClassVar

from textual.binding import Binding
from textual.containers import Vertical
from textual.message import Message
from textual.widgets import Label, ListItem, ListView

from justx.justfiles.models import Recipe, Source


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

    def set_source(self, source: Source) -> None:
        """Replace recipe list when the source changes."""
        self.clear()
        visible = [r for r in source.recipes if not r.name.startswith("_")]
        groups = self._group_recipes(visible)
        has_groups = any(g is not None for g, _ in groups)

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

    @staticmethod
    def _group_recipes(recipes: list[Recipe]) -> list[tuple[str | None, list[Recipe]]]:
        """Group recipes by group name, alphabetically, ungrouped last.

        Returns a list of (group_name, recipes) tuples. If no recipes have
        groups, returns [(None, recipes)] for flat-list behavior.
        """
        if not recipes:
            return []

        any_grouped = any(r.groups for r in recipes)
        if not any_grouped:
            return [(None, recipes)]

        seen_groups: dict[str, list[Recipe]] = {}
        ungrouped: list[Recipe] = []

        for recipe in recipes:
            if recipe.groups:
                for group in recipe.groups:
                    seen_groups.setdefault(group, []).append(recipe)
            else:
                ungrouped.append(recipe)

        result: list[tuple[str | None, list[Recipe]]] = []
        if ungrouped:
            result.append((None, ungrouped))
        result.extend((name, seen_groups[name]) for name in sorted(seen_groups))
        return result

    @staticmethod
    def _param_signature(recipe: Recipe) -> str:
        return " ".join(f"<{p.name}>" for p in recipe.parameters)

    def _build_item(self, recipe: Recipe) -> ListItem:
        meta = self._param_signature(recipe)
        if recipe.dependencies:
            dep_text = f"→ {', '.join(recipe.dependencies)}"
            meta = f"{meta}  {dep_text}" if meta else dep_text

        name_text = recipe.name
        if meta:
            name_text = f"{recipe.name} [dim]{meta}[/dim]"

        if recipe.doc:
            item = ListItem(
                Vertical(
                    Label(name_text, classes="recipe-name", markup=True),
                    Label(recipe.doc, classes="recipe-doc"),
                    classes="recipe-wrap",
                )
            )
        else:
            item = ListItem(Label(name_text, classes="recipe-name", markup=True))

        item._recipe = recipe  # type: ignore[attr-defined]
        return item

    def _highlighted_recipe(self) -> Recipe | None:
        return getattr(self.highlighted_child, "_recipe", None)

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
