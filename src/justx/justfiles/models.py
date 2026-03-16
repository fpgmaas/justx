from __future__ import annotations

import shutil
import subprocess
from collections.abc import Iterable
from enum import Enum
from pathlib import Path
from typing import NamedTuple

from pydantic import BaseModel
from rich.console import Console
from rich.markup import escape


class ParameterKind(str, Enum):
    REQUIRED = "required"
    OPTIONAL = "optional"
    VARIADIC = "variadic"


class Scope(str, Enum):
    GLOBAL = "global"
    LOCAL = "local"


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

    @property
    def private(self) -> bool:
        return self.name.startswith("_")

    def matches(self, query: str) -> bool:
        """Check if recipe matches a case-insensitive substring query."""
        q = query.lower()
        return (
            q in self.name.lower()
            or (self.doc is not None and q in self.doc.lower())
            or any(q in g.lower() for g in self.groups)
        )


class RecipeGroup(NamedTuple):
    name: str | None
    recipes: list[Recipe]


class Source(BaseModel):
    """A justfile source (global or local).

    Attributes:
        display_name: Display name for the source.
        scope: Whether this is a global or local justfile.
        path: Absolute path to the justfile.
        recipes: Recipes defined in this justfile.
        module_path: Qualified module path (e.g. "docker" or "infra::deploy"), None for root sources.
        root_justfile: Path to the root justfile (set on module sources so run() can invoke just correctly).
    """

    display_name: str
    scope: Scope
    path: Path
    recipes: list[Recipe]
    module_path: str | None = None
    root_justfile: Path | None = None

    def filter_recipes(self, query: str = "") -> list[Recipe]:
        """Return visible recipes matching query (case-insensitive substring on name, doc, groups, source name)."""
        visible = [r for r in self.recipes if not r.private]
        if not query:
            return visible
        q = query.lower()
        return [r for r in visible if r.matches(query) or q in self.display_name.lower()]

    def run(self, recipe_name: str, args: Iterable[str] = ()) -> int:
        from justx.justfiles.exceptions import JustNotFoundError

        just_bin = shutil.which("just")
        if just_bin is None:
            raise JustNotFoundError()
        result = subprocess.run(
            self._build_command(just_bin, recipe_name, args),
            check=False,
        )
        return result.returncode

    def _build_command(self, just_bin: str, recipe_name: str, args: Iterable[str]) -> list[str]:
        """Build the just invocation command.

        Global sources pass --working-directory so recipes run in the user's cwd.
        Local sources let just handle working directories natively.
        Module sources invoke just on the root justfile with a module::recipe target.
        """
        justfile = str(self.root_justfile or self.path)
        target = f"{self.module_path}::{recipe_name}" if self.module_path else recipe_name

        command = [just_bin, "--justfile", justfile]
        if self.scope == Scope.GLOBAL:
            command.extend(["--working-directory", str(Path.cwd())])
        command.extend([target, *args])
        return command

    def pretty_print(self, console: Console | None = None) -> None:
        console = console or Console()
        scope_label = self.scope.value
        console.print(
            f"[bold]{escape(self.display_name)}[/bold]  [dim]\\[{scope_label}][/dim]  [dim]{escape(str(self.path))}[/dim]"
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
