# Local Justfiles

Local justfiles live alongside your project and are only loaded when justx is run from that directory. They are the right place for project-specific tasks: running tests, building artifacts, starting dev servers, deploying, and so on.

## File discovery

justx looks for a `justfile` (or `Justfile`) in the current working directory. If found, it runs `just --dump` once on that file, which resolves all recipes and modules automatically.

## Modules

justx supports `just`'s native [module system](https://just.systems/man/en/modules1.html). Any modules declared in your root justfile are discovered and shown as separate sources in the TUI.

### Example layout

```
my-project/
├── justfile              # root — declares modules and top-level tasks
├── docker.just           # module source file
├── deploy/
│   └── justfile          # module source file (in subdirectory)
├── src/
└── tests/
```

The root `justfile`:

```just
mod docker
mod deploy

# Run the test suite
test *args:
    uv run pytest {{args}}

# Format and lint
lint:
    uv run ruff format .
    uv run ruff check --fix .
```

### How modules appear in the TUI

Each module becomes a separate source in the Sources pane. Nested modules (modules within modules) are flattened with `parent::child` display names.

| Module declaration | Display name |
|---|---|
| `mod docker` | `docker` |
| `mod deploy` (which itself declares `mod staging`) | `deploy`, `deploy::staging` |

### Running module recipes

In the TUI, select the module source and pick a recipe. From the CLI:

```bash
# Run 'build' from the 'docker' module
justx run -l docker:build

# Run 'up' from the nested 'deploy::staging' module
justx run -l "deploy::staging:up"
```

Under the hood, justx invokes `just` with the module-qualified recipe name (e.g. `just docker::build`), letting `just` handle working directory resolution natively.

## Working directory

For local sources, `just` handles working directories natively — module recipes run in the directory containing their source file by default. Use `just`'s own [`[no-cd]` attribute](https://just.systems/man/en/attributes.html) if you need a recipe to run in the caller's directory instead.
