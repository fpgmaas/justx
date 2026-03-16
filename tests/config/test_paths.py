from __future__ import annotations

from pathlib import Path

import pytest

from justx.config.paths import (
    DEFAULT_JUSTX_HOME,
    get_global_justfile_candidates,
    get_justx_home,
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
