from __future__ import annotations

from pathlib import Path

import pytest

from justx.config import DEFAULT_JUSTX_HOME
from justx.justfiles.discovery import DiscoveredPaths, JustxDiscovery


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


@pytest.fixture
def fake_user_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Set HOME to a temp directory for global justfile candidate resolution."""
    home = tmp_path / "fakehome"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
    monkeypatch.delenv("JUSTX_SKIP_GLOBAL_JUSTFILE", raising=False)
    return home


def test_discover_empty(tmp_home, tmp_cwd, fake_user_home):
    tmp_cwd.mkdir()
    result = JustxDiscovery().discover(cwd=tmp_cwd, justx_home=tmp_home)
    assert result.global_paths == []
    assert result.local_paths == []


def test_justx_home_justfile_is_ignored(tmp_home, tmp_cwd, fake_user_home):
    """A bare 'justfile' inside ~/.justx should NOT be discovered."""
    tmp_cwd.mkdir()
    _write_justfile(tmp_home / "justfile")

    result = JustxDiscovery().discover(cwd=tmp_cwd, justx_home=tmp_home)

    assert result.global_paths == []
    assert result.local_paths == []


def test_discover_local_root_justfile(tmp_home, tmp_cwd, fake_user_home):
    tmp_cwd.mkdir()
    _write_justfile(tmp_cwd / "justfile")

    result = JustxDiscovery().discover(cwd=tmp_cwd, justx_home=tmp_home)

    assert result.global_paths == []
    assert result.local_paths == [tmp_cwd / "justfile"]


def test_discover_global_just_files(tmp_home, tmp_cwd, fake_user_home):
    tmp_cwd.mkdir()
    _write_justfile(tmp_home / "ops.just")
    _write_justfile(tmp_home / "dev.just")

    result = JustxDiscovery().discover(cwd=tmp_cwd, justx_home=tmp_home)

    assert set(result.global_paths) == {tmp_home / "ops.just", tmp_home / "dev.just"}
    assert result.local_paths == []


def test_discover_local_just_files(tmp_home, tmp_cwd, fake_user_home):
    tmp_cwd.mkdir()
    _write_justfile(tmp_cwd / ".justx" / "ci.just")

    result = JustxDiscovery().discover(cwd=tmp_cwd, justx_home=tmp_home)

    assert result.global_paths == []
    assert result.local_paths == [tmp_cwd / ".justx" / "ci.just"]


def test_discover_global_justfile_comes_before_just_files(tmp_home, fake_user_home):
    """The global justfile (from just's locations) should appear before named sources."""
    cwd = fake_user_home / "project"
    cwd.mkdir()
    global_justfile = fake_user_home / ".config" / "just" / "justfile"
    _write_justfile(global_justfile)
    _write_justfile(tmp_home / "ops.just")

    result = JustxDiscovery().discover(cwd=cwd, justx_home=tmp_home)

    assert result.global_paths[0] == global_justfile
    assert result.global_paths[1] == tmp_home / "ops.just"


def test_discover_local_root_comes_before_just_files(tmp_home, tmp_cwd, fake_user_home):
    tmp_cwd.mkdir()
    _write_justfile(tmp_cwd / "justfile")
    _write_justfile(tmp_cwd / ".justx" / "ci.just")

    result = JustxDiscovery().discover(cwd=tmp_cwd, justx_home=tmp_home)

    assert result.local_paths[0] == tmp_cwd / "justfile"
    assert result.local_paths[1] == tmp_cwd / ".justx" / "ci.just"


def test_justx_home_env_var(monkeypatch, tmp_path):
    home = tmp_path / "fakehome"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)

    justx_home = tmp_path / "custom_home"
    _write_justfile(justx_home / "dev.just")
    cwd = tmp_path / "cwd"
    cwd.mkdir()

    monkeypatch.setenv("JUSTX_HOME", str(justx_home))
    result = JustxDiscovery().discover(cwd=cwd)

    assert result.global_paths == [justx_home / "dev.just"]


