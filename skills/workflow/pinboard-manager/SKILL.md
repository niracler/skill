---
name: pinboard-manager
description: Pinboard bookmark management — tag audit and dead link detection. Triggers on "pinboard", "bookmark", "tag audit", "dead link". 触发场景：用户说「pinboard 整理 tag」「pinboard 检查死链」「pinboard audit」「pinboard cleanup」「整理书签」时触发。
---

# Pinboard Manager

Interactive Pinboard bookmark management with tag auditing and dead link detection.

## Prerequisites

| Tool | Type | Required | How to get |
|------|------|----------|------------|
| Pinboard account | service | Yes | [pinboard.in](https://pinboard.in/) |
| `PINBOARD_AUTH_TOKEN` | env var | Yes | See [user-config.md](references/user-config.md) |
| `curl` | cli | Yes | Built-in on macOS/Linux |

> Do NOT proactively verify these tools on skill load. If a command fails due to a missing tool or token, directly guide the user through setup step by step.

## Mode Selection

| User Intent | Mode | Section |
|-------------|------|---------|
| 「pinboard 整理 tag」「pinboard audit」「整理书签」 | Tag Audit | [Tag Audit Mode](#tag-audit-mode) |
| 「pinboard 检查死链」「pinboard check links」 | Dead Link Detection | [Dead Link Detection Mode](#dead-link-detection-mode) |

## API Helpers

All Pinboard API calls use these patterns:

### Fetch bookmarks

```bash
# Fetch all bookmarks
curl -s "https://api.pinboard.in/v1/posts/all?auth_token=$PINBOARD_AUTH_TOKEN&format=json"

# Fetch bookmarks with toread=yes
curl -s "https://api.pinboard.in/v1/posts/all?auth_token=$PINBOARD_AUTH_TOKEN&format=json&toread=yes"

# Fetch a specific bookmark by URL
curl -s "https://api.pinboard.in/v1/posts/get?auth_token=$PINBOARD_AUTH_TOKEN&format=json&url=ENCODED_URL"
```

### Update a bookmark (overwrite mode)

**CRITICAL**: Always pass ALL fields to avoid data loss. The `/posts/add` endpoint overwrites the entire bookmark.

```bash
curl -s "https://api.pinboard.in/v1/posts/add?auth_token=$PINBOARD_AUTH_TOKEN&format=json&url=ENCODED_URL&description=ENCODED_TITLE&extended=ENCODED_NOTES&tags=ENCODED_TAGS&shared=ORIGINAL_SHARED&toread=ORIGINAL_TOREAD&replace=yes"
```

Required fields to preserve:

- `url` — the bookmark URL (identifier)
- `description` — title
- `extended` — notes/description
- `tags` — space-separated tag list
- `shared` — `yes` or `no`
- `toread` — `yes` or `no`
- `replace` — MUST be `yes` to update existing

### Delete a bookmark

```bash
curl -s "https://api.pinboard.in/v1/posts/delete?auth_token=$PINBOARD_AUTH_TOKEN&format=json&url=ENCODED_URL"
```

### Rate limiting

Pinboard recommends at most 1 API call per 3 seconds. When making multiple calls (batch updates, link checks), add `sleep 3` between calls.

> **`posts/all` special limit**: This endpoint is rate-limited to **once every 5 minutes**. Cache the result in `/tmp/pinboard_all.json` and reuse it within the same session. If both Tag Audit and Dead Link Detection are run consecutively, reuse the cached file.

## Tag Audit Mode

### Overview

Audit all bookmarks against the tag convention, present issues in batches, and apply fixes with user confirmation.

Reference: [tag-convention.md](references/tag-convention.md)

### Step 1: Fetch all bookmarks

```bash
curl -s "https://api.pinboard.in/v1/posts/all?auth_token=$PINBOARD_AUTH_TOKEN&format=json" > /tmp/pinboard_all.json
```

Parse the JSON and count total bookmarks.

### Step 2: Analyze tag issues

Load the tag convention from [tag-convention.md](references/tag-convention.md) and scan all bookmarks. Categorize issues:

| Priority | Category | Example |
|----------|----------|---------|
| 1 | Typos | `ainme` → `anime` |
| 2 | Missing tags | Bookmarks with empty `tags` field |
| 3 | Case issues | `Health` → `health` |
| 4 | Chinese tags | `终极文档` → `reference` |
| 5 | Concept overlap | `ai` + `llm` on same bookmark |
| 6 | Deprecated tags | `TODO`, year tags like `2025` |

### Step 3: Present issues in batches

For each category (in priority order), present **5-10 bookmarks per batch**:

```text
### Batch 1: Typos (3 items)

1. 「Some anime article」
   URL: https://example.com/anime
   Current tags: `ainme game`
   Suggested: `anime game`

2. 「Editor comparison」
   URL: https://example.com/editor
   Current tags: `editer tool`
   Suggested: `programming tool`

3. ...

Options: [confirm all] [modify] [skip all] [skip individual]
```

### Step 4: Apply confirmed changes

For each confirmed change, update via `/posts/add` with `replace=yes`:

```bash
# URL-encode all parameters
curl -s "https://api.pinboard.in/v1/posts/add?auth_token=$PINBOARD_AUTH_TOKEN&format=json&url=ENCODED_URL&description=ENCODED_TITLE&extended=ENCODED_NOTES&tags=NEW_TAGS&shared=ORIGINAL_SHARED&toread=ORIGINAL_TOREAD&replace=yes"
sleep 3  # Rate limit
```

**IMPORTANT**: Preserve ALL original fields. Only modify `tags`.

### Step 5: Summary

After all batches are processed, show:

```text
Tag Audit Complete
- Bookmarks scanned: 200
- Issues found: 45
- Fixed: 38
- Skipped: 7
```

## Dead Link Detection Mode

### Overview

Check all bookmarks for broken URLs and report results for user action.

### Step 1: Fetch all bookmarks

Same as Tag Audit Step 1.

### Step 2: Check links in batches

Process 10 URLs per batch using HTTP HEAD requests:

```bash
# HEAD request with 10 second timeout
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -L --max-redirs 5 -I -m 10 "URL")
```

Classification (based on final status after following redirects):

| Status | Meaning | Action |
|--------|---------|--------|
| 2xx | Working | No action |
| 403, 405 | HEAD rejected | Retry with GET |
| 4xx (other) | Broken | Report to user |
| 5xx | Server error | Report to user |
| 000 | Timeout/unreachable | Report to user |

For HEAD-rejected URLs, retry once with GET:

```bash
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -L --max-redirs 5 -m 10 "URL")
```

### Step 3: Present results

Show broken links grouped by status:

```text
### Dead Links Found (12 items)

#### 404 Not Found (5)
1. 「Article title」 — https://example.com/gone
   Tags: programming
   → [delete] [keep] [skip]

2. ...

#### Timeout (4)
1. 「Slow site article」 — https://slow-site.com/article
   Tags: reference
   → [delete] [keep] [skip]

#### Server Error 5xx (3)
1. ...
```

### Step 4: Apply user decisions

For deletions:

```bash
curl -s "https://api.pinboard.in/v1/posts/delete?auth_token=$PINBOARD_AUTH_TOKEN&format=json&url=ENCODED_URL"
sleep 3  # Rate limit
```

### Step 5: Summary

```text
Dead Link Check Complete
- Links checked: 200
- Working: 188
- Broken: 8 (deleted: 5, kept: 3)
- Timeout: 4 (deleted: 1, kept: 3)
```

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `PINBOARD_AUTH_TOKEN not set` | Env var missing | See [user-config.md](references/user-config.md) |
| `403 Forbidden` on API calls | Invalid or expired token | Re-check token at Pinboard settings |
| `429 Too Many Requests` | Rate limit exceeded | Increase sleep between calls; `posts/all` is limited to once per 5 min |
| Partial update lost data | Missing fields in `/posts/add` | Always pass ALL original fields with `replace=yes` |
