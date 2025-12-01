# Personal Claude Code Skills

My personal Claude Code skills collection.

## Installation

```bash
claude-code plugin add https://github.com/niracler/skill.git
```

Or in Claude Code:

```bash
/plugin add https://github.com/niracler/skill.git
```

## Skills

### 🔄 git-workflow

Standardized Git workflow for commits, PRs, and releases.

- Conventional Commits format (no AI signatures)
- Pull Request templates
- Release workflow with CHANGELOG

[View Documentation](git-workflow/SKILL.md)

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
│   ├── references/
│   └── scripts/
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
