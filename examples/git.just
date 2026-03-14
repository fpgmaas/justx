# Pretty graph log of all branches
lg:
    git log --all --oneline --graph --decorate

# Show your commits since yesterday
standup:
    git log --since="yesterday" --oneline --author=$(git config user.email)

# Undo last commit, keep changes staged
undo:
    git reset --soft HEAD~1

# Stash current changes with a WIP message
wip:
    git stash push -m "wip"

# Pop the most recent stash
unwip:
    git stash pop

# List branches sorted by last commit date
branches:
    git branch -v --sort=-committerdate

# Delete local branches already merged into main
clean-merged:
    git branch --merged main | grep -v '^\*\|main\|master\|dev' | xargs -r git branch -d

# List tags sorted by version
tags:
    git tag --sort=version:refname
