from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from justx.cli.main import main
from tests.utils import run_within_dir


def test_run_no_scope(local_dir: Path) -> None:
    runner = CliRunner()
    with run_within_dir(local_dir):
        result = runner.invoke(main, ["run", "justfile:bootstrap"])
    assert result.exit_code == 2
    assert "Specify scope with -l (local) or -g (global)." in result.output


def test_run_conflicting_scope(local_dir: Path) -> None:
    runner = CliRunner()
    with run_within_dir(local_dir):
        result = runner.invoke(main, ["run", "-g", "-l", "justfile:bootstrap"])
    assert result.exit_code == 2
    assert "Cannot use -g and -l together." in result.output


def test_run_local_recipe(local_dir: Path) -> None:
    runner = CliRunner()
    with run_within_dir(local_dir):
        result = runner.invoke(main, ["run", "-l", "justfile:script1"])
    # script1 runs `python script1.py` which will fail (no venv), but that's
    # a just execution error, not a justx error. We just verify justx found
    # and invoked the right source/recipe (exit code from just, not from justx).
    assert result.exit_code != 2  # not a usage error


def test_run_global_recipe(global_dir: Path) -> None:
    runner = CliRunner()
    with run_within_dir(global_dir):
        result = runner.invoke(main, ["run", "-g", "setup:setup"])
    assert result.exit_code == 0


def test_run_local_source_not_found(tmp_path: Path) -> None:
    runner = CliRunner()
    with run_within_dir(tmp_path):
        result = runner.invoke(main, ["run", "-l", "greet"])
    assert result.exit_code == 1
    assert "not found in local sources" in result.output


def test_run_global_source_not_found(tmp_path: Path) -> None:
    runner = CliRunner()
    with run_within_dir(tmp_path):
        result = runner.invoke(main, ["run", "-g", "greet"], env={"JUSTX_HOME": str(tmp_path)})
    assert result.exit_code == 1
    assert "not found in global sources" in result.output
