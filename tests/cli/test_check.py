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
    assert "(none)" in result.output


def test_check_just_found_with_sources(local_dir: Path, global_dir: Path) -> None:
    runner = CliRunner()
    with run_within_dir(local_dir):
        result = runner.invoke(main, ["check"])
    assert result.exit_code == 0
    assert "simple.just" in result.output  # local source
    assert "justfile" in result.output  # global source
