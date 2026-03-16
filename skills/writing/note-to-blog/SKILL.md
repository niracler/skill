---
name: note-to-blog
description: >-
  Use this skill whenever the user wants to find notes from their Obsidian vault to
  publish as blog posts, or wants to convert existing notes into blog-ready drafts.
  Invoke immediately when the user wants to: scan their note archive for publishable
  content, select a note for blogging, do blog topic selection from their notes, or
  convert a specific note to a blog post format. Trigger phrases: 选一篇笔记发博客,
  note to blog, 写博客, 博客选题, 从笔记里找文章. NOT for: writing a new blog post
  from scratch, proofreading a blog draft, or general note organization.
---

# Note to Blog

从 Obsidian Note 仓库中筛选适合发布的笔记，评估适配性，批量选题，双通道处理（快速转换 / 深度研究），并行 Agent 派发。

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| Python 3 | cli | Yes | Pre-installed on macOS |
| PyYAML | cli | Yes | `pip install pyyaml` |
| writing-proofreading | skill | No | Included in `npx skills add niracler/skill` |

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing tool, directly guide the user through installation and configuration step by step.

## When NOT to Use

- 笔记库少于 5 篇时，手动选题更快
- 只想转换单篇已确定的笔记 — 直接运行 `<skill-dir>/scripts/note-to-blog.py convert "<path>"`
- 博客草稿已存在，只需校对 — 使用 writing-proofreading

## Script Location

All deterministic operations are handled by the Python script:

```text
<skill-dir>/scripts/note-to-blog.py  (collect / convert / state subcommands)
```

Path configuration is in [user-config.md](references/user-config.md). All bash examples below use `<PLACEHOLDER>` — replace with values from user-config.md.

## Workflow Overview

```text
Step 1           Step 2            Step 3              Step 4             Step 5
 Collect   ──▶   Level Select ──▶  By Level     ──▶   Execute      ──▶   Summary
 (script)        (user)            ├─ L1 浏览          (Agent Teams)       (report)
                                   ├─ L2 推荐
                                   └─ L3 深探
                                        │
                                   Interact ──▶ track assign ──▶ confirm
```

## Step 1: Collect

Run the `collect` script with paths from [user-config.md](references/user-config.md):

```bash
python3 <skill-dir>/scripts/note-to-blog.py collect \
  --note-repo "<NOTE_REPO>" \
  --blog-content "<BLOG_CONTENT>" \
  --project-paths <PROJECT_PATHS> \
  --history-file "<HISTORY_FILE>"
```

The script outputs a single JSON object to stdout containing:

- `candidates`: all eligible notes with title, summary, char_count, outgoing_links
- `clusters`: wikilink hub nodes (3+ inbound links) with related notes
- `published_posts`: existing blog posts with title, tags, collection
- `session_keywords`: recent Claude Code session activity signals
- `stats`: total_scanned, filtered_out, candidates_count

Read the JSON output and proceed to Step 2.

## Step 2: Level Selection

Display data volume and offer Level choice:

```text
collect 完成：
  候选笔记: {candidates_count} 篇 (总扫描 {total_scanned}, 过滤 {filtered_out})
  主题簇: {clusters_count} 个 (3+ 引用 hub)

可选深度:
  Level 1 浏览    直接展示候选列表，手动选择          0 额外 token
  Level 2 推荐    LLM 评估 + 主题簇分析              ~2k token     ← 推荐
  Level 3 深探    Level 2 + 读取 hub 笔记全文         ~5k+ token

选择 Level (1-3)?
```

### Quick Reference

| Level | 名称 | 评估方式 | 后续流程 |
|:---:|:---|:---|:---|
| 1 | 浏览 | 无 LLM，候选按字数降序 | 用户直选 → 全部 fast track |
| 2 | 推荐 | LLM 评估摘要 + 主题簇 → 5-8 推荐 | fast/deep track 分配 |
| 3 | 深探 | Level 2 + 读取 hub 笔记全文 | fast/deep track，cluster 推荐更准确 |

### Recommendation logic

| 候选数 | clusters | 推荐 |
|--------|----------|------|
| ≤ 10 | any | Level 1 |
| > 10 | 0 | Level 2 |
| > 10 | 1+ | Level 2 |

用户明确说「想发现主题」「有什么可以整合的」时 → 推荐 Level 3。

## Step 3: By Level

### Level 1: Browse

Skip LLM evaluation. Display candidates sorted by char_count descending:

```text
#  标题                         字数    链接数
1  关于后LLM时代的代码Review     3200    5
2  SSH私钥加密                   1200    2
3  Feed内容阅读姿势              1800    3
...
```

User selects items by number. All selections go to **fast track only** (Level 1 does not offer deep track).

After selection, skip to **Confirm & Execute** below.

### Level 2: Recommend

Make a single LLM evaluation using the prompt template from [scoring-criteria.md](references/scoring-criteria.md).

