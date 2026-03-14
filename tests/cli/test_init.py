from __future__ import annotations

import urllib.error
from pathlib import Path
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from justx.cli.main import main

FAKE_FILES = [
    {"name": "docker.just", "download_url": "https://example.com/docker.just"},
    {"name": "git.just", "download_url": "https://example.com/git.just"},
    {"name": "uv.just", "download_url": "https://example.com/uv.just"},
]

runner = CliRunner()


# ---------------------------------------------------------------------------
# justx init (no flag)
# ---------------------------------------------------------------------------


def test_init_creates_user_just(tmp_path: Path) -> None:
    result = runner.invoke(main, ["init"], input="y\n", env={"JUSTX_HOME": str(tmp_path)})
    assert result.exit_code == 0
    user_just = tmp_path / "user.just"
    assert user_just.exists()
    assert "greet" in user_just.read_text()


def test_init_aborted(tmp_path: Path) -> None:
    result = runner.invoke(main, ["init"], input="n\n", env={"JUSTX_HOME": str(tmp_path)})
    assert result.exit_code == 0
    assert "Aborted" in result.output
    assert not (tmp_path / "user.just").exists()


def test_init_skips_existing_user_just(tmp_path: Path) -> None:
    (tmp_path / "user.just").write_text("# existing\n")
    result = runner.invoke(main, ["init"], input="y\n", env={"JUSTX_HOME": str(tmp_path)})
    assert result.exit_code == 0
    assert "already exists" in result.output
    assert (tmp_path / "user.just").read_text() == "# existing\n"


# ---------------------------------------------------------------------------
# justx init --download-examples
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_fetch():
    with patch("justx.cli.commands.init._fetch_example_files", return_value=FAKE_FILES):
        yield


def test_download_examples_all_selected(tmp_path: Path, mock_fetch: None) -> None:
    with (
        patch("justx.cli.commands.init.urllib.request.urlretrieve") as mock_retrieve,
        patch("justx.cli.commands.init.questionary.checkbox") as mock_cb,
    ):
        mock_cb.return_value.ask.return_value = FAKE_FILES
        result = runner.invoke(main, ["init", "--download-examples"], input="y\n", env={"JUSTX_HOME": str(tmp_path)})
    assert result.exit_code == 0
    assert mock_retrieve.call_count == 3
    for f in FAKE_FILES:
        mock_retrieve.assert_any_call(f["download_url"], tmp_path / f["name"])
    assert not (tmp_path / "user.just").exists()


def test_download_examples_partial_selection(tmp_path: Path, mock_fetch: None) -> None:
    selected = [FAKE_FILES[0], FAKE_FILES[2]]  # docker.just and uv.just
    with (
        patch("justx.cli.commands.init.urllib.request.urlretrieve") as mock_retrieve,
        patch("justx.cli.commands.init.questionary.checkbox") as mock_cb,
    ):
        mock_cb.return_value.ask.return_value = selected
        result = runner.invoke(main, ["init", "--download-examples"], input="y\n", env={"JUSTX_HOME": str(tmp_path)})
    assert result.exit_code == 0
    assert mock_retrieve.call_count == 2


def test_download_examples_none_selected(tmp_path: Path, mock_fetch: None) -> None:
    with patch("justx.cli.commands.init.questionary.checkbox") as mock_cb:
        mock_cb.return_value.ask.return_value = []
        result = runner.invoke(main, ["init", "--download-examples"], input="y\n", env={"JUSTX_HOME": str(tmp_path)})
    assert result.exit_code == 0
    assert "No files selected" in result.output


def test_download_examples_skips_existing_file(tmp_path: Path, mock_fetch: None) -> None:
    (tmp_path / "docker.just").write_text("# existing\n")
    with (
        patch("justx.cli.commands.init.urllib.request.urlretrieve") as mock_retrieve,
        patch("justx.cli.commands.init.questionary.checkbox") as mock_cb,
    ):
        mock_cb.return_value.ask.return_value = FAKE_FILES
        result = runner.invoke(main, ["init", "--download-examples"], input="y\n", env={"JUSTX_HOME": str(tmp_path)})
    assert result.exit_code == 0
    assert "already exists" in result.output
    assert mock_retrieve.call_count == 2  # git.just and uv.just only


def test_download_examples_aborted(tmp_path: Path) -> None:
    with patch("justx.cli.commands.init._fetch_example_files") as mock_fetch_fn:
        result = runner.invoke(main, ["init", "--download-examples"], input="n\n", env={"JUSTX_HOME": str(tmp_path)})
    assert result.exit_code == 0
    assert "Aborted" in result.output
    mock_fetch_fn.assert_not_called()


def test_download_examples_network_error(tmp_path: Path) -> None:
    with patch(
        "justx.cli.commands.init._fetch_example_files",
        side_effect=urllib.error.URLError("connection refused"),
    ):
        result = runner.invoke(main, ["init", "--download-examples"], input="y\n", env={"JUSTX_HOME": str(tmp_path)})
    assert result.exit_code == 1
    assert "Could not fetch examples" in result.output


def test_download_examples_no_files_found(tmp_path: Path) -> None:
    with (
        patch("justx.cli.commands.init._fetch_example_files", return_value=[]),
        patch("justx.cli.commands.init.questionary.checkbox") as mock_cb,
    ):
        result = runner.invoke(main, ["init", "--download-examples"], input="y\n", env={"JUSTX_HOME": str(tmp_path)})
    assert result.exit_code == 0
    assert "No example files found" in result.output
    mock_cb.assert_not_called()
