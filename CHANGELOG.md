# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.2.1] - 2026-03-16

### Fixed

- **plugin manifest** — Updated `marketplace.json` for v0.2.0 skill changes: replaced removed `writing-inspiration`/`writing-proofreading` with `writing-assistant` and `diary-note`

## [0.2.0] - 2026-03-16

### Added

- **weekly-report** — New skill replacing `worklog`, with structured 3-section corporate format, auto-collecting data from git logs, Obsidian diary, schedule YAML, GitHub PRs, and Yunxiao MRs
- **diary-note** — Lightweight quick-append skill for diary entries (split from diary-assistant)
- **writing-assistant** — Merged `writing-inspiration` + `writing-proofreading` into a dual-mode skill (inspiration + proofreading)
- **planning.py** — Script for workspace-planning YAML operations
- **Claude Code GitHub Workflow** — CI workflows for Claude Code review (#9)

### Changed

- **Comprehensive skill restructuring** (#8):
  - Restructured pinboard-manager: split mode details into `references/`, unified user config at `~/.config/nini-skill/`
  - Simplified diary-assistant: removed Work Log, streamlined flow
  - Deduplicated schedule-manager: removed inline commands, reference docs
  - Generalized code-sync: added `--base-dir` parameter and first-time setup flow
  - Updated skill-reviewer dependency: writing-skills → skill-creator
  - Updated markdown-lint pre-commit rev to v0.21.0
- **Optimized all 17 skill descriptions** for better triggering — action-forward pattern with explicit negative triggers
- **writing-proofreading** — Added formatting preferences for numbered headings and no horizontal rules (#7)
- **OpenClaw metadata** — Added to all remaining skills

### Removed

- **worklog** — Replaced by weekly-report
- **writing-inspiration** — Merged into writing-assistant
- **writing-proofreading** — Merged into writing-assistant

### Fixed

- **pinboard-manager** — Removed "claude" from timeliness tech tag filter

## [0.1.1] - 2026-03-05

### Changed

- **pinboard-manager** — Generalized for public use: renamed personal `tag-convention.md` to `.example.md`, added first-time setup flow for tag convention generation (#5)

### Added

- **ClawHub CI workflow** — Auto-publish 10 public skills to [ClawHub](https://clawhub.ai) on GitHub Release (#6)
- **OpenClaw metadata** — Added `metadata.openclaw` (emoji, required bins/env) to all 10 public skills

## [0.1.0] - 2026-03-05

First tagged release. All skills that existed before this point are included.

### Skills (17 total)

#### Workspace (NEW)

- **workspace-init** — Interactive 5-phase initialization for [dev-config-template](https://github.com/niracler/dev-config-template) workspaces. Includes template update detection and `validate.py` post-init verification.
- **workspace-planning** — YAML-based project schedule management with module status tracking, milestone countdowns, and optional Yunxiao sync.

#### Workflow

- **git-workflow** — Conventional Commits, PR templates, release workflow with commit message validator.
- **yunxiao** — Alibaba Cloud DevOps (Yunxiao/Codeup) integration for MR creation, task management, and Push Review.
- **schedule-manager** — Apple Calendar & Reminders management via osascript and reminders-cli (macOS).
- **worklog** — Personal work review aggregating git stats, GitHub activity, and Yunxiao tasks.
- **code-sync** — Batch sync git repos across machines (push at end-of-day, pull at start-of-day).
- **markdown-lint** — markdownlint-cli2 setup, pre-commit hook integration, and batch fix for monorepos.
- **skill-reviewer** — Audit skills for quality, cross-platform compatibility, and best practices.
- **ha-integration-reviewer** — Home Assistant integration code review for Quality Scale compliance.
- **pinboard-manager** — Pinboard bookmark tag audit, dead link detection, and timeliness check.

#### Writing

- **diary-assistant** — Daily journal with GTD task review, work log automation, and Anki card generation (macOS).
- **note-to-blog** — Scan Obsidian notes for blog-ready candidates, convert and publish drafts.
- **writing-proofreading** — 6-step Chinese article review workflow with markdown formatting.
- **writing-inspiration** — Guided writing for travel notes, TIL, and articles.

#### Learning

- **anki-card-generator** — Generate Anki flashcards in simple-anki-sync compatible format.

#### Fun

- **zaregoto-miko** — Convert text to Zaregoto series Miko Aoi's speaking style.

### Infrastructure

- Skills organized into category subdirectories (`workspace/`, `workflow/`, `writing/`, `learning/`, `fun/`)
- Standardized Prerequisites section across all skills
- Architecture diagram in README showing skill dependencies and external tool requirements

[0.2.1]: https://github.com/niracler/skill/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/niracler/skill/compare/v0.1.3...v0.2.0
[0.1.1]: https://github.com/niracler/skill/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/niracler/skill/releases/tag/v0.1.0
