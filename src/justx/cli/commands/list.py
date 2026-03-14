from __future__ import annotations

import click

from justx.justfiles.loader import JustxLoader
from justx.justfiles.models import Source


@click.command("list")
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
