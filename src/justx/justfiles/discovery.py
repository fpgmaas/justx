from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_JUIST_HOME = Path.home() / ".justx"


@dataclass
class DiscoveredPaths:
    global_paths: list[Path] = field(default_factory=list)
    local_paths: list[Path] = field(default_factory=list)


class JustxDiscovery:
    """Discovers justfile paths in global and local scopes."""

    def discover(self, cwd: Path | None = None, justx_home: Path | None = None) -> DiscoveredPaths:
        """Return all justfile paths found in the global and local scopes.

        Args:
            cwd: Local directory to scan. Defaults to the current working directory.
            justx_home: Global home directory. Defaults to $JUIST_HOME or ~/.justx.
        """
        home = self._resolve_home(justx_home)
        resolved_cwd = cwd or Path.cwd()

        return DiscoveredPaths(
            global_paths=self._discover_global(home),
            local_paths=self._discover_local(resolved_cwd),
        )

    def _resolve_home(self, justx_home: Path | None) -> Path:
        if justx_home is not None:
            return justx_home
        env = os.environ.get("JUIST_HOME")
        if env:
            return Path(env)
        return DEFAULT_JUIST_HOME

    def _discover_global(self, home: Path) -> list[Path]:
        paths: list[Path] = []
        root = home / "justfile"
        if root.exists():
            paths.append(root)
        paths.extend(self._scan_just_files(home))
        return paths

    def _discover_local(self, cwd: Path) -> list[Path]:
        paths: list[Path] = []
        root = cwd / "justfile"
        if root.exists():
            paths.append(root)
        paths.extend(self._scan_just_files(cwd / ".justx"))
        return paths

    def _scan_just_files(self, directory: Path) -> list[Path]:
        if not directory.is_dir():
            return []
        return sorted(directory.glob("*.just"))
