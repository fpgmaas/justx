from __future__ import annotations

from pathlib import Path

from justx.justfiles.models import Recipe, Scope, Source


def _recipe(
    name: str = "build",
    doc: str | None = None,
    groups: list[str] | None = None,
) -> Recipe:
    return Recipe(name=name, doc=doc, parameters=[], dependencies=[], groups=groups or [])


def _source(
    recipes: list[Recipe] | None = None,
    module_path: str | None = None,
) -> Source:
    return Source(
        scope=Scope.LOCAL,
        path=Path("/project") / "justfile",
        recipes=recipes or [],
        module_path=module_path,
    )


# ---------------------------------------------------------------------------
# Recipe.private
# ---------------------------------------------------------------------------


def test_private_recipe():
    assert _recipe(name="_internal").private is True


def test_public_recipe():
    assert _recipe(name="build").private is False


# ---------------------------------------------------------------------------
# Recipe.matches
# ---------------------------------------------------------------------------


def test_matches_by_name():
    assert _recipe(name="build").matches("bui") is True


def test_matches_by_name_case_insensitive():
    assert _recipe(name="Build").matches("build") is True


def test_matches_by_doc():
    assert _recipe(name="build", doc="Compile the project").matches("compile") is True


def test_matches_by_group():
    assert _recipe(name="build", groups=["dev"]).matches("dev") is True


def test_no_match():
    assert _recipe(name="build", doc="Compile").matches("deploy") is False


# ---------------------------------------------------------------------------
# Source.display_name
# ---------------------------------------------------------------------------


def test_display_name_from_module_path():
    source = _source(module_path="docker")
    assert source.display_name == "docker"


def test_display_name_from_file_stem():
    source = _source()
    assert source.display_name == "justfile"


# ---------------------------------------------------------------------------
# Source.filter_recipes
# ---------------------------------------------------------------------------


def test_filter_recipes_excludes_private():
    recipes = [_recipe(name="build"), _recipe(name="_internal")]
    source = _source(recipes=recipes)
    assert [r.name for r in source.filter_recipes()] == ["build"]


def test_filter_recipes_with_query():
    recipes = [_recipe(name="build", doc="Compile"), _recipe(name="test", doc="Run tests")]
    source = _source(recipes=recipes)
    assert [r.name for r in source.filter_recipes("compile")] == ["build"]


def test_filter_recipes_matches_source_name():
    recipes = [_recipe(name="build"), _recipe(name="test")]
    source = _source(recipes=recipes, module_path="docker")
    assert [r.name for r in source.filter_recipes("docker")] == ["build", "test"]


def test_filter_recipes_no_match():
    recipes = [_recipe(name="build")]
    source = _source(recipes=recipes)
    assert source.filter_recipes("deploy") == []
