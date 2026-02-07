# User Config

note-to-blog skill paths and settings.

## Note Repository

```yaml
# Obsidian vault root (supports ~ expansion)
# This path is for macOS + iCloud. Adjust for other platforms.
note_repo: ~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Note/

# Directories to scan for candidates
scan_dirs:
  - Areas/
  - Inbox/
  - Archives/

# State file (relative to note_repo root)
state_file: .note-to-blog.json
```

## Blog Repository

```yaml
# bokushi blog content root
blog_content: repos/bokushi/src/content/

# Target collections
collections:
  - blog/    # long-form essays, opinions, reviews
  - til/     # technical notes, tutorials, TIL
  - monthly/ # weekly/monthly life logs
```

## Session Data

```yaml
# Claude Code project data paths (read sessions-index.json from each)
project_paths:
  - ~/.claude/projects/-Users-sueharakyoko-code-nini-dev
  - ~/.claude/projects/-Users-sueharakyoko-code-nini-dev-repos-bokushi

# Global history file
history_file: ~/.claude/history.jsonl

# Activity window (days)
session_window: 30
```

## Default Behavior

If paths are not accessible:

- **Note repo** - skill cannot proceed, ask user for correct path
- **Blog content** - skill cannot proceed, ask user for correct path
- **Session data** - proceed without session signals, note "session 数据未找到，跳过活跃度分析"
