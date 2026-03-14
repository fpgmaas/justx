from __future__ import annotations

from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture
def example_justfile() -> Path:
    return DATA_DIR / "local" / "justfile"


@pytest.fixture
def local_dir() -> Path:
    return DATA_DIR / "local"


@pytest.fixture
def global_dir() -> Path:
    return DATA_DIR / "global"


@pytest.fixture
def justx_home_env(monkeypatch: pytest.MonkeyPatch, global_dir: Path) -> None:
    monkeypatch.setenv("JUSTX_HOME", str(global_dir))
