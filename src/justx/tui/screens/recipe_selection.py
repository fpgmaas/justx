from __future__ import annotations

from typing import ClassVar, NamedTuple

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView

from justx.justfiles.models import JustxConfig, Recipe, Source
from justx.tui.screens.recipe import RecipeScreen
from justx.tui.screens.recipe_detail import RecipeDetailScreen


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
    ListView > ListItem.header {
        background: $panel;
        color: $accent;
        text-style: bold;
    }
    ListView > ListItem.header:hover {
        background: $panel;
    }
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
        Binding("q", "quit", "Quit"),
        Binding("enter", "run_highlighted", "Run", show=True),
        Binding("d", "details", "Details"),
        Binding("left", "focus_sources", "Sources"),
        Binding("right", "focus_recipes", "Recipes"),
    ]

    def __init__(self, config: JustxConfig) -> None:
        super().__init__()
        self._config = config
        self._id_to_source: dict[str, Source] = {}
        self._selected_source: Source | None = None
        self._highlighted_recipe: Recipe | None = None

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal():
            source_items, self._id_to_source = self._build_source_items()
            yield ListView(*source_items, id="sources")
            yield ListView(id="recipes")
        yield Footer()

    def _build_source_items(self) -> tuple[list[ListItem], dict[str, Source]]:
        items: list[ListItem] = []
        id_to_source: dict[str, Source] = {}

        def make_header(title: str) -> ListItem:
            item = ListItem(Label(f" {title} "), classes="header")
            item.disabled = True
            return item

        items.append(make_header("Local"))
        for i, source in enumerate(self._config.local_sources):
            item_id = f"source-l{i}"
            id_to_source[item_id] = source
            items.append(ListItem(Label(f"  {source.name}"), id=item_id))

        items.append(make_header("Global"))
        for i, source in enumerate(self._config.global_sources):
            item_id = f"source-g{i}"
            id_to_source[item_id] = source
            items.append(ListItem(Label(f"  {source.name}"), id=item_id))

        return items, id_to_source

    def _build_recipe_item(self, recipe: Recipe) -> ListItem:
        if recipe.doc:
            return ListItem(
                Vertical(
                    Label(recipe.name, classes="recipe-name"),
                    Label(recipe.doc, classes="recipe-doc"),
                    classes="recipe-wrap",
                )
            )
        return ListItem(Label(recipe.name, classes="recipe-name"))

    def _populate_recipes(self, source: Source) -> None:
        self._selected_source = source
        recipes_list = self.query_one("#recipes", ListView)
        recipes_list.clear()
        for recipe in source.recipes:
            recipes_list.append(self._build_recipe_item(recipe))

    def on_list_view_highlighted(self, event: ListView.Highlighted) -> None:
        if event.list_view.id == "sources" and event.item is not None:
            source = self._id_to_source.get(event.item.id or "")
            if source is not None:
                self._populate_recipes(source)
        elif event.list_view.id == "recipes" and self._selected_source is not None:
            idx = event.list_view.index
            if idx is not None and idx < len(self._selected_source.recipes):
                self._highlighted_recipe = self._selected_source.recipes[idx]

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        if event.list_view.id == "sources":
            if self._id_to_source.get(event.item.id or "") is not None:
                self.action_focus_recipes()
        elif event.list_view.id == "recipes" and self._selected_source is not None:
            recipe_index = event.list_view.index
            if recipe_index is not None:
                self._select_recipe(self._selected_source.recipes[recipe_index])

    def _select_recipe(self, recipe: Recipe) -> None:
        source = self._selected_source
        if not recipe.parameters:
            self.dismiss(Selection(source=source, recipe=recipe, args={}))
        else:

            def on_args(args: dict[str, str] | None) -> None:
                if args is not None:
                    self.dismiss(Selection(source=source, recipe=recipe, args=args))

            self.app.push_screen(RecipeScreen(recipe, self._selected_source), on_args)

    def action_run_highlighted(self) -> None:
        pass  # Enter is handled by ListView.Selected; this exists for footer display

    def action_details(self) -> None:
        recipe = self._highlighted_recipe
        if recipe is not None:
            self.app.push_screen(RecipeDetailScreen(recipe, self._selected_source))

    def action_quit(self) -> None:
        self.dismiss(None)

    def action_focus_sources(self) -> None:
        self.query_one("#sources", ListView).focus()

    def action_focus_recipes(self) -> None:
        self.query_one("#recipes", ListView).focus()
