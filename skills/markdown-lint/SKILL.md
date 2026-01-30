---
name: markdown-lint
description: Use when setting up or running markdown formatting and linting in a repository, or when encountering markdownlint errors (MD013, MD040, MD060) or horizontal rule violations. Triggers on「格式化 markdown」「设置 markdown lint」「markdown 检查」「设置 pre-commit」「检查 md 格式」「markdownlint 报错」
---

# Markdown Lint

为仓库配置 markdown 格式检查（markdownlint + 水平线禁止）和 pre-commit hook。

## When to Use

- **新仓库初始化**：第一次为仓库添加 markdown 格式标准
- **检查/修复**：运行格式检查或批量修复现有文件
- **迁移**：将格式标准复制到另一个仓库

**不适用：**

- **单文件检查**：直接运行 `npx markdownlint-cli2 file.md`，不需要走 setup 流程
- **文章内容审校**：使用 writing-proofreading skill（步骤 6 会引用本 skill）

## 前置条件

```bash
brew install pre-commit   # 全局安装一次
node --version             # 需要 Node.js（markdownlint 依赖）
```

## Setup 流程

### 1. 检查仓库状态

```bash
# 已有配置？跳到「检查/修复」
ls .markdownlint.json .pre-commit-config.yaml 2>/dev/null
```

### 2. 创建配置文件

**`.markdownlint.json`：**

```json
{
  "default": true,
  "MD013": false,
  "MD024": { "siblings_only": true },
  "MD033": false,
  "MD035": false,
  "MD036": false,
  "MD041": false,
  "MD060": false
}
```

关闭规则说明：

| 规则 | 理由 |
|------|------|
| MD013 | CJK 文本和表格不适合行长度限制 |
| MD033 | 允许 `<br>`, `<small>` 等 inline HTML |
| MD035 | 水平线完全禁止，由独立脚本检查 |
| MD036 | 允许 bold 作视觉标题 |
| MD041 | YAML frontmatter 导致首行非标题 |
| MD060 | 表格管道符间距样式过于严格 |

**`.pre-commit-config.yaml`：**

```yaml
repos:
  - repo: https://github.com/DavidAnson/markdownlint-cli2
    rev: v0.20.0  # 运行 pre-commit autoupdate 获取最新
    hooks:
      - id: markdownlint-cli2
  - repo: local
    hooks:
      - id: no-horizontal-rules
        name: no horizontal rules outside frontmatter
        entry: scripts/check-horizontal-rules.sh
        language: script
        types: [markdown]
```

> 创建后必须运行 `pre-commit autoupdate`，上面的 rev 可能已过时。

**`scripts/check-horizontal-rules.sh`：**

从 [scripts/check-horizontal-rules.sh](scripts/check-horizontal-rules.sh) 复制，然后 `chmod +x`。

**`.gitignore`**（如果没有）：

```text
node_modules/
.mypy_cache/
__pycache__/
```

### 3. 移除现有 `---` 分隔线

保留 YAML frontmatter 的 `---`，删除其余所有水平线：

```bash
# 找出违规文件
bash scripts/check-horizontal-rules.sh $(find . -name '*.md' -not -path './node_modules/*')

# 批量移除（保留 frontmatter）
for file in $(bash scripts/check-horizontal-rules.sh \
  $(find . -name '*.md' -not -path './node_modules/*') 2>&1 \
  | grep -oE '^[^:]+' | sort -u); do
  awk '
    NR == 1 && /^---[[:space:]]*$/ { print; fm = 1; next }
    fm && /^---[[:space:]]*$/ { print; fm = 0; next }
    !fm && /^[[:space:]]*[-*_][[:space:]]*[-*_][[:space:]]*[-*_][-*_ ]*$/ { next }
    { print }
  ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
done
```

### 4. 格式化全部文件

```bash
npx markdownlint-cli2 --fix "**/*.md"
npx markdownlint-cli2 "**/*.md"        # 确认零错误
```

### 5. 安装 hook

```bash
pre-commit install
```

### 6. 验证

```bash
# 三项检查全部通过
npx markdownlint-cli2 "**/*.md"
bash scripts/check-horizontal-rules.sh $(find . -name '*.md' -not -path './node_modules/*')
# 测试 hook: 故意加 --- 到某 md 文件，git add + commit，应被拦截
```

## 检查/修复（已有配置的仓库）

```bash
npx markdownlint-cli2 "**/*.md"            # 检查
npx markdownlint-cli2 --fix "**/*.md"      # 自动修复
bash scripts/check-horizontal-rules.sh **/*.md  # HR 检查
```

## 常见问题

| 问题 | 原因 | 修复 |
|------|------|------|
| `pre-commit: command not found` | 未安装 | `brew install pre-commit` |
| markdownlint 大量 MD060 错误 | 表格管道符间距 | `.markdownlint.json` 中 `"MD060": false` |
| frontmatter `---` 被误删 | awk 脚本问题 | 确认文件第 1 行是 `---` 且紧接 YAML 内容 |
| `--fix` 未修复所有问题 | 部分规则无法自动修复 | 手动修复（通常是 MD040 缺少代码块语言） |
