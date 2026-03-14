# justx: Directives

justx supports a small set of in-file directives written as comments at the top of a justfile. Directives configure how justx handles that file's recipes without changing the behaviour of `just` itself.

## Syntax

```just
# justx: <key> = <value>
```

Directives are **file-level** — they apply to all recipes in the file.

## `working-directory`

Controls which directory is used as the working directory when running a recipe.

By default, `just` runs commands relative to the justfile's location. This makes sense when justfiles live alongside the project they operate on. However, `justx` inverts this default: since `justx` can run recipes from `.just` files stored in a central location (e.g. `~/.justx/`), it is more intuitive for commands to run relative to the user's current working directory. This way, global recipes behave as if you typed the command yourself. The `working-directory` directive lets you override this default on a per-file basis.

```just
# justx: working-directory = cwd|justfile
```

| Value | Behaviour |
|---|---|
| `cwd` *(default)* | Recipe runs in the shell's current directory at the time `justx` is invoked |
| `justfile` | Recipe runs in the directory that contains the justfile |

### Example — `templates.just`

A justfile that ships helper scripts or templates alongside itself needs `justfile` mode so it can reference those bundled files:

```just
# justx: working-directory = justfile

# Scaffold a new Python project from the bundled template
scaffold name:
    cp -r ./templates/python {{name}}
    echo "Created project {{name}}"

```

With `working-directory = justfile`, paths like `./templates/python` resolve relative to the directory containing `templates.just` (e.g. `~/.justx/`), not the user's current directory.
