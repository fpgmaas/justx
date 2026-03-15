from __future__ import annotations

from importlib.metadata import version

import click

from justx.cli.commands import check_cmd, init_cmd, list_cmd, run_cmd
from justx.config import get_settings
from justx.justfiles.loader import JustxLoader
from justx.tui import run_tui


def display_version(ctx: click.Context, _param: click.Parameter, value: bool) -> None:
    if not value or ctx.resilient_parsing:
        return
    click.echo(f"justx {version('justx')}")
    ctx.exit()


@click.group(invoke_without_command=True)
@click.option(
    "--version",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=display_version,
    help="Show version and exit.",
)
@click.pass_context
def main(ctx: click.Context) -> None:
    """justx — a TUI launcher for just recipes."""
    if ctx.invoked_subcommand is None:
        settings = get_settings()
        config = JustxLoader(config=settings.discovery).load()
        run_tui(config)


main.add_command(list_cmd)
main.add_command(run_cmd)
main.add_command(check_cmd)
main.add_command(init_cmd)
