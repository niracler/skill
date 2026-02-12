# Agent Instructions

Phase 4 dispatch 时，为每个选中条目启动独立 Agent。以下为各 track 的完整 prompt 模板。

All paths referenced below come from [user-config.md](user-config.md).

## Fast Track Agent

Each fast track Agent receives these instructions:

**Step 1 — Run the convert script** (use the absolute path to the script in the Agent prompt):

```bash
python3 "<skill-dir>/scripts/note-to-blog.py" convert "<full-path-to-note>"
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

## Deep Track Agent

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
