# Commit Message Guide

## Format

```text
type(scope): concise summary of what changed

- Optional bullet point for key changes
- Keep each point short and focused
- Maximum 3-4 bullet points
```

## Types

- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring without behavior change
- `docs`: Documentation changes
- `test`: Test additions or modifications
- `chore`: Maintenance tasks (dependencies, tooling, releases)

## Principles

1. **Be specific and concise** - Focus on impact over details
2. **Subject line under 72 characters**
3. **Use imperative mood** - "add feature" not "added feature"
4. **Omit obvious details** - Diff shows "what", commit explains "why"
5. **Use 3-4 bullet points maximum** if body is needed
6. **NO Claude Code signatures, co-author attributions, or AI-generated markers**

## Examples

### Good Examples

```text
feat(gateway): add group control support
```

```text
fix(sensor): correct energy calculation overflow
```

```text
refactor: move register_listener to entity objects

- Add register_listener() to Device/Group/Scene in SDK
- Remove gateway parameter from integration entities
- Simplify all-light creation from 14 lines to 1 line
```

```text
chore(release): bump version to 0.2.0
```

### Bad Examples

```text
refactor: cleanup
```

*Too vague - what was cleaned up?*

```text
fix: bug fixes
```

*Not specific - which bugs?*

```text
feat: implement new authentication system

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>
```

*Contains forbidden AI markers*
