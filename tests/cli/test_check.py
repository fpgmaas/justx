from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from justx.cli.main import main
from tests.utils import run_within_dir


def test_check_just_not_found(tmp_path: Path) -> None:
    runner = CliRunner()
    with patch("justx.cli.commands.check.shutil.which", return_value=None), run_within_dir(tmp_path):
        result = runner.invoke(main, ["check"])
    assert result.exit_code == 1


def test_check_just_found_no_sources(tmp_path: Path) -> None:
    runner = CliRunner()
    with patch("justx.cli.commands.check.shutil.which", return_value="/usr/bin/just"), run_within_dir(tmp_path):
        result = runner.invoke(main, ["check"], env={"JUSTX_HOME": str(tmp_path)})
    assert result.exit_code == 0
    assert "just" in result.output
    assert "0 global, 0 local" in result.output


def test_check_just_found_with_sources(local_dir: Path, global_dir: Path) -> None:
    runner = CliRunner()
    with run_within_dir(local_dir):
        result = runner.invoke(main, ["check"])
    assert result.exit_code == 0
    assert "global" in result.output
    assert "local" in result.output


def test_check_verbose_shows_paths(local_dir: Path, global_dir: Path) -> None:
    runner = CliRunner()
    with run_within_dir(local_dir):
        result = runner.invoke(main, ["check", "-v"])
    assert result.exit_code == 0
    assert "justfile" in result.output


def test_check_verbose_shows_recipes(local_dir: Path, global_dir: Path) -> None:
    runner = CliRunner()
    with run_within_dir(local_dir):
        result = runner.invoke(main, ["check", "-v"])
    assert result.exit_code == 0
    assert "Sources & recipes" in result.output


def test_check_counts_module_justfiles(project_with_modules: Path) -> None:
    runner = CliRunner()
    with run_within_dir(project_with_modules):
        result = runner.invoke(main, ["check"])
    assert result.exit_code == 0
    assert "4 local" in result.output


def test_check_verbose_lists_module_justfile_paths(project_with_modules: Path) -> None:
    runner = CliRunner()
    with run_within_dir(project_with_modules):
        result = runner.invoke(main, ["check", "-v"])
    assert result.exit_code == 0
    assert "bar/justfile" in result.output
    assert "bar/baz/justfile" in result.output
    assert "groups.just" in result.output
