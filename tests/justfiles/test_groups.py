from __future__ import annotations

from pathlib import Path

from justx.justfiles.models import Recipe, Scope
from justx.justfiles.parser import JustfileParser
from justx.justfiles.utils import group_recipes

# ---------------------------------------------------------------------------
# Parser tests
# ---------------------------------------------------------------------------


def test_parse_recipe_with_single_group():
    raw = {
        "name": "build",
        "doc": None,
        "parameters": [],
        "dependencies": [],
        "attributes": [{"group": "dev"}],
    }
    parser = JustfileParser()
    recipe = parser._parse_recipe(raw)
    assert recipe.groups == ["dev"]


def test_parse_recipe_without_group():
    raw = {
        "name": "lint",
        "doc": None,
        "parameters": [],
        "dependencies": [],
        "attributes": [],
    }
    parser = JustfileParser()
    recipe = parser._parse_recipe(raw)
    assert recipe.groups == []


def test_parse_groups_from_justfile(local_dir: Path):
    source = JustfileParser().parse(local_dir / ".justx" / "groups.just", Scope.LOCAL)
    recipes = {r.name: r for r in source.recipes}

    assert recipes["build"].groups == ["dev"]
    assert recipes["watch"].groups == ["dev"]
    assert recipes["test"].groups == ["test"]
    assert recipes["lint"].groups == []


# ---------------------------------------------------------------------------
# Grouping logic tests
# ---------------------------------------------------------------------------


def _recipe(name: str, groups: list[str] | None = None) -> Recipe:
    return Recipe(name=name, doc=None, parameters=[], dependencies=[], groups=groups or [])


def test_group_recipes_with_groups():
    recipes = [_recipe("build", ["dev"]), _recipe("test", ["test"])]
    result = group_recipes(recipes)
    assert result == [("dev", [recipes[0]]), ("test", [recipes[1]])]


def test_group_recipes_no_groups():
    recipes = [_recipe("lint"), _recipe("fmt")]
    result = group_recipes(recipes)
    assert result == [(None, recipes)]


def test_group_recipes_mixed():
    build = _recipe("build", ["dev"])
    lint = _recipe("lint")
    result = group_recipes([build, lint])
    assert result == [(None, [lint]), ("dev", [build])]


def test_group_recipes_preserves_order_within_group():
    build = _recipe("build", ["dev"])
    watch = _recipe("watch", ["dev"])
    result = group_recipes([build, watch])
    assert result == [("dev", [build, watch])]


def test_group_recipes_empty_list():
    assert group_recipes([]) == []


# ---------------------------------------------------------------------------
# Integration test (parser + model)
# ---------------------------------------------------------------------------


def test_parsed_source_contains_groups(local_dir: Path):
    source = JustfileParser().parse(local_dir / ".justx" / "groups.just", Scope.LOCAL)
    recipes = {r.name: r for r in source.recipes}

    assert set(recipes) == {"build", "watch", "test", "lint"}
    assert recipes["build"].groups == ["dev"]
    assert recipes["watch"].groups == ["dev"]
    assert recipes["test"].groups == ["test"]
    assert recipes["lint"].groups == []
