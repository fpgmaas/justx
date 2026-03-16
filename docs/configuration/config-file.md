# Config File

justx works out of the box with zero configuration. For advanced use cases — such as [recursive file discovery in monorepos](local.md#recursive-discovery-monorepos) — you can create an optional TOML config file at the global or local level.

## File locations

| Scope | Path | Root key |
|---|---|---|
| Global | `~/.justx/config.toml` | `[defaults.discovery]` |
| Local (preferred) | `./justx.toml` | `[discovery]` |
| Local (fallback) | `./.justx/config.toml` | `[discovery]` |

For local config, justx checks `justx.toml` in the current directory first, then `.justx/config.toml`. Only the first file found is used.

## Discovery options

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

## Examples

**Local config** (`justx.toml`):

```toml
[discovery]
recursive = true
max_depth = 2
extend_exclude = ["vendor", "third_party"]
```

**Global config** (`~/.justx/config.toml`):

```toml
[defaults.discovery]
recursive = true
max_depth = 2
```

Global settings act as defaults — they apply to every project unless a local config overrides them.

## Config merging

Settings are layered in the following order:

1. **Built-in defaults** — the values shown in the table above
2. **Global config** (`~/.justx/config.toml`) — overrides defaults
3. **Local config** (`justx.toml` or `.justx/config.toml`) — overrides global

Merging is recursive: nested keys in a higher-priority config override only the specific keys they set, leaving other nested values intact.
