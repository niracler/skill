---
name: weekly-report
description: >-
  Use this skill whenever the user wants to write or generate a structured weekly
  work report (软件研发周报) — the formal 3-section corporate format with 本周工作总结,
  下周工作计划, and 其他事项. This skill automatically collects data from git logs,
  Obsidian diary Work Log entries, and GitHub PRs to draft the report. Invoke when
  the user says 周报, 软件研发周报, 本周工作总结,
  写周报, weekly report, end-of-week summary, or asks to prepare a work summary for
  their manager/team. Do NOT use for personal diary entries, monthly reviews,
  OKR summaries, meeting notes, or quarterly retrospectives.
---

# Weekly Report

软件研发周报生成助手。自动扫描 `~/code/` 下所有项目的 Git 日志，结合前几周周报
做对比，生成结构化的三段式周报，写入 Obsidian 日记。

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| git | cli | Yes | `brew install git` |
| reminders-cli | cli | Yes | `brew install keith/formulae/reminders-cli` |
| macOS Calendar | system | Yes | Built-in, access via `osascript` |
| gh | cli | No | `brew install gh` then `gh auth login` — for GitHub PR/Issue data |

### Path Dependencies

| Path | Purpose | Required |
|------|---------|----------|
| `~/code/*/` | Project repositories | Yes |
| `~/code/*/repos/*/` | Nested repositories | No (scanned automatically if present) |
| Obsidian daily notes directory | Daily diary files with Work Log entries + report output | Yes |

The Obsidian vault path is auto-detected by scanning `~/Library/Mobile Documents/iCloud~md~obsidian/`.
If not found, ask the user.

> Do NOT proactively verify tools or paths on skill load. If a command fails due to a
> missing tool, skip that data source and continue with what's available.

## Workflow Overview

1. **Confirm** → 2. **Find previous** → 3. **Collect data** (parallel) → 4. **Draft** → 5. **Review + write** → 6. **Schedule next week**

```text
┌──────────────────────────────────────────────────────────────────┐
│                weekly-report 完整流程（~20min）                    │
└──────────────────────────────────────────────────────────────────┘

  ┌──────────────┐
  │ 用户触发周报  │
  └──────┬───────┘
         │
         ▼
  ┌────────────────────────────────────┐
  │ 1. 确认周期 + 定位文件    (~1min)   │
  └──────┬─────────────────────────────┘
         │
         ▼
  ┌────────────────────────────────────┐
  │ 2. 查找前几周周报         (~1min)   │
  │    提取上周「下周工作计划」         │
  └──────┬─────────────────────────────┘
         │
         ▼
  ┌─────────────────────────────────────────────────┐
  │ 3. 并行数据收集（subagent）          (~3-5min)   │
  │    ┌─ 本周日记 Work Log（各工作日）              │
  │    ├─ Git log（~/code/*/ 全扫描）                │
  │    └─ GitHub PR/Issue（gh CLI）                  │
  └──────┬──────────────────────────────────────────┘
         │
         ▼
  ┌────────────────────────────────────┐
  │ 4. 交叉比对 + 生成草稿    (~3min)   │
  │    上周计划 vs 本周实际             │
  └──────┬─────────────────────────────┘
         │
         ▼
  ┌────────────────────────────────────┐
  │ 5. 用户审阅 + 修改        (~5min)   │
  │    展示草稿 → 用户调整 → 写入日记  │
  └──────┬─────────────────────────────┘
         │
         ▼
  ┌────────────────────────────────────┐
  │ 6. 创建下周日程 + 提醒    (~3min)   │
  │    Calendar time block             │
  │    Reminders 任务列表              │
  └──────┬─────────────────────────────┘
         │
         ▼
      ┌──────┐
      │ 完成  │
      └──────┘
```

## Step 1: Confirm Period and Target File

- **Report period**: Current week's Monday through Friday
- **Target file**: The day's daily note (usually last workday of the week)
- **Write location**: Under `## 2 Work Log`, as `### 软件研发周报（M/D - M/D）`
- **Diary path**: Scan for Obsidian vault in `~/Library/Mobile Documents/iCloud~md~obsidian/`
  or ask the user if not found

If today is Saturday/Sunday, default to the previous Friday's daily note.
Confirm with the user before proceeding.

