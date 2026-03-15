from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

from justx.justfiles.exceptions import JustInvocationError, JustNotFoundError
from justx.justfiles.models import Parameter, ParameterKind, Recipe, RecipeDefault, Scope, Source, WorkingDirMode


class JustfileParser:
    """Parses justfiles into Source models by invoking just."""

    def parse(self, path: Path, scope: Scope) -> Source:
        """Parse a justfile and return a Source.

        Raises:
            FileNotFoundError: if the justfile does not exist.
            JustNotFoundError: if the just binary is not on PATH.
            JustInvocationError: if just exits with a non-zero status.
        """
        if not path.exists():
            raise FileNotFoundError(f"Justfile not found: {path}")  # noqa: TRY003

        binary = self._require_just()
        data = self._dump(binary, path)
        recipes = [self._parse_recipe(r) for r in data.get("recipes", {}).values()]
        working_dir_mode = self._parse_working_dir_mode(path)
        name = path.stem.replace(".", "")

        return Source(name=name, scope=scope, path=path, recipes=recipes, working_dir_mode=working_dir_mode)

    def _parse_working_dir_mode(self, path: Path) -> WorkingDirMode:
        _DIRECTIVE_RE = re.compile(r"#\s*justx:\s*working-directory\s*=\s*(\S+)")

        text = path.read_text()
        m = _DIRECTIVE_RE.search(text)
        if m and m.group(1) == "justfile":
            return WorkingDirMode.JUSTFILE
        return WorkingDirMode.CWD

    def _require_just(self) -> str:
        binary = shutil.which("just")
        if binary is None:
            raise JustNotFoundError
        return binary

    def _dump(self, binary: str, path: Path) -> dict:
        result = subprocess.run(
            [binary, "--dump", "--dump-format", "json", "--justfile", str(path)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            raise JustInvocationError(result.returncode, result.stderr.strip())
        return json.loads(result.stdout)

    def _parse_recipe(self, raw: dict) -> Recipe:
        parameters = [self._parse_parameter(p) for p in raw.get("parameters", [])]
        dependencies = [dep["recipe"] for dep in raw.get("dependencies", [])]
        groups = [attr["group"] for attr in raw.get("attributes", []) if "group" in attr]
        return Recipe(
            name=raw["name"],
            doc=raw.get("doc"),
            parameters=parameters,
            dependencies=dependencies,
            groups=groups,
        )

    def _parse_parameter(self, raw: dict) -> Parameter:
        raw_default = raw.get("default")
        if raw_default is None:
            default = None
            has_default = False
        else:
            default = RecipeDefault(
                value=raw_default,
                expression=not isinstance(raw_default, str),
            )
            has_default = True
        kind = self._parameter_kind(raw["kind"], has_default)
        return Parameter(name=raw["name"], default=default, kind=kind)

    @staticmethod
    def _parameter_kind(just_kind: str, has_default: bool) -> ParameterKind:
        if just_kind in ("star", "plus"):
            return ParameterKind.VARIADIC
        if has_default:
            return ParameterKind.OPTIONAL
        return ParameterKind.REQUIRED
