class JustNotFoundError(Exception):
    """Raised when the just binary is not found on PATH."""

    def __init__(self) -> None:
        super().__init__(
            "just binary not found on PATH. Install it before using justx, see https://github.com/casey/just "
        )


class JustInvocationError(Exception):
    """Raised when just exits with a non-zero status code."""

    def __init__(self, returncode: int, stderr: str) -> None:
        super().__init__(f"just exited with code {returncode}:\n{stderr}")
