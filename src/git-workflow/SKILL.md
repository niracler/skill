---
name: git-workflow
description: 个人 Git 工作流，遵循 conventional commits 和语义化版本。用于创建提交、PR 和发布版本。当用户说「帮我提交」「commit」「提交代码」「创建 PR」「发布版本」「打 tag」「写 commit message」「推代码」时触发。
---

# Git Workflow

Standardized Git workflow for commits, pull requests, and releases using conventional commits format and semantic versioning.

## When to Use

- **Creating commits**: Follow conventional commits with concise, imperative messages
- **Creating pull requests**: Generate PR with clear description and test plan
- **Creating releases**: Update versions, CHANGELOG, tags, and GitHub releases

These workflows can be used independently or together as needed.

## Platform Detection

**首先检测仓库类型**，根据 remote URL 选择正确的工作流：

```bash
git remote get-url origin
```

| Remote URL 包含        | 平台         | 使用的 Skill               |
| ---------------------- | ------------ | -------------------------- |
| `github.com`           | GitHub       | 本 skill（git-workflow）   |
| `codeup.aliyun.com`    | 云效 Codeup  | **调用 `yunxiao` skill**   |
| `gitlab.com`           | GitLab       | 本 skill（适配 GitLab CLI）|

**云效仓库检测到后**：立即调用 `yunxiao` skill 处理 MR 创建、代码评审等操作。

## Quick Reference

### Commit Format

```text
type(scope): concise summary

- Optional bullet points (max 3-4)
- Keep short and focused
```

**Types**: feat, fix, refactor, docs, test, chore

**Important**: NO Claude Code signatures or AI markers in commits.

### Branch Naming

- `feature/description`
- `fix/description`
- `docs/description`
- `refactor/description`
- `test/description`

### Release Checklist

1. Update version in project files
2. Update CHANGELOG.md
3. Commit: `chore(release): bump version to x.y.z`
4. Tag: `git tag v{version} && git push upstream v{version}`
5. Create GitHub release with `gh release create`

## Detailed Guides

For comprehensive guidelines and examples:

- **Commits**: See [commit-guide.md](references/commit-guide.md) for detailed format, principles, and examples
- **Pull Requests**: See [pr-guide.md](references/pr-guide.md) for PR process, structure, and templates
- **Releases**: See [release-guide.md](references/release-guide.md) for complete release workflow and CHANGELOG format

## Validation

Use `scripts/validate_commit.py` to validate commit messages:

```bash
python3 scripts/validate_commit.py "feat(auth): add OAuth2 support"
python3 scripts/validate_commit.py --file .git/COMMIT_EDITMSG
```

The validator checks:

- Conventional commits format
- Subject line length (< 72 chars)
- Imperative mood usage
- Absence of AI-generated markers
- Body format and bullet point count

## Common Workflows

### Independent Commit

```bash
# Make changes
git add .
# Create commit following format
git commit -m "feat(component): add new feature"
```

### Pull Request Workflow

```bash
# Create feature branch
git checkout -b feature/new-feature

# Make changes and commit
git add .
git commit -m "feat(component): add new feature"

# Push and create PR
git push origin feature/new-feature
gh pr create --title "feat(component): add new feature" --body "..."
```

### Release Workflow

```bash
# Update version files (manifest.json, pyproject.toml, etc.)
# Update CHANGELOG.md with release notes

# Commit release
git add .
git commit -m "chore(release): bump version to 1.2.0"

# Create tag and push
git tag v1.2.0
git push upstream v1.2.0

# Create GitHub release
gh release create v1.2.0 -R owner/repo --title "v1.2.0" --notes "..."
```

### Combined PR and Release

Sometimes you'll create a PR for the release:

```bash
# On release branch
# Update versions and CHANGELOG
git add .
git commit -m "chore(release): bump version to 1.2.0"

# Create PR for review
git push origin release/v1.2.0
gh pr create --title "chore(release): bump version to 1.2.0" --body "..."

# After merge to main
git checkout main
git pull
git tag v1.2.0
git push upstream v1.2.0
gh release create v1.2.0 -R owner/repo --title "v1.2.0" --notes "..."
```

## Common Issues

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| Subject line > 72 chars | 描述过长 | 缩短摘要，详情放 body |
| 多个 type 在同一提交 | 范围过大 | 拆分为多个单一功能的提交 |
| Merge commits 出现 | 使用了 merge | 改用 `git pull --rebase` |
| 验证脚本报错 | 格式不符 | 检查 type(scope): 格式 |
