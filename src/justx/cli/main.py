from __future__ import annotations

import click

from justx.cli.commands import check_cmd, init_cmd, list_cmd, run_cmd
from justx.justfiles.loader import JustxLoader
from justx.tui import run_tui


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context) -> None:
    """justx — a TUI launcher for just recipes."""
    if ctx.invoked_subcommand is None:
        config = JustxLoader().load()
        run_tui(config)


main.add_command(list_cmd)
main.add_command(run_cmd)
main.add_command(check_cmd)
main.add_command(init_cmd)