def test_justx_home_arg_takes_precedence_over_env_var(monkeypatch, tmp_path):
    home = tmp_path / "fakehome"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)

    env_home = tmp_path / "env_home"
    _write_justfile(env_home / "ops.just")

    arg_home = tmp_path / "arg_home"
    _write_justfile(arg_home / "dev.just")

    cwd = tmp_path / "cwd"
    cwd.mkdir()

    monkeypatch.setenv("JUSTX_HOME", str(env_home))
    result = JustxDiscovery().discover(cwd=cwd, justx_home=arg_home)

    assert result.global_paths == [arg_home / "dev.just"]


def test_discover_global_justfile_extension(tmp_home, tmp_cwd, fake_user_home):
    tmp_cwd.mkdir()
    _write_justfile(tmp_home / "ops.justfile")
    _write_justfile(tmp_home / "dev.justfile")

    result = JustxDiscovery().discover(cwd=tmp_cwd, justx_home=tmp_home)

    assert set(result.global_paths) == {tmp_home / "ops.justfile", tmp_home / "dev.justfile"}
    assert result.local_paths == []


def test_discover_local_justfile_extension(tmp_home, tmp_cwd, fake_user_home):
    tmp_cwd.mkdir()
    _write_justfile(tmp_cwd / ".justx" / "ci.justfile")

    result = JustxDiscovery().discover(cwd=tmp_cwd, justx_home=tmp_home)

    assert result.global_paths == []
    assert result.local_paths == [tmp_cwd / ".justx" / "ci.justfile"]


def test_default_home_is_dot_justx():
    assert Path.home() / ".justx" == DEFAULT_JUSTX_HOME


def test_returns_discovered_paths_instance(tmp_home, tmp_cwd, fake_user_home):
    tmp_cwd.mkdir()
    result = JustxDiscovery().discover(cwd=tmp_cwd, justx_home=tmp_home)
    assert isinstance(result, DiscoveredPaths)


# --- Global justfile discovery (just's locations) ---


def test_global_justfile_from_xdg_config_home(fake_user_home, tmp_home):
    cwd = fake_user_home / "project"
    cwd.mkdir()
    justfile = fake_user_home / ".config" / "just" / "justfile"
    _write_justfile(justfile)

    result = JustxDiscovery().discover(cwd=cwd, justx_home=tmp_home)

    assert justfile in result.global_paths


def test_global_justfile_from_home_justfile(fake_user_home, tmp_home):
    cwd = fake_user_home / "project"
    cwd.mkdir()
    justfile = fake_user_home / "justfile"
    _write_justfile(justfile)

    result = JustxDiscovery().discover(cwd=cwd, justx_home=tmp_home)

    assert justfile in result.global_paths


def test_global_justfile_from_home_dot_justfile(fake_user_home, tmp_home):
    cwd = fake_user_home / "project"
    cwd.mkdir()
    justfile = fake_user_home / ".justfile"
    _write_justfile(justfile)

    result = JustxDiscovery().discover(cwd=cwd, justx_home=tmp_home)

    assert justfile in result.global_paths


def test_global_justfile_xdg_takes_precedence(fake_user_home, tmp_home):
    """XDG location should win over ~/justfile."""
    cwd = fake_user_home / "project"
    cwd.mkdir()
    xdg_justfile = fake_user_home / ".config" / "just" / "justfile"
    home_justfile = fake_user_home / "justfile"
    _write_justfile(xdg_justfile)
    _write_justfile(home_justfile)

    result = JustxDiscovery().discover(cwd=cwd, justx_home=tmp_home)

    assert xdg_justfile in result.global_paths
    assert home_justfile not in result.global_paths


def test_global_justfile_xdg_env_override(monkeypatch, tmp_path):
    home = tmp_path / "fakehome"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))
    monkeypatch.delenv("JUSTX_SKIP_GLOBAL_JUSTFILE", raising=False)

    custom_xdg = tmp_path / "custom_xdg"
    justfile = custom_xdg / "just" / "justfile"
    _write_justfile(justfile)
    monkeypatch.setenv("XDG_CONFIG_HOME", str(custom_xdg))

    justx_home = tmp_path / "justx_home"
    cwd = tmp_path / "cwd"
    cwd.mkdir()

    result = JustxDiscovery().discover(cwd=cwd, justx_home=justx_home)

    assert justfile in result.global_paths
