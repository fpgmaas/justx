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

As your justfile grows, you can split recipes into separate files using `just`'s native [module system](https://just.systems/man/en/modules.html). Declare a module in your root justfile with `mod`, and `just` looks for the source file in this order:

- `<name>.just`
- `<name>/mod.just`
- `<name>/justfile` (any capitalisation)

For example:

```
my-project/
├── justfile              # root — declares modules and top-level recipes
├── docker.just           # module: mod docker
├── deploy/
│   ├── justfile          # module: mod deploy
│   └── staging.just      # submodule: mod staging (inside deploy)
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

The above example could look as follows in the TUI:

<div style="background: #1e1e2e; color: #cdd6f4; font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', Menlo, Consolas, monospace; font-size: 13px; line-height: 1.5; border-radius: 8px; overflow: hidden; margin: 1em 0;">
  <div style="background: #181825; padding: 6px 12px; color: #6c7086; text-align: center; font-size: 12px; border-bottom: 1px solid #313244;">
    justx
  </div>
  <div style="display: flex; padding: 0; min-height: 260px;">
    <div style="width: 35%; border-right: 1px solid #1e90ff; padding: 8px 0;">
      <div style="color: #fab387; font-weight: bold; padding: 2px 10px;">Local</div>
      <div style="padding: 2px 10px 2px 20px;">justfile</div>
      <div style="background: #1e90ff; color: #1e1e2e; padding: 2px 10px 2px 20px; font-weight: bold;">docker</div>
      <div style="padding: 2px 10px 2px 20px;">deploy</div>
      <div style="padding: 2px 10px 2px 20px;">deploy::staging</div>
    </div>
    <div style="width: 65%; padding: 8px 12px;">
      <div><span style="color: #a6e3a1; font-weight: bold;">build</span> <span style="color: #6c7086;">&lt;tag&gt;</span></div>
      <div style="color: #6c7086; padding-left: 16px;">Build the Docker image</div>
      <div><span style="color: #a6e3a1; font-weight: bold;">push</span> <span style="color: #6c7086;">&lt;tag&gt;</span></div>
      <div style="color: #6c7086; padding-left: 16px;">Push image to registry</div>
      <div><span style="color: #a6e3a1; font-weight: bold;">up</span></div>
      <div style="color: #6c7086; padding-left: 16px;">Start containers</div>
      <div><span style="color: #a6e3a1; font-weight: bold;">down</span></div>
      <div style="color: #6c7086; padding-left: 16px;">Stop containers</div>
    </div>
  </div>
  <div style="background: #181825; padding: 4px 12px; color: #6c7086; font-size: 11px; border-top: 1px solid #313244;">
    <span style="color: #f9e2af;">q</span> Quit&nbsp;&nbsp;&nbsp;<span style="color: #f9e2af;">s</span> Search&nbsp;&nbsp;&nbsp;<span style="color: #f9e2af;">d</span> Details&nbsp;&nbsp;&nbsp;<span style="color: #f9e2af;">enter</span> Run
  </div>
</div>

### Running module recipes

In the TUI, select the module source and pick a recipe. It's also technically possible to run local recipes through the `justx` CLI:

```bash
# Run 'build' from the 'docker' module
justx run -l docker::build
```

but it's probably easier to simply run `just docker::build` 🤷

## Working directory

For local sources, `just` handles working directories natively — module recipes run in the directory containing their source file by default. Use `just`'s own [`[no-cd]` attribute](https://just.systems/man/en/attributes.html) if you need a recipe to run in the caller's directory instead.
