# Niracler Skills

Personal Codex and Claude Code workflows packaged as three installable plugins. The same bundled skills remain discoverable through the skills CLI.

## Codex installation

Register the marketplace and install any needed plugins:

```bash
codex plugin marketplace add niracler/skill --ref main
codex plugin add developer-workflows@niracler-skills
codex plugin add personal-knowledge@niracler-skills
codex plugin add creative-fun@niracler-skills
```

Start a new task after installation so Codex loads the bundled skills.

## Other installation methods

Skills CLI:

```bash
npx skills add niracler/skill
```

## Plugins and skills

### Developer Workflows

Git, repository synchronization, review, linting, and engineering-report workflows.

| Skill | Purpose | Main dependencies |
| --- | --- | --- |
| [git-workflow](plugins/developer-workflows/skills/git-workflow/SKILL.md) | Commits, pull requests, and releases | Git, optional GitHub CLI |
| [code-sync](plugins/developer-workflows/skills/code-sync/SKILL.md) | Synchronize multiple repositories | Git, `git-workflow` |
| [ha-integration-reviewer](plugins/developer-workflows/skills/ha-integration-reviewer/SKILL.md) | Review Home Assistant integrations | Git, GitHub CLI, Context7 |
| [markdown-lint](plugins/developer-workflows/skills/markdown-lint/SKILL.md) | Configure and repair Markdown linting | Node.js, markdownlint-cli2 |
| [skill-reviewer](plugins/developer-workflows/skills/skill-reviewer/SKILL.md) | Audit Agent Skill quality and compatibility | Built-in `skill-creator` |
| [weekly-report](plugins/developer-workflows/skills/weekly-report/SKILL.md) | Generate software-engineering weekly reports | Git, Reminders, optional GitHub |

### Personal Knowledge

Schedules, bookmarks, diaries, writing, blogging, and learning workflows.

| Skill | Purpose | Main dependencies |
| --- | --- | --- |
| [schedule-manager](plugins/personal-knowledge/skills/schedule-manager/SKILL.md) | Manage Apple Calendar and Reminders | macOS, reminders-cli |
| [pinboard-manager](plugins/personal-knowledge/skills/pinboard-manager/SKILL.md) | Audit and maintain Pinboard bookmarks | curl, Pinboard API |
| [writing-assistant](plugins/personal-knowledge/skills/writing-assistant/SKILL.md) | Plan, review, and polish personal writing | Optional `markdown-lint` from Developer Workflows |
| [diary-assistant](plugins/personal-knowledge/skills/diary-assistant/SKILL.md) | Run a guided daily-journal workflow | macOS, `schedule-manager` |
| [diary-note](plugins/personal-knowledge/skills/diary-note/SKILL.md) | Append short notes to the current diary | None |
| [note-to-blog](plugins/personal-knowledge/skills/note-to-blog/SKILL.md) | Convert Obsidian notes into blog drafts | Python, PyYAML, optional `writing-assistant` |
| [biweekly-collector](plugins/personal-knowledge/skills/biweekly-collector/SKILL.md) | Collect material for a personal biweekly diary | macOS, curl, Git, Pinboard API |
| [anki-card-generator](plugins/personal-knowledge/skills/anki-card-generator/SKILL.md) | Generate atomic Anki cards | None |

### Creative Fun

| Skill | Purpose | Main dependencies |
| --- | --- | --- |
| [zaregoto-miko](plugins/creative-fun/skills/zaregoto-miko/SKILL.md) | Rewrite text using the configured character-voice pattern | None |

## Dependency notes

Required skill dependencies stay inside each plugin. The only cross-plugin relationship is optional: `writing-assistant` can use `markdown-lint` when Developer Workflows is also installed.

Several skills depend on local applications, CLI tools, APIs, MCP servers, or personal paths. Each `SKILL.md` documents its own prerequisites and fallback behavior.

## Local development

Validate the Marketplace, plugin manifests, bundled skills, and repository contracts:

```bash
bash scripts/validate.sh
```

Preview synchronization into local Agent Skill directories:

```bash
./scripts/sync --dry-run
```

List the skills discovered by the skills CLI:

```bash
npx skills add . --list --full-depth
```

The Codex plugin layout follows the [official plugin build documentation](https://learn.chatgpt.com/docs/build-plugins).

## Resources

- [Codex plugins](https://learn.chatgpt.com/docs/plugins)
- [Codex plugin authoring](https://learn.chatgpt.com/docs/build-plugins)
- [skills.sh](https://skills.sh/)
- [skills CLI](https://github.com/vercel-labs/skills)
- [Agent Skills specification](https://github.com/anthropics/skills)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
