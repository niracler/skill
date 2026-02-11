---
name: note-to-blog
description: Use when user wants to find a note to publish as a blog post. Triggers on「选一篇笔记发博客」「note to blog」「写博客」「博客选题」. Scans Obsidian notes via Python script, evaluates blog-readiness, supports batch selection with fast/deep dual-track and parallel Agent dispatch.
---

# Note to Blog

从 Obsidian Note 仓库中筛选适合发布的笔记，评估适配性，批量选题，双通道处理（快速转换 / 深度研究），并行 Agent 派发。

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| Python 3 | cli | Yes | Pre-installed on macOS |
| PyYAML | pip | Yes | `pip install pyyaml` |
| writing-proofreading | skill | No | Included in `npx skills add niracler/skill` |

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing tool, directly guide the user through installation and configuration step by step.

## Script Location

All deterministic operations are handled by the Python script:

```text
scripts/note-to-blog.py  (collect / convert / state subcommands)
```

Path configuration is in [user-config.md](references/user-config.md).

## Workflow Overview

```text
Phase 1          Phase 2         Phase 3            Phase 4              Phase 5
 Collect   ──▶   Evaluate  ──▶   Interact    ──▶   Execute        ──▶   Summary
 (script)        (LLM)          (user)             (Agent Teams)         (report)
                                 ├─ select          ├─ Fast track
                                 ├─ skip            └─ Deep track
                                 └─ assign track
```

## Phase 1: Collect

Run the `collect` script to gather all data in one call:

```bash
python3 scripts/note-to-blog.py collect \
  --note-repo "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Note/" \
  --blog-content "repos/bokushi/src/content/" \
  --project-paths \
    "~/.claude/projects/-Users-sueharakyoko-code-nini-dev" \
    "~/.claude/projects/-Users-sueharakyoko-code-nini-dev-repos-bokushi" \
  --history-file "~/.claude/history.jsonl"
```

The script outputs a single JSON object to stdout containing:

- `candidates`: all eligible notes with title, summary, char_count, outgoing_links
- `clusters`: wikilink hub nodes (3+ inbound links) with related notes
- `published_posts`: existing blog posts with title, tags, collection
- `session_keywords`: recent Claude Code session activity signals
- `stats`: total_scanned, filtered_out, candidates_count

Read the JSON output and proceed to Phase 2.

## Phase 2: Evaluate

Make a single LLM evaluation using the prompt template from [scoring-criteria.md](references/scoring-criteria.md).

### Input

Construct the evaluation prompt with the `collect` JSON data:

- `candidates`: title + summary + char_count for each
- `clusters`: hub_title + related count + link_count for each
- `published_posts`: title + tags for deduplication
- `session_keywords`: for timeliness scoring

### Output

The LLM SHALL return a JSON array of 5~8 recommendations, mixing individual notes and topic clusters:

```json
[
  {
    "type": "single",
    "path": "Areas/大模型(LLM)/关于后LLM时代的代码Review.md",
    "title": "关于后 LLM 时代的代码 Review 的看法",
    "score": 92,
    "collection": "blog",
    "effort": "小",
    "session_activity": "★★★",
    "duplicate_risk": "none",
    "reason": "结构完整、有真实案例、观点独特"
  },
  {
    "type": "cluster",
    "hub_title": "优雅的哲学",
    "hub_path": "Areas/生活(Life)/优雅的哲学-v2.0.md",
    "related_count": 9,
    "score": 88,
    "collection": "blog",
    "effort": "大",
    "theme_summary": "关于如何优雅地生活的哲学思考，散落在多篇笔记中",
    "reason": "主题深度足够，需要整合多篇笔记"
  }
]
```

If the LLM response is not valid JSON, retry once with explicit format instructions.

## Phase 3: Interact

### Step 3.1: Present recommendations

Display the recommendation list as a mixed table:

```text
#  类型    标题                    适配分  目标   工作量  活跃   重复风险
1  单篇    后LLM时代代码Review      92    blog    小    ★★★    无
2  主题簇  优雅的哲学 (9篇关联)      88    blog    大    ★      无
3  单篇    SSH私钥加密              85    til     小    ─      无
4  单篇    Feed内容阅读姿势         82    blog    小    ★      无
...
```

For cluster entries, show the hub title and related note count.

### Step 3.2: User actions

The user can perform batch operations:

| Action | Example | Effect |
|--------|---------|--------|
| Select + assign track | "1 和 3 快速转换，2 走深度" | Queue items with track assignment |
| Override collection | "1 放 til" | Change target collection |
| Batch skip | "4~6 跳过，reason: private" | Mark as skipped via `state skip` |
| See more | "还有别的吗" | Request additional recommendations (exclude previously shown items) |
| Check status | "状态" | Run `state status` to show drafted/published/skipped counts |

**On skip**: run the state script immediately for each skipped item:

```bash
python3 scripts/note-to-blog.py state skip "<path>" --reason "<reason>" \
  --note-repo "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Note/"
```

### Step 3.3: Track assignment

Each selected item must be assigned a track:

| Track | When to use | What happens |
|-------|-------------|--------------|
| **Fast** (快速) | Independent, mostly complete notes | Script converts → Agent reviews → draft |
| **Deep** (深度) | Topic clusters or rough notes needing research | Agent reads all related notes → research report |

