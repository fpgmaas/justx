from __future__ import annotations

from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Footer, Label

from justx.justfiles.models import ParameterKind, Recipe, Source


class RecipeDetailScreen(Screen[None]):
    CSS = """
    RecipeDetailScreen {
        align: center middle;
    }
    #dialog {
        width: 80;
        height: auto;
        border: solid $accent;
        padding: 1 2;
        background: $surface;
    }
    #name {
        text-style: bold;
        color: $success;
        margin-bottom: 1;
    }
    .section-header {
        text-style: bold;
        color: $accent;
        margin-top: 1;
    }
    .detail-value {
        color: $text;
        padding-left: 2;
    }
    .detail-muted {
        color: $text-muted;
        padding-left: 2;
    }
.param-row {
        height: auto;
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
        with Vertical(id="dialog"):
            yield Label(self._recipe.name, id="name")

            if self._recipe.doc:
                yield Label("Description", classes="section-header")
                yield Label(self._recipe.doc, classes="detail-value")

            if self._source is not None:
                yield Label("Justfile", classes="section-header")
                yield Label(str(self._source.path), classes="detail-muted")

            if self._recipe.dependencies:
                yield Label("Dependencies", classes="section-header")
                yield Label(", ".join(self._recipe.dependencies), classes="detail-value")

            if self._recipe.parameters:
                yield Label("Parameters", classes="section-header")
                for param in self._recipe.parameters:
                    yield self._build_param_label(param)
            else:
                yield Label("Parameters", classes="section-header")
                yield Label("none", classes="detail-muted")

        yield Footer()

    def _build_param_label(self, param) -> Label:
        kind_map = {
            ParameterKind.required: "required",
            ParameterKind.optional: "optional",
            ParameterKind.variadic: "variadic",
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
