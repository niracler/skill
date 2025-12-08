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

[View Documentation](git-workflow/SKILL.md)

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

[View Documentation](writing-assistant/SKILL.md)

### 🃏 anki-card-generator

Generate high-quality Anki flashcards following atomization principles and cognitive science best practices.

- simple-anki-sync compatible markdown output
- Atomization rules (word limits, one concept per card)
- Standardized question templates
- Domain examples (history, programming, language, psychology)

[View Documentation](anki-card-generator/SKILL.md)

## Development

### Add New Skill

```bash
# Initialize
python3 scripts/init_skill.py your-skill-name --path .

# Edit files
# - your-skill-name/SKILL.md
# - your-skill-name/references/
# - your-skill-name/scripts/

# Update .claude-plugin/marketplace.json
# Add "./your-skill-name" to skills array

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
├── git-workflow/
│   ├── SKILL.md
│   └── references/
├── writing-assistant/
│   ├── SKILL.md
│   ├── references/
│   └── scripts/
├── anki-card-generator/
│   ├── SKILL.md
│   └── references/
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
