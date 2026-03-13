from __future__ import annotations

from pathlib import Path

from justx.justfiles.discovery import JustxDiscovery
from justx.justfiles.models import JustxConfig, Scope, Source
from justx.justfiles.parser import JustfileParser


class JustxLoader:
    """Discovers and parses justfiles into a JustxConfig."""

    def __init__(
        self,
        discovery: JustxDiscovery | None = None,
        parser: JustfileParser | None = None,
    ) -> None:
        self._discovery = discovery or JustxDiscovery()
        self._parser = parser or JustfileParser()

    def load(self, cwd: Path | None = None, justx_home: Path | None = None) -> JustxConfig:
        """Discover all justfiles and return a parsed JustxConfig.

        Args:
            cwd: Local directory to scan. Defaults to the current working directory.
            justx_home: Global home directory. Defaults to $JUIST_HOME or ~/.justx.
        """
        paths = self._discovery.discover(cwd=cwd, justx_home=justx_home)
        return JustxConfig(
            global_sources=self._parse_all(paths.global_paths, Scope.global_),
            local_sources=self._parse_all(paths.local_paths, Scope.local),
        )

    def _parse_all(self, paths: list[Path], scope: Scope) -> list[Source]:
        return [self._parser.parse(p, scope) for p in paths]
