from __future__ import annotations

import shutil
import sys

import click
from rich.console import Console
from rich.markup import escape

from justx.justfiles.exceptions import JustNotFoundError
from justx.justfiles.loader import JustxLoader
from justx.justfiles.models import Source
from justx.tui import run_tui


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context) -> None:
    """justx — a TUI launcher for just recipes."""
    if ctx.invoked_subcommand is None:
        config = JustxLoader().load()
        run_tui(config)


@main.command("list")
@click.option("-g", "--global", "global_only", is_flag=True, default=False, help="Show global sources only.")
@click.option("-l", "--local", "local_only", is_flag=True, default=False, help="Show local sources only.")
def list_cmd(global_only: bool, local_only: bool) -> None:
    """List all discovered groups and their recipes."""
    if global_only and local_only:
        raise click.UsageError("Cannot use -g and -l together.")  # noqa: TRY003

    config = JustxLoader().load()

    sources: list[Source] = []

    if not global_only:
        sources.extend(config.local_sources)

    if not local_only:
        sources.extend(config.global_sources)

    if not sources:
        click.echo("No justfiles found.")
        return

    for source in sources:
        source.pretty_print()


@main.command("run")
@click.option("-g", "--global", "use_global", is_flag=True, default=False, help="Target global scope.")
@click.option("-l", "--local", "use_local", is_flag=True, default=False, help="Target local scope.")
@click.option(
    "-G",
    "--group",
    "group",
    default=None,
    metavar="GROUP",
    help="Justfile group name. Defaults to root justfile if omitted.",
)
@click.argument("recipe")
@click.argument("args", nargs=-1)
def run_cmd(use_global: bool, use_local: bool, group: str | None, recipe: str, args: tuple[str, ...]) -> None:
    """Run a recipe without the TUI.

    Exactly one of -l (local) or -g (global) is required.
    Use -G to target a named group; omit for the root justfile.
    """
    if use_global and use_local:
        raise click.UsageError("Cannot use -g and -l together.")  # noqa: TRY003
    if not use_global and not use_local:
        raise click.UsageError("Specify scope: -l (local) or -g (global).")  # noqa: TRY003

    config = JustxLoader().load()
    sources = config.global_sources if use_global else config.local_sources
    source = _find_source(sources, group)

    scope = "global" if use_global else "local"
    label = group or "root justfile"
    if source is None:
        raise click.ClickException(f"'{label}' not found in {scope} sources.")  # noqa: TRY003

    try:
        sys.exit(source.run(recipe, args))
    except JustNotFoundError as e:
        raise click.ClickException(str(e)) from e


@main.command("check")
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

    config = JustxLoader().load()

    console.print("\n[bold]Global justfiles:[/bold]")
    if config.global_sources:
        for source in config.global_sources:
            console.print(f"  {escape(str(source.path))}")
    else:
        console.print("  (none)")

    console.print("\n[bold]Local justfiles:[/bold]")
    if config.local_sources:
        for source in config.local_sources:
            console.print(f"  {escape(str(source.path))}")
    else:
        console.print("  (none)")


def _find_source(sources: list[Source], group: str | None) -> Source | None:
    for source in sources:
        if group is None and source.name in ("justfile", "Justfile"):
            return source
        if group is not None and source.name == group:
            return source
    return None
