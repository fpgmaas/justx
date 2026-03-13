from __future__ import annotations

from typing import ClassVar, NamedTuple

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.screen import Screen
from textual.widgets import Footer, Header

from justx.justfiles.models import JustxConfig, Recipe, Source
from justx.tui.screens.recipe import RecipeScreen
from justx.tui.screens.recipe_detail import RecipeDetailScreen
from justx.tui.widgets import RecipesPane, SourcesPane


class Selection(NamedTuple):
    source: Source
    recipe: Recipe
    args: dict[str, str]


class RecipeSelectionScreen(Screen[Selection | None]):
    CSS = """
    Horizontal {
        height: 1fr;
    }
    #sources {
        width: 1fr;
    }
    #recipes {
        width: 2fr;
    }
    """

    BINDINGS: ClassVar = [
        Binding("left", "focus_sources", "Sources"),
        Binding("right", "focus_recipes", "Recipes"),
    ]

    def __init__(self, config: JustxConfig) -> None:
        super().__init__()
        self._config = config
        self._selected_source: Source | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            yield SourcesPane(self._config)
            yield RecipesPane()
        yield Footer()

    def on_sources_pane_source_selected(self, message: SourcesPane.SourceSelected) -> None:
        self._selected_source = message.source
        self.query_one(RecipesPane).set_source(message.source)

    def on_sources_pane_source_activated(self, message: SourcesPane.SourceActivated) -> None:
        self.action_focus_recipes()

    def on_recipes_pane_recipe_run(self, message: RecipesPane.RecipeRun) -> None:
        recipe = message.recipe
        source = self._selected_source
        if not recipe.parameters:
            self.dismiss(Selection(source=source, recipe=recipe, args={}))
        else:
            self.app.push_screen(
                RecipeScreen(recipe, source),
                lambda args: (
                    self.dismiss(Selection(source=source, recipe=recipe, args=args)) if args is not None else None
                ),
            )

    def on_recipes_pane_recipe_details(self, message: RecipesPane.RecipeDetails) -> None:
        self.app.push_screen(RecipeDetailScreen(message.recipe, self._selected_source))

    def action_focus_sources(self) -> None:
        self.query_one(SourcesPane).focus()

    def action_focus_recipes(self) -> None:
        pane = self.query_one(RecipesPane)
        pane.focus()
        if pane.index is None and len(pane) > 0:
            pane.index = 0
