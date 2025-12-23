# Release Guide

## Process

1. **Update version** in relevant files (manifest.json, pyproject.toml, package.json, etc.)
2. **Update CHANGELOG.md** with release notes
3. **Commit changes** to main branch: `chore(release): bump version to x.y.z`
4. **Create and push tag**: `git tag v{version} && git push upstream v{version}`
5. **Create GitHub release**: `gh release create v{version} -R {owner}/{repo} --title "v{version}" --notes "..."`
6. **Push to all remote repositories** if using multiple remotes

## Semantic Versioning

Follow MAJOR.MINOR.PATCH format:

- **MAJOR**: Incompatible API changes
- **MINOR**: Backward-compatible functionality additions
- **PATCH**: Backward-compatible bug fixes

## CHANGELOG.md Structure

Follow [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format:

```markdown
## [x.y.z] - YYYY-MM-DD

### Added
- New user-facing features

### Fixed
- Important bug fixes (#issue)

### Technical
- Dependency updates, CI/CD improvements, code refactoring
```

### Guidelines

- **Added**: User-facing features
- **Fixed**: Bug fixes with issue references (#123)
- **Technical**: Internal changes (dependencies, CI/CD, refactoring)
  - Include commit hashes (abc1234) for technical changes without issues
- Keep entries concise and user-focused
- Update version links at bottom of changelog

## Example Workflow

### Step 1: Update Version Files

```bash
# Update version in manifest.json
# Update version in pyproject.toml
# Update version in package.json (if applicable)
```

### Step 2: Update CHANGELOG.md

```markdown
## [0.3.0] - 2025-12-01

### Added
- Group control support for smart home devices (#45)
- Energy monitoring dashboard (#48)

### Fixed
- Energy calculation overflow in sensor component (#52)

### Technical
- Migrate to new SDK API structure (commit: abc1234)
- Update dependencies to latest versions (commit: def5678)
- Improve CI/CD pipeline with parallel tests (commit: ghi9012)

[0.3.0]: https://github.com/owner/repo/compare/v0.2.0...v0.3.0
```

### Step 3: Commit Changes

```bash
git add manifest.json pyproject.toml CHANGELOG.md
git commit -m "chore(release): bump version to 0.3.0"
git push origin main
```

### Step 4: Create and Push Tag

```bash
git tag v0.3.0
git push upstream v0.3.0
```

### Step 5: Create GitHub Release

```bash
gh release create v0.3.0 \
  -R owner/repo \
  --title "v0.3.0" \
  --notes "$(cat <<'EOF'
## Added
- Group control support for smart home devices (#45)
- Energy monitoring dashboard (#48)

## Fixed
- Energy calculation overflow in sensor component (#52)

## Technical
- Migrate to new SDK API structure (commit: abc1234)
- Update dependencies to latest versions (commit: def5678)
- Improve CI/CD pipeline with parallel tests (commit: ghi9012)
EOF
)"
```

## Tips

- Always test the build before releasing
- Verify all CI checks pass
- Double-check version numbers are consistent across all files
- Review CHANGELOG for completeness and accuracy
- Consider pre-release tags (v1.0.0-beta.1) for testing
