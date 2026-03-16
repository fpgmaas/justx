# Local Justfiles

Local justfiles live alongside your project and are only loaded when justx is run from that directory (or a subdirectory). They are the right place for project-specific tasks: running tests, building artifacts, starting dev servers, deploying, and so on.

By default, local recipes run relative to the **project root** — the directory containing the `justfile`, or the directory containing `.justx/` for recipe files inside it. This can be changed per file with a [directive](working-directory.md).

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

## Recursive discovery (monorepos)

By default, justx only looks for justfiles in the current directory. For monorepos and multi-project repositories, you can enable **recursive discovery** so that justx walks subdirectories to find additional justfiles and `.justx/` recipe directories.

Recursive discovery is enabled by setting `recursive = true` in a [config file](config-file.md). See the [config file reference](config-file.md) for all available options such as depth limits and exclusion patterns.

### What gets scanned

When recursive discovery is enabled, justx walks subdirectories of the current working directory (up to `max_depth` levels deep) looking for:

- A `justfile` in the directory root
- `*.just` and `*.justfile` files inside a `.justx/` subdirectory

Directories listed in `exclude` or `extend_exclude` are skipped entirely, along with `.justx/` directories (which are scanned for recipe files, not traversed further).

### Display names

Discovered files appear in the TUI alongside your root-level sources, with display names derived from their relative path. The `.justx/` segment and `.just`/`.justfile` extensions are stripped. For example:

| File path | Display name |
|---|---|
| `services/api/justfile` | `services/api/justfile` |
| `services/api/.justx/docker.just` | `services/api/docker` |
| `libs/core/.justx/test.just` | `libs/core/test` |

### Example monorepo layout

```
my-monorepo/
├── justx.toml                  # recursive = true
├── justfile                    # top-level tasks
├── .justx/
│   └── ci.just                 # CI recipes
├── services/
│   ├── api/
│   │   ├── justfile            # API service tasks
│   │   └── .justx/
│   │       └── docker.just     # API Docker recipes
│   └── web/
│       └── justfile            # Web service tasks
└── libs/
    └── core/
        └── .justx/
            └── test.just       # Library test recipes
```
