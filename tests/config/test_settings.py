from __future__ import annotations

from pathlib import Path

import pytest

from justx.config.settings.discovery import DEFAULT_EXCLUDE
from justx.config.settings.main import (
    ConfigError,
    find_config_path,
    load_settings,
)


def _write_toml(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path


# --- Defaults (no config file) ---


def test_defaults_when_no_config_file(tmp_path: Path) -> None:
    settings = load_settings(cwd=tmp_path)
    assert settings.discovery.recursive is False
    assert settings.discovery.max_depth == 3
    assert settings.discovery.exclude == DEFAULT_EXCLUDE
    assert settings.discovery.extend_exclude == []


# --- find_config_path ---


def test_find_config_path_returns_path_when_present(tmp_path: Path) -> None:
    (tmp_path / "justx.toml").write_text("")
    assert find_config_path(tmp_path) == tmp_path / "justx.toml"


def test_find_config_path_returns_none_when_missing(tmp_path: Path) -> None:
    assert find_config_path(tmp_path) is None


# --- Loading from justx.toml ---


def test_load_settings_from_justx_toml(tmp_path: Path) -> None:
    _write_toml(tmp_path / "justx.toml", "[discovery]\nrecursive = true\nmax_depth = 5\n")
    settings = load_settings(cwd=tmp_path)
    assert settings.discovery.recursive is True
    assert settings.discovery.max_depth == 5


def test_load_settings_preserves_unset_defaults(tmp_path: Path) -> None:
    _write_toml(tmp_path / "justx.toml", "[discovery]\nrecursive = true\n")
    settings = load_settings(cwd=tmp_path)
    assert settings.discovery.max_depth == 3
    assert settings.discovery.exclude == DEFAULT_EXCLUDE
    assert settings.discovery.extend_exclude == []


# --- Errors ---


def test_invalid_toml_raises_config_error(tmp_path: Path) -> None:
    _write_toml(tmp_path / "justx.toml", "[discovery\n")
    with pytest.raises(ConfigError) as exc_info:
        load_settings(cwd=tmp_path)
    assert exc_info.value.path == tmp_path / "justx.toml"


def test_invalid_schema_raises_config_error(tmp_path: Path) -> None:
    _write_toml(tmp_path / "justx.toml", "[discovery]\nrecursive = 42\n")
    with pytest.raises(ConfigError):
        load_settings(cwd=tmp_path)


def test_unknown_top_level_key_raises_config_error(tmp_path: Path) -> None:
    _write_toml(tmp_path / "justx.toml", "bogus = true\n")
    with pytest.raises(ConfigError):
        load_settings(cwd=tmp_path)
