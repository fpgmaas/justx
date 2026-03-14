from __future__ import annotations

import shutil
import sys

import click
from rich.console import Console
from rich.markup import escape

from justx.justfiles.discovery import JustxDiscovery


@click.command("check")
def check_cmd() -> None:
    """Verify that just is installed and show discovered justfile locations."""
    console = Console()
    stderr = Console(stderr=True)

    just_bin = shutil.which("just")
    if just_bin is None:
        stderr.print("[bold red]ERROR:[/bold red] just binary not found on PATH.")
        stderr.print("Install it from https://github.com/casey/just")
        sys.exit(1)

    console.print(f"[bold]just:[/bold] [cyan]{escape(just_bin)}[/cyan]")

    paths = JustxDiscovery().discover()

    console.print("\n[bold]Global justfiles:[/bold]")
    if paths.global_paths:
        for path in paths.global_paths:
            console.print(f"  {escape(str(path))}")
    else:
        console.print("  (none)")

    console.print("\n[bold]Local justfiles:[/bold]")
    if paths.local_paths:
        for path in paths.local_paths:
            console.print(f"  {escape(str(path))}")
    else:
        console.print("  (none)")
