from __future__ import annotations

import os
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator


@contextmanager
def run_within_dir(path: Path) -> Generator[None, None, None]:
    """
    Utility function to run some code within a directory, and change back to the current directory afterwards.

    Example usage:

    ```
    with run_within_dir(directory):
        some_code()
    ```

    """
    oldpwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)
