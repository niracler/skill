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
│             skill-reviewer                           │
│    Writing  diary-assistant · writing-proofreading   │
│             writing-inspiration                      │
│    Learning anki-card-generator                      │
│    Fun      zaregoto-miko                            │
│                                                      │
│  ──▶ dependency  ╌╌▶ conditional routing             │
╰──────────────────────────────────────────────────────╯
```

### 🔄 git-workflow

Standardized Git workflow for commits, PRs, and releases.

- Conventional Commits format (no AI signatures)
- Pull Request templates
- Release workflow with CHANGELOG

[View Documentation](skills/git-workflow/SKILL.md)

### ☁️ yunxiao

CLI tools for Alibaba Cloud DevOps (Yunxiao/云效).

- git-repo installation and commands (git pr)
- Push Review Mode (zero-install alternative)
- aliyun CLI + OpenAPI for Projex tasks

[View Documentation](skills/yunxiao/SKILL.md)

### 🏠 ha-integration-reviewer

Strict Home Assistant integration code reviewer for PR preparation.

- Quality Scale rules verification (Bronze/Silver/Gold/Platinum)
- Parallel checking with multiple agents (code style, config flow, tests, docs)
- Dynamic fetching of latest HA developer documentation
- Common issues checklist from real PR reviews

[View Documentation](skills/ha-integration-reviewer/SKILL.md)

### 📔 diary-assistant

Daily journal writing with GTD integration. Designed for **45-minute workflow**.

- Reminders integration for task review and planning
- Work Log automation on workdays (git/yunxiao)
- Adaptive questioning (workday vs weekend)
- Smart follow-up (TIL → Anki cards)

[View Documentation](skills/diary-assistant/SKILL.md)

### ✍️ writing-inspiration

Guided writing for travel notes, TIL, and general articles.

- Travel writing framework (departure → journey → reflection)
- TIL framework (background → process → solution → takeaway)
- General article framework (trigger → viewpoint → expansion → conclusion)

[View Documentation](skills/writing-inspiration/SKILL.md)

### 📝 writing-proofreading

6-step article review workflow for Chinese writing.

- Structure diagnosis & reader context check
- Chinese style guide (based on Yu Guangzhong's "How to Improve Anglicized Chinese")
- Source verification & footnotes
- Personal style consistency

[View Documentation](skills/writing-proofreading/SKILL.md)

### 🃏 anki-card-generator

Generate high-quality Anki flashcards following atomization principles and cognitive science best practices.

- simple-anki-sync compatible markdown output
- Atomization rules (word limits, one concept per card)
- Standardized question templates
- Domain examples (history, programming, language, psychology)

[View Documentation](skills/anki-card-generator/SKILL.md)

### 🔧 markdown-lint

Configure markdown formatting and linting for any repository.

- markdownlint + pre-commit hook setup
- Horizontal rule ban (outside YAML frontmatter)
- Batch fix and validation workflow

[View Documentation](skills/markdown-lint/SKILL.md)

### 🔍 skill-reviewer

Audit Claude Code skills for quality and cross-platform/cross-agent compatibility.

- Delegates structure checks to bundled `validate.sh`, quality checks to `writing-skills`
- Platform compatibility scan (macOS-only commands, Windows incompatibilities)
- Agent compatibility check (Claude Code-first with fallback annotations)
- npx skills ecosystem validation (marketplace.json, symlink safety, cross-skill dependencies)

[View Documentation](skills/skill-reviewer/SKILL.md)

### 📅 schedule-manager

Manage Apple Calendar and Reminders via osascript, following GTD methodology.

- GTD-style workflow (Calendar = fixed commitments, Reminders = tasks)
- osascript + icalBuddy dual support for better recurring event handling
- Quick capture, meeting scheduling, daily/weekly planning
- Permission and dependency check scripts

[View Documentation](skills/schedule-manager/SKILL.md)

### 🎭 zaregoto-miko

Convert text to Zaregoto series Miko Aoi's speaking style - the energetic 19-year-old with absurd metaphors.

- Core pattern: `就好像『A，可是B』耶！`
- Original quotes reference from the novel
- Material → Style conversion workflow
- Tone markers and rhythm guide

[View Documentation](skills/zaregoto-miko/SKILL.md)

## Development

### Add New Skill

```bash
# Initialize
python3 scripts/init_skill.py your-skill-name --path skills

# Edit files
# - your-skill-name/SKILL.md
# - your-skill-name/references/
# - your-skill-name/scripts/

# Update .claude-plugin/marketplace.json
# Add "./skills/your-skill-name" to skills array

# Validate
./scripts/validate.sh

# Commit
git add .
git commit -m "feat: add your-skill-name"
git push
```

### Validate Skills

```bash
./scripts/validate.sh
```

## Structure

```text
skill/
├── .claude-plugin/
│   └── marketplace.json
├── .markdownlint.json
├── .pre-commit-config.yaml
├── skills/
│   ├── anki-card-generator/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── diary-assistant/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── git-workflow/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── scripts/
│   ├── ha-integration-reviewer/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── markdown-lint/
│   │   ├── SKILL.md
│   │   └── scripts/
│   ├── schedule-manager/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── scripts/
│   ├── skill-reviewer/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── scripts/
│   ├── writing-inspiration/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── writing-proofreading/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── yunxiao/
│   │   ├── SKILL.md
│   │   └── references/
│   └── zaregoto-miko/
│       ├── SKILL.md
│       └── references/
└── scripts/
    ├── check-horizontal-rules.sh
    ├── init_skill.py
    ├── quick_validate.py
    └── validate.sh
```

## Recommended External Skills

| Skill | Source | Purpose |
|-------|--------|---------|
| `writing-skills` | [obra/superpowers](https://github.com/obra/superpowers) | Deep quality audit for skill-reviewer |
| `brainstorming` | [obra/superpowers](https://github.com/obra/superpowers) | Structured brainstorming before creative work |

```bash
npx skills add https://github.com/obra/superpowers --skill writing-skills
```

## Resources

- [Agent Skills Documentation](https://code.claude.com/docs/en/skills)
- [How to Create Custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
