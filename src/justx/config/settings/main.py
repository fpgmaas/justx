from __future__ import annotations

import sys
from pathlib import Path

from pydantic import BaseModel, ValidationError

from justx.config.settings.discovery import DiscoveryConfig

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


class Settings(BaseModel):
    model_config = {"extra": "forbid"}
    discovery: DiscoveryConfig = DiscoveryConfig()


class ConfigError(Exception):
    """Raised when a config file cannot be parsed or validated."""

    def __init__(self, path: Path, cause: Exception) -> None:
        self.path = path
        self.cause = cause
        super().__init__(f"Error loading config from {path}: {cause}")


def find_config_path(cwd: Path | None = None) -> Path | None:
    """Find justx.toml in the given directory."""
    resolved = cwd or Path.cwd()
    path = resolved / "justx.toml"
    return path if path.is_file() else None


def load_settings(cwd: Path | None = None) -> Settings:
    """Load settings from justx.toml if present, otherwise return defaults."""
    config_path = find_config_path(cwd)
    if config_path is None:
        return Settings()
    return _load_and_validate(config_path)


def _load_and_validate(path: Path) -> Settings:
    try:
        with open(path, "rb") as file:
            data = tomllib.load(file)
    except tomllib.TOMLDecodeError as error:
        raise ConfigError(path, error) from error

    try:
        return Settings.model_validate(data)
    except ValidationError as error:
        raise ConfigError(path, error) from error
