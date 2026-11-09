# Niracler Skills

Personal Codex and Claude Code workflows packaged as three general-purpose plugins. The same bundled skills remain discoverable through the skills CLI.

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

Markdown linting and skill review workflows.

| Skill | Purpose | Main dependencies |
| --- | --- | --- |
| [markdown-lint](plugins/developer-workflows/skills/markdown-lint/SKILL.md) | Configure and repair Markdown linting | Node.js, markdownlint-cli2 |
| [skill-reviewer](plugins/developer-workflows/skills/skill-reviewer/SKILL.md) | Audit Agent Skill quality and compatibility | Built-in `skill-creator` |

### Personal Knowledge

Reusable Anki flashcard workflow.

| Skill | Purpose | Main dependencies |
| --- | --- | --- |
| [anki-card-generator](plugins/personal-knowledge/skills/anki-card-generator/SKILL.md) | Generate atomic Anki cards | None |

### Creative Fun

| Skill | Purpose | Main dependencies |
| --- | --- | --- |
| [zaregoto-miko](plugins/creative-fun/skills/zaregoto-miko/SKILL.md) | Rewrite text using the configured character-voice pattern | None |

## Dependency notes

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
- [Semantic Versioning](https://semver.org/)
