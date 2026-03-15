from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from justx.config import get_global_justfile_candidates, get_justx_home


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
        global_justfile = self._discover_default_global_justfile()
        if global_justfile is not None:
            paths.append(global_justfile)
        paths.extend(self._scan_just_files(home))
        return paths

    def _discover_default_global_justfile(self) -> Path | None:
        """Find the global justfile using just's search order."""
        for candidate in get_global_justfile_candidates():
            if candidate.is_file():
                return candidate
        return None

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
        return sorted([*directory.glob("*.just"), *directory.glob("*.justfile")])
