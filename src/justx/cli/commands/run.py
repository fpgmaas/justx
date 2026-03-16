from __future__ import annotations

import sys

import click

from justx.cli.commands.helpers import resolve_target
from justx.justfiles.exceptions import JustNotFoundError
from justx.justfiles.loader import JustxLoader


@click.command("run")
@click.option("-g", "--global", "use_global", is_flag=True, default=False, help="Run from global sources.")
@click.option("-l", "--local", "use_local", is_flag=True, default=False, help="Run from local sources.")
@click.argument("target")
@click.argument("args", nargs=-1)
def run_cmd(use_global: bool, use_local: bool, target: str, args: tuple[str, ...]) -> None:
    """Run a recipe. Specify scope with -l or -g.

    TARGET format: source::recipe (e.g. justfile::build, foo::lint, foo::baz::lint).
    """
    if use_global and use_local:
        raise click.UsageError("Cannot use -g and -l together.")  # noqa: TRY003
    if not use_global and not use_local:
        raise click.UsageError("Specify scope with -l (local) or -g (global).")  # noqa: TRY003

    config = JustxLoader().load()
    scope = "global" if use_global else "local"
    sources = config.global_sources if use_global else config.local_sources

    source, recipe = resolve_target(target, sources)

    if source is None:
        raise click.ClickException(f"'{target}' not found in {scope} sources.")  # noqa: TRY003

    try:
        sys.exit(source.run(recipe, args))
    except JustNotFoundError as e:
        raise click.ClickException(str(e)) from e
