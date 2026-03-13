import click

from justx.justfiles.loader import JustxLoader
from justx.tui import run_tui


@click.command()
def main() -> None:
    config = JustxLoader().load()

    click.echo("=== Global files ===")
    for source in config.global_sources:
        click.echo(f"  [{source.name}] {source.path}")

    click.echo("\n=== Local files ===")
    for source in config.local_sources:
        click.echo(f"  [{source.name}] {source.path}")

    click.echo("\n=== Parsed config ===")
    click.echo(config.model_dump_json(indent=2))

    run_tui(config)
