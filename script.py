from pathlib import Path

from justx.justfiles.parser import JustfileParser

source = JustfileParser().parse(Path("justfile"))

print(source.model_dump_json(indent=2))
