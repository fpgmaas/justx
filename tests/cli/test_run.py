from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from justx.cli.main import main
from tests.utils import run_within_dir


def test_run_no_scope(tmp_path: Path) -> None:
    runner = CliRunner()
    with run_within_dir(tmp_path):
        result = runner.invoke(main, ["run", "greet"])
    assert result.exit_code == 2
    assert "Specify scope" in result.output


def test_run_conflicting_flags(tmp_path: Path) -> None:
    runner = CliRunner()
    with run_within_dir(tmp_path):
        result = runner.invoke(main, ["run", "-g", "-l", "greet"])
    assert result.exit_code == 2
    assert "Cannot use -g and -l together" in result.output


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


def test_run_success(global_dir: Path) -> None:
    runner = CliRunner()
    with run_within_dir(global_dir):
        result = runner.invoke(main, ["run", "-g", "setup", "-G", "setup"])
    assert result.exit_code == 0
