from __future__ import annotations

import click

from justx.config import load_settings
from justx.justfiles.loader import JustxLoader


@click.command("list")
@click.option("-g", "--global", "use_global", is_flag=True, default=False, help="List global sources only.")
@click.option("-l", "--local", "use_local", is_flag=True, default=False, help="List local sources only.")
@click.argument("source", required=False, default=None)
def list_cmd(use_global: bool, use_local: bool, source: str | None) -> None:
    """List recipes. Shows all scopes by default."""
    if use_global and use_local:
        raise click.UsageError("Cannot use -g and -l together.")  # noqa: TRY003

    settings = load_settings()
    config = JustxLoader(config=settings.discovery).load()

    if use_global:
        sources = config.global_sources
    elif use_local:
        sources = config.local_sources
    else:
        sources = [*config.local_sources, *config.global_sources]

    if source is not None:
        sources = [s for s in sources if s.display_name == source]

    if not sources:
        click.echo("No justfiles found.")
        return

    for source in sources:
        source.pretty_print()
