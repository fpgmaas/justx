from __future__ import annotations

from pydantic import BaseModel

DEFAULT_EXCLUDE = [
    "node_modules",
    ".venv",
    "venv",
    "target",
    ".git",
    "__pycache__",
    ".tox",
    "dist",
    "build",
]


class DiscoveryConfig(BaseModel):
    model_config = {"extra": "forbid"}
    recursive: bool = False
    max_depth: int = 3
    exclude: list[str] = DEFAULT_EXCLUDE.copy()
    extend_exclude: list[str] = []

    @property
    def effective_exclude(self) -> set[str]:
        return set(self.exclude) | set(self.extend_exclude)
