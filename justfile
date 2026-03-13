# List commands
default:
    @just --list

# Install the uv environment.
install:
    @echo "🚀 Creating virtual environment using uv"
    uv sync

# Run code quality tools.
check:
    @echo "🚀 Linting code: Running pre-commit"
    pre-commit run -a
    @echo "🚀 Checking for dependency issues: Running deptry"
    uv run deptry src

# Run unit tests.
test:
    @echo "🚀 Running unit tests"
    uv run pytest tests

# Test if documentation can be built without warnings or errors. Test if documentation can be built without warnings or errors.
docs-test:
    uv run mkdocs build -s

# Build and serve the documentation.
docs:
    uv run mkdocs serve
