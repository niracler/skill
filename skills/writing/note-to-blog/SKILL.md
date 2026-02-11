---
name: note-to-blog
description: Use when user wants to find a note to publish as a blog post. Triggers on「选一篇笔记发博客」「note to blog」「写博客」「博客选题」. Scans Obsidian notes, evaluates blog-readiness, converts and creates draft.
---

# Note to Blog

从 Obsidian Note 仓库中筛选适合发布的笔记，评估适配性，转换格式并生成博客草稿。

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| writing-proofreading | skill | No | Included in `npx skills add niracler/skill` |

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing tool, directly guide the user through installation and configuration step by step.

## Workflow Overview

```text
Phase 1: 收集    Phase 2: 评估    Phase 3: 交互    Phase 4: 转换
 扫描+过滤  ──▶  LLM 打分  ──▶  选择+标记  ──▶  格式转换+草稿
```

Each phase completes before the next begins. The entire flow targets one article per run.

## Phase 1: Collect

Gather data from three sources in parallel:

```text
┌─ Source A: Note 仓库 *.md (候选池)
├─ Source B: bokushi blog/til/monthly (已发布)
└─ Source C: Claude Code sessions (活跃信号)
```

### Step 1.1: Scan Note repository

1. Read the Note repository path from [user-config.md](references/user-config.md)
2. Find all `*.md` files under `Areas/`, `Inbox/`, and `Archives/`
3. Read `.note-to-blog.json` from the Note repository root
   - If it does not exist, create an empty one: `{"published": {}, "skipped": {}}`
4. Exclude files already in `published` or `skipped` (silently ignore entries whose files no longer exist on disk)
5. For each remaining candidate, extract:
   - **Title**: from frontmatter `title` or `aliases`, fallback to filename (without `.md`)
   - **Summary**: first 20 non-empty, non-frontmatter lines
   - **Word count**: total characters in the file
   - **Path**: relative to the Note repository root

### Step 1.2: Read published blog posts

Read all files from `repos/bokushi/src/content/blog/`, `til/`, and `monthly/`. Extract title and tags from each file's frontmatter. This list is used for deduplication.

### Step 1.3: Extract session activity signals

1. Read the session data paths from [user-config.md](references/user-config.md)
2. For each configured project path, read `sessions-index.json`:
   - Filter entries with `fileMtime` within the last 30 days
   - Extract `summary` and `firstPrompt` fields
3. Read `~/.claude/history.jsonl`:
   - Filter entries with `timestamp` within the last 30 days and matching project paths
   - Extract `display` field
4. Compile into a keyword list for the LLM

**If session data is not found**: proceed without session signals. Note "session 数据未找到，跳过活跃度分析" in the output.

## Phase 2: Evaluate

Make a single LLM evaluation call using the prompt template from [scoring-criteria.md](references/scoring-criteria.md).

### Input

Construct the prompt with:

- Candidate list: title + summary + word count (from Phase 1)
- Published list: title + tags (from Phase 1)
- Session keywords: compiled keyword list (from Phase 1)

### Output

The LLM SHALL return a JSON array of 5~8 recommendations:

```json
[
  {
    "path": "Areas/大模型(LLM)/关于后 LLM 时代的代码 Review 的看法.md",
    "title": "关于后 LLM 时代的代码 Review 的看法",
    "score": 92,
    "collection": "blog",
    "effort": "小",
    "session_activity": "★★★",
    "duplicate_risk": "none",
    "reason": "结构完整、有真实案例、观点独特，且近期 session 高度活跃"
  }
]
```

### Validation

If the LLM response is not valid JSON or missing required fields, retry once with explicit format instructions.

## Phase 3: Interact

### Step 3.1: Present recommendations

Display the recommendation list as a table:

```text
#  标题                          适配分  目标      工作量  活跃   重复风险
1  后LLM时代代码Review            92    blog      小     ★★★   无
2  SSH私钥加密                    88    til       小     ─     无
3  Feed内容阅读姿势               85    blog      小     ★     无
...
```

