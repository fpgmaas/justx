python := if os_family() == "windows" { "python" } else { "python3" }

# Run with expression default
run version=(python):
    echo {{ version }}
