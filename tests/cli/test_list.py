from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from justx.cli.main import main
from tests.utils import run_within_dir


def test_list_no_sources(tmp_path: Path) -> None:
    runner = CliRunner()
    with run_within_dir(tmp_path):
        result = runner.invoke(main, ["list"], env={"JUSTX_HOME": str(tmp_path)})
    assert result.exit_code == 0
    assert "No justfiles found." in result.output


def test_list_both_scopes(local_dir: Path, global_dir: Path) -> None:
    runner = CliRunner()
    with run_within_dir(local_dir):
        result = runner.invoke(main, ["list"])
    assert result.exit_code == 0
    assert "greet" in result.output  # from local simple.just
    assert "setup" in result.output  # from global justfile
    assert "Greet someone" in result.output
    assert "Global setup task" in result.output


def test_list_global_only(local_dir: Path) -> None:
    runner = CliRunner()
    with run_within_dir(local_dir):
        result = runner.invoke(main, ["list", "-g"])
    assert result.exit_code == 0
    assert "setup" in result.output
    assert "Global setup task" in result.output
    assert "greet" not in result.output


def test_list_local_only(local_dir: Path) -> None:
    runner = CliRunner()
    with run_within_dir(local_dir):
        result = runner.invoke(main, ["list", "-l"])
    assert result.exit_code == 0
    assert "greet" in result.output
    assert "Greet someone" in result.output
    assert "Global setup task" not in result.output


def test_list_conflicting_flags(local_dir: Path) -> None:
    runner = CliRunner()
    with run_within_dir(local_dir):
        result = runner.invoke(main, ["list", "-g", "-l"])
    assert result.exit_code == 2
    assert "Cannot use -g and -l together." in result.output


def test_list_with_group_filter(local_dir: Path) -> None:
    runner = CliRunner()
    with run_within_dir(local_dir):
        result = runner.invoke(main, ["list", "-g", "setup"])
    assert result.exit_code == 0
    assert "setup" in result.output
    assert "Global setup task" in result.output
    assert "greet" not in result.output
