from __future__ import annotations

from typing import ClassVar, NamedTuple

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal
from textual.message import Message
from textual.screen import Screen
from textual.widgets import Footer, Header, Input

from justx.justfiles.models import JustxConfig, Recipe, Source
from justx.tui.screens.recipe import RecipeScreen
from justx.tui.screens.recipe_detail import RecipeDetailScreen
from justx.tui.widgets import RecipesPane, SourcesPane


class Selection(NamedTuple):
    source: Source
    recipe: Recipe
    args: list[str]


class SearchInput(Input):
    class Submitted(Message):
        """Posted when the user confirms (Enter or Down)."""

    class Cancelled(Message):
        """Posted when the user cancels (Escape). Input is cleared before posting."""

    BINDINGS: ClassVar = [
        Binding("enter", "focus_sources", "Confirm"),
        Binding("down", "focus_sources", show=False),
        Binding("escape", "clear_and_focus", "Cancel"),
    ]

    def action_focus_sources(self) -> None:
        self.post_message(self.Submitted())

    def action_clear_and_focus(self) -> None:
        self.clear()
        self.post_message(self.Cancelled())


class RecipeSelectionScreen(Screen[Selection | None]):
    CSS = """
    #search-input {
        dock: top;
        border: solid dodgerblue 40%;
    }
    #search-input:focus {
        border: solid dodgerblue;
    }
    Horizontal {
        height: 1fr;
    }
    #sources {
        width: 1fr;
        margin-right: 1;
        border: solid dodgerblue 40%;
        border-title-color: dodgerblue 40%;
    }
    #sources:focus-within {
        border: solid dodgerblue;
        border-title-color: dodgerblue;
    }
    #recipes {
        width: 2fr;
        border: solid dodgerblue 40%;
        border-title-color: dodgerblue 40%;
    }
    #recipes:focus-within {
        border: solid dodgerblue;
        border-title-color: dodgerblue;
    }
    """

    BINDINGS: ClassVar = [
        Binding("left", "focus_sources", "Sources"),
        Binding("h", "focus_sources", show=False),
        Binding("right", "focus_recipes", "Recipes"),
        Binding("l", "focus_recipes", show=False),
        Binding("s", "focus_search", "Search", show=True),
    ]

    def __init__(self, config: JustxConfig) -> None:
        super().__init__()
        self._config = config
        self._selected_source: Source | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield SearchInput(placeholder="Search recipes...", id="search-input")
        with Horizontal():
            yield SourcesPane(self._config)
            yield RecipesPane()
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(SourcesPane).focus()

    def on_input_changed(self, event: Input.Changed) -> None:
        query = event.value.strip()
        sources_pane = self.query_one(SourcesPane)
        recipes_pane = self.query_one(RecipesPane)
        sources_pane.filter(query)
        recipes_pane.filter(query)

    def on_sources_pane_source_selected(self, message: SourcesPane.SourceSelected) -> None:
        self._selected_source = message.source
        self.query_one(RecipesPane).set_source(message.source)

    def on_sources_pane_source_activated(self, message: SourcesPane.SourceActivated) -> None:
        self.action_focus_recipes()

    def on_recipes_pane_recipe_run(self, message: RecipesPane.RecipeRun) -> None:
        recipe = message.recipe
        source = self._selected_source
        if not recipe.parameters:
            self.dismiss(Selection(source=source, recipe=recipe, args=[]))
        else:
            self.app.push_screen(
                RecipeScreen(recipe, source),
                lambda args: (
                    self.app.call_later(self.dismiss, Selection(source=source, recipe=recipe, args=args))
                    if args is not None
                    else None
                ),
            )

    def on_recipes_pane_recipe_details(self, message: RecipesPane.RecipeDetails) -> None:
        self.app.push_screen(RecipeDetailScreen(message.recipe, self._selected_source))

    def on_search_input_submitted(self, message: SearchInput.Submitted) -> None:
        self.action_focus_sources()

    def on_search_input_cancelled(self, message: SearchInput.Cancelled) -> None:
        self.action_focus_sources()

    def action_dismiss_screen(self) -> None:
        self.dismiss(None)

    def action_focus_sources(self) -> None:
        self.query_one(SourcesPane).focus()

    def action_focus_recipes(self) -> None:
        self.query_one(RecipesPane).focus_first_enabled()

    def action_focus_search(self) -> None:
        self.query_one("#search-input", Input).focus()
