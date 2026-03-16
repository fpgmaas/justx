# CLI Reference

## `justx`

Launch the interactive TUI.

```
justx
```

Discovers all global (`~/.justx/` or `$JUSTX_HOME`) and local (`./`) justfiles, then opens the TUI.

### Options

| Option | Description |
|--------|-------------|
| `--version` | Show version and exit |

---

## `justx init`

Initialise the justx home directory.

```
justx init [OPTIONS]
```

### Options

| Option | Description |
|--------|-------------|
| `--download-examples` | Download example justfiles from GitHub instead of creating `user.just` |

### Behaviour

**Default** (no flags): creates `~/.justx/user.just` with two sample recipes (`greet` and `now`). Skips if the file already exists.

**With `--download-examples`**: fetches a list of curated `.just` files from the justx GitHub repository, shows an interactive checkbox (all pre-selected), and downloads the chosen files into the justx home directory. Skips any file that already exists.

### Examples

```bash
# Create ~/.justx/user.just with sample recipes
justx init

# Interactively download example files
justx init --download-examples
```

---

## `justx list`

List all discovered sources and their recipes.

```
justx list [OPTIONS] [SOURCE]
```

### Arguments

| Argument | Description |
|----------|-------------|
| `SOURCE` | Optional. Filter output to a single named justfile source (e.g. `docker`). |

### Options

| Option | Description |
|--------|-------------|
| `-g`, `--global` | Show global sources only |
| `-l`, `--local` | Show local sources only |

`-g` and `-l` are mutually exclusive. Without either flag, all sources (local then global) are listed.

### Examples

```bash
# List everything
justx list

# List only global recipes
justx list -g

# List only local recipes
justx list -l

# List only the global 'docker' source
justx list -g docker
```

---

## `justx run`

Run a recipe without the TUI.

```
justx run (-g | -l) TARGET [ARGS]...
```

### Arguments

| Argument | Description |
|----------|-------------|
| `TARGET` | Recipe to run. Use `source:recipe` to target a named justfile source, or `recipe` alone to target the root `justfile`. |
| `ARGS` | Optional extra arguments passed through to `just`. |

### Options

| Option | Description |
|--------|-------------|
| `-g`, `--global` | Target the global scope |
| `-l`, `--local` | Target the local scope |

Exactly one of `-g` or `-l` is required. They are mutually exclusive.

### Examples

```bash
# Run 'greet' from the global justfile, passing 'Alice' as an argument
# Equivalent to: just --justfile ~/.config/just/justfile --working-directory . greet Alice
justx run -g greet Alice

# Run 'shell' from the global 'docker' source with `my-image` as the tag
# Equivalent to: just --justfile ~/.justx/docker.just --working-directory . shell my-image
justx run -g docker:shell my-image

# Run the local 'test' recipe with extra pytest flags
# Equivalent to: just test -x -v
justx run -l test -x -v

# Run 'staging' from the local 'deploy' source
# Equivalent to: just --justfile .justx/deploy.just --working-directory . staging
justx run -l deploy:staging
```

---

## `justx check`

Verify that `just` is installed, show discovered justfile counts, and display configuration file locations.

```
justx check [OPTIONS]
```

Exits with code `1` if `just` is not found on `PATH`. Otherwise prints the `just` binary location, a summary of discovered justfiles, and the config file path (if present).

### Options

| Option | Description |
|--------|-------------|
| `-v`, `--verbose` | Show detailed discovery paths, sources with recipes, and full settings |

### Default output

```
just:      /usr/local/bin/just ✓
justfiles: 3 global, 1 local
config:    ./justx.toml
```

### Verbose output

With `-v`, the command additionally shows:

- **Global justfiles** — full paths to each discovered global justfile
- **Local justfiles** — full paths to each discovered local justfile
- **Sources & recipes** — all loaded sources with their recipes
- **Settings** — the fully resolved settings
