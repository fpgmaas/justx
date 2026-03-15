from __future__ import annotations

from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture(autouse=True)
def _auto_test_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("JUSTX_HOME", str(DATA_DIR / "global"))
    monkeypatch.setenv("JUSTX_SKIP_GLOBAL_JUSTFILE", "1")
    monkeypatch.setenv("COLUMNS", "200")


@pytest.fixture
def example_justfile() -> Path:
    return DATA_DIR / "local" / "justfile"


@pytest.fixture
def local_dir() -> Path:
    return DATA_DIR / "local"


@pytest.fixture
def global_dir() -> Path:
    return DATA_DIR / "global"
