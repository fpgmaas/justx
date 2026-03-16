from __future__ import annotations

from pathlib import Path

import pytest

from justx.config.settings.discovery import DEFAULT_EXCLUDE
from justx.config.settings.main import (
    ConfigError,
    LocalSettings,
    SettingsLoader,
    get_settings,
    init_settings,
    load_settings,
    reset_settings,
)


def _write_toml(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return path


# --- Defaults (no config files) ---


def test_defaults_when_no_config_files(tmp_path: Path) -> None:
    settings = load_settings(cwd=tmp_path, justx_home=tmp_path / "empty")
    assert settings.discovery.recursive is False
    assert settings.discovery.max_depth == 3
    assert settings.discovery.exclude == DEFAULT_EXCLUDE
    assert settings.discovery.extend_exclude == []


# --- Global config from test data ---


def test_global_config_from_data_dir(global_dir: Path, tmp_path: Path) -> None:
    settings = load_settings(cwd=tmp_path, justx_home=global_dir)
    assert settings.discovery.recursive is True
    assert settings.discovery.max_depth == 5


def test_global_config_preserves_unset_defaults(global_dir: Path, tmp_path: Path) -> None:
    settings = load_settings(cwd=tmp_path, justx_home=global_dir)
    assert settings.discovery.exclude == DEFAULT_EXCLUDE
    assert settings.discovery.extend_exclude == []


# --- Local overrides global ---


def test_local_overrides_global(global_dir: Path, tmp_path: Path) -> None:
    _write_toml(tmp_path / ".justx" / "config.toml", "[discovery]\nmax_depth = 1\n")
    settings = load_settings(cwd=tmp_path, justx_home=global_dir)
    assert settings.discovery.recursive is True  # from global
    assert settings.discovery.max_depth == 1  # local wins


def test_justx_toml_used_as_local_config(global_dir: Path, tmp_path: Path) -> None:
    _write_toml(tmp_path / "justx.toml", "[discovery]\nmax_depth = 2\n")
    settings = load_settings(cwd=tmp_path, justx_home=global_dir)
    assert settings.discovery.max_depth == 2  # from justx.toml


def test_justx_toml_preferred_over_dot_justx(global_dir: Path, tmp_path: Path) -> None:
    _write_toml(tmp_path / "justx.toml", "[discovery]\nmax_depth = 2\n")
    _write_toml(tmp_path / ".justx" / "config.toml", "[discovery]\nmax_depth = 9\n")
    settings = load_settings(cwd=tmp_path, justx_home=global_dir)
    assert settings.discovery.max_depth == 2  # justx.toml wins


def test_local_does_not_clobber_unset_global_fields(global_dir: Path, tmp_path: Path) -> None:
    _write_toml(tmp_path / ".justx" / "config.toml", '[discovery]\nextend_exclude = ["vendor"]\n')
    settings = load_settings(cwd=tmp_path, justx_home=global_dir)
    assert settings.discovery.recursive is True  # from global
    assert settings.discovery.max_depth == 5  # from global
    assert settings.discovery.extend_exclude == ["vendor"]  # from local


# --- Global config uses [defaults.discovery] ---


def test_global_config_requires_defaults_namespace(tmp_path: Path) -> None:
    _write_toml(tmp_path / "config.toml", "[defaults.discovery]\nrecursive = true\n")
    settings = load_settings(cwd=tmp_path / "nowhere", justx_home=tmp_path)
    assert settings.discovery.recursive is True


def test_global_config_rejects_bare_discovery(tmp_path: Path) -> None:
    _write_toml(tmp_path / "config.toml", "[discovery]\nrecursive = true\n")
    with pytest.raises(ConfigError):
        load_settings(cwd=tmp_path / "nowhere", justx_home=tmp_path)


# --- Errors ---


def test_invalid_toml_raises_config_error(tmp_path: Path) -> None:
    _write_toml(tmp_path / "config.toml", "[discovery\n")
    with pytest.raises(ConfigError) as exc_info:
        load_settings(cwd=tmp_path / "nowhere", justx_home=tmp_path)
    assert exc_info.value.path == tmp_path / "config.toml"


def test_invalid_schema_raises_config_error(tmp_path: Path) -> None:
    _write_toml(tmp_path / "config.toml", "[defaults.discovery]\nrecursive = 42\n")
    with pytest.raises(ConfigError):
        load_settings(cwd=tmp_path / "nowhere", justx_home=tmp_path)


def test_unknown_top_level_key_raises_config_error(tmp_path: Path) -> None:
    _write_toml(tmp_path / "config.toml", "bogus = true\n")
    with pytest.raises(ConfigError):
        load_settings(cwd=tmp_path / "nowhere", justx_home=tmp_path)


# --- SettingsLoader ---


def test_loader_resolves_existing_paths(global_dir: Path, tmp_path: Path) -> None:
    _write_toml(tmp_path / ".justx" / "config.toml", "[discovery]\n")
    loader = SettingsLoader(cwd=tmp_path, justx_home=global_dir)
    assert loader.global_path == global_dir / "config.toml"
    assert loader.local_path == tmp_path / ".justx" / "config.toml"


def test_loader_paths_none_when_missing(tmp_path: Path) -> None:
    loader = SettingsLoader(cwd=tmp_path, justx_home=tmp_path / "empty")
    assert loader.global_path is None
    assert loader.local_path is None


# --- Cached access ---


def test_init_and_get_settings(global_dir: Path, tmp_path: Path) -> None:
    reset_settings()
    result = init_settings(cwd=tmp_path, justx_home=global_dir)
    assert result.discovery.recursive is True
    assert get_settings() is result


def test_get_settings_lazy_loads(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    reset_settings()
    monkeypatch.setenv("JUSTX_HOME", str(tmp_path / "empty"))
    monkeypatch.chdir(tmp_path)
    settings = get_settings()
    assert isinstance(settings, LocalSettings)


def test_reset_clears_cache(global_dir: Path, tmp_path: Path) -> None:
    reset_settings()
    first = init_settings(cwd=tmp_path, justx_home=global_dir)
    reset_settings()
    second = init_settings(cwd=tmp_path, justx_home=tmp_path / "empty")
    assert first is not second
    assert second.discovery.recursive is False  # defaults, no config file
