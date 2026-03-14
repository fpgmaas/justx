# Global Configuration

Global justfiles are available in every directory. They are the right place for personal utilities — git helpers, Docker shortcuts, SSH tools, and anything else you reach for regardless of which project you are in.

## Default location

```
~/.justx/
```

Override by setting the `JUSTX_HOME` environment variable:

```bash
export JUSTX_HOME=/path/to/my/justx-home
```

## What goes there

| File pattern | Description |
|---|---|
| `~/.justx/justfile` | Root justfile. |
| `~/.justx/*.just` | Additional recipe groups (one topic per file). |

Each file becomes a named **group** in the TUI. The group name is the file stem — `docker.just` becomes the `docker` group, `git.just` becomes `git`, and so on. The root `justfile` (if present) is loaded first; the rest are loaded alphabetically.

## Example directory layout

```
~/.justx/
├── justfile          # personal one-off recipes
├── docker.just       # container management shortcuts
├── git.just          # git workflow helpers
├── kubernetes.just   # kubectl shortcuts
├── ssh.just          # SSH utilities
└── user.just         # created by `justx init`
```

## Suggested organisation

Organise by tool or topic — one file per concern. This keeps each group focused and makes it easy to find recipes in the TUI:

```just
# git.just — git workflow shortcuts

# Pretty one-line log
lg:
    git log --oneline --graph --decorate

# Stage all and commit with a message
wip message:
    git add -A && git commit -m "wip: {{message}}"
```

Use `justx init --download-examples` to get a starter set of example files. See [Examples](../examples.md) for details.
