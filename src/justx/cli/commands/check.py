from __future__ import annotations

import shutil
import sys

import click
from rich.console import Console
from rich.markup import escape

from justx.justfiles.discovery import DiscoveredPaths, JustxDiscovery
from justx.justfiles.loader import JustxLoader


@click.command("check")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Show detailed discovery and sources.")
def check_cmd(verbose: bool) -> None:
    """Verify that just is installed and show discovered justfile locations."""
    console = Console()
    _check_just_binary(console)

    paths = JustxDiscovery().discover()

    _print_summary(console, paths)

    if not verbose:
        return

    _print_discovered_paths(console, paths)
    _print_sources_and_recipes(console)


def _check_just_binary(console: Console) -> None:
    just_bin = shutil.which("just")
    if just_bin is None:
        stderr = Console(stderr=True)
        stderr.print("[bold red]ERROR:[/bold red] just binary not found on PATH.")
        stderr.print("Install it from https://github.com/casey/just")
        sys.exit(1)
    console.print(f"[bold]just:[/bold]      [cyan]{escape(just_bin)}[/cyan] [green]✓[/green]")


def _print_summary(console: Console, paths: DiscoveredPaths) -> None:
    n_global = len(paths.global_paths)
    n_local = len(paths.local_paths)
    console.print(f"[bold]justfiles:[/bold] {n_global} global, {n_local} local")


def _print_discovered_paths(console: Console, paths: DiscoveredPaths) -> None:
    console.print()
    console.print("[bold]Global justfiles:[/bold]")
    if paths.global_paths:
        for path in paths.global_paths:
            console.print(f"  [cyan]{escape(str(path))}[/cyan]")
    else:
        console.print("  [dim](none)[/dim]")

    console.print("\n[bold]Local justfiles:[/bold]")
    if paths.local_paths:
        for path in paths.local_paths:
            console.print(f"  [cyan]{escape(str(path))}[/cyan]")
    else:
        console.print("  [dim](none)[/dim]")


def _print_sources_and_recipes(console: Console) -> None:
    config = JustxLoader().load()
    all_sources = [*config.global_sources, *config.local_sources]
    if all_sources:
        console.print("\n[bold]Sources & recipes:[/bold]")
        for source in all_sources:
            source.pretty_print(console)
