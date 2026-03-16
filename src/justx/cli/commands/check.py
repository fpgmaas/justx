from __future__ import annotations

import shutil
import sys

import click
from rich.console import Console
from rich.markup import escape

from justx.config import LocalSettings, SettingsLoader
from justx.justfiles.discovery import DiscoveredPaths, JustxDiscovery
from justx.justfiles.loader import JustxLoader


@click.command("check")
@click.option("-v", "--verbose", is_flag=True, default=False, help="Show detailed discovery, sources, and settings.")
def check_cmd(verbose: bool) -> None:
    """Verify that just is installed and show discovered justfile locations."""
    console = Console()
    _check_just_binary(console)

    loader = SettingsLoader()
    settings = loader.load()
    paths = JustxDiscovery(config=settings.discovery).discover()

    _print_summary(console, paths)
    _print_config_paths(console, loader)

    if not verbose:
        return

    _print_discovered_paths(console, paths)
    _print_sources_and_recipes(console, settings)
    _print_verbose_settings(console, settings)


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


def _print_config_paths(console: Console, loader: SettingsLoader) -> None:
    console.print("[bold]config:[/bold]")
    if loader.global_path:
        console.print(f"  [dim]global:[/dim] [cyan]{escape(str(loader.global_path))}[/cyan]")
    else:
        console.print("  [dim]global: (not found)[/dim]")
    if loader.local_path:
        console.print(f"  [dim]local:[/dim]  [cyan]{escape(str(loader.local_path))}[/cyan]")
    else:
        console.print("  [dim]local:  (not found)[/dim]")


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


def _print_sources_and_recipes(console: Console, settings: LocalSettings) -> None:
    config = JustxLoader(config=settings.discovery).load()
    all_sources = [*config.global_sources, *config.local_sources]
    if all_sources:
        console.print("\n[bold]Sources & recipes:[/bold]")
        for source in all_sources:
            source.pretty_print(console)


def _print_verbose_settings(console: Console, settings: LocalSettings) -> None:
    console.print("[bold]Settings:[/bold]")
    data = settings.model_dump()
    _print_settings(console, data)


def _print_settings(console: Console, data: dict | list | object, indent: int = 1) -> None:
    """Print settings with consistent styling (dim keys, cyan values)."""
    prefix = "  " * indent
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, dict):
                console.print(f"{prefix}[dim]{escape(str(key))}:[/dim]")
                _print_settings(console, value, indent + 1)
            elif isinstance(value, list):
                console.print(f"{prefix}[dim]{escape(str(key))}:[/dim] [cyan]{escape(repr(value))}[/cyan]")
            else:
                console.print(f"{prefix}[dim]{escape(str(key))}:[/dim] [cyan]{escape(str(value))}[/cyan]")
