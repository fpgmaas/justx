from __future__ import annotations

import sys

import click

from justx.justfiles.exceptions import JustNotFoundError
from justx.justfiles.loader import JustxLoader
from justx.justfiles.models import Source


@click.command("run")
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

    Under the hood, justx resolves the justfile path and delegates to just directly.
    For example, `justx run -g -G docker build <image-tag>` is equivalent to running
    `just --justfile ~/.justx/docker.just --working-directory=. build <image-tag>`.
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


def _find_source(sources: list[Source], group: str | None) -> Source | None:
    for source in sources:
        if group is None and source.name in ("justfile", "Justfile"):
            return source
        if group is not None and source.name == group:
            return source
    return None
