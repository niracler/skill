# Output Template

## Structure Overview

```text
┌─────────────────────────────────────────────┐
│  > 概览引用行 (数字速览)                       │
├─────────────────────────────────────────────┤
│  主题 A                                      │
│    叙事段落 (做了什么、为什么)                  │
│    活动表格 (MR/Bug/Task/PR 合并单表)         │
│    代码统计行                                 │
├─────────────────────────────────────────────┤
│  主题 B ...                                  │
├─────────────────────────────────────────────┤
│  其他 (低活动仓库聚合)                        │
├─────────────────────────────────────────────┤
│  本周统计 + 亮点 (仅 weekly)                  │
└─────────────────────────────────────────────┘
```

## Daily Template

```markdown
## 工作回顾 ({date})

> {total_commits} commits · +{insertions} / -{deletions} · {repos_active} repos · {prs_merged} PRs merged

### {主题名}

{叙事段落：1-3 句话概述这个主题下做了什么、解决了什么问题或推进了什么目标。}

| 类型 | 编号 | 内容 | 状态 |
|------|------|------|------|
| MR | #52-#55 | 功能 A 整合 | 已合并 |
| PR | #3 | Skill improvements | merged |
| Bug | MYCP-131 | xxx 显示异常 | 修复中 |
| Task | MYCP-114 | yyy 重构 | 已完成 |

{repo_a} {n} commits +{ins}/-{del} · {repo_b} {n} commits +{ins}/-{del}

### 其他

{repo_x} ({n} commits, +{ins}/-{del}) · {repo_y} ({n} commits)
```

### No Activity

```markdown
No activity recorded for {date}.
```

## Grouping Rules

### Theme Grouping

Group by **work theme** (not by data source). A theme is a logical unit of work, typically corresponding to:

- A project or product area (e.g., "Sunlite Backend", "HA 开源贡献")
- A cross-cutting initiative (e.g., "Skills 重构", "基础设施优化")

Merge data from all sources (stats.sh + github.sh + 云效) under the same theme. For example, if `azoulalite-backend` in 云效 corresponds to the same project as local git repo `sunlite`, group them together.

### Activity Table

One unified table per theme with columns `类型 | 编号 | 内容 | 状态`. Row ordering: MR → PR → Bug → Task.

- **Related MRs** that belong to the same logical change go on **one row** (e.g., `#52-#55 功能 A 整合`).
- **Unrelated MRs** get separate rows.
- **GitHub PRs** follow the same rule: related PRs share a row.
- Each **Bug** gets its own row (each has a distinct status).
- Each **Task** gets its own row.
- Goal: reduce noise. 9 individual items → 3-5 themed rows.
- Omit the table entirely if no MR/Bug/Task/PR data for the theme (git-only themes show only narrative + stats line).

### "其他" Aggregation

- Repos with **≤ 2 commits** in the period go into the "其他" line.
- Format: inline list with commit count and code changes.
- If no low-activity repos, omit the section.

### Section Omission

- Omit the activity table if no MR/Bug/Task/PR data for the theme.
- Omit the "其他" section if no low-activity repos.
- If a remote source failed, add a note: `> ⚠ {source} 数据未获取`

## Weekly Template

Includes everything from Daily Template, plus these sections at the end:

```markdown
### 本周统计

  Mon  ████████░░  8 commits
  Tue  ██████░░░░  6 commits
  Wed  ████░░░░░░  4 commits
  Thu  ███░░░░░░░  3 commits
  Fri  ██░░░░░░░░  2 commits

### 本周亮点

- 最活跃仓库: {repo} ({commits} commits)
- 最大变更: {description} (+{lines} 行)
- {其他成就: sprint 完成、PR 活动总结等}
```

### Commit Distribution Rules

- Fixed width: 10 characters per bar
- Filled block: `█`, empty block: `░`
- Scale: max day's commits = 10 blocks, others proportional
- Only show Mon–Fri by default; include Sat/Sun if they have commits
- Days with 0 commits: all `░`

### Highlights Rules

- **Most active repo**: highest commit count from stats.sh
- **Largest change**: highest insertions count from stats.sh
- **Notable achievements**: sprint completion, significant PRs merged, etc. (from all sources)

## Overview Line Format

The blockquote overview line summarizes key numbers at a glance:

```text
> {commits} commits · +{insertions} / -{deletions} · {repos} repos · {prs_merged} PRs merged
```

- Include PR/MR counts only if data is available.
- If only git data: `> {commits} commits · +{ins} / -{del} · {repos} repos`
- If all sources: `> {commits} commits · +{ins} / -{del} · {repos} repos · {prs} PRs merged · {mrs} MRs`
