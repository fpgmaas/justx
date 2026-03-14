# Local Configuration

Local justfiles live alongside your project and are only loaded when justx is run from that directory (or a subdirectory). They are the right place for project-specific tasks: running tests, building artifacts, starting dev servers, deploying, and so on.

## File locations

| File pattern | Description |
|---|---|
| `./justfile` or `./Justfile` | Root justfile. |
| `./.justx/*.just` | Additional recipe sources (one topic per file). |

## Example layout for a Python project

```
my-project/
├── justfile              # top-level project tasks
├── .justx/
│   ├── docker.just       # container tasks for this project
│   └── deploy.just       # deployment recipes
├── src/
└── tests/
```

A typical `justfile` at the project root:

```just
# Run the test suite
test *args:
    uv run pytest {{args}}

# Format and lint
lint:
    uv run ruff format .
    uv run ruff check --fix .

# Build the package
build:
    uv build
```

Additional sources in `.justx/` follow the same naming convention as global files — the file stem becomes the source name shown in the TUI.
