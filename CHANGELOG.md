# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

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

[0.1.0]: https://github.com/niracler/skill/releases/tag/v0.1.0
