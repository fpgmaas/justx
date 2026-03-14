from __future__ import annotations

import os
from pathlib import Path

DEFAULT_JUSTX_HOME = Path.home() / ".justx"


def get_justx_home() -> Path:
    """Resolve the justx home directory: $JUSTX_HOME env var, or ~/.justx."""
    env = os.environ.get("JUSTX_HOME")
    if env:
        return Path(env)
    return DEFAULT_JUSTX_HOME
