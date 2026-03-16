---
name: weekly-report
description: >-
  Generate structured weekly work reports (软件研发周报) by scanning project schedules,
  git logs, and previous reports. Use when user wants to write a weekly report, review
  weekly progress, or prepare end-of-week summaries.
  Triggers on「写周报」「软件研发周报」「weekly report」「本周总结」「周报」「周工作总结」.
  Also trigger on Friday afternoons when user mentions work summary or report writing.
  Do NOT trigger for personal daily diary (use diary-assistant instead).
  This skill specifically produces the 3-section corporate report
  format: 本周工作总结 / 下周工作计划 / 其他事项.
---

# Weekly Report

软件研发周报生成助手。自动扫描 `~/code/` 下所有项目的 schedule YAML 和 git log，
结合前几周周报做对比，生成结构化的三段式周报，写入 Obsidian 日记。

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| git | cli | Yes | `brew install git` |
| reminders-cli | cli | Yes | `brew install keith/formulae/reminders-cli` |
| macOS Calendar | system | Yes | Built-in, access via `osascript` |
| gh | cli | No | `brew install gh` then `gh auth login` — for GitHub PR/Issue data |
| yunxiao | skill | No | For 云效 MR/Task/Bug data (invoke via Skill tool) |

### Path Dependencies

| Path | Purpose | Required |
|------|---------|----------|
| `~/code/*/` | Monorepo workspaces (git repos + schedule YAMLs) | Yes |
| `~/code/*/planning/schedules/*.yaml` | Project schedule definitions | No (skip projects without schedule) |
| `~/code/*/repos/*/` | Sub-repos within each monorepo workspace | No (scanned automatically if present) |
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
  │    ├─ Schedule YAML（本周 + 下周模块）           │
  │    ├─ Git log（~/code/*/ 全扫描）                │
  │    ├─ GitHub PR/Issue（gh CLI）                  │
  │    └─ 云效 MR/Task/Bug（yunxiao skill）          │
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

Launch subagents concurrently. The five data sources are independent — run as many in
parallel as possible. If any source fails or is unavailable, skip it and continue.

### 3a. Daily Notes (Work Log)

Read the daily notes for each workday in the report period (Monday through Friday).
Extract content under `## 2 Work Log` from each day's note.

This is the richest data source — daily work logs often contain context, decisions, and
details that git commits and PR titles don't capture. Prioritize this content when
writing the report.

### 3b. Schedule YAML Scan

Scan `~/code/*/planning/schedules/*.yaml` — same directory structure as code-sync
(`~/code/*/` monorepo workspaces).

For each YAML found:

1. Read `project`, `title`, `timeline.start`, `phases`, `modules`
2. Calculate the current week number: `ceil((today - timeline.start) / 7)`
3. Extract modules where `weeks` includes current week → this week's work
4. Extract modules where `weeks` includes next week → next week's plan
5. Count `status: done` modules in current phase → progress fraction (e.g., 4/6)

### 3c. Git Log Collection

Scan `~/code/*/` and `~/code/*/repos/*/` for git repos (same candidates as code-sync's
scan.sh pattern), then for each:

```bash
git log --oneline --since="{monday}" --until="{saturday}" --author="{user}" --all
```

Where `{user}` is from `git config user.name`.

Group commits by workspace → repo. This supplements the daily notes — useful for catching
work the user forgot to log in their diary.

### 3d. GitHub Activity (if `gh` available)

```bash
# PRs authored this week
gh search prs --author=@me --created="{monday}..{saturday}" --json repository,title,number,state,url

# Issues authored/assigned this week
gh search issues --author=@me --created="{monday}..{saturday}" --json repository,title,number,state,url
```

Include merged PRs, open PRs, and closed issues in the report. PR numbers and titles
provide concrete references for the boss.

### 3e. 云效 Activity (if yunxiao skill available)

Spawn a subagent to invoke yunxiao skill via Skill tool:

```text
Agent tool:
- subagent_type: general-purpose
- prompt: |
    Invoke the yunxiao skill to query work activity from {monday} to {friday}.
    Get: MRs authored (merged + open), Tasks assigned (modified this week),
    Bugs assigned (modified this week).
    Return: list of items with identifier, title, status, and dates.
```

MR numbers (e.g., MR#67) and task identifiers (e.g., YWQO-4) add traceability to the report.

### Data Source Priority

When the same work appears in multiple sources, merge intelligently:

| Priority | Source | Strength |
|---|---|---|
| 1 | Daily notes | Most context, user's own words, decisions and reasoning |
| 2 | Schedule YAML | Structured progress, phase tracking, module status |
| 3 | GitHub / 云效 | Concrete references (PR#, MR#, issue#, task ID) |
| 4 | Git log | Catch unreported work, verify claims |

The daily notes provide the narrative; schedule YAML provides structure; GitHub/云效
provide traceability; git log fills gaps.

### Data Source Degradation

| Source unavailable | Behavior |
|---|---|
| Daily notes missing for some days | Use available days, note gaps |
| No schedule YAML for a project | Include project based on git/daily notes alone, omit progress fraction |
| `gh` not installed or auth failed | Skip GitHub data, note "GitHub 数据未获取" |
| yunxiao skill unavailable | Skip 云效 data, note "云效数据未获取" |
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
2. **Schedule YAML `title` field**: use as display name
3. **Common sense merging**: repos under the same `~/code/<workspace>/` that share a
   schedule can be grouped together

Omit projects with zero activity this week.

### Draft Generation

Generate three sections following [report-template.md](references/report-template.md).

**本周工作总结:**

- Group by project, each header includes phase progress (e.g., `进度 4/6`) when available
- Each bullet: `**bold key phrase**：` + concrete description with numbers
- Boss-readable: explain "what was done" + "why it matters", not implementation details

**下周工作计划:**

- Source from schedule YAML next-week modules + carry-forward items
- Include time estimates when known (e.g., `（1 天）`)
- Each bullet: `**bold key phrase**：` + expected outcome

**其他事项:**

- Handoffs, blockers, cross-team coordination
- Carry-forward items from last week's plan that didn't get done
- Status changes (task transferred to someone else, scope changes, etc.)

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

**Concrete over vague.** Every bullet should have at least one specific number or reference:
commit count, test coverage, API count, PR/MR number, issue number. "Completed auth module"
is bad. "Completed auth module (9 endpoints, 91% coverage, MR merged)" is good.

**Match previous report style.** If a previous report exists, mirror its voice, detail level,
and formatting choices. The goal is consistency across weeks so the boss sees a coherent
narrative, not a different writing style each time.

## Common Issues

| Issue | Fix |
|-------|-----|
| No daily notes found | Verify Obsidian vault path, check iCloud sync status |
| Schedule YAML parse error | Validate YAML syntax, check `timeline.start` date format |
| Previous report not found | Normal for first week — skip accountability check |
| `gh search` returns 0 results | Check date range format, verify `gh auth status` |
| Calendar "工作" not found | Run `osascript -e 'tell application "Calendar" to get name of calendars'` to list available calendars, use an existing one |
| Reminders list not found | Run `reminders show-lists` and use an available list |
| Git log shows upstream commits | Filter by `--author` to exclude upstream noise |
