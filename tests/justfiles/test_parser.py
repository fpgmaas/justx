from pathlib import Path

import pytest

from justx.justfiles.models import ParameterKind, Scope
from justx.justfiles.parser import JustfileParser


def test_parse_justfile(example_justfile):
    source = JustfileParser().parse(example_justfile, Scope.local)

    assert source.name == "justfile"
    assert source.path == example_justfile

    recipes = {r.name: r for r in source.recipes}
    assert set(recipes) == {"bootstrap", "upgrade-deps", "script1", "script2"}

    assert recipes["bootstrap"].doc == "Set up development environment"
    assert recipes["bootstrap"].parameters == []
    assert recipes["bootstrap"].dependencies == []

    assert recipes["upgrade-deps"].dependencies == ["bootstrap"]

    assert recipes["script1"].parameters == []

    args = recipes["script2"].parameters[0]
    assert args.name == "ARGS"
    assert args.kind == ParameterKind.variadic
    assert args.default is None


def test_parse_justfile_not_found():
    with pytest.raises(FileNotFoundError):
        JustfileParser().parse(Path("nonexistent/justfile"), Scope.local)
