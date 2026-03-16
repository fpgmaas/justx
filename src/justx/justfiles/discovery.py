from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from justx.config import get_global_justfile_candidates, get_justx_home
from justx.config.settings.discovery import DiscoveryConfig


@dataclass
class DiscoveredPaths:
    global_paths: list[Path] = field(default_factory=list)
    local_paths: list[Path] = field(default_factory=list)


class JustxDiscovery:
    """Discovers justfile paths in global and local scopes."""

    def __init__(self, config: DiscoveryConfig | None = None) -> None:
        self._config = config or DiscoveryConfig()

    def discover(
        self,
        cwd: Path | None = None,
        justx_home: Path | None = None,
    ) -> DiscoveredPaths:
        """Return all justfile paths found in the global and local scopes.

        Args:
            cwd: Local directory to scan. Defaults to the current working directory.
            justx_home: Global home directory. Defaults to $JUSTX_HOME or ~/.justx.
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
        return get_justx_home()

    def _discover_global(self, home: Path) -> list[Path]:
        paths: list[Path] = []
        global_justfile = self._discover_default_global_justfile(home)
        if global_justfile is not None:
            paths.append(global_justfile)
        scanned = self._scan_just_files(home)
        paths.extend(path for path in scanned if path != global_justfile)
        return paths

    def _discover_default_global_justfile(self, justx_home: Path) -> Path | None:
        """Find the global justfile using just's search order."""
        for candidate in get_global_justfile_candidates(justx_home):
            if candidate.is_file():
                return candidate
        return None

    def _discover_local(self, cwd: Path) -> list[Path]:
        paths: list[Path] = []
        root = cwd / "justfile"
        if root.exists():
            paths.append(root)
        paths.extend(self._scan_just_files(cwd / ".justx"))
        if self._config.recursive:
            paths.extend(self._discover_local_recursive(cwd))
        return paths

    def _discover_local_recursive(self, cwd: Path) -> list[Path]:
        """Walk subdirectories of cwd up to max_depth, finding justfiles and .justx/ dirs."""
        paths: list[Path] = []
        config = self._config
        exclude = config.effective_exclude

        for current_dir, dirnames, _filenames in os.walk(cwd):
            current = Path(current_dir)
            depth = len(current.relative_to(cwd).parts)

            # Skip the root directory (handled by flat discovery)
            if depth == 0:
                # Filter dirnames in-place to control os.walk traversal
                dirnames[:] = [d for d in dirnames if d not in exclude and d != ".justx"]
                continue

            if depth > config.max_depth:
                dirnames.clear()
                continue

            # Filter dirnames for further traversal
            dirnames[:] = [d for d in dirnames if d not in exclude and d != ".justx"]

            justfile = current / "justfile"
            if justfile.exists():
                paths.append(justfile)
            paths.extend(self._scan_just_files(current / ".justx"))

        return sorted(paths)

    def _scan_just_files(self, directory: Path) -> list[Path]:
        if not directory.is_dir():
            return []
        return sorted([*directory.glob("*.just"), *directory.glob("*.justfile")])
