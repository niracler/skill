---
name: skill-reviewer
description: Use when reviewing, auditing, or validating Claude Code skills for quality and cross-platform/cross-agent compatibility. Triggers on「审查 skill」「review skill」「检查 skill 质量」「skill 兼容性检查」「review 兼容性」
---

# Skill Reviewer

审计 Claude Code skills 的质量和兼容性。作为编排器，委托已有工具处理结构/质量检查，自身专注兼容性审计。

## 审计流程

### Step 1: 结构校验（委托）

运行 skill-reviewer 自带的校验脚本，汇总 YAML frontmatter、name 格式、description 格式等结果：

```bash
bash <skill-reviewer-dir>/scripts/validate.sh
```

> 若脚本不可用（如未通过 npx skills 安装），手动检查每个 SKILL.md 的 YAML frontmatter：name（hyphen-case，≤64 字符）、description（无尖括号，≤1024 字符）。

### Step 2: 内容质量（委托，推荐）

**推荐执行**：若已安装 `writing-skills`，调用该 skill 进行深度质量审查（token 效率、渐进式披露、反模式、TDD 方法论等）。

若未安装，提示用户可选安装：

```bash
npx skills add https://github.com/obra/superpowers --skill writing-skills
```

> 跳过此步骤时应明确告知用户，避免静默省略。

### Step 3: 兼容性审计（自身核心）

按 `references/compatibility-checklist.md` 逐项检查目标 skill 的所有文件（SKILL.md + scripts/ + references/）：

**3a. 跨平台兼容性** — 扫描平台锁定模式（macOS-only 命令、Windows 不兼容项等）。

**3b. 跨 Agent 兼容性** — 检测 Claude Code 专属工具引用和 MCP 依赖。

**3c. npx skills 生态兼容性** — 校验 marketplace.json 注册、symlink 可用性、跨 skill 依赖。

**3d. 工具引用规范** — 检查是否保留了 Claude Code 工具术语并提供了其他环境的 fallback 备注。详见 checklist 的 "Tool Reference Best Practices" 部分。

详见 `references/compatibility-checklist.md`。

### Step 4: 输出报告

使用以下格式输出统一报告：

```markdown
## Skill Review: {skill-name}

### 总览
| 维度 | 状态 | 方式 |
|------|------|------|
| 结构与元数据 | PASS / FAIL | validate.sh |
| 内容质量 | 建议使用 writing-skills | 委托 |
| 平台兼容性 | PASS / FAIL (N issues) | 自查 |
| Agent 兼容性 | PASS / FAIL (N issues) | 自查 |
| npx skills 生态 | PASS / FAIL (N issues) | 自查 |

### Critical
- **[维度]** 问题描述
  当前: ...
  建议: ...

### High
...

### Medium / Low
...
```

严重度分级：

- **Critical** — 功能不可用或分发失败，必须修复
- **High** — 显著影响可用范围，建议修复
- **Medium** — 可改进项，不影响核心功能
- **Low** — 建议性改进
