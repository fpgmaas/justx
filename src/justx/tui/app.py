import subprocess

from textual.app import App

from justx.justfiles.models import JustxConfig
from justx.tui.screens.recipe_selection import RecipeSelectionScreen, Selection


class Justx(App[Selection | None]):
    def __init__(self, config: JustxConfig) -> None:
        super().__init__()
        self._config = config

    def on_mount(self) -> None:
        self.push_screen(RecipeSelectionScreen(self._config), self.exit)


def run_tui(config: JustxConfig) -> None:
    selection = Justx(config).run()
    if selection is not None:
        subprocess.run(
            [
                "just",
                "--justfile",
                str(selection.source.path),
                selection.recipe.name,
                *selection.args.values(),
            ],
            check=False,
        )
