# Getting Started

## Prerequisites

- **[just](https://github.com/casey/just)** — the command runner justx is built on. Install it with your package manager or from the [just releases page](https://github.com/casey/just/releases).
- **Python 3.10+**

## Install justx

```bash
# Recommended — installs as an isolated tool
uv tool install justx

# Alternative
pip install justx
```

## Initialise your recipe directory

Run `justx init` to create `~/.justx/user.just` with two sample recipes:

```bash
justx init
```

To populate `~/.justx/` with a set of example recipes, use `--download-examples`:

```bash
justx init --download-examples
```

Available examples include `docker.just`, `git.just`, `kubernetes.just`, `uv.just`, and more. See a list of the avilable [examples](https://github.com/fpgmaas/justx/tree/dev/examples) on Github.

## Launch the TUI

To open the TUI, simply run

```bash
justx
```

navigate to the recipe you want to run, and press `Enter`. If the recipe has input arguments, you will be prompted to enter those before running the command.

## Local recipes

If you run `justx` from a directory that already contains a `justfile`, it will appear automatically in the Sources pane alongside your global recipes — no extra setup needed.

## Verify your setup

```bash
justx check
```

This confirms that the `just` binary is on your `PATH` and prints all discovered justfile paths in both global and local scopes.
