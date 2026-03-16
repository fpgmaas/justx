from __future__ import annotations

from pathlib import Path

from justx.cli.commands.helpers import resolve_target
from justx.justfiles.models import Scope, Source


def _source(display_name: str) -> Source:
    return Source(
        display_name=display_name,
        scope=Scope.LOCAL,
        path=Path("/fake"),
        recipes=[],
    )


def test_resolve_source_and_recipe() -> None:
    sources = [_source("justfile"), _source("foo")]
    source, recipe = resolve_target("justfile::bootstrap", sources)
    assert source is not None
    assert source.display_name == "justfile"
    assert recipe == "bootstrap"


def test_resolve_module_recipe() -> None:
    sources = [_source("justfile"), _source("foo")]
    source, recipe = resolve_target("foo::lint", sources)
    assert source is not None
    assert source.display_name == "foo"
    assert recipe == "lint"


def test_resolve_nested_module_recipe() -> None:
    sources = [_source("justfile"), _source("foo"), _source("foo::baz")]
    source, recipe = resolve_target("foo::baz::lint-baz", sources)
    assert source is not None
    assert source.display_name == "foo::baz"
    assert recipe == "lint-baz"


def test_resolve_unknown_target() -> None:
    sources = [_source("justfile")]
    source, _ = resolve_target("unknown::build", sources)
    assert source is None


def test_resolve_no_separator() -> None:
    sources = [_source("justfile")]
    source, recipe = resolve_target("build", sources)
    assert source is None
    assert recipe == "build"
