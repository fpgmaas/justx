from __future__ import annotations

from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Button, Footer, Input, Label

from justx.justfiles.models import Parameter, ParameterKind, Recipe, Source


class RecipeScreen(Screen[dict[str, str] | None]):
    CSS = """
    RecipeScreen {
        align: center middle;
    }
    #dialog {
        width: 70;
        height: auto;
        border: solid $accent;
        padding: 1 2;
        background: $surface;
    }
    #title {
        text-style: bold;
        color: $success;
        margin-bottom: 1;
    }
    #doc {
        color: $text-muted;
        margin-bottom: 1;
    }
    .param-row {
        height: auto;
        margin-bottom: 1;
    }
    .param-label {
        width: 1fr;
        padding-top: 1;
    }
    .param-input {
        width: 2fr;
    }
    #buttons {
        height: auto;
        margin-top: 1;
        align: right middle;
    }
    """
    BINDINGS: ClassVar = [
        Binding("escape", "cancel", "Cancel", show=True, priority=True),
        Binding("ctrl+enter", "run", "Run", show=True, priority=True),
        Binding("d", "details", "Details", show=True, priority=True),
        Binding("up", "focus_prev_field", "↑ Prev", show=True, priority=True),
        Binding("down", "focus_next_field", "↓ Next", show=True, priority=True),
        Binding("left", "focus_button_left", show=False, priority=True),
        Binding("right", "focus_button_right", show=False, priority=True),
    ]

    def __init__(self, recipe: Recipe, source: Source | None = None) -> None:
        super().__init__()
        self._recipe = recipe
        self._source = source

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label(self._recipe.name, id="title")
            if self._recipe.doc:
                yield Label(self._recipe.doc, id="doc")
            for param in self._recipe.parameters:
                yield self._build_param_row(param)
            with Horizontal(id="buttons"):
                yield Button("Cancel", variant="default", id="cancel")
                yield Button("Run", variant="primary", id="run")
        yield Footer()

    def _build_param_row(self, param: Parameter) -> Horizontal:
        suffix = (
            " *" if param.kind == ParameterKind.required else (" ..." if param.kind == ParameterKind.variadic else "")
        )
        return Horizontal(
            Label(f"{param.name}{suffix}", classes="param-label"),
            Input(
                value=param.default or "",
                id=f"param-{param.name}",
                classes="param-input",
            ),
            classes="param-row",
        )

    def _collect_args(self) -> dict[str, str]:
        return {param.name: self.query_one(f"#param-{param.name}", Input).value for param in self._recipe.parameters}

    def _inputs(self) -> list[Input]:
        return list(self.query(Input))

    def _advance_focus(self, current: Input) -> None:
        inputs = self._inputs()
        idx = inputs.index(current)
        if idx < len(inputs) - 1:
            inputs[idx + 1].focus()
        else:
            self.query_one("#run", Button).focus()

    def _retreat_focus(self, current: Input) -> None:
        inputs = self._inputs()
        idx = inputs.index(current)
        if idx > 0:
            inputs[idx - 1].focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self._advance_focus(event.input)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "run":
            self.dismiss(self._collect_args())
        elif event.button.id == "cancel":
            self.dismiss(None)

    def action_details(self) -> None:
        from justx.tui.screens.recipe_detail import RecipeDetailScreen

        self.app.push_screen(RecipeDetailScreen(self._recipe, self._source))

    def action_cancel(self) -> None:
        self.dismiss(None)

    def action_run(self) -> None:
        self.dismiss(self._collect_args())

    def action_focus_next_field(self) -> None:
        if isinstance(self.focused, Input):
            self._advance_focus(self.focused)

    def action_focus_button_left(self) -> None:
        if isinstance(self.focused, Button) and self.focused.id == "run":
            self.query_one("#cancel", Button).focus()

    def action_focus_button_right(self) -> None:
        if isinstance(self.focused, Button) and self.focused.id == "cancel":
            self.query_one("#run", Button).focus()

    def action_focus_prev_field(self) -> None:
        if isinstance(self.focused, Input):
            self._retreat_focus(self.focused)
        elif isinstance(self.focused, Button) and self.focused.id == "run":
            inputs = self._inputs()
            if inputs:
                inputs[-1].focus()
