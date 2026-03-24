from __future__ import annotations

from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Label, Static

from justx.justfiles.body_reader import JustfileBodyReader
from justx.justfiles.models import ParameterKind, Recipe, Source


class RecipeDetailScreen(Screen[None]):
    CSS = """
    RecipeDetailScreen {
        align: center middle;
    }
    #dialog {
        width: 80;
        max-height: 80%;
        border: solid dodgerblue;
        border-title-color: dodgerblue;
        background: $surface;
    }
    #dialog-scroll {
        padding: 1 2;
    }
    #name {
        text-style: bold;
        color: $success;
    }
    #description {
        color: $text-muted;
    }
    .tag-row {
        height: auto;
    }
    .detail-label {
        color: $accent;
        text-style: bold;
    }
    .detail-row {
        height: auto;
        margin-top: 1;
    }
    .section-header {
        text-style: bold;
        color: $accent;
        margin-top: 1;
    }
    .param-row {
        height: auto;
        padding-left: 2;
    }
    .body-separator {
        color: $accent;
        margin-top: 1;
    }
    #body-code {
        color: $text;
        padding-left: 2;
    }
    """
    BINDINGS: ClassVar = [
        Binding("left", "dismiss", "Back", show=True, priority=True),
        Binding("backspace", "dismiss", "Back", show=False, priority=True),
    ]

    def __init__(self, recipe: Recipe, source: Source | None = None) -> None:
        super().__init__()
        self._recipe = recipe
        self._source = source

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog") as dialog:
            dialog.border_title = "Recipe Details"
            with VerticalScroll(id="dialog-scroll"):
                yield Label(self._display_name(), id="name")
                yield from self._compose_description()
                yield from self._compose_tags()
                yield from self._compose_metadata()
                yield from self._compose_parameters()
                yield from self._compose_body()
        yield Footer()

    def _display_name(self) -> str:
        if self._source and self._source.module_path:
            return f"{self._source.module_path}::{self._recipe.name}"
        return self._recipe.name

    def _compose_description(self) -> ComposeResult:
        if self._recipe.doc:
            yield Label(self._recipe.doc, id="description")

    def _compose_tags(self) -> ComposeResult:
        tags = self._build_tags()
        if tags:
            yield Static(" ".join(tags), classes="tag-row")

    def _compose_metadata(self) -> ComposeResult:
        if self._source is not None:
            yield Static(
                f"[bold $accent]Justfile[/]  {self._source.path}",
                classes="detail-row",
                markup=True,
            )
        if self._recipe.dependencies:
            dependencies = ", ".join(self._recipe.dependencies)
            yield Static(
                f"[bold $accent]Depends[/]   {dependencies}",
                classes="detail-row",
                markup=True,
            )

    def _compose_parameters(self) -> ComposeResult:
        if not self._recipe.parameters:
            return
        yield Label("Parameters", classes="section-header")
        for param in self._recipe.parameters:
            yield self._build_param_label(param)

    def _compose_body(self) -> ComposeResult:
        if self._source is None:
            return
        body = JustfileBodyReader().read(self._source.path, self._recipe.name)
        if body:
            yield Static("── Body ──", classes="body-separator")
            yield Static("\n".join(body), id="body-code")

    def _build_tags(self) -> list[str]:
        tags = []
        if self._recipe.quiet:
            tags.append("[dim]quiet[/]")
        for attribute in self._recipe.attributes:
            tags.append(f"[dim]{attribute}[/]")
        return tags

    def _build_param_label(self, param) -> Label:
        kind_map = {
            ParameterKind.REQUIRED: "required",
            ParameterKind.OPTIONAL: "optional",
            ParameterKind.VARIADIC: "variadic",
        }
        if param.default is None:
            default = ""
        elif param.default.expression:
            default = ", default: <expression>"
        else:
            default = f", default: {param.default.value!r}"
        return Label(f"  {param.name}  ({kind_map[param.kind]}{default})", classes="param-row")

    def action_dismiss(self) -> None:
        self.dismiss()
