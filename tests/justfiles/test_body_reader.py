from __future__ import annotations

from pathlib import Path

from justx.justfiles.body_reader import JustfileBodyReader


def test_read_simple_recipe(example_justfile):
    body = JustfileBodyReader().read(example_justfile, "script1")
    assert body == ["{{ python }} script1.py"]


def test_read_multiline_recipe(example_justfile):
    body = JustfileBodyReader().read(example_justfile, "bootstrap")
    assert len(body) == 3
    assert body[0] == "if test ! -e .venv; then {{ system_python }} -m venv .venv; fi"


def test_read_recipe_with_parameters(example_justfile):
    body = JustfileBodyReader().read(example_justfile, "script2")
    assert body == ["{{ python }} script2.py {{ ARGS }}"]


def test_read_nonexistent_recipe(example_justfile):
    body = JustfileBodyReader().read(example_justfile, "nonexistent")
    assert body == []


def test_read_nonexistent_file():
    body = JustfileBodyReader().read(Path("/nonexistent/justfile"), "build")
    assert body == []


def test_read_preserves_relative_indentation(tmp_path):
    justfile = tmp_path / "justfile"
    justfile.write_text("shebang:\n\t#!/usr/bin/env bash\n\tif true; then\n\t\techo nested\n\tfi\n")
    body = JustfileBodyReader().read(justfile, "shebang")
    assert body == [
        "#!/usr/bin/env bash",
        "if true; then",
        "\techo nested",
        "fi",
    ]


def test_read_quiet_recipe(tmp_path):
    justfile = tmp_path / "justfile"
    justfile.write_text("@quiet-recipe:\n  echo hello\n")
    body = JustfileBodyReader().read(justfile, "quiet-recipe")
    assert body == ["echo hello"]


def test_read_recipe_with_empty_body(tmp_path):
    justfile = tmp_path / "justfile"
    justfile.write_text("empty:\n\nother:\n  echo hi\n")
    body = JustfileBodyReader().read(justfile, "empty")
    assert body == []


def test_read_last_recipe_when_duplicates(tmp_path):
    justfile = tmp_path / "justfile"
    justfile.write_text("set allow-duplicate-recipes\n\nbuild:\n  echo first\n\nbuild:\n  echo second\n")
    body = JustfileBodyReader().read(justfile, "build")
    assert body == ["echo second"]
