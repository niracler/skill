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

## Step 1: Locate Diary File and Style Preferences

Diary configuration is shared with diary-assistant.

Check for config at `~/.config/nini-skill/diary/user-config.md`.
If not found, check diary-assistant's `references/user-config.md` as fallback.
If neither exists, ask the user for their diary path.

After locating the config, **also read the `## 写作风格` section if present**.
Layer those personal style preferences on top of the universal rules in Step 3
(formatting, punctuation, voice cues). If the section is absent, the universal
rules alone are enough.

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
to the target section.

### Universal rules

- **Diary is for the writer's future self, not for explaining things they already
  know.** Leave hooks (keywords, dates, context references) instead of unfolding
  the full story. Aim for "reminder" not "article".
- **Filter for human-side content, not agent-side debugging.** Diary entries
  should capture the human writer's strategic decisions, principles they
  articulated, surprises in their own thinking, or experience-level reflections.
  Agent-side tooling pitfalls (broken pre-commit hooks, MCP API gaps, sandbox
  SSL hiccups, missed `git add`, plugin install commands) are operational
  debugging notes — they belong in agent memory (`feedback_*.md`) or workflow
  READMEs, NOT in the user's diary. When summarizing a session, ask:
  "would the human want to recall this in 3 months, or is this just what
  the agent had to fight through to get the job done?"
- **Avoid narrator / reflective framing**. Phrases like 「今天最大的洞察」
  「之前一直以为……但其实」「借这个机会」「值得记录的是」 are AI-style article
  openings; strip them. Same in English: "The key insight today is", "What I
  realized is".
- **Prefer prose paragraphs over sub-headings inside an entry.** Sub-headings
  invite filler (an AI will pad bullets to balance them even when there's nothing
  to say). One H3 per entry is enough; the body should flow as prose. If multiple
  logical units exist in one entry, separate them with an inline divider (the
  user's preferred divider lives in `## 写作风格`) rather than another heading.
- Use bullet points or short paragraphs.
- Preserve the user's voice — don't over-polish.
- Add a timestamp prefix if multiple entries exist in the same section:
  `**14:30** — content here`
- If the user provides raw conversation context ("record what we just did"),
  summarize the key takeaways concisely.

### Style precedence

When the diary content includes Chinese prose, apply this layered precedence
(higher layers override lower layers on conflict):

1. **`tech-doc-style-chinese` skill rules** (highest) — punctuation (`「」`
   not `“”`, no exclamation marks), 中英留白, term capitalization (`GitHub` /
   `Codeup` / `OpenSpec` etc. per its extended list), blacklist words
   (`兜底` / `赋能` / `抓手` …), error-translation table, register guidance
   (「克制、直接、可执行」). If the `tech-doc-style-chinese` skill is not
   loaded in the current session, still apply its core conventions where
   reasonable.
2. **Universal rules above** (this skill's own rules: reminder hooks,
   no narrator framing, agent-side filter, prose over sub-headings).
3. **Personal style overlay** from `## 写作风格` in user-config — bold-as-TLDR,
   divider character, quote style, em-dash policy, register choice. Apply only
   for items that don't conflict with layer 1 or 2.

**Common conflict resolutions** (`tech-doc-style-chinese` wins):

- `register: 工程师口语` (user-config) vs 「克制、直接、可执行」 (tech-doc):
  prefer the more restrained tech-doc register; technical terms can still
  stay in English (e.g., `provider`, `callback`, `submodule`).
- `self_deprecating_close: true` (user-config): minimize. Tech-doc avoids
  decorative closes; if a closing remark is genuinely useful, keep it short
  and factual rather than self-deprecating (`（笑）`, `（埋雷）` etc.).
- `parenthetical_asides: true` (user-config): allow brief technical
  clarifications in parens, but avoid narrator-voice asides.
- `quote_style`, `em_dash`, `bold_as_tldr`, `section_divider`: typically
  aligned across both layers, no conflict.

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
