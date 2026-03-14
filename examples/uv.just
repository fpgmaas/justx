# Sync dependencies (including all optional groups)
sync:
    uv sync --all-groups

# Add a package
add package:
    uv add {{ package }}

# Remove a package
remove package:
    uv remove {{ package }}

# Lock dependencies
lock:
    uv lock

# Upgrade all dependencies to latest compatible versions
upgrade:
    uv lock --upgrade

# Upgrade a single package
upgrade-package package:
    uv lock --upgrade-package {{ package }}

# Export dependencies to requirements.txt
export:
    uv export --format requirements-txt --no-hashes --frozen --no-emit-project > requirements.txt
    @echo "Project dependencies written to requirements.txt"

# List outdated packages
outdated:
    uv pip list --outdated

# Run a command in the venv
run +args:
    uv run {{ args }}

# Show dependency tree
tree:
    uv tree
