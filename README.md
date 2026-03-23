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
│    CLI: git(7) · gh(3) · curl(2) · reminders-cli(3)     │
│         jq(2) · markdownlint-cli2(2) · osascript(3)     │
│         aliyun-cli(1) · pre-commit(1) · python3(1)      │
│    API: Pinboard(2)                                      │
│    MCP: yunxiao(3) · context7(1)                         │
│                                                          │
│  Skill Dependencies:                                     │
│    diary-assistant                                       │
│    ├──▶ schedule-manager        task review               │
│    └──▶ anki-card-generator     TIL → flashcards         │
│    diary-note                                            │
│    └╌╌▶ anki-card-generator     optional TIL cards       │
│    weekly-report                                         │
│    └╌╌▶ yunxiao                 云效 data                 │
│    note-to-blog                                          │
│    └╌╌▶ writing-assistant       draft proofreading       │
│    writing-assistant                                     │
│    └╌╌▶ markdown-lint           step 6 formatting        │
│    code-sync                                             │
│    └╌╌▶ git-workflow            dirty repo commits       │
│    git-workflow                                          │
│    └╌╌▶ yunxiao                 codeup.aliyun.com        │
│    skill-reviewer                                        │
│    └╌╌▶ skill-creator           quality audit (built-in)  │
│    workspace-init ◇ dev-config-template                  │
│    workspace-planning ◇ dev-config-template              │
│    biweekly-collector ◆ Pinboard API                     │
│    pinboard-manager ◆ Pinboard API                       │
│                                                          │
│  Groups:                                                 │
│    Workspace workspace-init · workspace-planning         │
│    Workflow  git-workflow · yunxiao · schedule-mgr        │
│             ha-integration-reviewer · markdown-lint      │
│             skill-reviewer · code-sync · weekly-report   │
│             pinboard-manager                             │
│    Writing  writing-assistant · diary-assistant           │
│             diary-note · note-to-blog                    │
│             biweekly-collector                            │
│    Learning anki-card-generator                          │
│    Fun      zaregoto-miko                                │
│                                                          │
│  ──▶ dependency  ╌╌▶ conditional/optional                │
│  ◇ requires external template/repo                      │
│  ◆ requires external API/service                        │
╰──────────────────────────────────────────────────────────╯
```

Scope: EN-friendly · macOS only · personal/niche

### Workspace

| Skill | Description | Dependencies | Scope |
|-------|-------------|--------------|-------|
| [workspace-init](skills/workspace/workspace-init/SKILL.md) | Interactive initialization for [dev-config-template](https://github.com/niracler/dev-config-template) workspaces — repos.json, CLAUDE.md, OpenSpec, environments, validation | git, jq, openspec | EN-friendly |
| [workspace-planning](skills/workspace/workspace-planning/SKILL.md) | Project schedule management with YAML-based modules, milestones, and delivery tracking | [dev-config-template](https://github.com/niracler/dev-config-template) | EN-friendly |

### Workflow

| Skill | Description | Dependencies | Scope |
|-------|-------------|--------------|-------|
| [git-workflow](skills/workflow/git-workflow/SKILL.md) | Conventional Commits, PR templates, release workflow | git, gh | EN-friendly |
| [code-sync](skills/workflow/code-sync/SKILL.md) | Batch sync git repos — push (end-of-day) or pull (start-of-day) | git | EN-friendly |
| [weekly-report](skills/workflow/weekly-report/SKILL.md) | 软件研发周报: scan schedules, git logs, daily notes into structured weekly report | git, reminders-cli, gh, yunxiao | personal |
| [markdown-lint](skills/workflow/markdown-lint/SKILL.md) | markdownlint + pre-commit hook setup and batch fix | Node.js, markdownlint-cli2 | |
| [skill-reviewer](skills/workflow/skill-reviewer/SKILL.md) | Audit skills for quality and cross-platform compatibility | skill-creator (built-in) | |
| [yunxiao](skills/workflow/yunxiao/SKILL.md) | Alibaba Cloud DevOps CLI (git-repo, Push Review, OpenAPI) | git, yunxiao MCP / aliyun CLI | |
| [ha-integration-reviewer](skills/workflow/ha-integration-reviewer/SKILL.md) | Home Assistant integration code review for PR prep | git, gh, Context7 MCP | personal |
| [pinboard-manager](skills/workflow/pinboard-manager/SKILL.md) | Pinboard bookmark tag audit, dead link detection, and timeliness check | curl, Pinboard API | EN-friendly |
| [schedule-manager](skills/workflow/schedule-manager/SKILL.md) | Apple Calendar & Reminders via osascript, GTD methodology | reminders-cli | macOS |

### Writing

| Skill | Description | Dependencies | Scope |
|-------|-------------|--------------|-------|
| [writing-assistant](skills/writing/writing-assistant/SKILL.md) | Writing companion: inspiration mode (brainstorm from scratch) + proofreading mode (6-step Chinese article review) | markdownlint-cli2 | |
| [diary-assistant](skills/writing/diary-assistant/SKILL.md) | Daily journal with GTD task review and planning | reminders-cli, schedule-manager | macOS, personal |
| [diary-note](skills/writing/diary-note/SKILL.md) | Quick-append notes to today's diary (experiences, TIL, insights) | — | |
| [note-to-blog](skills/writing/note-to-blog/SKILL.md) | Scan Obsidian notes, evaluate blog-readiness, convert and create draft | writing-assistant | personal |
| [biweekly-collector](skills/writing/biweekly-collector/SKILL.md) | Collect raw materials from 8 sources (diary, Pinboard, Douban, Telegram, Calendar, Reminders, RSS digests, plrom) for personal biweekly diary | curl, reminders-cli, osascript, git, python3, Pinboard API | macOS, personal |

### Learning

| Skill | Description | Dependencies | Scope |
|-------|-------------|--------------|-------|
| [anki-card-generator](skills/learning/anki-card-generator/SKILL.md) | Generate Anki flashcards with atomization principles | — | EN-friendly |

### Fun

| Skill | Description | Dependencies | Scope |
|-------|-------------|--------------|-------|
| [zaregoto-miko](skills/fun/zaregoto-miko/SKILL.md) | Convert text to Zaregoto series Miko Aoi's speaking style | — | personal |

## Recommended External Skills

| Skill | Source | Purpose |
|-------|--------|---------|
| `brainstorming` | [obra/superpowers](https://github.com/obra/superpowers) | Structured brainstorming before creative work |

## Resources

- [skills.sh](https://skills.sh/) - Community-driven marketplace for AI agent skills. Browse by popularity and category, discover quality skills (React best practices, web design standards, security guides, etc.). Supports Claude Code, Cursor, Copilot, and 30+ agents.
- [skills CLI](https://github.com/vercel-labs/skills) - Agent skills management CLI by Vercel. `npx skills add <owner/repo>` to install. Supports global/project-level installation, auto-detects local agents, and batch updates. Pairs with skills.sh for a complete discover -> install -> manage workflow.
- [Agent Skills Documentation](https://code.claude.com/docs/en/skills)
- [How to Create Custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
