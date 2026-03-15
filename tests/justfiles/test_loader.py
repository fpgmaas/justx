from __future__ import annotations

from pathlib import Path

import pytest

from justx.justfiles.loader import JustxLoader
from justx.justfiles.models import Scope

SIMPLE_JUSTFILE = """\
# Do something
hello:
    echo hello
"""

ANOTHER_JUSTFILE = """\
# Do another thing
world:
    echo world
"""


@pytest.fixture
def tmp_home(tmp_path: Path) -> Path:
    return tmp_path / "justx_home"


@pytest.fixture
def tmp_cwd(tmp_path: Path) -> Path:
    return tmp_path / "project"


def _write_justfile(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path


def test_load_empty(tmp_home, tmp_cwd):
    tmp_cwd.mkdir()
    config = JustxLoader().load(cwd=tmp_cwd, justx_home=tmp_home)
    assert config.global_sources == []
    assert config.local_sources == []


def test_load_global_root_justfile(tmp_home, tmp_cwd):
    tmp_cwd.mkdir()
    _write_justfile(tmp_home / "justfile", SIMPLE_JUSTFILE)

    config = JustxLoader().load(cwd=tmp_cwd, justx_home=tmp_home)

    assert len(config.global_sources) == 1
    assert config.global_sources[0].name == "justfile"
    assert config.global_sources[0].scope == Scope.global_
    assert config.local_sources == []


def test_load_local_root_justfile(tmp_home, tmp_cwd):
    tmp_cwd.mkdir()
    _write_justfile(tmp_cwd / "justfile", SIMPLE_JUSTFILE)

    config = JustxLoader().load(cwd=tmp_cwd, justx_home=tmp_home)

    assert config.global_sources == []
    assert len(config.local_sources) == 1
    assert config.local_sources[0].name == "justfile"
    assert config.local_sources[0].scope == Scope.local


def test_load_global_just_files(tmp_home, tmp_cwd):
    tmp_cwd.mkdir()
    _write_justfile(tmp_home / "ops.just", SIMPLE_JUSTFILE)
    _write_justfile(tmp_home / "dev.just", ANOTHER_JUSTFILE)

    config = JustxLoader().load(cwd=tmp_cwd, justx_home=tmp_home)

    names = {s.name for s in config.global_sources}
    assert names == {"ops", "dev"}
    assert all(s.scope == Scope.global_ for s in config.global_sources)


def test_load_local_just_files(tmp_home, tmp_cwd):
    tmp_cwd.mkdir()
    _write_justfile(tmp_cwd / ".justx" / "ci.just", SIMPLE_JUSTFILE)

    config = JustxLoader().load(cwd=tmp_cwd, justx_home=tmp_home)

    assert config.global_sources == []
    assert len(config.local_sources) == 1
    assert config.local_sources[0].name == "ci"
    assert config.local_sources[0].scope == Scope.local


def test_load_with_real_fixture(local_dir, tmp_path):

    config = JustxLoader().load(cwd=local_dir, justx_home=tmp_path)

    assert len(config.local_sources) == 4
    assert all(s.scope == Scope.local for s in config.local_sources)

    by_name = {s.name: s for s in config.local_sources}

    assert {r.name for r in by_name["groups"].recipes} == {"build", "lint", "test", "watch"}
    assert {r.name for r in by_name["justfile"].recipes} == {"bootstrap", "upgrade-deps", "script1", "script2"}
    assert {r.name for r in by_name["expressions"].recipes} == {"run"}
    assert {r.name for r in by_name["simple"].recipes} == {"greet", "date"}
