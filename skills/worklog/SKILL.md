---
name: worklog
description: Use when user wants work review or work summary. Triggers on「工作回顾」「日报」「周报」「worklog」「今天做了什么」「本周总结」.
---

# Worklog

个人工作回顾，整合本地 git 统计、GitHub 和云效数据，输出结构化 Markdown 报告。

## Mode Selection

| User says | Mode |
|-----------|------|
| 「日报」「今天做了什么」"daily worklog" | Daily |
| 「周报」「本周总结」"weekly worklog" | Weekly |
| 「工作回顾」「worklog」 | Ask user |

## Workflow

1. **Determine mode + dates** → 2. **Collect data** (parallel) → 3. **Integrate + render**

If no data from any source, output: "No activity recorded for {period}."

### Step 1: Determine Dates

| Mode | --since | --until |
|------|---------|---------|
| Daily | Today (`YYYY-MM-DD`) | Today |
| Weekly | Monday of current week | Today |

### Step 2: Collect Data (Parallel)

Run all three sources concurrently using subagents:

> Other agent environments: the three sources are independent — run them sequentially if parallel execution is not available.

```text
┌─ Bash: stats.sh --since {since} --until {until}       (local git)
├─ Bash: github.sh --since {since} --until {until}      (GitHub)
└─ subagent: 云效 MR/Bug/Task                            (yunxiao skill)
```

#### 2a. Local Git Statistics

```bash
bash scripts/stats.sh --since YYYY-MM-DD --until YYYY-MM-DD
```

Output: JSON with `period`, `repos[]` (name, path, remote_url, commits, insertions, deletions, files_changed, authors, first_commit, last_commit), and `totals` (repos_active, repos_scanned, commits, insertions, deletions).

> Other agent environments: run this command directly via shell.

#### 2b. GitHub Activity

```bash
bash scripts/github.sh --since YYYY-MM-DD --until YYYY-MM-DD
```

Output: JSON with `period`, `prs[]` (repo, number, title, state, created_at, merged_at), `issues[]` (repo, number, title, state, created_at), and `totals` (prs_merged, prs_open, issues_opened, issues_closed).

Optionally pass `--username` from [user-config.md](references/user-config.md). Without it, defaults to `gh api user`.

> Other agent environments: run this command directly via shell.

#### 2c. 云效 Activity

Start subagent to invoke yunxiao skill with specific MCP queries:

```text
Task tool:
- subagent_type: general-purpose
- prompt: 使用 yunxiao skill 获取 {since} 到 {until} 的工作记录
  组织 ID: {从 user-config.md 读取 yunxiao_org_id}
  用户名: {从 user-config.md 读取 yunxiao_username}

  需要获取:
  1. MR: list_change_requests — state=all, authorCodeupIdList=[user_id]
     返回: id, title, state, sourceRef, targetRef, createTime, mergeTime
  2. Bug: search_workitems — category=Bug, space=..., conditions=[assignee=username]
     返回: identifier, subject, status, assignedTo, gmtModified
  3. 任务: search_workitems — category=Task, space=..., conditions=[assignee=username]
     返回: identifier, subject, status, assignedTo, gmtModified
```

> Other agent environments: if yunxiao skill is unavailable, skip and note "云效数据未获取".

### Step 3: Integrate and Render

Merge all sources. For any failed source, note it (e.g., "GitHub 数据未获取") and continue with available data.

Render using [template.md](references/template.md).

**Weekly mode** additionally requires:

1. **Commit distribution** — For active repos from stats.sh, count commits per weekday:

   ```bash
   git log --since={since} --until={until_next_day} --author="{author}" --format="%aI" | \
     awk -F'T' '{print $1}' | sort | uniq -c
   ```

   Render as ASCII bar chart (Mon–Fri).

2. **Highlights** — From stats.sh data: most active repo (by commits), largest change (by insertions).

### Data Source Degradation

| Source failed | Behavior |
|---------------|----------|
| GitHub | Note "GitHub 数据未获取", continue |
| 云效 | Note "云效数据未获取", continue |
| Both remote | Output local git stats only |

## Common Issues

| Issue | Fix |
|-------|-----|
| stats.sh empty repos | Check date range and `--author` filter |
| github.sh fails / 401 | Run `gh auth login` |
| 云效 MCP not connected | Check MCP server configuration |

## Dependencies

> If a dependency is unavailable, the corresponding data source is skipped with a note.

| Skill | Purpose | When |
|-------|---------|------|
| `yunxiao` | 云效 MR/Bug/Task data | Step 2c |

## User Configuration

See [user-config.md](references/user-config.md) for identity and data source settings.
