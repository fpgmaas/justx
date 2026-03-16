from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel, ValidationError

from justx.config.paths import get_justx_home, resolve_global_config_path, resolve_local_config_path
from justx.config.settings.discovery import DiscoveryConfig

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


class LocalSettings(BaseModel):
    model_config = {"extra": "forbid"}
    discovery: DiscoveryConfig = DiscoveryConfig()


class GlobalSettings(BaseModel):
    model_config = {"extra": "forbid"}
    defaults: LocalSettings = LocalSettings()


class ConfigError(Exception):
    """Raised when a config file cannot be parsed or validated."""

    def __init__(self, path: Path, cause: Exception) -> None:
        self.path = path
        self.cause = cause
        super().__init__(f"Error loading config from {path}: {cause}")


class SettingsLoader:
    """Loads and merges TOML config files into validated settings.

    Global config uses [defaults.discovery] to set defaults for local projects.
    Local config uses [discovery] directly.
    """

    def __init__(self, cwd: Path | None = None, justx_home: Path | None = None) -> None:
        justx_home = justx_home or get_justx_home()
        cwd = cwd or Path.cwd()
        self.global_path = resolve_global_config_path(justx_home)
        self.local_path = resolve_local_config_path(cwd)

    def load(self) -> LocalSettings:
        merged = LocalSettings().model_dump()

        if self.global_path is not None:
            global_data = self._load_file(self.global_path)
            global_settings = self._validate_global(global_data, self.global_path)
            self._deep_merge(merged, global_settings.defaults.model_dump(exclude_defaults=True))

        if self.local_path is not None:
            local_data = self._load_file(self.local_path)
            self._validate_local(local_data, self.local_path)
            self._deep_merge(merged, local_data)

        return self._validate_local(merged)

    @staticmethod
    def _load_file(path: Path) -> dict:
        """Load a TOML config file. Raises ConfigError on invalid TOML."""
        try:
            with open(path, "rb") as f:
                return tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            raise ConfigError(path, e) from e

    @staticmethod
    def _deep_merge(base: dict, override: dict) -> None:
        """Recursively merge override into base, mutating base in place."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                SettingsLoader._deep_merge(base[key], value)
            else:
                base[key] = value

    @staticmethod
    def _validate_global(data: dict, path: Path | None = None) -> GlobalSettings:
        try:
            return GlobalSettings.model_validate(data)
        except ValidationError as e:
            raise ConfigError(path or Path("<global>"), e) from e

    @staticmethod
    def _validate_local(data: dict, path: Path | None = None) -> LocalSettings:
        try:
            return LocalSettings.model_validate(data)
        except ValidationError as e:
            raise ConfigError(path or Path("<merged>"), e) from e


def load_settings(cwd: Path | None = None, justx_home: Path | None = None) -> LocalSettings:
    """Load settings by layering: defaults -> global config -> local config."""
    return SettingsLoader(cwd, justx_home).load()


# --- Cached access ---

_settings: LocalSettings | None = None


def init_settings(cwd: Path | None = None, justx_home: Path | None = None) -> LocalSettings:
    """Load and cache settings. Call once at CLI startup."""
    global _settings
    _settings = load_settings(cwd, justx_home)
    return _settings


def get_settings() -> LocalSettings:
    """Return cached settings, loading defaults if init wasn't called."""
    global _settings
    if _settings is None:
        _settings = load_settings()
    return _settings


def reset_settings() -> None:
    """Clear cached settings. Intended for tests."""
    global _settings
    _settings = None
