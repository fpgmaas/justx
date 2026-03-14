# justx

**A TUI command launcher built on [just](https://github.com/casey/just) — define recipes once, run them anywhere.**

![justx TUI demo](static/placeholder.png)

Store your frequently used commands as `just` recipes in `~/.justx/`, then run them from any directory through an interactive terminal UI by simply running `justx`. No memorising command names or flags; just pick a recipe and go.

## Features

- **TUI launcher** — browse and run recipes interactively with a keyboard-driven interface
- **Global & local scopes** — maintain a personal recipe library in `~/.justx/` alongside per-project justfiles
- **Non-interactive mode** — `justx run` for scripting and CI pipelines
- **Zero config** — works with your existing justfiles.

## Non-interactive usage

`justx run` lets you execute recipes directly, acting as a shorthand for long `just` invocations:

```bash
# Run 'build' from the global 'docker' group with `my-image` as the tag
# Equivalent to `just --justfile ~/.justx/docker.just --working-directory . build my-image`
justx run -g -G docker build my-image
```

See the [CLI Reference](cli-reference.md) for the full list of commands and options.

## Get started

[Getting Started →](getting-started.md)
