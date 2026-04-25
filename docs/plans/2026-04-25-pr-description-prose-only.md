# PR Description Prose-Only Implementation Plan

Status: Executed inline on 2026-04-25 in the same session that wrote the spec.

Spec: [`../specs/2026-04-25-pr-description-prose-only.md`](../specs/2026-04-25-pr-description-prose-only.md)

## Goal

Switch `git-workflow` and `yunxiao` skill PR/MR description guidance from a two-section markdown template to a prose-only schema. Pure documentation change, four files, validated by `grep` and `pre-commit`.

## File Map

| File | Change |
|------|--------|
| `skills/workflow/git-workflow/references/examples-and-templates.md` | Replace `## PR Template` block with prose schema, forbidden-patterns list, and three examples (English fix, English refactor, Chinese illustrating bilingual `验证：`). |
| `skills/workflow/git-workflow/SKILL.md` | Add bullet under "Default Behaviors" pointing to the new schema. |
| `skills/workflow/yunxiao/references/openapi.md` | Replace two inline `description="## Summary…"` example strings with prose. |
| `CHANGELOG.md` | Add `### Changed` under `## [Unreleased]`. |

No file is created or deleted (other than this plan and the spec).

## Tasks

1. Replace `## PR Template` block in `examples-and-templates.md`. Keep heading slug short (`## PR Description`) so SKILL.md anchor link resolves cleanly.
2. Add the prose-only bullet to `SKILL.md` Default Behaviors.
3. Rewrite both inline `## Summary` example strings in `yunxiao/references/openapi.md`.
4. Add CHANGELOG `### Changed` entry under `[Unreleased]`.
5. Verify `grep "## Summary\|## Test plan"` returns no matches in `git-workflow/` or `yunxiao/` source. Two unrelated headings in `code-sync/` and `note-to-blog/` skills are false positives — they describe each skill's own output format, not PR templates.
6. Single commit including all four files, with a commit message that itself follows the new prose-only schema (eat your own dog food).

## Verification

```bash
grep -rn "## Summary\|## Test plan" \
  skills/workflow/git-workflow/ skills/workflow/yunxiao/
# expected: 0 matches

pre-commit run --files \
  skills/workflow/git-workflow/SKILL.md \
  skills/workflow/git-workflow/references/examples-and-templates.md \
  skills/workflow/yunxiao/references/openapi.md \
  CHANGELOG.md
# expected: all hooks pass
```

## Drift from spec during execution

- Spec listed three examples as `中文 fix / 英文 refactor / Docs-only`. Execution swapped the Chinese fix to English fix and re-typed the Chinese example as a different scenario — user mid-execution requested the skill be predominantly English, so only one Chinese example remains (purpose: demonstrate that `验证：` is first-class).
- Heading rendered as `## PR Description` instead of `## PR / MR Description` — slash in heading produced an awkward GitHub anchor slug (`pr--mr-description`); simplified for clean linking.
