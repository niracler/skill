#!/usr/bin/env python3
"""note-to-blog: Obsidian Note → Blog pipeline tool.

Subcommands:
  collect  Scan Note repo, extract summaries, build wikilink graph, output JSON
  convert  Convert Obsidian Markdown to standard Markdown (stdout)
  state    Manage .note-to-blog.json (status / draft / publish / skip)

Dependencies: PyYAML (pip install pyyaml)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

try:
    import yaml
except ImportError:
    print(
        "Error: PyYAML is required but not installed.\n"
        "Install it with: pip install pyyaml",
        file=sys.stderr,
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

STATE_FILE = ".note-to-blog.json"

# Match [[wikilink]] or [[wikilink|display]] — but NOT inside fenced code blocks
WIKILINK_RE = re.compile(r"\[\[([^\]|]+?)(?:\|[^\]]*?)?\]\]")


def load_state(note_repo: Path) -> dict:
    """Load .note-to-blog.json, creating it if missing."""
    state_path = note_repo / STATE_FILE
    if not state_path.exists():
        empty = {"drafted": {}, "published": {}, "skipped": {}}
        state_path.write_text(json.dumps(empty, indent=2, ensure_ascii=False) + "\n")
        return empty
    return json.loads(state_path.read_text(encoding="utf-8"))


def save_state(note_repo: Path, state: dict):
    """Write .note-to-blog.json atomically."""
    state_path = note_repo / STATE_FILE
    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter from body. Returns (metadata, body)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_text = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")
    try:
        meta = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError:
        meta = {}
    return meta, body


def extract_title(meta: dict, filepath: Path) -> str:
    """Extract title from frontmatter or fallback to filename."""
    if meta.get("title"):
        return str(meta["title"])
    aliases = meta.get("aliases")
    if aliases and isinstance(aliases, list) and len(aliases) > 0:
        return str(aliases[0])
    return filepath.stem


def is_inside_code_block(lines: list[str], line_idx: int) -> bool:
    """Check if a line is inside a fenced code block."""
    in_code = False
    for i in range(line_idx):
        stripped = lines[i].strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
    return in_code


def extract_wikilinks_from_text(text: str) -> list[str]:
    """Extract wikilink targets, excluding those inside code blocks."""
    lines = text.split("\n")
    links = []
    in_code = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            continue
        if in_code:
            continue
        for m in WIKILINK_RE.finditer(line):
            links.append(m.group(1))
    return links


# ---------------------------------------------------------------------------
# collect subcommand
# ---------------------------------------------------------------------------

def collect_candidates(note_repo: Path, state: dict) -> tuple[list[dict], int, int]:
    """Scan all *.md files, filter by state, extract summaries.

    Returns (candidates, total_scanned, filtered_out).
    """
    marked = set()
    for category in ("drafted", "published", "skipped"):
        marked.update(state.get(category, {}).keys())

    candidates = []
    total_scanned = 0

    for md_file in sorted(note_repo.rglob("*.md")):
        # Skip the state file itself and hidden directories
        rel = str(md_file.relative_to(note_repo))
        if rel == STATE_FILE or rel.startswith("."):
            continue
        total_scanned += 1

        if rel in marked:
            continue

        try:
            text = md_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue

        meta, body = parse_frontmatter(text)
        title = extract_title(meta, md_file)

        # Extract first 20 non-empty, non-frontmatter lines as summary
        non_empty = [l for l in body.split("\n") if l.strip()]
        summary = "\n".join(non_empty[:20])

        # Character count (body only)
        char_count = len(body)

        # Outgoing wikilinks (deduplicated, preserving order)
        raw_links = extract_wikilinks_from_text(body)
        seen = set()
        outgoing = []
        for link in raw_links:
            if link not in seen:
                seen.add(link)
                outgoing.append(link)

        candidates.append({
            "path": rel,
            "title": title,
            "summary": summary,
            "char_count": char_count,
            "outgoing_links": outgoing,
        })

    filtered_out = len(marked)
    return candidates, total_scanned, filtered_out


def build_clusters(candidates: list[dict]) -> list[dict]:
    """Build wikilink graph and identify hub nodes (3+ inbound links)."""
    # Map: target_name → list of source paths that link to it
    inbound: dict[str, list[str]] = defaultdict(list)

    # Also build a lookup from filename stem to candidate path
    stem_to_path: dict[str, str] = {}
    for c in candidates:
        stem = Path(c["path"]).stem
        stem_to_path[stem] = c["path"]

    for c in candidates:
        for link_target in c["outgoing_links"]:
            inbound[link_target].append(c["path"])

    clusters = []
    for hub_name, sources in sorted(inbound.items(), key=lambda x: -len(x[1])):
        if len(sources) < 3:
            continue
        hub_path = stem_to_path.get(hub_name)
        clusters.append({
            "hub_path": hub_path,  # None if hub note isn't a candidate
            "hub_title": hub_name,
            "related": sorted(sources),
            "link_count": len(sources),
        })

    return clusters


def collect_session_keywords(
    project_paths: list[str], history_file: str | None, window_days: int
) -> list[str]:
    """Extract session activity signals from Claude Code data."""
    keywords = []
    cutoff = datetime.now() - timedelta(days=window_days)

    # Read sessions-index.json from each project path
    for pp in project_paths:
        pp_path = Path(pp).expanduser()
        idx_file = pp_path / "sessions-index.json"
        if not idx_file.exists():
            print(f"Warning: {idx_file} not found, skipping", file=sys.stderr)
            continue
        try:
            raw = json.loads(idx_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            print(f"Warning: failed to read {idx_file}", file=sys.stderr)
            continue

        # sessions-index.json format: {version, entries: [...], originalPath}
        sessions = raw.get("entries", raw) if isinstance(raw, dict) else raw

        for session in sessions:
            mtime = session.get("fileMtime")
            if not mtime:
                continue
            try:
                # Handle ISO format or epoch
                if isinstance(mtime, (int, float)):
                    session_time = datetime.fromtimestamp(mtime / 1000)
                else:
                    session_time = datetime.fromisoformat(str(mtime).replace("Z", "+00:00")).replace(tzinfo=None)
            except (ValueError, TypeError):
                continue

            if session_time < cutoff:
                continue

            summary = session.get("summary", "")
            first_prompt = session.get("firstPrompt", "")
            if summary:
                keywords.append(summary)
            elif first_prompt:
                keywords.append(first_prompt)

    # Read history.jsonl
    if history_file:
        hist_path = Path(history_file).expanduser()
        if not hist_path.exists():
            print(f"Warning: {hist_path} not found, skipping", file=sys.stderr)
        else:
            try:
                for line in hist_path.read_text(encoding="utf-8").strip().split("\n"):
                    if not line.strip():
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    mtime = entry.get("timestamp")
                    if not mtime:
                        continue
                    try:
                        if isinstance(mtime, (int, float)):
                            entry_time = datetime.fromtimestamp(mtime / 1000)
                        else:
                            entry_time = datetime.fromisoformat(str(mtime).replace("Z", "+00:00")).replace(tzinfo=None)
                    except (ValueError, TypeError):
                        continue
                    if entry_time < cutoff:
                        continue
                    prompt = entry.get("display", "") or entry.get("prompt", "")
                    if prompt and not prompt.startswith("/"):
                        keywords.append(prompt)
            except OSError:
                print(f"Warning: failed to read {hist_path}", file=sys.stderr)

    if not project_paths and not history_file:
        print("Warning: session 数据路径未配置，跳过活跃度分析", file=sys.stderr)

    return keywords


def collect_published_posts(blog_content: Path) -> list[dict]:
    """Scan bokushi blog content for published posts."""
    posts = []
    for collection in ("blog", "til", "monthly"):
        coll_dir = blog_content / collection
        if not coll_dir.exists():
            continue
        for md_file in sorted(coll_dir.rglob("*.md")) + sorted(coll_dir.rglob("*.mdx")):
            try:
                text = md_file.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            meta, _ = parse_frontmatter(text)
            posts.append({
                "title": meta.get("title", md_file.stem),
                "tags": meta.get("tags", []),
                "collection": collection,
            })
    return posts


def cmd_collect(args):
    """Scan Note repo and output structured JSON."""
    note_repo = Path(args.note_repo).expanduser().resolve()
    blog_content = Path(args.blog_content).expanduser().resolve()

    if not note_repo.is_dir():
        print(f"Error: Note repo not found: {note_repo}", file=sys.stderr)
        sys.exit(1)
    if not blog_content.is_dir():
        print(f"Error: Blog content not found: {blog_content}", file=sys.stderr)
        sys.exit(1)

    state = load_state(note_repo)
    candidates, total_scanned, filtered_out = collect_candidates(note_repo, state)
    clusters = build_clusters(candidates)
    session_keywords = collect_session_keywords(
        args.project_paths, args.history_file, args.session_window
    )
    published_posts = collect_published_posts(blog_content)

    output = {
        "candidates": candidates,
        "clusters": clusters,
        "published_posts": published_posts,
        "session_keywords": session_keywords,
        "stats": {
            "total_scanned": total_scanned,
            "filtered_out": filtered_out,
            "candidates_count": len(candidates),
        },
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# convert subcommand
# ---------------------------------------------------------------------------

# Obsidian image embed: ![[image.png]] or ![[image.png|400]]
OBSIDIAN_IMAGE_RE = re.compile(r"!\[\[([^\]|]+?)(?:\|\d+)?\]\]")

# Obsidian wikilink with display: [[target|display]]
WIKILINK_DISPLAY_RE = re.compile(r"\[\[[^\]|]+?\|([^\]]+?)\]\]")

# Obsidian wikilink without display: [[target]]
WIKILINK_PLAIN_RE = re.compile(r"\[\[([^\]|]+?)\]\]")

# Obsidian callout: > [!type] optional title
CALLOUT_RE = re.compile(r"^(>\s*)\[!(\w+)\]\s*(.*)", re.MULTILINE)

# Obsidian highlight: ==text==
HIGHLIGHT_RE = re.compile(r"==(.*?)==")

# Obsidian comment: %%text%%  (single-line and multi-line)
COMMENT_SINGLE_RE = re.compile(r"%%.*?%%")
COMMENT_MULTI_RE = re.compile(r"%%.*?%%", re.DOTALL)

# Obsidian inline tag: #TagName (not in headings, not in code, not URL fragments)
INLINE_TAG_RE = re.compile(r"(?<![\w/])#([A-Za-z\u4e00-\u9fff][\w\u4e00-\u9fff/\-]*)")

# Obsidian span directive: :span[text]{.class}
SPAN_DIRECTIVE_RE = re.compile(r":span\[([^\]]+)\]\{\.(\w+)\}")

# Obsidian frontmatter fields to strip
OBSIDIAN_FM_FIELDS = {"aliases", "date", "modified", "date updated", "score", "cssclasses"}


def convert_obsidian_to_standard(text: str, filepath: Path) -> str:
    """Convert Obsidian-specific Markdown to standard Markdown."""
    meta, body = parse_frontmatter(text)

    # Collect inline tags from body (outside code blocks)
    collected_tags = []
    converted_body = _convert_body(body, collected_tags)

    # Build new frontmatter
    new_meta = _convert_frontmatter(meta, collected_tags, filepath)

    # Assemble output
    fm_text = yaml.dump(new_meta, allow_unicode=True, default_flow_style=False).strip()
    return f"---\n{fm_text}\n---\n\n{converted_body}"


def _convert_body(body: str, collected_tags: list[str]) -> str:
    """Apply all Obsidian→standard conversions to the body text."""
    lines = body.split("\n")
    result_lines = []
    in_code = False

    for line in lines:
        stripped = line.strip()

        # Track code block boundaries
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code = not in_code
            result_lines.append(line)
            continue

        if in_code:
            result_lines.append(line)
            continue

        # Remove comments (single-line %%...%%)
        line = COMMENT_SINGLE_RE.sub("", line)

        # Skip lines that are now empty after comment removal
        # (but preserve intentionally empty lines from original)

        # Collect and remove inline tags
        for m in INLINE_TAG_RE.finditer(line):
            tag = m.group(1)
            # Skip if it looks like a heading (line starts with #)
            if not stripped.startswith("#"):
                collected_tags.append(tag)

        # Remove inline tags from body (only non-heading lines)
        if not stripped.startswith("#"):
            line = INLINE_TAG_RE.sub("", line).rstrip()

        # Image embeds: ![[image.png|400]] → ![](image.png)
        line = OBSIDIAN_IMAGE_RE.sub(r"![](\1)", line)

        # Wikilinks with display: [[target|display]] → display
        line = WIKILINK_DISPLAY_RE.sub(r"\1", line)

        # Wikilinks plain: [[target]] → target
        line = WIKILINK_PLAIN_RE.sub(r"\1", line)

        # Callouts: > [!type] title → > **Type:** title
        line = CALLOUT_RE.sub(
            lambda m: f"{m.group(1)}**{m.group(2).capitalize()}:** {m.group(3)}".rstrip(),
            line,
        )

        # Highlights: ==text== → **text**
        line = HIGHLIGHT_RE.sub(r"**\1**", line)

        # Span directives: :span[text]{.class} → <span class="class">text</span>
        line = SPAN_DIRECTIVE_RE.sub(r'<span class="\2">\1</span>', line)

        result_lines.append(line)

    # Handle multi-line comments that might have been missed
    result_text = "\n".join(result_lines)
    result_text = COMMENT_MULTI_RE.sub("", result_text)

    return result_text.strip() + "\n"


def _convert_frontmatter(meta: dict, collected_tags: list[str], filepath: Path = Path("untitled")) -> dict:
    """Strip Obsidian fields, generate bokushi-compatible frontmatter."""
    title = extract_title(meta, filepath)

    # Merge tags from frontmatter + collected inline tags
    fm_tags = meta.get("tags", []) or []
    if isinstance(fm_tags, str):
        fm_tags = [fm_tags]
    all_tags = list(dict.fromkeys(fm_tags + collected_tags))  # deduplicate, preserve order

    new_meta = {
        "title": title,
        "pubDate": datetime.now().strftime("%Y-%m-%d"),
        "tags": all_tags,
        "hidden": True,
    }
    # Do NOT include description — that's generated by the LLM Agent
    return new_meta


def cmd_convert(args):
    """Convert a single Obsidian Markdown file to standard Markdown."""
    filepath = Path(args.path).expanduser().resolve()
    if not filepath.exists():
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    text = filepath.read_text(encoding="utf-8")
    converted = convert_obsidian_to_standard(text, filepath)
    print(converted, end="")


# ---------------------------------------------------------------------------
# state subcommand
# ---------------------------------------------------------------------------

def cmd_state_status(args):
    """Display pipeline status overview."""
    note_repo = Path(args.note_repo).expanduser().resolve()
    state = load_state(note_repo)

    drafted = state.get("drafted", {})
    published = state.get("published", {})
    skipped = state.get("skipped", {})

    print(f"Pipeline Status ({note_repo / STATE_FILE})")
    print(f"  Drafted:   {len(drafted)}")
    print(f"  Published: {len(published)}")
    print(f"  Skipped:   {len(skipped)}")
    print()

    if drafted:
        print("Drafted items:")
        for path, info in drafted.items():
            target = info.get("target", "?")
            date = info.get("date", "?")
            print(f"  {path} → {target} ({date})")


def cmd_state_draft(args):
    """Mark a note as drafted."""
    note_repo = Path(args.note_repo).expanduser().resolve()
    state = load_state(note_repo)

    today = datetime.now().strftime("%Y-%m-%d")
    state.setdefault("drafted", {})[args.note_path] = {
        "target": args.target,
        "date": today,
    }
    save_state(note_repo, state)
    print(f"Drafted: {args.note_path} → {args.target}")


def cmd_state_publish(args):
    """Move a drafted note to published."""
    note_repo = Path(args.note_repo).expanduser().resolve()
    state = load_state(note_repo)

    drafted = state.get("drafted", {})
    if args.note_path not in drafted:
        print(f"Error: {args.note_path} is not in drafted state", file=sys.stderr)
        sys.exit(1)

    entry = drafted.pop(args.note_path)
    today = datetime.now().strftime("%Y-%m-%d")
    state.setdefault("published", {})[args.note_path] = {
        "target": entry.get("target", ""),
        "date": today,
    }
    save_state(note_repo, state)
    print(f"Published: {args.note_path} (target: {entry.get('target', '')})")


def cmd_state_skip(args):
    """Mark a note as skipped."""
    note_repo = Path(args.note_repo).expanduser().resolve()
    state = load_state(note_repo)

    today = datetime.now().strftime("%Y-%m-%d")
    state.setdefault("skipped", {})[args.note_path] = {
        "reason": args.reason,
        "date": today,
    }
    save_state(note_repo, state)
    print(f"Skipped: {args.note_path} (reason: {args.reason})")


# ---------------------------------------------------------------------------
# CLI setup
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="note-to-blog",
        description="Obsidian Note → Blog pipeline tool",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # -- collect --
    p_collect = subparsers.add_parser("collect", help="Scan notes and output JSON")
    p_collect.add_argument(
        "--note-repo",
        required=True,
        help="Path to the Obsidian vault root",
    )
    p_collect.add_argument(
        "--blog-content",
        required=True,
        help="Path to bokushi blog content directory",
    )
    p_collect.add_argument(
        "--project-paths",
        nargs="*",
        default=[],
        help="Claude Code project data paths for session signals",
    )
    p_collect.add_argument(
        "--history-file",
        default=None,
        help="Path to Claude Code global history.jsonl",
    )
    p_collect.add_argument(
        "--session-window",
        type=int,
        default=30,
        help="Session activity window in days (default: 30)",
    )
    p_collect.set_defaults(func=cmd_collect)

    # -- convert --
    p_convert = subparsers.add_parser(
        "convert", help="Convert Obsidian Markdown to standard Markdown"
    )
    p_convert.add_argument("path", help="Path to the Markdown file to convert")
    p_convert.set_defaults(func=cmd_convert)

    # -- state --
    p_state = subparsers.add_parser("state", help="Manage pipeline state")
    state_sub = p_state.add_subparsers(dest="state_command", required=True)

    # state status
    p_status = state_sub.add_parser("status", help="Show pipeline status")
    p_status.add_argument(
        "--note-repo",
        required=True,
        help="Path to the Obsidian vault root (for locating .note-to-blog.json)",
    )
    p_status.set_defaults(func=cmd_state_status)

    # state draft
    p_draft = state_sub.add_parser("draft", help="Mark note as drafted")
    p_draft.add_argument("note_path", help="Relative path to the note in vault")
    p_draft.add_argument(
        "--target", required=True, help="Target path in blog content (e.g. blog/xxx.md)"
    )
    p_draft.add_argument(
        "--note-repo",
        required=True,
        help="Path to the Obsidian vault root",
    )
    p_draft.set_defaults(func=cmd_state_draft)

    # state publish
    p_publish = state_sub.add_parser("publish", help="Move drafted note to published")
    p_publish.add_argument("note_path", help="Relative path to the note in vault")
    p_publish.add_argument(
        "--note-repo",
        required=True,
        help="Path to the Obsidian vault root",
    )
    p_publish.set_defaults(func=cmd_state_publish)

    # state skip
    p_skip = state_sub.add_parser("skip", help="Mark note as skipped")
    p_skip.add_argument("note_path", help="Relative path to the note in vault")
    p_skip.add_argument(
        "--reason", default="no reason", help="Reason for skipping (default: no reason)"
    )
    p_skip.add_argument(
        "--note-repo",
        required=True,
        help="Path to the Obsidian vault root",
    )
    p_skip.set_defaults(func=cmd_state_skip)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