Default suggestions:

- `type: "single"` with `effort: "小"` → suggest fast track
- `type: "cluster"` or `effort: "大"` → suggest deep track
- User always makes the final decision

### Step 3.4: Confirm selections

Before proceeding, display a summary:

```text
确认选择：
  Fast track:
    1. 后LLM时代代码Review → blog/
    3. SSH私钥加密 → til/
  Deep track:
    2. 优雅的哲学 (9篇关联) → blog/

开始处理？
```

Wait for user confirmation.

## Phase 4: Execute (Agent Teams)

Dispatch N parallel Agents using the Task tool, one per selected item. Each Agent operates independently.

### Parallel dispatch

```text
总编 (Main Agent)
├── Task Agent 1: 文章 A (fast track)
├── Task Agent 2: 文章 B (fast track)
└── Task Agent 3: 主题簇 C (deep track)
```

Use the Task tool to launch all Agents in a single message (parallel execution). Each Agent should be a `general-purpose` subagent with a detailed prompt containing all the information it needs (note path, script path, target collection, etc.).

### Fast Track Agent Instructions

Each fast track Agent receives these instructions:

**Step 1 — Run the convert script** (use the absolute path to the script in the Agent prompt):

```bash
python3 "<absolute-path-to-skill>/scripts/note-to-blog.py" convert "<full-path-to-note>"
```

**Step 2 — Review the converted output** (the script automatically handles):

- Obsidian fields stripped (aliases, date, modified, etc.)
- Frontmatter set to: title, pubDate (today), tags (merged from frontmatter + inline #tags), hidden: true
- Wikilinks → plain text, image embeds → standard markdown, callouts → bold, highlights → bold, comments → removed
- Verify no conversion artifacts or TODO comments from unrecognized syntax

**Step 3 — Generate a description**: Write a one-sentence description for the blog post frontmatter (in the same language as the article content).

**Step 4 — Write the draft**: Add the `description` field to the converted frontmatter, then write to `repos/bokushi/src/content/<collection>/<slug>.md` where `<slug>` is a kebab-case version of the title.

**Step 5 — Return a result object**:

```json
{
  "status": "done",
  "note_path": "<relative note path>",
  "draft_path": "<collection>/<slug>.md",
  "description": "<generated description>",
  "issues": ["<any issues found>"],
  "suggestions": ["<improvement suggestions>"]
}
```

### Deep Track Agent Instructions

Each deep track Agent receives these instructions:

**Step 1 — Read all related notes**: Read the hub note and all related notes listed in the cluster.

**Step 2 — Produce a structured research report**:

```markdown
## 主题报告：<hub_title>

### 涉及笔记 (N 篇)
- <title> (hub, <char_count>字)
- <title> (<char_count>字)
- ...

### 主题地图
- 核心论点：...
- 子话题 A：...（涉及 N 篇）
- 子话题 B：...（涉及 N 篇）

### 重叠与矛盾
- <specific overlaps or contradictions found>

### 缺口
- <missing arguments, incomplete sections>

### 建议大纲
1. 引言：...
2. 第一部分：...（来源：笔记 A、B）
3. 第二部分：...（来源：笔记 C、需要补充）
4. 结论：...
```

**Step 3 — Return a result object**:

```json
{
  "status": "done",
  "note_path": "<hub note path>",
  "related_paths": ["<related note paths>"],
  "report": "<full research report markdown>",
  "suggested_collection": "<blog/til/monthly>"
}
```

### Important: State updates

Individual Agents do NOT update `.note-to-blog.json` directly. After all Agents complete, the main agent collects results and runs state updates sequentially:

For each fast track result:

```bash
python3 scripts/note-to-blog.py state draft "<note_path>" \
  --target "<collection>/<slug>.md" \
  --note-repo "~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Note/"
```

Deep track items are NOT marked as drafted (they need further user decision).

## Phase 5: Summary

After all Agents complete, present a unified summary:

### Fast track results

```text
Fast Track 完成：
  ✓ 后LLM时代代码Review → repos/bokushi/src/content/blog/llm-code-review.md
    - 转换正常，无问题
    - 建议：可补充最新的 AI code review 工具对比
  ✓ SSH私钥加密 → repos/bokushi/src/content/til/ssh-key-encryption.md
    - 发现 1 个 TODO 标记需要手动处理
```

### Deep track results

```text
Deep Track 完成：
  📋 优雅的哲学 (9篇关联)
    - 研究报告已生成
    - 建议大纲：4 部分，来源涵盖 7 篇笔记
    - 下一步？
      a) 按大纲写作（调用 Agent 生成初稿）
      b) 修改大纲
      c) 暂不处理
```

### State update confirmation

```text
状态更新：
  drafted: 2 篇
  下次 collect 时这些笔记将不再出现在候选列表中。

草稿均为 hidden: true，需要手动 review 后改为 false 发布。
建议使用 /writing-proofreading 进行审校。

发布后运行 state publish 更新状态：
  python3 scripts/note-to-blog.py state publish "<note_path>" --note-repo "..."
```

## Detailed References

- Path configuration: [user-config.md](references/user-config.md)
- LLM evaluation prompt and scoring: [scoring-criteria.md](references/scoring-criteria.md)
