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
        self._recipes: list[Recipe] = []

    def set_source(self, source: Source) -> None:
        """Replace recipe list when the source changes."""
        self.clear()
        self._recipes = list(source.recipes)
        for recipe in self._recipes:
            self.append(self._build_item(recipe))

    def _build_item(self, recipe: Recipe) -> ListItem:
        if recipe.doc:
            return ListItem(
                Vertical(
                    Label(recipe.name, classes="recipe-name"),
                    Label(recipe.doc, classes="recipe-doc"),
                    classes="recipe-wrap",
                )
            )
        return ListItem(Label(recipe.name, classes="recipe-name"))

    def _highlighted_recipe(self) -> Recipe | None:
        if self.index is not None and self.index < len(self._recipes):
            return self._recipes[self.index]
        return None

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
