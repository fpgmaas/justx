# Build and serve the documentation.
[no-cd]
serve:
    uv run zensical serve

# Test if documentation can be built without warnings or errors.
[no-cd]
test:
    uv run zensical build --clean