## Step 2: Find Previous Reports

Scan recent daily notes (previous 14 days) for the heading pattern `### 软件研发周报`.

From the most recent previous report, extract:

1. **「下周工作计划」section** → baseline for accountability check (what was planned vs what happened)
2. **Format and style** → maintain consistency (project groupings, level of detail, bold patterns)

If no previous report found, skip comparison and proceed — this is normal for the first report.

## Step 3: Parallel Data Collection

Launch subagents concurrently. The three data sources are independent — run as many in
parallel as possible. If any source fails or is unavailable, skip it and continue.

### 3a. Daily Notes (Work Log)

Read the daily notes for each workday in the report period (Monday through Friday).
Extract content under `## 2 Work Log` from each day's note.

This is the richest data source — daily work logs often contain context, decisions, and
details that git commits and PR titles don't capture. Prioritize this content when
writing the report.

### 3b. Git Log Collection

Scan `~/code/*/` and `~/code/*/repos/*/` for Git repositories, then for each:

```bash
git log --oneline --since="{monday}" --until="{saturday}" --author="{user}" --all
```

Where `{user}` is from `git config user.name`.

Group commits by project → repository. This supplements the daily notes — useful for catching
work the user forgot to log in their diary.

### 3c. GitHub Activity (if `gh` available)

```bash
# PRs authored this week
gh search prs --author=@me --created="{monday}..{saturday}" --json repository,title,number,state,url

# Issues authored/assigned this week
gh search issues --author=@me --created="{monday}..{saturday}" --json repository,title,number,state,url
```

Include merged PRs, open PRs, and closed issues in the report. PR numbers and titles
provide concrete references for the boss.

### Data Source Priority

When the same work appears in multiple sources, merge intelligently:

