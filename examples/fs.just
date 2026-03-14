# justx: working-directory = justfile

# Disk usage by subdirectory, sorted by size
usage path="." depth="1":
    du -h -d {{depth}} {{path}} | sort -hr

# Show the N largest files under a path
biggest path="." n="20":
    find {{path}} -type f -exec du -h {} + | sort -rh | head -{{n}}

# Find files by name pattern
find-name pattern path=".":
    find {{path}} -type f -name "{{pattern}}"

# Search for text recursively in files
find-text pattern path=".":
    grep -r "{{pattern}}" {{path}}

# Find empty directories
empty-dirs path=".":
    find {{path}} -type d -empty

# Show permissions for all files recursively
permissions path=".":
    ls -lR {{path}}
