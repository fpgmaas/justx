from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

import click
import questionary
from rich.console import Console
from rich.markup import escape

from justx.justfiles.discovery import DEFAULT_JUSTX_HOME

GITHUB_EXAMPLES_API = "https://api.github.com/repos/fpgmaas/ckit/contents/examples?ref=dev"

USER_JUST_CONTENT = """\
# User-defined recipes for justx

# Greet someone by name
greet name:
    @echo "Hello, {{name}}! Welcome to justx."

# Show the current date and time
now:
    date
"""


def _fetch_example_files() -> list[dict]:
    """Fetch list of *.just files from the ckit examples directory on GitHub."""
    req = urllib.request.Request(GITHUB_EXAMPLES_API, headers={"Accept": "application/vnd.github+json"})  # noqa: S310
    with urllib.request.urlopen(req, timeout=10) as resp:  # noqa: S310
        entries = json.loads(resp.read())
    return [e for e in entries if e.get("name", "").endswith(".just") and e.get("download_url")]


def _prompt_selection(files: list[dict]) -> list[dict]:
    """Interactively select files with all pre-checked; return chosen subset."""
    choices = [questionary.Choice(title=f["name"], value=f, checked=True) for f in files]
    selected = questionary.checkbox("Select example files to download:", choices=choices).ask()
    return selected or []


def _download_file(url: str, dest: Path, console: Console, stderr: Console) -> None:
    """Download a single file to dest, skipping if it already exists."""
    if dest.exists():
        stderr.print(f"[yellow]WARNING:[/yellow] {escape(str(dest))} already exists. Skipping.")
        return
    urllib.request.urlretrieve(url, dest)  # noqa: S310
    console.print(f"[green]Downloaded[/green] {escape(str(dest))}")


def _init_from_examples(justx_home: Path, console: Console, stderr: Console) -> None:
    """Download selected example justfiles from GitHub into justx_home."""
    console.print(f"This will download example justfiles into [bold]{escape(str(justx_home))}[/bold].")
    if not click.confirm("Proceed?", default=True):
        console.print("Aborted.")
        sys.exit(0)

    justx_home.mkdir(parents=True, exist_ok=True)

    console.print("Fetching example files from GitHub...")
    try:
        files = _fetch_example_files()
    except (urllib.error.URLError, OSError) as exc:
        stderr.print(f"[red]ERROR:[/red] Could not fetch examples: {exc}")
        sys.exit(1)

    if not files:
        console.print("[yellow]No example files found.[/yellow]")
        sys.exit(0)

    selected = _prompt_selection(files)
    if not selected:
        console.print("No files selected.")
        sys.exit(0)

    for f in selected:
        _download_file(f["download_url"], justx_home / f["name"], console, stderr)


def _init_default(justx_home: Path, console: Console, stderr: Console) -> None:
    """Create justx_home with a sample user.just file."""
    user_just = justx_home / "user.just"
    console.print(f"This will create [bold]{escape(str(justx_home))}[/bold] with a sample [cyan]user.just[/cyan].")
    if not click.confirm("Proceed?", default=True):
        console.print("Aborted.")
        sys.exit(0)

    if user_just.exists():
        stderr.print(f"[yellow]WARNING:[/yellow] [cyan]{escape(str(user_just))}[/cyan] already exists. Skipping.")
        sys.exit(0)

    justx_home.mkdir(parents=True, exist_ok=True)
    user_just.write_text(USER_JUST_CONTENT)
    console.print(f"[green]Created[/green] {escape(str(user_just))}")


@click.command("init")
@click.option(
    "--home",
    default=None,
    help="Override the justx home directory (default: ~/.justx).",
    type=click.Path(),
)
@click.option(
    "--download-examples",
    is_flag=True,
    default=False,
    help="Download example justfiles from the ckit GitHub repo into the justx home directory.",
)
def init_cmd(home: str | None, download_examples: bool) -> None:
    """Initialize the ~/.justx directory with a sample user.just file."""
    console = Console()
    stderr = Console(stderr=True)
    justx_home = Path(home) if home else DEFAULT_JUSTX_HOME

    if download_examples:
        _init_from_examples(justx_home, console, stderr)
    else:
        _init_default(justx_home, console, stderr)

    console.print("\nRun [bold]justx[/bold] to launch the TUI.")
