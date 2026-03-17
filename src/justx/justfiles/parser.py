from __future__ import annotations

import json
import shutil
import subprocess
from collections.abc import Iterator
from pathlib import Path

from justx.justfiles.exceptions import JustInvocationError, JustNotFoundError
from justx.justfiles.models import Parameter, ParameterKind, Recipe, RecipeDefault, Scope, Source


class JustfileParser:
    """Parses justfiles into Source models by invoking just."""

    def parse(self, path: Path, scope: Scope) -> list[Source]:
        """Parse a justfile and return sources for it and its modules.

        Runs ``just --dump`` once on the root justfile. The root recipes become
        one source; each module (recursively) becomes an additional source with
        its module path as display name.

        Args:
            path: Absolute path to the justfile.
            scope: Whether this is a global or local justfile.

        Returns:
            A list of sources: root first, then flattened modules in depth-first order.

        Raises:
            FileNotFoundError: if the justfile does not exist.
            JustNotFoundError: if the just binary is not on PATH.
            JustInvocationError: if just exits with a non-zero status.
        """
        if not path.exists():
            raise FileNotFoundError(f"Justfile not found: {path}")  # noqa: TRY003

        binary = self._require_just()
        data = self._dump(binary, path)

        root_source = self._build_root_source(data, path, scope)
        module_sources = list(self._extract_modules(data.get("modules", {}), scope, root_justfile=path))

        return [root_source, *module_sources]

    def _build_root_source(self, data: dict, path: Path, scope: Scope) -> Source:
        recipes = [self._parse_recipe(r) for r in data.get("recipes", {}).values()]
        return Source(
            scope=scope,
            path=path,
            recipes=recipes,
        )

    def _extract_modules(
        self,
        modules: dict,
        scope: Scope,
        *,
        root_justfile: Path,
        parent_path: str = "",
    ) -> Iterator[Source]:
        """Recursively yield nested modules as sources in depth-first order."""
        for name, module_data in modules.items():
            module_path = f"{parent_path}::{name}" if parent_path else name
            yield self._build_module_source(module_data, module_path, scope, root_justfile)
            nested_modules = module_data.get("modules", {})
            if nested_modules:
                yield from self._extract_modules(
                    nested_modules, scope, root_justfile=root_justfile, parent_path=module_path
                )

    def _build_module_source(self, module_data: dict, module_path: str, scope: Scope, root_justfile: Path) -> Source:
        recipes = [self._parse_recipe(r) for r in module_data.get("recipes", {}).values()]
        source_path = Path(module_data["source"])
        return Source(
            scope=scope,
            path=source_path,
            recipes=recipes,
            module_path=module_path,
            root_justfile=root_justfile,
        )

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
        raw_attributes = raw.get("attributes", [])
        groups = [attr["group"] for attr in raw_attributes if isinstance(attr, dict) and "group" in attr]
        attributes = [attr for attr in raw_attributes if isinstance(attr, str)]
        return Recipe(
            name=raw["name"],
            doc=raw.get("doc"),
            parameters=parameters,
            dependencies=dependencies,
            groups=groups,
            quiet=raw.get("quiet", False),
            attributes=attributes,
        )

    def _parse_parameter(self, raw: dict) -> Parameter:
        raw_default = raw.get("default")
        default = (
            None
            if raw_default is None
            else RecipeDefault(
                value=raw_default,
                expression=not isinstance(raw_default, str),
            )
        )
        kind = self._parameter_kind(raw["kind"], has_default=default is not None)
        return Parameter(name=raw["name"], default=default, kind=kind)

    @staticmethod
    def _parameter_kind(just_kind: str, has_default: bool) -> ParameterKind:
        if just_kind in ("star", "plus"):
            return ParameterKind.VARIADIC
        if has_default:
            return ParameterKind.OPTIONAL
        return ParameterKind.REQUIRED
