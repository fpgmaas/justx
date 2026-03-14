from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.markup import escape

from justx.justfiles.discovery import DEFAULT_JUSTX_HOME

USER_JUST_CONTENT = """\
# User-defined recipes for justx

# Greet someone by name
greet name:
    @echo "Hello, {{name}}! Welcome to justx."

# Show the current date and time
now:
    date
"""


@click.command("init")
@click.option(
    "--home",
    default=None,
    help="Override the justx home directory (default: ~/.justx).",
    type=click.Path(),
)
def init_cmd(home: str | None) -> None:
    """Initialize the ~/.justx directory with a sample user.just file."""
    console = Console()
    stderr = Console(stderr=True)

    justx_home = Path(home) if home else DEFAULT_JUSTX_HOME
    user_just = justx_home / "user.just"

    console.print(f"This will create [bold]{escape(str(justx_home))}[/bold] with a sample [cyan]user.just[/cyan].")

    if not click.confirm("Proceed?", default=True):
        console.print("Aborted.")
        sys.exit(0)

    if justx_home.exists() and user_just.exists():
        stderr.print(f"[yellow]WARNING:[/yellow] [cyan]{escape(str(user_just))}[/cyan] already exists. Skipping.")
        sys.exit(0)

    justx_home.mkdir(parents=True, exist_ok=True)
    user_just.write_text(USER_JUST_CONTENT)

    console.print(f"[green]Created[/green] {escape(str(user_just))}")
    console.print("\nRun [bold]justx[/bold] to launch the TUI.")
