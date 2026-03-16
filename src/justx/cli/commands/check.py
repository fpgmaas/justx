from __future__ import annotations

import shutil
import sys
from pathlib import Path

import click
from rich.console import Console
from rich.markup import escape

from justx.justfiles.loader import JustxLoader
from justx.justfiles.models import JustxConfig, Source


@click.command("check")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Show detailed discovery and sources.")
def check_cmd(verbose: bool) -> None:
    """Verify that just is installed and show discovered justfile locations."""
    console = Console()
    _check_just_binary(console)

    config = JustxLoader().load()

    _print_summary(console, config)

    if not verbose:
        return

    _print_discovered_paths(console, config)
    _print_sources_and_recipes(console, config)


def _check_just_binary(console: Console) -> None:
    just_bin = shutil.which("just")
    if just_bin is None:
        stderr = Console(stderr=True)
        stderr.print("[bold red]ERROR:[/bold red] just binary not found on PATH.")
        stderr.print("Install it from https://github.com/casey/just")
        sys.exit(1)
    console.print(f"[bold]just:[/bold]      [cyan]{escape(just_bin)}[/cyan] [green]✓[/green]")


def _unique_paths(sources: list[Source]) -> list[Path]:
    seen: set[Path] = set()
    paths: list[Path] = []
    for source in sources:
        if source.path not in seen:
            seen.add(source.path)
            paths.append(source.path)
    return paths


def _print_summary(console: Console, config: JustxConfig) -> None:
    n_global = len(_unique_paths(config.global_sources))
    n_local = len(_unique_paths(config.local_sources))
    console.print(f"[bold]justfiles:[/bold] {n_global} global, {n_local} local")


def _print_discovered_paths(console: Console, config: JustxConfig) -> None:
    global_paths = _unique_paths(config.global_sources)
    local_paths = _unique_paths(config.local_sources)

    console.print()
    console.print("[bold]Global justfiles:[/bold]")
    if global_paths:
        for path in global_paths:
            console.print(f"  [cyan]{escape(str(path))}[/cyan]")
    else:
        console.print("  [dim](none)[/dim]")

    console.print("\n[bold]Local justfiles:[/bold]")
    if local_paths:
        for path in local_paths:
            console.print(f"  [cyan]{escape(str(path))}[/cyan]")
    else:
        console.print("  [dim](none)[/dim]")


def _print_sources_and_recipes(console: Console, config: JustxConfig) -> None:
    all_sources = [*config.global_sources, *config.local_sources]
    if all_sources:
        console.print("\n[bold]Sources & recipes:[/bold]")
        for source in all_sources:
            source.pretty_print(console)
