from __future__ import annotations

import os
from pathlib import Path

DEFAULT_JUSTX_HOME = Path.home() / ".justx"


def get_justx_home() -> Path:
    """Resolve the justx home directory: $JUSTX_HOME env var, or ~/.justx."""
    env = os.environ.get("JUSTX_HOME")
    if env:
        return Path(env)
    return DEFAULT_JUSTX_HOME


def resolve_global_config_path(justx_home: Path) -> Path | None:
    """Return the global config path if it exists, else None."""
    path = justx_home / "config.toml"
    return path if path.is_file() else None


def resolve_local_config_path(cwd: Path) -> Path | None:
    """Find local config: justx.toml in cwd first, then .justx/config.toml."""
    candidates = [
        cwd / "justx.toml",
        cwd / ".justx" / "config.toml",
    ]
    return next((p for p in candidates if p.is_file()), None)


def get_global_justfile_candidates(justx_home: Path | None = None) -> list[Path]:
    """Return candidate paths for the global justfile, in just's search order.

    Falls back to justx_home/justfile and justx_home/.justfile when no
    standard global justfile is present.

    See https://just.systems/man/en/global-and-user-justfiles.html#global-justfile
    """
    if os.environ.get("JUSTX_SKIP_GLOBAL_JUSTFILE"):
        return []

    home = Path.home()
    xdg = os.environ.get("XDG_CONFIG_HOME")
    xdg_config = Path(xdg) if xdg else home / ".config"

    resolved_justx_home = justx_home or get_justx_home()

    return [
        xdg_config / "just" / "justfile",
        home / "justfile",
        home / ".justfile",
        resolved_justx_home / "justfile",
        resolved_justx_home / ".justfile",
    ]
