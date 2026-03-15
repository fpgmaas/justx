# Global Justfiles

Global justfiles are available in every directory. They are the right place for personal utilities — git helpers, Docker shortcuts, SSH tools, and anything else you reach for regardless of which project you are in.

## Example layout

```
~/.justx/
├── docker.just           # container management shortcuts
├── git.just              # git workflow helpers
├── kubernetes.just       # kubectl shortcuts
├── ssh.just              # SSH utilities
└── user.just             # created by `justx init`

~/.config/just/
└── justfile              # optional — global justfile shared with `just -g`
```

Each `*.just` file in `~/.justx/` becomes a named global **source** in the TUI. `justx` also parses the global justfile and presents it in the TUI, see [below](#global-justfile) for more details.

The above example could look as follows in the TUI:


<div style="background: #1e1e2e; color: #cdd6f4; font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', Menlo, Consolas, monospace; font-size: 13px; line-height: 1.5; border-radius: 8px; overflow: hidden; margin: 1em 0;">
  <div style="background: #181825; padding: 6px 12px; color: #6c7086; text-align: center; font-size: 12px; border-bottom: 1px solid #313244;">
    justx
  </div>
  <div style="display: flex; padding: 0; min-height: 260px;">
    <div style="width: 35%; border-right: 1px solid #1e90ff; padding: 8px 0;">
      <div style="color: #fab387; font-weight: bold; padding: 2px 10px;">Global</div>
      <div style="padding: 2px 10px 2px 20px;">docker</div>
      <div style="background: #1e90ff; color: #1e1e2e; padding: 2px 10px 2px 20px; font-weight: bold;">git</div>
      <div style="padding: 2px 10px 2px 20px;">kubernetes</div>
      <div style="padding: 2px 10px 2px 20px;">ssh</div>
      <div style="padding: 2px 10px 2px 20px;">user</div>
      <div style="padding: 2px 10px 2px 20px;">justfile</div>
    </div>
    <div style="width: 65%; padding: 8px 12px;">
      <div><span style="color: #a6e3a1; font-weight: bold;">lg</span></div>
      <div style="color: #6c7086; padding-left: 16px;">Pretty one-line log</div>
      <div><span style="color: #a6e3a1; font-weight: bold;">wip</span> <span style="color: #6c7086;">&lt;message&gt;</span></div>
      <div style="color: #6c7086; padding-left: 16px;">Stage all and commit</div>
      <div><span style="color: #a6e3a1; font-weight: bold;">sync</span></div>
      <div style="color: #6c7086; padding-left: 16px;">Pull with rebase and push</div>
      <div><span style="color: #a6e3a1; font-weight: bold;">branches</span></div>
      <div style="color: #6c7086; padding-left: 16px;">List branches sorted by date</div>
      <div><span style="color: #a6e3a1; font-weight: bold;">cleanup</span></div>
      <div style="color: #6c7086; padding-left: 16px;">Delete merged branches</div>
    </div>
  </div>
  <div style="background: #181825; padding: 4px 12px; color: #6c7086; font-size: 11px; border-top: 1px solid #313244;">
    <span style="color: #f9e2af;">q</span> Quit&nbsp;&nbsp;&nbsp;<span style="color: #f9e2af;">s</span> Search&nbsp;&nbsp;&nbsp;<span style="color: #f9e2af;">d</span> Details&nbsp;&nbsp;&nbsp;<span style="color: #f9e2af;">enter</span> Run
  </div>
</div>

## File discovery

### Named sources

All `*.just` files in `~/.justx/` are loaded alphabetically. The name of the file becomes the source name in the TUI. For example,`docker.just` appears as `docker`, `git.just` as `git`, and so on. It is recommended to organise by tool or topic, one file per concern.

Override the directory that `justx` will use to scan for source files with the environment variable `JUSTX_HOME`:

```bash
export JUSTX_HOME=/path/to/my/justx-home
```

Use `justx init --download-examples` to get a starter set of files. See [Examples](https://github.com/fpgmaas/justx/tree/main/examples) for details.

> **Note:** A bare `justfile` inside `~/.justx/` is **not** loaded. Use one of the global justfile locations below instead.


### Default global justfile

justx also discovers a global justfile from the same locations as `just --global-justfile` ([docs](https://just.systems/man/en/global-and-user-justfiles.html#global-justfile)). The first path that exists wins:

1. `$XDG_CONFIG_HOME/just/justfile` (defaults to `~/.config/just/justfile`)
2. `~/justfile`
3. `~/.justfile`

This is optional — it is useful if you already have a global justfile for `just -g` and want those recipes to show up in justx as well.
