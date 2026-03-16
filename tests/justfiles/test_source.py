from __future__ import annotations

from pathlib import Path

from justx.justfiles.models import Scope, Source


def _source(
    scope: Scope = Scope.LOCAL,
    path: str = "/project/justfile",
    module_path: str | None = None,
    root_justfile: str | None = None,
) -> Source:
    return Source(
        display_name=module_path or "justfile",
        scope=scope,
        path=Path(path),
        recipes=[],
        module_path=module_path,
        root_justfile=Path(root_justfile) if root_justfile else None,
    )


def test_build_command_local_root():
    source = _source(scope=Scope.LOCAL)
    command = source._build_command("just", "build", [])
    assert command == ["just", "--justfile", str(Path("/project/justfile")), "build"]


def test_build_command_local_root_with_args():
    source = _source(scope=Scope.LOCAL)
    command = source._build_command("just", "deploy", ["--force", "prod"])
    assert command == ["just", "--justfile", str(Path("/project/justfile")), "deploy", "--force", "prod"]


def test_build_command_global(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    source = _source(scope=Scope.GLOBAL, path="/home/user/.justx/ops.just")
    command = source._build_command("just", "status", [])
    assert command == [
        "just",
        "--justfile",
        str(Path("/home/user/.justx/ops.just")),
        "--working-directory",
        str(Path.cwd()),
        "status",
    ]


def test_build_command_module():
    source = _source(
        scope=Scope.LOCAL,
        path="/project/docker.just",
        module_path="docker",
        root_justfile="/project/justfile",
    )
    command = source._build_command("just", "build", [])
    assert command == ["just", "--justfile", str(Path("/project/justfile")), "docker::build"]


def test_build_command_nested_module():
    source = _source(
        scope=Scope.LOCAL,
        path="/project/infra/deploy.just",
        module_path="infra::deploy",
        root_justfile="/project/justfile",
    )
    command = source._build_command("just", "staging", ["--dry-run"])
    assert command == ["just", "--justfile", str(Path("/project/justfile")), "infra::deploy::staging", "--dry-run"]
