from __future__ import annotations

from pathlib import Path

import pytest

from justx.config.paths import (
    DEFAULT_JUSTX_HOME,
    get_global_justfile_candidates,
    get_justx_home,
    resolve_global_config_path,
    resolve_local_config_path,
)


def test_default_justx_home_is_dot_justx(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("JUSTX_HOME", raising=False)
    assert get_justx_home() == DEFAULT_JUSTX_HOME


def test_justx_home_env_override(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("JUSTX_HOME", str(tmp_path / "custom"))
    assert get_justx_home() == tmp_path / "custom"


def test_skip_global_justfile_returns_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("JUSTX_SKIP_GLOBAL_JUSTFILE", "1")
    assert get_global_justfile_candidates() == []


def test_global_justfile_candidates_returns_five(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("JUSTX_SKIP_GLOBAL_JUSTFILE", raising=False)
    monkeypatch.delenv("XDG_CONFIG_HOME", raising=False)
    candidates = get_global_justfile_candidates()
    assert len(candidates) == 5
    assert all(isinstance(c, Path) for c in candidates)


def test_global_justfile_xdg_config_home_override(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("JUSTX_SKIP_GLOBAL_JUSTFILE", raising=False)
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))
    candidates = get_global_justfile_candidates()
    assert candidates[0] == tmp_path / "xdg" / "just" / "justfile"


# --- resolve_global_config_path ---


def test_resolve_global_config_path_found(tmp_path: Path) -> None:
    config = tmp_path / "config.toml"
    config.write_text("")
    assert resolve_global_config_path(tmp_path) == config


def test_resolve_global_config_path_missing(tmp_path: Path) -> None:
    assert resolve_global_config_path(tmp_path) is None


# --- resolve_local_config_path ---


def test_resolve_local_config_path_prefers_justx_toml(tmp_path: Path) -> None:
    (tmp_path / "justx.toml").write_text("")
    (tmp_path / ".justx").mkdir()
    (tmp_path / ".justx" / "config.toml").write_text("")
    assert resolve_local_config_path(tmp_path) == tmp_path / "justx.toml"


def test_resolve_local_config_path_falls_back_to_dot_justx(tmp_path: Path) -> None:
    (tmp_path / ".justx").mkdir()
    (tmp_path / ".justx" / "config.toml").write_text("")
    assert resolve_local_config_path(tmp_path) == tmp_path / ".justx" / "config.toml"


def test_resolve_local_config_path_none_when_missing(tmp_path: Path) -> None:
    assert resolve_local_config_path(tmp_path) is None
