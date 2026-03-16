# Working Directory

When justx runs a recipe, it needs to decide which directory to use as the working directory. The right default depends on where the justfile lives.

## Defaults

| Scope | Behaviour |
|---|---|
| Global files (`~/.justx/`) | Recipes run in whatever directory you invoked `justx` from. A global `git.just` recipe works the same whether you're in `~/projects/foo` or `~/projects/bar`. |
| Local files (`./justfile`) | `just` handles working directories natively. The root justfile runs in its own directory; module recipes run in the directory containing their source file. Use `just`'s [`[no-cd]` attribute](https://just.systems/man/en/attributes.html) to override this per-recipe. |
