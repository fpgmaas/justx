# Publishing a new release to AUR

The AUR package lives at [github.com/fpgmaas/python-justx](https://github.com/fpgmaas/python-justx),
which mirrors the AUR repo at `ssh://aur@aur.archlinux.org/python-justx.git`.

## Prerequisites

- AUR account with your SSH key added
- Write access to the `python-justx` repo (or submit a PR)
- Docker (if on macOS)

## Steps

### 1. Clone the package repo

```bash
git clone git@github.com:fpgmaas/python-justx.git
cd python-justx
```

### 2. Update the version and checksum in `PKGBUILD`

```bash
# Set the new version
pkgver=<new-version>

# Get the sha256 of the new PyPI tarball
curl -sL https://files.pythonhosted.org/packages/source/j/justx/justx-<new-version>.tar.gz | sha256sum
```

Update `pkgver` and `sha256sums` in `PKGBUILD` accordingly.

### 3. Regenerate `.SRCINFO`

**On Arch Linux:**
```bash
makepkg --printsrcinfo > .SRCINFO
```

**On macOS** (Docker required):
```bash
docker run --rm --platform linux/amd64 -v "$PWD":/pkg -w /pkg menci/archlinuxarm bash -c \
  "useradd -m builder && cp -r /pkg /home/builder/pkg && chown -R builder /home/builder/pkg \
  && su builder -c 'cd /home/builder/pkg && makepkg --printsrcinfo'" > .SRCINFO
```

### 4. Commit and push to GitHub

```bash
git add PKGBUILD .SRCINFO
git commit -m "Update to v<new-version>"
git push
```

### 5. Push to AUR

```bash
git remote add aur ssh://aur@aur.archlinux.org/python-justx.git  # first time only
git push aur master
```

> AUR uses `master` as the branch name.
