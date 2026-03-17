# Local Justfiles

Local justfiles live alongside your project and are only loaded when justx is run from that directory. They are the right place for project-specific tasks: running tests, building artifacts, starting dev servers, deploying, and so on.

## File discovery

justx looks for a `justfile` (or `Justfile`) in the current working directory. All recipes and modules declared in that file are automatically discovered and shown in the TUI.

## Example

A typical project justfile:

```just
# Run the test suite
test *args:
    uv run pytest {{args}}

# Format and lint
lint:
    uv run ruff format .
    uv run ruff check --fix .

# Start dev server
dev:
    uv run uvicorn app:main --reload
```

## Organising with modules

As your justfile grows, you can split recipes into separate files using `just`'s native [module system](https://just.systems/man/en/modules1190.html). Declare a module in your root justfile with `mod`, and `just` looks for the source file in this order:

- `<name>.just`
- `<name>/mod.just`
- `<name>/justfile` (any capitalisation)

For example:

```
my-project/
├── justfile              # root — declares modules and top-level recipes
├── docker.just           # module: mod docker
├── deploy/
│   └── justfile          # module: mod deploy
├── src/
└── tests/
```

```just
mod docker
mod deploy

# Run the test suite
test *args:
    uv run pytest {{args}}
```

Each module appears as a separate source in the TUI. Nested modules (modules within modules) are flattened with `parent::child` display names.

| Module declaration | Display name |
|---|---|
| `mod docker` | `docker` |
| `mod deploy` (which itself declares `mod staging`) | `deploy`, `deploy::staging` |

### Running module recipes

In the TUI, select the module source and pick a recipe. From the CLI:

```bash
# Run 'build' from the 'docker' module
justx run -l docker::build

# Run 'up' from the nested 'deploy::staging' module
justx run -l "deploy::staging::up"
```

## Working directory

For local sources, `just` handles working directories natively — module recipes run in the directory containing their source file by default. Use `just`'s own [`[no-cd]` attribute](https://just.systems/man/en/attributes.html) if you need a recipe to run in the caller's directory instead.
