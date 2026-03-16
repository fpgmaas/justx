# Config File

justx works out of the box with zero configuration. For advanced use cases — such as [recursive file discovery in monorepos](local.md#recursive-discovery-monorepos) — you can create an optional `justx.toml` file in your project root.

## File location

Place a `justx.toml` file in the directory where you run `justx`:

```
my-project/
├── justx.toml
├── justfile
└── ...
```

## Discovery options

All options live under the `[discovery]` section:

| Option | Type | Default | Description |
|---|---|---|---|
| `recursive` | `bool` | `false` | Enable recursive scanning of subdirectories for justfiles |
| `max_depth` | `int` | `3` | Maximum directory depth to scan when `recursive` is enabled |
| `exclude` | `list[str]` | see below | Directory names to skip during recursive scanning |
| `extend_exclude` | `list[str]` | `[]` | Additional directory names to skip, merged with `exclude` |

Default `exclude` list:

```toml
exclude = [
    "node_modules",
    ".venv",
    "venv",
    "target",
    ".git",
    "__pycache__",
    ".tox",
    "dist",
    "build",
]
```

## Example

```toml
[discovery]
recursive = true
max_depth = 2
extend_exclude = ["vendor", "third_party"]
```
