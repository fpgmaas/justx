# Configuration

justx works out of the box with zero configuration.

## Global home directory

Override the directory that justx uses for global recipe files with the `JUSTX_HOME` environment variable:

```bash
export JUSTX_HOME=/path/to/my/justx-home
```

The default location is `~/.justx/`.

## Local project setup

For local projects, justx relies on `just`'s native module system. Declare modules in your root `justfile` using `mod` — no additional configuration files are needed. See [Local Justfiles](local.md) for details.
