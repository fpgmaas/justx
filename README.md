<p align="center">
  <img alt="justx logo" width="400" height="240" src="https://raw.githubusercontent.com/fpgmaas/justx/refs/heads/main/docs/static/justx-logo-path.svg">
</p>


<p align="center">
  <a href="https://img.shields.io/github/v/release/fpgmaas/justx"><img alt="Release" src="https://img.shields.io/github/v/release/fpgmaas/justx"></a>
  <a href="https://github.com/fpgmaas/justx/actions/workflows/main.yml?query=branch%3Amain"><img alt="Build status" src="https://img.shields.io/github/actions/workflow/status/fpgmaas/justx/main.yml?branch=main"></a>
  <a href="https://pypi.org/project/justx/"><img alt="Supported Python versions" src="https://img.shields.io/pypi/pyversions/justx"></a>
  <a href="https://pypistats.org/packages/justx"><img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/justx"></a>
</p>

---


<p align="center">
<bold>justx</bold> is a TUI command launcher built on top of <a href = "https://github.com/casey/just">just</a>. Define recipes once, run them anywhere.
</p>


<p align="center">
  <img src="https://raw.githubusercontent.com/fpgmaas/justx/assets/demo.gif" alt="justx TUI demo"/>
</p>


---

<p align="center">
  <a href="https://fpgmaas.github.io/justx/">Documentation</a> &nbsp;·&nbsp;
  <a href="https://pypi.org/project/justx/">PyPI</a>
</p>

---

## Installation

```shell
uv tool install justx
# or
pip install justx
# or
pipx install justx
```

Or on Arch Linux:

```sh
yay -S python-justx
```

> **Prerequisite:** the [`just`](https://github.com/casey/just#installation) binary must be available on `$PATH`.

## Quickstart

**1. Initialise your global recipe library:**

```shell
justx init
```

This creates `~/.justx/` with a sample justfile to get you started. To pull in a richer set of ready-made recipes (git, docker, filesystem tools, and more), run:

```shell
justx init --download-examples
```

**2. Launch the TUI:**

```shell
justx
```

Browse your recipes with the arrow keys and press `Enter` to run one. Press `q` to quit.

## Global recipes

**justx** supports global recipes; recipes that are available from anywhere on your machine, no matter which project you're in.

Global recipes are discovered automatically when you run `justx`. justx searches for the [global justfile](https://just.systems/man/en/global-and-user-justfiles.html#global-justfile) and also discovers all `.just` files in the `~/.justx/` directory. For example:

```
~/.justx/
├── git.just        # git workflows
├── docker.just     # container management
└── ssh.just        # remote connections
```

Where `~/.justx/docker.just` might contain:

```just
# Run a container interactively with a shell
shell image_tag:
    docker run --rm -it --entrypoint bash {{image_tag}}
```

You can also skip the TUI and run recipes directly with `justx run`:

```shell
# Run 'shell' from the global 'docker' source with `my-image` as the tag
# Equivalent to: just --justfile ~/.justx/docker.just --working-directory . shell my-image
justx run -g docker:shell my-image
```

## Local recipes and modules

If you run `justx` from a directory that contains a `justfile`, its recipes appear automatically in the TUI. **justx** also supports `just`'s native [module system](https://just.systems/man/en/modules1.html) — any modules declared in your justfile are discovered and shown as separate sources.

```just
# justfile
mod docker
mod deploy

test:
    pytest
```

---

For full details on file discovery, CLI reference, and example justfiles, see the [documentation](https://fpgmaas.github.io/justx/).
