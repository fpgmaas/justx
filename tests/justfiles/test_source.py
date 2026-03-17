from __future__ import annotations

from pathlib import Path

from justx.justfiles.models import Scope, Source

PROJECT_JUSTFILE = Path("/project") / "justfile"


def _source(
    scope: Scope = Scope.LOCAL,
    path: Path = PROJECT_JUSTFILE,
    module_path: str | None = None,
    root_justfile: Path | None = None,
) -> Source:
    return Source(
        scope=scope,
        path=path,
        recipes=[],
        module_path=module_path,
        root_justfile=root_justfile,
    )


def test_build_command_local_root():
    source = _source(scope=Scope.LOCAL)
    command = source._build_command("just", "build", [])
    assert command == ["just", "--justfile", str(PROJECT_JUSTFILE), "build"]


def test_build_command_local_root_with_args():
    source = _source(scope=Scope.LOCAL)
    command = source._build_command("just", "deploy", ["--force", "prod"])
    assert command == ["just", "--justfile", str(PROJECT_JUSTFILE), "deploy", "--force", "prod"]


def test_build_command_global(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    global_justfile = Path("/home") / "user" / ".justx" / "ops.just"
    source = _source(scope=Scope.GLOBAL, path=global_justfile)
    command = source._build_command("just", "status", [])
    assert command == [
        "just",
        "--justfile",
        str(global_justfile),
        "--working-directory",
        str(Path.cwd()),
        "status",
    ]


def test_build_command_module():
    source = _source(
        scope=Scope.LOCAL,
        path=Path("/project") / "docker.just",
        module_path="docker",
        root_justfile=PROJECT_JUSTFILE,
    )
    command = source._build_command("just", "build", [])
    assert command == ["just", "--justfile", str(PROJECT_JUSTFILE), "docker::build"]


def test_build_command_nested_module():
    source = _source(
        scope=Scope.LOCAL,
        path=Path("/project") / "infra" / "deploy.just",
        module_path="infra::deploy",
        root_justfile=PROJECT_JUSTFILE,
    )
    command = source._build_command("just", "staging", ["--dry-run"])
    assert command == ["just", "--justfile", str(PROJECT_JUSTFILE), "infra::deploy::staging", "--dry-run"]
