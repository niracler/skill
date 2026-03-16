---
name: writing-assistant
metadata: {"openclaw":{"emoji":"✏️","requires":{"anyBins":["markdownlint-cli2"]}}}
description: >-
  Use this skill when the user needs help with personal writing — either starting a
  new piece from scratch (inspiration/brainstorming) or reviewing and polishing an
  existing article (proofreading/editing). Invoke immediately when: the user shares
  an article and asks for feedback, wants to improve their writing style, feels stuck
  on what to write, wants help structuring a travel piece/TIL note/personal essay, or
  asks to review Chinese writing quality. Trigger phrases: 帮我改文章, 检查一下, 润色,
  校对, 不知道写什么, 帮我构思, 写游记, 记录 TIL, 写点什么. NOT for diary writing
  (use diary-assistant) or formal business communications.
---

# Writing Assistant

写作助手，两种模式：**构思引导**（从零开始写）和**审校打磨**（改已有文章）。

**注意**：日记写作请使用 `diary-assistant` skill。

## Prerequisites

| Tool | Type | Required | Install |
|------|------|----------|---------|
| markdownlint-cli2 | cli | No | `npx markdownlint-cli2` (no install needed, used in proofreading step 6) |
| markdown-lint | skill | No | Included in `npx skills add niracler/skill` (for repo setup) |

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing tool, directly guide the user through installation and configuration step by step.

## Mode Selection

| User Intent | Mode | Section |
|-------------|------|---------|
| 「不知道写什么」「帮我构思」「写游记」「记录 TIL」「写点什么」 | Inspiration | [Inspiration Mode](#inspiration-mode) |
| 「帮我改文章」「检查一下」「润色」「校对一下」「看看文章」 | Proofreading | [Proofreading Mode](#proofreading-mode) |

If unclear, ask the user.

## Inspiration Mode

帮助用户在不知道写什么或如何写下去时，通过启发式提问引导写作。

### Core Principles

| Principle | Description |
|-----------|-------------|
| **One question at a time** | Design a TodoList of prompts, ask one by one |
| **Confirm before next** | User thinks -> writes -> revises -> confirms -> next question |
| **Inspire, don't ghostwrite** | Use questions to spark thinking, don't decide content direction |

### Article Type Detection

| User Intent | Type | Framework |
|-------------|------|-----------|
| 「写游记」「记录旅行」 | Travel | Departure -> Journey -> Reflection |
| 「记录 TIL」「今天学到」 | TIL | Context -> Process -> Solution -> Takeaway |
| 「写点什么」「帮我构思」 | General | Trigger -> Viewpoint -> Develop -> Close |

### Flow

```text
Detect article type -> List prompt questions -> Ask one by one -> User answers -> Confirm -> Next -> Compose
```

### Pacing

```text
Claude: "Why did you want to visit this place?"
User: [writes answer]
Claude: [confirm/follow-up] -> "OK, next question: what was the first thing you saw when you arrived?"
```

### Frameworks

Each type has a detailed framework with structure and prompt questions.
See [writing-frameworks.md](references/writing-frameworks.md) for full reference.

**After the draft is complete**, suggest switching to Proofreading Mode for review.

## Proofreading Mode

文章审校，提供 6 步审校流程，帮助打磨中文文章。

### Core Principles

| Principle | Description |
|-----------|-------------|
| **Discuss before editing** | Propose changes for user to choose, don't edit directly |
| **Review by section** | Use Markdown headings as checkpoints, 1-2 headings at a time |
| **Inspire, don't decide** | Use questions to guide draft content, don't decide for user |

### 6-Step Review Flow

```text
1. Structure -> 2. Reader Context -> 3. Language -> 4. Source Verification -> 5. Style -> 6. Markdown Format
```

### Step 1: Structure Diagnosis

**Goal**: Ensure clear structure and focused topic

- Break down paragraphs, identify themes
- Propose 2-3 reorganization options, **discuss before editing**
- Move deleted content to a separate "material.md" file

See [structure-review.md](references/structure-review.md)

### Step 2: Reader Context Check

**Core question**: "Would a reader be confused here?"

| Issue | Symptom | Fix |
|-------|---------|-----|
| Background assumption | Uses jargon/acronyms without explanation | Add explanation or footnote |
| Self-referential | "It's like that thing..." without explaining | Make description concrete |
| Logic gap | Jumps from A to C | Add transitional explanation |
| Implicit emotion | "It was so..." without setup | Add context first |
| Information gap | Assumes reader knows the backstory | Briefly provide background |

See [structure-review.md](references/structure-review.md)

### Step 3: Language Standards

Based on Yu Guangzhong's "How to Improve Europeanized Chinese":

| Issue | Example |
|-------|---------|
| Abstract noun as subject | Bad: Income reduction changes life -> Good: He changed his life due to income reduction |
| Verbose phrasing | Bad: Based on this reason -> Good: Therefore |
| Weak verbs | Bad: Make a contribution -> Good: Contribute |
| Preposition pileup | Reduce overuse of linking words |
| Passive voice abuse | Bad: The problem was solved -> Good: The problem is solved |

See [chinese-style.md](references/chinese-style.md)

### Step 4: Source Verification

**Source priority**: Government official > Authoritative media > Industry media > Avoid personal blogs

**Pacing**: Verify one -> discuss -> write one -> confirm -> next

See [source-verification.md](references/source-verification.md)

### Step 5: Style Consistency

Check against personal writing style:

| Check | Description |
|-------|-------------|
| Signature expressions | "How to put it", "Actually", "A bit..." |
| Tone | Self-deprecating openings, parenthetical commentary |
| Quantification | Use specific numbers for persuasion |
| Bold restraint | Max 3 bold phrases per heading section |

**Avoid**:

- "Not X... but Y..." pattern (AI-flavored)
- Quoted "humor" metaphors
- Emoji or numbered list openings
- Frequent dashes
- `---` horizontal rules (use headings or numbers for natural transitions)

See [personal-style.md](references/personal-style.md)

### Step 6: Markdown Formatting

```bash
npx markdownlint-cli2 article.md          # Check
npx markdownlint-cli2 --fix article.md    # Auto-fix
```

Additional manual checks:

- Heading levels are logical (H2->H3, no skipping)
- List format is consistent (all `-` or all `*`)
- Code blocks have language labels

### Review Pacing

```text
1. Read current section
2. Check against 6 steps
3. Propose suggestions (don't edit directly)
4. Wait for user confirmation
5. After confirmation, move to next section
```

**Key**: Wait for confirmation after each section review.

## Writing Style Quick Reference

| Element | Requirement |
|---------|-------------|
| Language | Conversational, like chatting with a friend |
| Paragraphs | One topic per paragraph |
| Bold | Only at important turns/insights, max 3 per section |
| Data | Weave into experience, put detailed sources in footnotes |
| Honesty | Admit gaps, mark unfinished parts, keep thinking traces |

## Detailed References

- [writing-frameworks.md](references/writing-frameworks.md) - Inspiration frameworks for travel, TIL, and general articles
- [chinese-style.md](references/chinese-style.md) - Chinese language standards
- [structure-review.md](references/structure-review.md) - Structure diagnosis and reader context
- [source-verification.md](references/source-verification.md) - Source verification and footnotes
- [personal-style.md](references/personal-style.md) - Personal style guide
