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
╭──────────────────────────────────────────────────────────╮
│  $ skill architecture                                    │
│                                                          │
│  External Dependencies:                                  │
│    CLI: git(6) · gh(3) · curl(1) · reminders-cli(2)     │
│         jq(2) · markdownlint-cli2(2) · osascript(2)     │
│         aliyun-cli(1) · pre-commit(1)                    │
│    API: Pinboard(1)                                      │
│    MCP: yunxiao(3) · context7(1)                         │
│                                                          │
│  Skill Dependencies:                                     │
│    diary-assistant                                       │
│    ├──▶ schedule-manager        task review               │
│    ├──▶ worklog                 work log                  │
│    │    └╌╌▶ yunxiao            云效 data                 │
│    └──▶ anki-card-generator     TIL → flashcards         │
│    note-to-blog                                          │
│    └╌╌▶ writing-proofreading    draft proofreading       │
│    writing-proofreading                                  │
│    └╌╌▶ markdown-lint           step 6 formatting        │
│    code-sync                                             │
│    └╌╌▶ git-workflow            dirty repo commits       │
│    git-workflow                                          │
│    └╌╌▶ yunxiao                 codeup.aliyun.com        │
│    skill-reviewer                                        │
│    └╌╌▶ writing-skills          quality audit (ext)       │
│    workspace-init ◇ dev-config-template                  │
│    workspace-planning ◇ dev-config-template              │
│    pinboard-manager ◆ Pinboard API                       │
│                                                          │
│  Groups:                                                 │
│    Workspace workspace-init · workspace-planning         │
│    Workflow  git-workflow · yunxiao · schedule-mgr        │
│             ha-integration-reviewer · markdown-lint      │
│             skill-reviewer · code-sync · worklog         │
│             pinboard-manager                             │
│    Writing  diary-assistant · note-to-blog               │
│             writing-proofreading · writing-inspiration   │
│    Learning anki-card-generator                          │
│    Fun      zaregoto-miko                                │
│                                                          │
│  ──▶ dependency  ╌╌▶ conditional/optional                │
│  ◇ requires external template/repo                      │
│  ◆ requires external API/service                        │
╰──────────────────────────────────────────────────────────╯
```

Scope: 🌐 = EN-friendly · 🍎 = macOS only · 🔒 = personal/niche

### Workspace

| Skill | Description | Dependencies | Scope |
|-------|-------------|--------------|-------|
| [workspace-init](skills/workspace/workspace-init/SKILL.md) | Interactive initialization for [dev-config-template](https://github.com/niracler/dev-config-template) workspaces — repos.json, CLAUDE.md, OpenSpec, environments, validation | git, jq, openspec | 🌐 |
| [workspace-planning](skills/workspace/workspace-planning/SKILL.md) | Project schedule management with YAML-based modules, milestones, and delivery tracking | [dev-config-template](https://github.com/niracler/dev-config-template) | 🌐 |

### Workflow

| Skill | Description | Dependencies | Scope |
|-------|-------------|--------------|-------|
| [git-workflow](skills/workflow/git-workflow/SKILL.md) | Conventional Commits, PR templates, release workflow | git, gh | 🌐 |
| [code-sync](skills/workflow/code-sync/SKILL.md) | Batch sync git repos — push (end-of-day) or pull (start-of-day) | git | 🌐 |
| [worklog](skills/workflow/worklog/SKILL.md) | Personal work review with git stats, GitHub & Yunxiao integration | git, gh, jq, yunxiao MCP | 🔒 |
| [markdown-lint](skills/workflow/markdown-lint/SKILL.md) | markdownlint + pre-commit hook setup and batch fix | Node.js, markdownlint-cli2 | |
| [skill-reviewer](skills/workflow/skill-reviewer/SKILL.md) | Audit skills for quality and cross-platform compatibility | — | |
| [yunxiao](skills/workflow/yunxiao/SKILL.md) | Alibaba Cloud DevOps CLI (git-repo, Push Review, OpenAPI) | git, yunxiao MCP / aliyun CLI | |
| [ha-integration-reviewer](skills/workflow/ha-integration-reviewer/SKILL.md) | Home Assistant integration code review for PR prep | git, gh, Context7 MCP | 🔒 |
| [pinboard-manager](skills/workflow/pinboard-manager/SKILL.md) | Pinboard bookmark tag audit, dead link detection, and timeliness check | curl, Pinboard API | 🌐 |
| [schedule-manager](skills/workflow/schedule-manager/SKILL.md) | Apple Calendar & Reminders via osascript, GTD methodology | reminders-cli | 🍎 |

### Writing

| Skill | Description | Dependencies | Scope |
|-------|-------------|--------------|-------|
| [note-to-blog](skills/writing/note-to-blog/SKILL.md) | Scan Obsidian notes, evaluate blog-readiness, convert and create draft | writing-proofreading | 🔒 |
| [writing-inspiration](skills/writing/writing-inspiration/SKILL.md) | Guided writing for travel notes, TIL, and articles | — | |
| [writing-proofreading](skills/writing/writing-proofreading/SKILL.md) | 6-step Chinese article review workflow | markdownlint-cli2 | |
| [diary-assistant](skills/writing/diary-assistant/SKILL.md) | Daily journal with GTD task review and work log automation | reminders-cli | 🍎 🔒 |

### Learning

| Skill | Description | Dependencies | Scope |
|-------|-------------|--------------|-------|
| [anki-card-generator](skills/learning/anki-card-generator/SKILL.md) | Generate Anki flashcards with atomization principles | — | 🌐 |

### Fun

| Skill | Description | Dependencies | Scope |
|-------|-------------|--------------|-------|
| [zaregoto-miko](skills/fun/zaregoto-miko/SKILL.md) | Convert text to Zaregoto series Miko Aoi's speaking style | — | 🔒 |

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
