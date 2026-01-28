# Personal Claude Code Skills

My personal Claude Code skills collection.

## Installation

```bash
claude plugin marketplace add https://github.com/niracler/skill.git
```

## Skills

### 🔄 git-workflow

Standardized Git workflow for commits, PRs, and releases.

- Conventional Commits format (no AI signatures)
- Pull Request templates
- Release workflow with CHANGELOG

[View Documentation](src/git-workflow/SKILL.md)

### ☁️ yunxiao

CLI tools for Alibaba Cloud DevOps (Yunxiao/云效).

- git-repo installation and commands (git pr)
- Push Review Mode (zero-install alternative)
- aliyun CLI + OpenAPI for Projex tasks

[View Documentation](src/yunxiao/SKILL.md)

### 🏠 ha-integration-reviewer

Strict Home Assistant integration code reviewer for PR preparation.

- Quality Scale rules verification (Bronze/Silver/Gold/Platinum)
- Parallel checking with multiple agents (code style, config flow, tests, docs)
- Dynamic fetching of latest HA developer documentation
- Common issues checklist from real PR reviews

[View Documentation](src/ha-integration-reviewer/SKILL.md)

### ✍️ writing-assistant

Chinese writing assistant with two modes. Designed specifically for **Chinese language writing workflows**.

**Inspiration Mode** - Guided writing for when you don't know what to write

- Diary / Weekly / Monthly journal prompts
- Travel writing guidance
- TIL (Today I Learned) technical notes
- General article brainstorming

**Review Mode** - Polish and refine articles

- Structure diagnosis & reader context check
- Chinese style guide (based on Yu Guangzhong's "How to Improve Anglicized Chinese")
- Source verification & footnotes
- Personal style consistency
- Markdown formatting (prettier + markdownlint)

[View Documentation](src/writing-assistant/SKILL.md)

### 🃏 anki-card-generator

Generate high-quality Anki flashcards following atomization principles and cognitive science best practices.

- simple-anki-sync compatible markdown output
- Atomization rules (word limits, one concept per card)
- Standardized question templates
- Domain examples (history, programming, language, psychology)

[View Documentation](src/anki-card-generator/SKILL.md)

### 📅 schedule-manager

Manage Apple Calendar and Reminders via osascript, following GTD methodology.

- GTD-style workflow (Calendar = fixed commitments, Reminders = tasks)
- osascript + icalBuddy dual support for better recurring event handling
- Quick capture, meeting scheduling, daily/weekly planning
- Permission and dependency check scripts

[View Documentation](src/schedule-manager/SKILL.md)

### 🎭 zaregoto-miko

Convert text to Zaregoto series Miko Aoi's speaking style - the energetic 19-year-old with absurd metaphors.

- Core pattern: `就好像『A，可是B』耶！`
- Original quotes reference from the novel
- Material → Style conversion workflow
- Tone markers and rhythm guide

[View Documentation](src/zaregoto-miko/SKILL.md)

## Development

### Add New Skill

```bash
# Initialize
python3 scripts/init_skill.py your-skill-name --path src

# Edit files
# - your-skill-name/SKILL.md
# - your-skill-name/references/
# - your-skill-name/scripts/

# Update .claude-plugin/marketplace.json
# Add "./src/your-skill-name" to skills array

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
├── src/
│   ├── git-workflow/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── ha-integration-reviewer/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── writing-assistant/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── scripts/
│   ├── anki-card-generator/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── yunxiao/
│   │   ├── SKILL.md
│   │   └── references/
│   ├── schedule-manager/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── scripts/
│   └── zaregoto-miko/
│       ├── SKILL.md
│       └── references/
└── scripts/
    ├── init_skill.py
    ├── quick_validate.py
    └── validate.sh
```

## Resources

- [Agent Skills Documentation](https://code.claude.com/docs/en/skills)
- [How to Create Custom Skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