**Input**: Construct the evaluation prompt with `collect` JSON data (candidates, clusters, published_posts, session_keywords).

**Output**: The LLM SHALL return a JSON array of 5-8 recommendations. See [scoring-criteria.md](references/scoring-criteria.md) for the full specification.

If the LLM response is not valid JSON, retry once with explicit format instructions.

After evaluation, proceed to **Interact** below.

### Level 3: Deep Explore

Same as Level 2, but **before** calling the LLM, Read the full text of each cluster hub note and append it to the evaluation prompt.

For each cluster in the collect JSON where `hub_path` is not null:

1. Read the hub note full text from the Note repository
2. Append it to the LLM prompt under a `## Hub 笔记全文` section (see [scoring-criteria.md](references/scoring-criteria.md) for the Level 3 input format)

This gives the LLM actual content context for cluster recommendations instead of just metadata.

After evaluation, proceed to **Interact** below.

## Interact (Level 2/3)

### Present recommendations

Display the recommendation list as a mixed table:

```text
#  类型    标题                    适配分  目标   工作量  活跃   重复风险
1  单篇    后LLM时代代码Review      92    blog    小    ★★★    无
2  主题簇  优雅的哲学 (9篇关联)      88    blog    大    ★      无
3  单篇    SSH私钥加密              85    til     小    ─      无
...
```

### User actions

| Action | Example | Effect |
|--------|---------|--------|
| Select + assign track | "1 和 3 快速转换，2 走深度" | Queue items with track assignment |
| Override collection | "1 放 til" | Change target collection |
| Batch skip | "4~6 跳过，reason: private" | Mark as skipped via `state skip` |
| See more | "还有别的吗" | Request additional recommendations |
| Check status | "状态" | Run `state status` |

**On skip**: run immediately:

```bash
python3 <skill-dir>/scripts/note-to-blog.py state skip "<path>" --reason "<reason>" \
  --note-repo "<NOTE_REPO>"
```

### Track assignment

| Track | When to use | What happens |
|-------|-------------|--------------|
| **Fast** (快速) | Independent, mostly complete notes | Script converts → Agent reviews → draft |
| **Deep** (深度) | Topic clusters or rough notes needing research | Agent reads all related notes → research report |

Default: `effort: "小"` → fast; `type: "cluster"` or `effort: "大"` → deep. User decides.

## Confirm & Execute

Display a confirmation summary (all Levels):

```text
确认选择：
  Fast track:
    1. 后LLM时代代码Review → blog/
    3. SSH私钥加密 → til/
  Deep track:
    2. 优雅的哲学 (9篇关联) → blog/

开始处理？
```

Wait for user confirmation, then dispatch.

### Parallel dispatch

Dispatch N parallel Agents using the Task tool, one per selected item.

> 其他 Agent 环境：以下 Fast/Deep track 任务相互独立，可按顺序依次执行。

```text
总编 (Main Agent)
├── Task Agent 1: 文章 A (fast track)
├── Task Agent 2: 文章 B (fast track)
└── Task Agent 3: 主题簇 C (deep track)
```

Use the Task tool to launch all Agents in a single message. Each Agent should be a `general-purpose` subagent with a detailed prompt containing all the information it needs.

See [agent-instructions.md](references/agent-instructions.md) for the complete Fast Track and Deep Track agent prompt templates.

### State updates

Individual Agents do NOT update `.note-to-blog.json` directly. After all Agents complete, the main agent runs state updates sequentially:

```bash
python3 <skill-dir>/scripts/note-to-blog.py state draft "<note_path>" \
  --target "<collection>/<slug>.md" \
  --note-repo "<NOTE_REPO>"
```

Deep track items are NOT marked as drafted (they need further user decision).

## Summary

After all Agents complete, present a unified summary:

```text
Fast Track 完成：
  ✓ 后LLM时代代码Review → repos/bokushi/src/content/blog/llm-code-review.md
    - 转换正常，无问题
  ✓ SSH私钥加密 → repos/bokushi/src/content/til/ssh-key-encryption.md
    - 发现 1 个 TODO 标记需要手动处理

Deep Track 完成：
  📋 优雅的哲学 (9篇关联)
    - 研究报告已生成
    - 下一步？ a) 按大纲写作  b) 修改大纲  c) 暂不处理

状态更新：
  drafted: N 篇

草稿均为 hidden: true，需要手动 review 后改为 false 发布。
建议使用 /writing-proofreading 进行审校。

发布后运行:
  python3 <skill-dir>/scripts/note-to-blog.py state publish "<note_path>" --note-repo "<NOTE_REPO>"
```

## Detailed References

- Path configuration: [user-config.md](references/user-config.md)
- LLM evaluation prompt and scoring: [scoring-criteria.md](references/scoring-criteria.md)
- Agent prompt templates: [agent-instructions.md](references/agent-instructions.md)
