from __future__ import annotations

from pathlib import Path

import pytest

from justx.justfiles.discovery import DEFAULT_JUSTX_HOME, DiscoveredPaths, JustxDiscovery


def _write_justfile(path: Path, content: str = "hello:\n    echo hello\n") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path


@pytest.fixture
def tmp_home(tmp_path: Path) -> Path:
    return tmp_path / "justx_home"


@pytest.fixture
def tmp_cwd(tmp_path: Path) -> Path:
    return tmp_path / "project"


def test_discover_empty(tmp_home, tmp_cwd):
    tmp_cwd.mkdir()
    result = JustxDiscovery().discover(cwd=tmp_cwd, justx_home=tmp_home)
    assert result.global_paths == []
    assert result.local_paths == []


def test_discover_global_root_justfile(tmp_home, tmp_cwd):
    tmp_cwd.mkdir()
    _write_justfile(tmp_home / "justfile")

    result = JustxDiscovery().discover(cwd=tmp_cwd, justx_home=tmp_home)

    assert result.global_paths == [tmp_home / "justfile"]
    assert result.local_paths == []


def test_discover_local_root_justfile(tmp_home, tmp_cwd):
    tmp_cwd.mkdir()
    _write_justfile(tmp_cwd / "justfile")

    result = JustxDiscovery().discover(cwd=tmp_cwd, justx_home=tmp_home)

    assert result.global_paths == []
    assert result.local_paths == [tmp_cwd / "justfile"]


def test_discover_global_just_files(tmp_home, tmp_cwd):
    tmp_cwd.mkdir()
    _write_justfile(tmp_home / "ops.just")
    _write_justfile(tmp_home / "dev.just")

    result = JustxDiscovery().discover(cwd=tmp_cwd, justx_home=tmp_home)

    assert set(result.global_paths) == {tmp_home / "ops.just", tmp_home / "dev.just"}
    assert result.local_paths == []


def test_discover_local_just_files(tmp_home, tmp_cwd):
    tmp_cwd.mkdir()
    _write_justfile(tmp_cwd / ".justx" / "ci.just")

    result = JustxDiscovery().discover(cwd=tmp_cwd, justx_home=tmp_home)

    assert result.global_paths == []
    assert result.local_paths == [tmp_cwd / ".justx" / "ci.just"]


def test_discover_global_root_comes_before_just_files(tmp_home, tmp_cwd):
    tmp_cwd.mkdir()
    _write_justfile(tmp_home / "justfile")
    _write_justfile(tmp_home / "ops.just")

    result = JustxDiscovery().discover(cwd=tmp_cwd, justx_home=tmp_home)

    assert result.global_paths[0] == tmp_home / "justfile"
    assert result.global_paths[1] == tmp_home / "ops.just"


def test_discover_local_root_comes_before_just_files(tmp_home, tmp_cwd):
    tmp_cwd.mkdir()
    _write_justfile(tmp_cwd / "justfile")
    _write_justfile(tmp_cwd / ".justx" / "ci.just")

    result = JustxDiscovery().discover(cwd=tmp_cwd, justx_home=tmp_home)

    assert result.local_paths[0] == tmp_cwd / "justfile"
    assert result.local_paths[1] == tmp_cwd / ".justx" / "ci.just"


def test_justx_home_env_var(monkeypatch, tmp_path):
    home = tmp_path / "custom_home"
    _write_justfile(home / "justfile")
    cwd = tmp_path / "cwd"
    cwd.mkdir()

    monkeypatch.setenv("JUSTX_HOME", str(home))
    result = JustxDiscovery().discover(cwd=cwd)

    assert result.global_paths == [home / "justfile"]


def test_justx_home_arg_takes_precedence_over_env_var(monkeypatch, tmp_path):
    env_home = tmp_path / "env_home"
    _write_justfile(env_home / "justfile")

    arg_home = tmp_path / "arg_home"
    _write_justfile(arg_home / "dev.just")

    cwd = tmp_path / "cwd"
    cwd.mkdir()

    monkeypatch.setenv("JUSTX_HOME", str(env_home))
    result = JustxDiscovery().discover(cwd=cwd, justx_home=arg_home)

    assert result.global_paths == [arg_home / "dev.just"]


def test_default_home_is_dot_justx():
    assert Path.home() / ".justx" == DEFAULT_JUSTX_HOME


def test_returns_discovered_paths_instance(tmp_home, tmp_cwd):
    tmp_cwd.mkdir()
    result = JustxDiscovery().discover(cwd=tmp_cwd, justx_home=tmp_home)
    assert isinstance(result, DiscoveredPaths)
