# Personal Claude Code Skills

My personal Claude Code skills collection.

## Installation

```bash
npx skills add niracler/skill
```

Or via Claude Code marketplace:

```bash
claude plugin marketplace add https://github.com/niracler/skill.git
```

## Skills

```text
╭──────────────────────────────────────────────────────╮
│  $ skill architecture                                │
│                                                      │
│  Dependencies:                                       │
│    diary-assistant                                   │
│    ├──▶ schedule-manager        task review           │
│    ├──▶ yunxiao                 work log              │
│    └──▶ anki-card-generator     TIL → flashcards     │
│    writing-proofreading                              │
│    └──▶ markdown-lint           step 6 formatting    │
│    git-workflow                                      │
│    └╌╌▶ yunxiao                 codeup.aliyun.com    │
│    skill-reviewer                                    │
│    └╌╌▶ writing-skills          quality audit (ext)   │
│                                                      │
│  Groups:                                             │
│    Workflow  git-workflow · yunxiao · schedule-mgr    │
│             ha-integration-reviewer · markdown-lint  │
│             skill-reviewer · code-sync               │
│    Writing  diary-assistant · writing-proofreading   │
│             writing-inspiration                      │
│    Learning anki-card-generator                      │
│    Fun      zaregoto-miko                            │
│                                                      │
│  ──▶ dependency  ╌╌▶ conditional routing             │
╰──────────────────────────────────────────────────────╯
```

Scope: 🌐 = EN-friendly · 🍎 = macOS only · 🔒 = personal/niche

### Workflow

| Skill | Description | Scope |
|-------|-------------|-------|
| [git-workflow](skills/git-workflow/SKILL.md) | Conventional Commits, PR templates, release workflow | 🌐 |
| [code-sync](skills/code-sync/SKILL.md) | Batch sync git repos — push (end-of-day) or pull (start-of-day) | 🌐 |
| [markdown-lint](skills/markdown-lint/SKILL.md) | markdownlint + pre-commit hook setup and batch fix | |
| [skill-reviewer](skills/skill-reviewer/SKILL.md) | Audit skills for quality and cross-platform compatibility | |
| [yunxiao](skills/yunxiao/SKILL.md) | Alibaba Cloud DevOps CLI (git-repo, Push Review, OpenAPI) | |
| [ha-integration-reviewer](skills/ha-integration-reviewer/SKILL.md) | Home Assistant integration code review for PR prep | 🔒 |
| [schedule-manager](skills/schedule-manager/SKILL.md) | Apple Calendar & Reminders via osascript, GTD methodology | 🍎 |

### Writing

| Skill | Description | Scope |
|-------|-------------|-------|
| [writing-inspiration](skills/writing-inspiration/SKILL.md) | Guided writing for travel notes, TIL, and articles | |
| [writing-proofreading](skills/writing-proofreading/SKILL.md) | 6-step Chinese article review workflow | |
| [diary-assistant](skills/diary-assistant/SKILL.md) | Daily journal with GTD task review and work log automation | 🍎 🔒 |

### Learning

| Skill | Description | Scope |
|-------|-------------|-------|
| [anki-card-generator](skills/anki-card-generator/SKILL.md) | Generate Anki flashcards with atomization principles | 🌐 |

### Fun

| Skill | Description | Scope |
|-------|-------------|-------|
| [zaregoto-miko](skills/zaregoto-miko/SKILL.md) | Convert text to Zaregoto series Miko Aoi's speaking style | 🔒 |

## Recommended External Skills

| Skill | Source | Purpose |
|-------|--------|---------|
| `writing-skills` | [obra/superpowers](https://github.com/obra/superpowers) | Deep quality audit for skill-reviewer |
| `brainstorming` | [obra/superpowers](https://github.com/obra/superpowers) | Structured brainstorming before creative work |

## Resources

- [skills.sh](https://skills.sh/) - Community-driven marketplace for AI agent skills. Browse by popularity and category, discover quality skills (React best practices, web design standards, security guides, etc.). Supports Claude Code, Cursor, Copilot, and 30+ agents.
- [skills CLI](https://github.com/vercel-labs/skills) - Agent skills management CLI by Vercel. `npx skills add <owner/repo>` to install. Supports global/project-level installation, auto-detects local agents, and batch updates. Pairs with skills.sh for a complete discover → install → manage workflow.
- [Agent Skills Documentation](https://code.claude.com/docs/en/skills)
- [How to Create Custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