### Step 3.2: User actions

The user can:

| Action | How |
|--------|-----|
| Select one article | "选 1" or "第一篇" |
| Mark as skip | "跳过 3, 5, 7" with optional reason |
| Override collection | "放 til 吧" |
| See more candidates | "还有别的吗" |
| Batch mark skip | "3~7 全部跳过，reason: private" |

**On skip**: update `.note-to-blog.json` immediately:

```json
{
  "skipped": {
    "<relative-path>": {
      "reason": "<user-provided or 'no reason'>",
      "date": "2026-02-07"
    }
  }
}
```

### Step 3.3: Confirm selection

After the user selects one article:

1. Read the full text of the selected file
2. Show a confirmation:

```text
「关于后 LLM 时代的代码 Review 的看法」
  字数: ~1200 字
  工作量: 小（格式转换 + 基本修复）
  目标: blog/
  确认？
```

1. Wait for user confirmation before proceeding to Phase 4

## Phase 4: Convert

### Step 4.1: Obsidian syntax conversion

Apply all rules from [obsidian-conversion.md](references/obsidian-conversion.md):

| Obsidian syntax | Output |
|-----------------|--------|
| `![[image.png]]` | `![](original-url)` |
| `![[image.png\|400]]` | `![](original-url)` (size removed) |
| `[[wikilink]]` | plain text |
| `[[wikilink\|display]]` | display text |
| `:span[text]{.spoiler}` | `<span class="spoiler">text</span>` |
| `> [!type] title` | `> **Type:** title` |
| inline `#tag` | remove from body, collect to frontmatter tags |

**For unrecognized Obsidian syntax**: preserve as-is and add a comment `<!-- TODO: manual conversion needed -->` nearby.

**Standard Markdown** (e.g., `![alt](url)`, `[text](url)`) SHALL be preserved unchanged — only convert Obsidian-specific syntax.

### Step 4.2: Generate frontmatter

Generate bokushi-compatible frontmatter:

Frontmatter fields:

| Field | Value |
|-------|-------|
| `title` | From Note title |
| `pubDate` | Today's date |
| `tags` | From Note tags + inline #tags |
| `description` | LLM-generated one-sentence summary |
| `hidden` | `true` (draft mode) |

- `pubDate` SHALL be today's date (not the Note's original date)
- `hidden` SHALL always be `true` (draft mode)
- `description` SHALL be generated by the LLM based on the article content

### Step 4.3: Light editing

Apply basic readability fixes:

- Remove Obsidian-specific frontmatter fields (`aliases`, `date`, `modified`, `date updated`, `score`)
- Remove orphaned inline tags (already collected to frontmatter)
- Fix broken links or image references (add TODO comments if unresolvable)
- Ensure consistent heading levels

Do NOT restructure the article or rewrite paragraphs. Deep editing is handled by `/writing-proofreading`.

### Step 4.4: Write draft

1. Generate a kebab-case filename from the title (e.g., "SSH 私钥加密" → `ssh-key-encryption.md`)
2. Write to `repos/bokushi/src/content/<collection>/<filename>.md`
3. Update `.note-to-blog.json`:

```json
{
  "published": {
    "<relative-path>": {
      "target": "<collection>/<filename>.md",
      "date": "2026-02-07"
    }
  }
}
```

### Step 4.5: Suggest proofreading

Output:

```text
草稿已生成：repos/bokushi/src/content/<collection>/<filename>.md（hidden: true）

建议下次运行 /writing-proofreading 进行审校，完成后改 hidden: false 发布。
```

## Detailed References

- Path configuration: [user-config.md](references/user-config.md)
- Obsidian conversion rules: [obsidian-conversion.md](references/obsidian-conversion.md)
- LLM evaluation prompt and scoring: [scoring-criteria.md](references/scoring-criteria.md)
