# justx

<p align="center">
  <img alt="justx logo" width="400" height="240" src="https://raw.githubusercontent.com/fpgmaas/justx/refs/heads/main/docs/static/justx-logo-path.svg">
</p>

<p align="center">
A TUI command launcher built on top of <a href = "https://github.com/casey/just">just</a>. Define recipes once, run them anywhere.
</p>


![justx TUI demo](https://raw.githubusercontent.com/fpgmaas/justx/assets/demo.gif)

Store your frequently used commands as `just` recipes in `~/.justx/`, then run them from any directory through an interactive terminal UI by simply running `justx`. No memorising command names or flags; just pick a recipe and go.

## Features

- **TUI launcher** — browse and run recipes interactively with a keyboard-driven interface
- **Global & local scopes** — maintain a personal recipe library in `~/.justx/` alongside per-project justfiles
- **Non-interactive mode** — `justx run` for scripting and CI pipelines
- **Zero config** — works with your existing justfiles.

## Non-interactive usage

`justx run` lets you execute recipes directly, acting as a shorthand for long `just` invocations:

```bash
# Run 'build' from the global 'docker' source with `my-image` as the tag
# Equivalent to `just --justfile ~/.justx/docker.just --working-directory . build my-image`
justx run -g docker:build my-image
```

See the [CLI Reference](cli-reference.md) for the full list of commands and options.

## Get started

[Getting Started →](getting-started.md)
