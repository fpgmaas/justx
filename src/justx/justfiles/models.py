from __future__ import annotations

from enum import Enum
from pathlib import Path

from pydantic import BaseModel


class ParameterKind(str, Enum):
    required = "required"
    optional = "optional"
    variadic = "variadic"


class Scope(str, Enum):
    global_ = "global"
    local = "local"


class Parameter(BaseModel):
    """A parameter declared in a just recipe.

    Attributes:
        name: Parameter name.
        default: Default value, or None if not set.
        kind: Whether the parameter is required, optional, or variadic.
    """

    name: str
    default: str | None
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


class JustxConfig(BaseModel):
    global_sources: list[Source]
    local_sources: list[Source]