| Priority | Source | Strength |
|---|---|---|
| 1 | Daily notes | Most context, user's own words, decisions and reasoning |
| 2 | GitHub | Concrete references (PR#, issue#) |
| 3 | Git log | Catch unreported work, verify claims |

The daily notes provide the narrative; GitHub provides traceability; Git logs fill gaps.

### Data Source Degradation

| Source unavailable | Behavior |
|---|---|
| Daily notes missing for some days | Use available days, note gaps |
| `gh` not installed or auth failed | Skip GitHub data, note "GitHub 数据未获取" |
| Git log returns nothing | Project may have had non-code work (meetings, design) — check daily notes |
| All remote sources fail | Proceed with daily notes + git log only |

## Step 4: Cross-Reference and Draft

### Accountability Check (when previous report exists)

Compare last week's 「下周工作计划」 against this week's actual output:

| Last week planned | This week status | How to handle |
|---|---|---|
| Completed | Done | Include in 本周总结 |
| Partially done | In progress | Note progress in 本周总结, carry forward to 下周计划 |
| Not started | Missed | Flag in 其他事项 with reason if known |
| Unplanned work done | New | Add to 本周总结 as new item |

### Project Grouping

Do not hardcode groups. Instead, derive grouping from:

1. **Previous report** (if exists): reuse the same project display names and grouping
2. **Daily notes**: use the project names already used by the author
3. **Repository layout**: group nested repositories under the same project when appropriate

Omit projects with zero activity this week.

### Draft Generation

Generate three sections following [report-template.md](references/report-template.md).

**本周工作总结:**

- Group by project and reuse established display names when available
- Each project 1-2 bullets max, compress into core deliverables
- Each bullet: `**bold key phrase**：` + business-language description
- Use domain numbers (接口数、页面数、参数个数), NOT internal numbers (commit 数、PR#)
- Skip entirely: CI/CD changes, version bumps, SDK sub-releases, upstream open-source contributions, internal process improvements (CLAUDE.md, openspec schema)
- sunlite and sylsmart are separate projects — never merge them

**下周工作计划:**

- Source from carry-forward items, daily notes, Reminders, and explicit user input
- Include time estimates when known (e.g., `（2.5 天）`)
- Each bullet: `**bold key phrase**：` + expected outcome in business terms
- sunlite and sylsmart must have separate headers with separate time allocations

**其他事项:**

- Carry-forward items from last week's plan that didn't get done, with brief reason
- Handoffs, blockers, cross-team coordination
- Keep it concise — no technical explanations in parentheses

## Step 5: User Review and Write

1. Present the full draft
2. Wait for user feedback
3. Apply changes — important: if user doesn't mention an item, it's fine as-is, do NOT remove it
4. Write final version to the daily note under `## 2 Work Log`

## Step 6: Schedule Next Week

After the report is written, parse the 「下周工作计划」 section and create Calendar events
and Reminders for next week. This closes the loop — what you wrote in the plan becomes
actionable items on your schedule.

### Parse Plan Items

From each bullet in 下周工作计划, extract:

- **Task name**: the bold key phrase
- **Project**: the project header it belongs to
- **Time estimate**: if `（N 天）` is specified

### Create Reminders

First check available lists with `reminders show-lists`, then create items in an
appropriate list (prefer "提醒" or the first available work-related list):

```bash
reminders add "提醒" "{project}: {task name}" --due-date "next monday"
```

If a task has a specific day mentioned (e.g., "周三前完成"), use that date instead.

### Create Calendar Time Blocks (optional)

If time estimates are available per project, suggest Calendar time blocks.
Calculate actual next-week dates (not relative offsets) to ensure accuracy:

```bash
# Example: create a time block for next Monday (2026-03-16) 9:00-17:00
osascript -e '
tell application "Calendar"
    tell calendar "工作"
        set startDate to date "2026年3月16日 09:00:00"
        set endDate to date "2026年3月16日 17:00:00"
        make new event with properties {summary:"sylsmart: auth 接口适配", start date:startDate, end date:endDate}
    end tell
end tell'
```

### Defaults

- **Calendar name**: "Work " (note trailing space) (with trailing space — verify with `osascript -e 'tell application "Calendar" to get name of calendars'`)
- **Time block**: 9:30-11:45 (morning focus block, not full day)
- **No all-day events**: Always create timed events, never all-day
- **Reminders list**: `提醒`

### Date calculation

Use `current date` with day offsets to calculate next week's dates. Do not use
hardcoded date strings — they cause locale-dependent parse errors on macOS.

```applescript
set baseDate to current date
set time of baseDate to 0
set nextMon to baseDate + ({offset} * days)
set startTime to nextMon + (9 * hours) + (30 * minutes)
set endTime to nextMon + (11 * hours) + (45 * minutes)
```

Present the proposed schedule to the user first — only create after confirmation:

```text
下周日程建议（Work 日历，9:30-11:45）：
  周一 3/23: sylsmart - xxx（1 天）
  周二-周三 3/24-3/25: sunlite - xxx（2 天）
  周四 3/26: HA 集成 - xxx（1 天）
  周五 3/27: buffer / 周报

确认创建到 Calendar 和 Reminders 吗？
```

## Important Behaviors

**Do not remove items the user didn't mention.** During review, the user will only call out
things that need changing. Silence means approval. This is a lesson learned from real usage:
removing "good" items to make room for user corrections breaks the report.

**Business language, not technical jargon.** The boss does NOT read code. Write what was
done and what it enables, using domain terms (接口、页面、配置参数、用户可以...). Never use:
implementation details (Router Factory, Playwright E2E, migration downgrade), internal process
names (CLAUDE.md, openspec review schema), version bumps (v0.2.0→v0.2.1), commit/PR counts,
or CI/CD details. These are valuable data for collection but must be translated to
business outcomes in the final report.

**Concrete with business numbers.** Use domain-relevant numbers: 14 个接口, 17 个页面,
4 个配置参数, 18 个待确认问题. NOT: 13 commits, PR#78, 91% coverage.

**Match previous report style.** If a previous report exists, mirror its voice, detail level,
and formatting choices. The goal is consistency across weeks so the boss sees a coherent
narrative, not a different writing style each time.

## Common Issues

| Issue | Fix |
|-------|-----|
| No daily notes found | Verify Obsidian vault path, check iCloud sync status |
| Previous report not found | Normal for first week — skip accountability check |
| `gh search` returns 0 results | Check date range format, verify `gh auth status` |
| Calendar "工作" not found | Run `osascript -e 'tell application "Calendar" to get name of calendars'` to list available calendars, use an existing one |
| Reminders list not found | Run `reminders show-lists` and use an available list |
| Git log shows upstream commits | Filter by `--author` to exclude upstream noise |
