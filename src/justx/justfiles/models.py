from __future__ import annotations

import shutil
import subprocess
from collections.abc import Iterable
from enum import Enum
from pathlib import Path

from pydantic import BaseModel
from rich.console import Console
from rich.markup import escape


class ParameterKind(str, Enum):
    required = "required"
    optional = "optional"
    variadic = "variadic"


class Scope(str, Enum):
    global_ = "global"
    local = "local"


class WorkingDirMode(str, Enum):
    cwd = "cwd"
    justfile = "justfile"


class RecipeDefault(BaseModel):
    """The default value of a recipe parameter.

    Attributes:
        value: Raw value from just --dump (string, list, or None for empty string default).
        expression: True if the default is a complex expression (list), False for string literals.
    """

    value: str | list | None
    expression: bool


class Parameter(BaseModel):
    """A parameter declared in a just recipe.

    Attributes:
        name: Parameter name.
        default: Default value, or None if not set.
        kind: Whether the parameter is required, optional, or variadic.
    """

    name: str
    default: RecipeDefault | None
    kind: ParameterKind


class Recipe(BaseModel):
    """A just recipe (target).

    Attributes:
        name: Recipe name.
        doc: Doc comment from the justfile, or None.
        parameters: Ordered list of parameters.
        dependencies: Names of recipes this recipe depends on.
    """

    name: str
    doc: str | None
    parameters: list[Parameter]
    dependencies: list[str]
    groups: list[str] = []


class Source(BaseModel):
    """A justfile source (global or local).

    Attributes:
        name: Display name for the source.
        scope: Whether this is a global or local justfile.
        path: Absolute path to the justfile.
        recipes: Recipes defined in this justfile.
    """

    name: str
    scope: Scope
    path: Path
    recipes: list[Recipe]
    working_dir_mode: WorkingDirMode = WorkingDirMode.cwd

    def run(self, recipe_name: str, args: Iterable[str] = ()) -> int:
        from justx.justfiles.exceptions import JustNotFoundError

        just_bin = shutil.which("just")
        if just_bin is None:
            raise JustNotFoundError()
        working_directory = self.path.parent if self.working_dir_mode == WorkingDirMode.justfile else Path.cwd()
        result = subprocess.run(
            [just_bin, "--justfile", str(self.path), "--working-directory", str(working_directory), recipe_name, *args],
            check=False,
        )
        return result.returncode

    def pretty_print(self, console: Console | None = None) -> None:
        console = console or Console()
        scope_label = self.scope.value
        console.print(
            f"[bold]{escape(self.name)}[/bold]  [dim]\\[{scope_label}][/dim]  [dim]{escape(str(self.path))}[/dim]"
        )
        for recipe in self.recipes:
            params = " ".join(p.name for p in recipe.parameters)
            signature = escape(f"{recipe.name} {params}".strip())
            doc = f"  [dim]# {escape(recipe.doc)}[/dim]" if recipe.doc else ""
            console.print(f"  [cyan]{signature}[/cyan]{doc}")
        console.print()


class JustxConfig(BaseModel):
    global_sources: list[Source]
    local_sources: list[Source]
