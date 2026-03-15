from __future__ import annotations

from pathlib import Path

from justx.config.settings.discovery import DiscoveryConfig
from justx.justfiles.discovery import JustxDiscovery
from justx.justfiles.models import JustxConfig, Scope, Source
from justx.justfiles.parser import JustfileParser


class JustxLoader:
    """Discovers and parses justfiles into a JustxConfig."""

    def __init__(self, config: DiscoveryConfig | None = None) -> None:
        self._discovery = JustxDiscovery(config=config)
        self._parser = JustfileParser()

    def load(self, cwd: Path | None = None, justx_home: Path | None = None) -> JustxConfig:
        """Discover all justfiles and return a parsed JustxConfig.

        Args:
            cwd: Local directory to scan. Defaults to the current working directory.
            justx_home: Global home directory. Defaults to $JUSTX_HOME or ~/.justx.
        """
        resolved_cwd = cwd or Path.cwd()
        paths = self._discovery.discover(cwd=resolved_cwd, justx_home=justx_home)
        return JustxConfig(
            global_sources=self._parse_all(paths.global_paths, Scope.GLOBAL),
            local_sources=self._parse_all(paths.local_paths, Scope.LOCAL, resolved_cwd),
        )

    def _parse_all(self, paths: list[Path], scope: Scope, cwd: Path | None = None) -> list[Source]:
        return [self._parser.parse(path, scope, display_name=self._source_name(path, scope, cwd)) for path in paths]

    @staticmethod
    def _source_name(path: Path, scope: Scope, cwd: Path | None) -> str | None:
        """Compute a display name for a source.

        For global sources, returns None (parser falls back to stem).
        For local sources, returns the path relative to cwd with .justx/ segments
        and .just/.justfile extensions removed.
        """
        if scope == Scope.GLOBAL or cwd is None:
            return None
        rel = path.relative_to(cwd)
        parts = [p for p in rel.parts if p != ".justx"]
        # Strip .just/.justfile extension from the last part, but keep "justfile" as-is
        filename = parts[-1]
        for ext in (".just", ".justfile"):
            if filename.endswith(ext):
                filename = filename[: -len(ext)]
                break
        parts[-1] = filename
        return "/".join(parts)
