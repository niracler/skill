---
name: diary-note
metadata: {"openclaw":{"emoji":"📝"}}
description: >-
  Use this skill to instantly capture a quick note, insight, TIL, or lesson learned
  directly into today's diary — without going through a full journaling session.
  Invoke when the user says things like 记到日记里, 记录一下, 追记, jot this down,
  or "add this to my diary". Perfect for end-of-coding-session learnings, spontaneous
  insights, or brief experience logs. Appends to the existing diary file in the right
  section automatically. Not for full diary writing sessions (use diary-assistant) or
  work summaries (use weekly-report).
---

# Diary Note

快速追记一段内容到今天的日记。适合 agent session 结束时记录经验、随手记 TIL、
或任何不想走完整日记流程的场景。

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| None | — | — | No external dependencies |

## When to Use

- Agent session 结束后，想把经验/教训记下来
- 随手记一个 TIL 或想法
- 工作中遇到值得记录的事，但不想启动完整日记流程

**不适用：**

- 完整日记写作 → 使用 `diary-assistant`
- 周报写作 → 使用 `weekly-report`

## Flow

```text
1. Locate diary file   (~0min, automatic)
2. Determine section   (~0min, automatic)
3. Append content      (~1min)
4. Optional: Anki      (~0min, ask only)
```

## Step 1: Locate Diary File

Diary path configuration is shared with diary-assistant.

Check for config at `~/.config/nini-skill/diary/user-config.md`.
If not found, check diary-assistant's `references/user-config.md` as fallback.
If neither exists, ask the user for their diary path.

**File name**: `{YYYY-MM-DD}.md` (today's date).

If the file doesn't exist, create it with a basic heading:

```markdown
# {YYYY-MM-DD}
```

## Step 2: Determine Section

Read the existing diary file and decide where to append:

| Content type | Target section | Create if missing |
|-------------|----------------|-------------------|
| Work experience / technical | `## 2 Work Log` | Yes |
| Personal note / thought | `## 3 Record` | Yes |
| User specifies section | As specified | Yes |

If the diary file has no section structure, append at the end.

## Step 3: Append Content

Write the content provided by the user (or summarized from the conversation)
to the target section. Format rules:

- Use bullet points or short paragraphs
- Preserve the user's voice — don't over-polish
- Add a timestamp prefix if multiple entries exist in the same section:
  `**14:30** — content here`
- If the user provides raw conversation context (e.g., "record what we just did"),
  summarize the key takeaways concisely

## Step 4: Optional Anki

If the content contains a TIL (Today I Learned) pattern:

```text
"Want to generate Anki cards from this? (invoke anki-card-generator)"
```

Only ask, don't auto-invoke.

## Common Issues

| Issue | Fix |
|-------|-----|
| Diary path not found | Ask user, suggest saving to `~/.config/nini-skill/diary/user-config.md` |
| File encoding issues | Obsidian uses UTF-8, ensure write uses UTF-8 |
| Section heading mismatch | Read file first, match existing section names |
