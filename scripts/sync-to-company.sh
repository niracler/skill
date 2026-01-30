#!/bin/bash
# Sync selected skills to the company repo (sunricher-skills)
#
# Usage:
#   cd repos/skill && ./scripts/sync-to-company.sh
#
# After running, review the diff and commit manually:
#   cd /tmp/sunricher-skills-sync
#   git add -A && git commit -m "sync: update skills" && git push

set -euo pipefail

COMPANY_REPO="git@codeup.aliyun.com:623ea833581fc62661c91d9e/public/sunricher-skills.git"
SYNC_DIR="/tmp/sunricher-skills-sync"
SKILLS_TO_SYNC=(git-workflow yunxiao markdown-lint skill-reviewer)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# --- Clone or pull ---
if [ -d "$SYNC_DIR/.git" ]; then
    echo "Pulling latest from company repo..."
    git -C "$SYNC_DIR" pull --ff-only
else
    echo "Cloning company repo..."
    rm -rf "$SYNC_DIR"
    git clone "$COMPANY_REPO" "$SYNC_DIR"
fi

# --- Sync skills ---
echo ""
echo "Syncing skills: ${SKILLS_TO_SYNC[*]}"
for skill in "${SKILLS_TO_SYNC[@]}"; do
    src="$REPO_ROOT/skills/$skill/"
    dst="$SYNC_DIR/skills/$skill/"
    if [ -d "$src" ]; then
        mkdir -p "$dst"
        rsync -av --delete "$src" "$dst"
    else
        echo "WARNING: $src not found, skipping"
    fi
done

# --- Sync validation scripts ---
echo ""
echo "Syncing validation scripts..."
mkdir -p "$SYNC_DIR/scripts"
cp "$REPO_ROOT/scripts/validate.sh" "$SYNC_DIR/scripts/"
cp "$REPO_ROOT/scripts/quick_validate.py" "$SYNC_DIR/scripts/"

# --- Generate README ---
echo ""
echo "Generating README.md..."
cat > "$SYNC_DIR/README.md" << 'READMEEOF'
# Sunricher Skills

用于 AI 编程助手的 Skills 集合。遵循 [Agent Skills 规范](https://github.com/anthropics/skills)。

## 安装

```bash
npx skills add git@codeup.aliyun.com:623ea833581fc62661c91d9e/public/sunricher-skills.git
```

## Skills

```text
╭──────────────────────────────────────────────────╮
│  Dependencies:                                   │
│    git-workflow                                   │
│    └╌╌▶ yunxiao          codeup.aliyun.com       │
│    skill-reviewer                                │
│    └╌╌▶ writing-skills   quality audit (ext)     │
│    yunxiao               standalone               │
│    markdown-lint         standalone               │
│                                                   │
│  ──▶ dependency  ╌╌▶ conditional/optional         │
╰──────────────────────────────────────────────────╯
```

### git-workflow

标准化 Git 提交、PR 和 Release 工作流。

**触发词:** "commit"、"提交代码"、"创建 PR"、"发布版本"、"打 tag"

**功能:**

- Conventional Commits 格式化提交
- Pull Request 模板和流程
- Release 工作流和 CHANGELOG 生成

### yunxiao

阿里云云效 DevOps CLI，支持代码评审、任务管理和发布。

**触发词:** "创建 MR"、"提交评审"、"推送代码"、"更新任务"、"查看任务"、"发布版本"、"打 tag"

**功能:**

- MR 创建与管理
- 任务查询、更新、评论
- 发布 Tag

**依赖:** Git、aliyun CLI、jq（跨平台安装说明见 skill 文档）

### markdown-lint

Markdown 格式化和 Lint 配置。

**触发词:** "设置 markdownlint"、"修复 markdown 格式"、"markdownlint 报错"

**功能:**

- markdownlint + pre-commit hook 配置
- 批量修复和验证工作流

### skill-reviewer

Claude Code Skill 质量审查工具。

**触发词:** "审查 skill"、"检查 skill 质量"、"验证 skill 兼容性"

**功能:**

- 结构检查（frontmatter、目录规范）
- 平台兼容性扫描
- Agent 兼容性检查

## 验证

```bash
./scripts/validate.sh
```

## 目录结构

```text
skills/
├── git-workflow/
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── yunxiao/
│   ├── SKILL.md
│   └── references/
│       ├── cheatsheet.md
│       └── openapi.md
├── markdown-lint/
│   ├── SKILL.md
│   └── scripts/
└── skill-reviewer/
    ├── SKILL.md
    ├── references/
    └── scripts/
```

## 相关链接

- [Agent Skills 规范](https://github.com/anthropics/skills)
- [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills)
- [云效 OpenAPI 文档](https://help.aliyun.com/zh/yunxiao/developer-reference/)
READMEEOF

# --- Show diff ---
echo ""
echo "========================================="
echo "  Sync complete. Changes:"
echo "========================================="
echo ""
git -C "$SYNC_DIR" status
echo ""
git -C "$SYNC_DIR" diff --stat
echo ""
echo "To review full diff:  git -C $SYNC_DIR diff"
echo "To commit and push:"
echo "  cd $SYNC_DIR"
echo "  git add -A && git commit -m 'sync: update skills from niracler/skill' && git push"
