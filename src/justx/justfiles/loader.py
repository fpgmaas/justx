from __future__ import annotations

from pathlib import Path

from justx.justfiles.discovery import JustxDiscovery
from justx.justfiles.models import JustxConfig, Scope, Source
from justx.justfiles.parser import JustfileParser


class JustxLoader:
    """Discovers and parses justfiles into a JustxConfig."""

    def __init__(self) -> None:
        self._discovery = JustxDiscovery()
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
            local_sources=self._parse_all(paths.local_paths, Scope.LOCAL),
        )

    def _parse_all(self, paths: list[Path], scope: Scope) -> list[Source]:
        sources = []
        for path in paths:
            sources.extend(self._parser.parse(path, scope))
        return sources
