# Configuration Overview

justx organises recipes into two scopes: **global** and **local**. Both scopes are shown in the TUI simultaneously, making it easy to mix personal utilities with project-specific tasks.

## Scopes

| Scope | Default location | Use case |
|-------|-----------------|----------|
| [**Global**](global.md) | `~/.justx/` (or `$JUSTX_HOME`) | Personal tools available in every directory |
| [**Local**](local.md) | `./justfile` + `./.justx/` | Project-specific tasks |

### In the TUI

Sources in the Sources pane are labelled by scope:

- `[Global]` — recipes loaded from `~/.justx/` (or `$JUSTX_HOME`)
- `[Local]` — recipes loaded from the current working directory

## Next steps

- [Global Configuration](global.md) — set up your personal recipe library
- [Local Configuration](local.md) — add project-specific justfiles
