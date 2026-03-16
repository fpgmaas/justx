from pathlib import Path

import pytest

from justx.justfiles.models import ParameterKind, Scope
from justx.justfiles.parser import JustfileParser


def test_parse_justfile(example_justfile):
    sources = JustfileParser().parse(example_justfile, Scope.LOCAL)

    assert len(sources) == 1
    source = sources[0]
    assert source.display_name == "justfile"
    assert source.path == example_justfile
    assert source.module_path is None

    recipes = {r.name: r for r in source.recipes}
    assert set(recipes) == {"bootstrap", "upgrade-deps", "script1", "script2"}

    assert recipes["bootstrap"].doc == "Set up development environment"
    assert recipes["bootstrap"].parameters == []
    assert recipes["bootstrap"].dependencies == []

    assert recipes["upgrade-deps"].dependencies == ["bootstrap"]

    assert recipes["script1"].parameters == []

    args = recipes["script2"].parameters[0]
    assert args.name == "ARGS"
    assert args.kind == ParameterKind.VARIADIC
    assert args.default is None


def test_parse_justfile_not_found():
    with pytest.raises(FileNotFoundError):
        JustfileParser().parse(Path("nonexistent/justfile"), Scope.LOCAL)


def test_parse_modules(module_justfile):
    sources = JustfileParser().parse(module_justfile, Scope.LOCAL)

    assert len(sources) == 3

    root = sources[0]
    assert root.display_name == "justfile"
    assert root.module_path is None
    assert root.path == module_justfile
    assert {r.name for r in root.recipes} == {"build", "run"}

    foo = sources[1]
    assert foo.display_name == "foo"
    assert foo.module_path == "foo"
    assert foo.path == module_justfile.parent / "bar" / "justfile"
    assert {r.name for r in foo.recipes} == {"lint", "format"}

    baz = sources[2]
    assert baz.display_name == "foo::baz"
    assert baz.module_path == "foo::baz"
    assert baz.path == module_justfile.parent / "bar" / "baz" / "justfile"
    assert {r.name for r in baz.recipes} == {"lint", "format"}


def test_parse_modules_root_justfile(module_justfile):
    sources = JustfileParser().parse(module_justfile, Scope.LOCAL)

    root = sources[0]
    assert root.root_justfile is None

    foo = sources[1]
    assert foo.root_justfile == module_justfile

    baz = sources[2]
    assert baz.root_justfile == module_justfile


def test_parse_no_modules(example_justfile):
    sources = JustfileParser().parse(example_justfile, Scope.LOCAL)

    assert len(sources) == 1
    assert sources[0].module_path is None
