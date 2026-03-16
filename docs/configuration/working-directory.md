# Working Directory

When justx runs a recipe, it needs to decide which directory to use as the working directory. The right default depends on where the justfile lives — a global recipe should behave as if you typed the command yourself, while a local recipe should run relative to its project.

## Defaults

| Scope | Default | Behaviour |
|---|---|---|
| Global files (`~/.justx/`) | `cwd` | Recipes run in whatever directory you invoked `justx` from. A global `git.just` recipe works the same whether you're in `~/projects/foo` or `~/projects/bar`. |
| Local files (`./justfile`, `./.justx/`) | `project` | Recipes run relative to their nearest project root. For a `justfile`, that is its own directory. For a file inside `.justx/`, that is the parent of `.justx/`. For example, `services/api/.justx/deploy.just` runs in `services/api/`. |

## Overriding the default

You can override the working directory on a per-file basis with a **directive** — a special comment at the top of a justfile:

```just
# justx: working-directory = cwd|project
```

Directives are file-level and apply to all recipes in the file. They are read by justx but ignored by `just` itself (they are regular comments).

### Values

| Value | Behaviour |
|---|---|
| `cwd` | Recipe runs in the shell's current directory at the time `justx` is invoked |
| `project` | When the file is a `justfile`, resolves to the directory of that file. When the file is inside a `.justx/` directory, resolves to the project root (the parent of `.justx/`), not `.justx/` itself |

### Example

A global recipe that defaults to `cwd` can be switched to `project` so that paths resolve relative to the justfile's location:

```just
# justx: working-directory = project

# Scaffold a new Python project from the bundled template
scaffold name:
    cp -r ./templates/python {{name}}
    echo "Created project {{name}}"
```

With `working-directory = project`, paths like `./templates/python` resolve relative to the directory containing the justfile (e.g. `~/.justx/`), not the user's current directory.

!!! tip
    In monorepo setups with [recursive discovery](local.md#recursive-discovery-monorepos), `project` is already the default for local files — recipes in `.justx/` subdirectories automatically resolve paths relative to their sub-project root, not the `.justx/` directory itself.
